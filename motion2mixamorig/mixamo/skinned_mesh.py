"""Load Mixamo character meshes + skin clusters from binary FBX.

Does not change retargeting. FK is the existing T * Rpre * R_anim chain;
finger bones stay at rest (identity R_anim) and follow the hands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .fbx_skeleton import (
    _child_named,
    bone_local_matrix,
    build_hierarchy,
    collect_limb_nodes,
    compose_world,
    euler_xyz_deg_to_matrix,
    extract_connections,
    extract_global_settings,
    extract_objects,
    parse_fbx,
    unit_to_meters,
)
from .kinematics import MixamoBone, MixamoRig, forward_kinematics


def _fbx_name(raw: str) -> str:
    return str(raw).split("\x00", 1)[0]


def _mat4_fbx(values) -> np.ndarray:
    return np.asarray(values, dtype=np.float64).reshape(4, 4).T


def _triangulate(indices: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fan-triangulate PolygonVertexIndex.

    Returns the vertex ids per triangle, the *flat* polygon-vertex slots they
    came from, and the polygon each triangle belongs to. The slots index the
    per-polygon-vertex layers (UV), and the polygon id indexes the per-polygon
    ones (material), so both can be read back after triangulation.
    """
    faces: list[tuple[int, int, int]] = []
    slots: list[tuple[int, int, int]] = []
    polys: list[int] = []
    corner: list[int] = []
    corner_slot: list[int] = []
    poly_id = 0
    for flat, raw in enumerate(indices):
        value = int(raw)
        corner_slot.append(flat)
        if value < 0:
            corner.append(~value)
            for i in range(1, len(corner) - 1):
                faces.append((corner[0], corner[i], corner[i + 1]))
                slots.append((corner_slot[0], corner_slot[i], corner_slot[i + 1]))
                polys.append(poly_id)
            corner = []
            corner_slot = []
            poly_id += 1
        else:
            corner.append(value)
    if not faces:
        return (np.zeros((0, 3), dtype=np.int32),
                np.zeros((0, 3), dtype=np.int64),
                np.zeros((0,), dtype=np.int64))
    return (np.asarray(faces, dtype=np.int32),
            np.asarray(slots, dtype=np.int64),
            np.asarray(polys, dtype=np.int64))


# Mixamo ships diffuse alongside normal/spec/emission maps under one material,
# and only the file names tell them apart.
_DIFFUSE_HINTS = ("diffuse", "albedo", "basecolor", "base_color")
_OTHER_MAP_HINTS = ("normal", "spec", "gloss", "rough", "metal", "emission",
                    "occlusion", "_ao", "bump", "displace", "opacity", "transparen")


def _texture_rank(filename: str) -> int:
    low = filename.lower()
    if any(h in low for h in _DIFFUSE_HINTS):
        return 0
    if any(h in low for h in _OTHER_MAP_HINTS):
        return 2
    return 1


def _decode_video(obj: dict) -> "np.ndarray | None":
    """Decoded texture, keeping any alpha channel.

    Alpha matters: the facial decals and hair/cape cards are masked art painted
    on an opaque backing, so discarding alpha stamps that backing onto the model.
    """
    import cv2

    content = _child_named(obj["raw"], "Content")
    if content is None or not content["props"]:
        return None
    blob = content["props"][0]
    if not isinstance(blob, (bytes, bytearray)):
        return None
    if len(blob) == 0:
        return None
    image = cv2.imdecode(np.frombuffer(bytes(blob), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if image is None:
        return None
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def _videos_by_filename(objects: dict) -> dict[str, list[int]]:
    """Several Video nodes can share one file with only one holding the bytes."""
    out: dict[str, list[int]] = {}
    for uid, obj in objects.items():
        if obj["node_name"] != "Video":
            continue
        node = _child_named(obj["raw"], "RelativeFilename")
        if node is None or not node["props"]:
            continue
        key = _fbx_name(str(node["props"][0]))
        if key:
            out.setdefault(key, []).append(uid)
    return out


def _material_textures(objects: dict, connections: list) -> dict[int, list[tuple[int, str]]]:
    """material uid → its textures as (video uid, filename), best diffuse first."""
    tex_uids = {u for u, o in objects.items() if o["node_name"] == "Texture"}
    video_uids = {u for u, o in objects.items() if o["node_name"] == "Video"}
    mat_uids = {u for u, o in objects.items() if o["node_name"] == "Material"}

    tex_video: dict[int, int] = {}
    for kind, src, dst in connections:
        if kind == "OO" and src in video_uids and dst in tex_uids:
            tex_video[dst] = src

    out: dict[int, list[tuple[int, str]]] = {}
    for kind, src, dst in connections:
        if src not in tex_uids or dst not in mat_uids:
            continue
        node = _child_named(objects[src]["raw"], "RelativeFilename")
        filename = _fbx_name(str(node["props"][0])) if node is not None and node["props"] else ""
        video = tex_video.get(src)
        if video is None:
            continue
        entry = (video, filename)
        bucket = out.setdefault(dst, [])
        if entry not in bucket:
            bucket.append(entry)
    for uid, bucket in out.items():
        bucket.sort(key=lambda e: _texture_rank(e[1]))
    return out


def _geometry_materials(objects: dict, connections: list) -> dict[int, list[int]]:
    """geometry uid → material uids in the order the Model declares them.

    A `ByPolygon` material layer indexes this list, and FBX defines the order by
    the sequence of material→model connections.
    """
    geom_uids = {u for u, o in objects.items() if o["node_name"] == "Geometry"}
    mat_uids = {u for u, o in objects.items() if o["node_name"] == "Material"}
    model_uids = {u for u, o in objects.items()
                  if o["node_name"] == "Model" and o.get("class") == "Mesh"}

    geom_model: dict[int, int] = {}
    model_mats: dict[int, list[int]] = {}
    for kind, src, dst in connections:
        if kind != "OO":
            continue
        if src in geom_uids and dst in model_uids:
            geom_model[src] = dst
        if src in mat_uids and dst in model_uids:
            model_mats.setdefault(dst, []).append(src)
    return {g: model_mats.get(m, []) for g, m in geom_model.items()}


def _uv_per_slot(geom_raw: dict) -> np.ndarray | None:
    """(n_polygon_vertex, 2) UVs, resolved through UVIndex when present."""
    layer = _child_named(geom_raw, "LayerElementUV")
    if layer is None:
        return None
    uv_node = _child_named(layer, "UV")
    if uv_node is None or not uv_node["props"]:
        return None
    uvs = np.asarray(uv_node["props"][0], dtype=np.float64).reshape(-1, 2)
    idx_node = _child_named(layer, "UVIndex")
    if idx_node is not None and idx_node["props"]:
        idx = np.asarray(idx_node["props"][0], dtype=np.int64)
        idx = np.clip(idx, 0, uvs.shape[0] - 1)
        return uvs[idx]
    return uvs


def _material_per_polygon(geom_raw: dict, n_poly: int) -> np.ndarray:
    layer = _child_named(geom_raw, "LayerElementMaterial")
    if layer is None:
        return np.zeros(n_poly, dtype=np.int64)
    arr = _child_named(layer, "Materials")
    if arr is None or not arr["props"]:
        return np.zeros(n_poly, dtype=np.int64)
    mats = np.asarray(arr["props"][0], dtype=np.int64)
    if mats.size == 1:
        return np.full(n_poly, int(mats[0]), dtype=np.int64)
    if mats.size < n_poly:
        mats = np.pad(mats, (0, n_poly - mats.size), mode="edge")
    return mats[:n_poly]


def _sample(image: np.ndarray, uv: np.ndarray) -> np.ndarray:
    """Nearest-texel BGR at UV. FBX UV origin is bottom-left, images are top-down.

    UVs are wrapped, not clamped: Mixamo reuses one half of an atlas by offsetting
    the other half a whole tile in U, so clamping folds every one of those faces
    onto the texture's edge column.
    """
    h, w = image.shape[:2]
    u = np.mod(uv[:, 0], 1.0)
    v = np.mod(1.0 - uv[:, 1], 1.0)
    xs = np.clip((u * (w - 1)).astype(np.int64), 0, w - 1)
    ys = np.clip((v * (h - 1)).astype(np.int64), 0, h - 1)
    return image[ys, xs].astype(np.float64)


# Barycentric weights of points strictly inside a triangle. One texel at the
# centroid lands in the black gutter between UV islands often enough to speckle
# a whole character, so each triangle is probed at several interior points and
# the median is kept, which ignores a stray sample or two.
_PROBES = np.array([
    [1 / 3, 1 / 3, 1 / 3],
    [0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6],
    [0.45, 0.45, 0.10], [0.45, 0.10, 0.45], [0.10, 0.45, 0.45],
])


def _sample_triangles(image: np.ndarray, corners: np.ndarray) -> np.ndarray:
    """(T, 3, 2) triangle UVs -> (T, C) sample, median over the interior probes."""
    channels = image.shape[2]
    stack = np.empty((_PROBES.shape[0], corners.shape[0], channels), dtype=np.float64)
    for i, w in enumerate(_PROBES):
        uv = (corners[:, 0] * w[0] + corners[:, 1] * w[1] + corners[:, 2] * w[2])
        stack[i] = _sample(image, uv)
    return np.median(stack, axis=0)


def face_colors_from_textures(
    objects: dict,
    connections: list,
    geom_uid: int,
    geom_raw: dict,
    slots: np.ndarray,
    poly_ids: np.ndarray,
    lift: float = 1.0,
) -> tuple[np.ndarray, np.ndarray] | None:
    """One BGR per triangle, read from the diffuse map at the UV centroid.

    UVs never move, so this is paid once per character rather than per frame,
    and the painter fill stays exactly as cheap as a flat colour.

    `lift` below 1 is a gamma on the sampled colour. Several of these characters
    wear near-black clothing that no amount of ambient light separates from a
    dark backdrop; the curve raises those without touching the bright end.
    """
    uv_slots = _uv_per_slot(geom_raw)
    if uv_slots is None or slots.shape[0] == 0:
        return None
    mats = _geometry_materials(objects, connections).get(geom_uid, [])
    if not mats:
        return None
    textures = _material_textures(objects, connections)
    shared = _videos_by_filename(objects)

    n_poly = int(poly_ids.max()) + 1 if poly_ids.size else 0
    poly_mat = _material_per_polygon(geom_raw, n_poly)
    tri_mat = poly_mat[poly_ids]

    slot_clip = np.clip(slots, 0, uv_slots.shape[0] - 1)
    corners = np.stack([uv_slots[slot_clip[:, 0]], uv_slots[slot_clip[:, 1]],
                        uv_slots[slot_clip[:, 2]]], axis=1)

    out = np.full((slots.shape[0], 3), np.nan, dtype=np.float64)
    opacity = np.full(slots.shape[0], 255.0, dtype=np.float64)
    for local_idx, mat_uid in enumerate(mats):
        picked = tri_mat == local_idx
        if not np.any(picked):
            continue
        image = None
        for video_uid, filename in textures.get(mat_uid, []):
            for candidate in [video_uid, *shared.get(filename, [])]:
                image = _decode_video(objects[candidate])
                if image is not None:
                    break
            if image is not None:
                break
        if image is None:
            continue
        sampled = _sample_triangles(image, corners[picked])
        out[picked] = sampled[:, :3]
        if sampled.shape[1] == 4:
            opacity[picked] = sampled[:, 3]
        del image
    if np.all(np.isnan(out)):
        return None
    fallback = np.nanmean(out.reshape(-1, 3), axis=0)
    bad = np.isnan(out[:, 0])
    out[bad] = fallback
    if abs(lift - 1.0) > 1e-9:
        out = 255.0 * np.power(np.clip(out / 255.0, 0.0, 1.0), lift)
    return out, opacity >= 128.0


@dataclass
class SkinnedMesh:
    name: str
    vertices: np.ndarray  # (V, 3) bind pose, FBX cm
    faces: np.ndarray  # (F, 3)
    weights: np.ndarray  # (V, B)
    ibm: np.ndarray  # (B, 4, 4) inverse bind = Cluster.Transform
    color: np.ndarray
    face_colors: np.ndarray | None = None  # (F, 3) BGR from the diffuse map


@dataclass
class YBotAsset:
    rig: MixamoRig
    meshes: list[SkinnedMesh]
    bone_index: dict[str, int] = field(default_factory=dict)

    @property
    def n_bones(self) -> int:
        return len(self.rig.order)


def load_full_rig(fbx_path: Path) -> MixamoRig:
    """Every Mixamo limb, same PreRotation local-matrix convention as the core rig."""
    fbx_path = Path(fbx_path)
    version, nodes = parse_fbx(fbx_path)
    objects = extract_objects(nodes)
    connections = extract_connections(nodes)
    settings = extract_global_settings(nodes)
    limbs = collect_limb_nodes(objects)
    parent_of = build_hierarchy(limbs, connections)
    local_of: dict[int, np.ndarray] = {}
    parts_of: dict[int, dict[str, np.ndarray]] = {}
    for uid, obj in limbs.items():
        local, parts = bone_local_matrix(obj["props"])
        local_of[uid] = local
        parts_of[uid] = parts
    world_of = compose_world(parent_of, local_of)

    children_of: dict[int, list[int]] = {uid: [] for uid in limbs}
    for uid, parent in parent_of.items():
        if parent in children_of:
            children_of[parent].append(uid)
    roots = [uid for uid, parent in parent_of.items() if parent is None]
    ordered: list[int] = []

    def walk(uid: int) -> None:
        ordered.append(uid)
        for child in children_of[uid]:
            walk(child)

    for root in roots:
        walk(root)

    bones: dict[str, MixamoBone] = {}
    order: list[str] = []
    for uid in ordered:
        obj = limbs[uid]
        name = _fbx_name(obj["name"])
        parts = parts_of[uid]
        parent_uid = parent_of[uid]
        parent_name = _fbx_name(limbs[parent_uid]["name"]) if parent_uid in limbs else None
        child_names = [_fbx_name(limbs[c]["name"]) for c in children_of[uid]]
        bones[name] = MixamoBone(
            name=name,
            parent=parent_name,
            children=child_names,
            pre_rotation=euler_xyz_deg_to_matrix(parts["pre_rotation_euler_deg"]),
            lcl_translation_cm=parts["lcl_translation"].copy(),
            rest_world=world_of[uid],
            rest_local=local_of[uid],
            pre_rotation_euler_deg=parts["pre_rotation_euler_deg"].copy(),
        )
        order.append(name)
    return MixamoRig(
        bones=bones,
        order=order,
        meters_per_unit=unit_to_meters(settings),
        source=fbx_path,
        coord_system={"fbx_unit": "centimeter", "meters_per_fbx_unit": unit_to_meters(settings)},
    )


def load_character_asset(
    fbx_path: Path, *, textures: bool = False, lift: float = 1.0
) -> YBotAsset:
    """Rig + skinned meshes (optionally with diffuse-sampled face colors)."""
    fbx_path = Path(fbx_path)
    rig = load_full_rig(fbx_path)
    _, nodes = parse_fbx(fbx_path)
    objects = extract_objects(nodes)
    connections = extract_connections(nodes)
    bone_index = {name: i for i, name in enumerate(rig.order)}
    n_bones = len(rig.order)

    uid_name = {uid: _fbx_name(obj["name"]) for uid, obj in objects.items()}

    limb_uids = {uid for uid, obj in objects.items() if obj["node_name"] == "Model" and obj.get("class") == "LimbNode"}
    skin_uids = {uid for uid, obj in objects.items() if obj["node_name"] == "Deformer" and obj.get("class") == "Skin"}
    geom_uids = {uid for uid, obj in objects.items() if obj["node_name"] == "Geometry"}
    cluster_uids = {uid for uid, obj in objects.items() if obj["node_name"] == "Deformer" and obj.get("class") == "Cluster"}

    skin_to_geom: dict[int, int] = {}
    cluster_to_skin: dict[int, int] = {}
    cluster_to_limb: dict[int, int] = {}
    for kind, src, dst in connections:
        if kind != "OO":
            continue
        if src in cluster_uids and dst in skin_uids:
            cluster_to_skin[src] = dst
        if src in limb_uids and dst in cluster_uids:
            cluster_to_limb[dst] = src
        if src in skin_uids and dst in geom_uids:
            skin_to_geom[src] = dst
        if src in geom_uids and dst in skin_uids:
            skin_to_geom[dst] = src

    colors = {
        "Alpha_Surface": np.array([0.72, 0.74, 0.78]),
        "Alpha_Joints": np.array([0.38, 0.40, 0.44]),
    }
    meshes: list[SkinnedMesh] = []
    for geom_uid in geom_uids:
        geom = objects[geom_uid]
        verts_node = _child_named(geom["raw"], "Vertices")
        idx_node = _child_named(geom["raw"], "PolygonVertexIndex")
        if verts_node is None or idx_node is None:
            continue
        vertices = np.asarray(verts_node["props"][0], dtype=np.float64).reshape(-1, 3)
        faces, slots, poly_ids = _triangulate(np.asarray(idx_node["props"][0], dtype=np.int64))
        tinted = None
        if textures:
            sampled = face_colors_from_textures(
                objects, connections, geom_uid, geom["raw"], slots, poly_ids, lift
            )
            if sampled is not None:
                tinted, visible = sampled
                # Masked-out faces are dropped outright rather than blended, so
                # the painter fill stays a single opaque pass.
                if not np.all(visible):
                    faces = faces[visible]
                    tinted = tinted[visible]
        n_verts = vertices.shape[0]
        weights = np.zeros((n_verts, n_bones), dtype=np.float64)
        ibm = np.repeat(np.eye(4)[None, ...], n_bones, axis=0)
        for cluster_uid, skin_uid in cluster_to_skin.items():
            if skin_to_geom.get(skin_uid) != geom_uid:
                continue
            limb_uid = cluster_to_limb.get(cluster_uid)
            if limb_uid is None:
                continue
            bone_name = uid_name[limb_uid]
            if bone_name not in bone_index:
                continue
            cluster = objects[cluster_uid]
            idx_elem = _child_named(cluster["raw"], "Indexes")
            w_elem = _child_named(cluster["raw"], "Weights")
            t_elem = _child_named(cluster["raw"], "Transform")
            b = bone_index[bone_name]
            if t_elem is not None and t_elem["props"]:
                ibm[b] = _mat4_fbx(t_elem["props"][0])
            if idx_elem is None or w_elem is None:
                continue
            indexes = np.asarray(idx_elem["props"][0], dtype=np.int64)
            wts = np.asarray(w_elem["props"][0], dtype=np.float64)
            weights[indexes, b] = wts
        row = weights.sum(axis=1, keepdims=True)
        row = np.where(row < 1e-8, 1.0, row)
        weights = weights / row
        meshes.append(
            SkinnedMesh(
                name=_fbx_name(geom["name"]),
                vertices=vertices,
                faces=faces,
                weights=weights,
                ibm=ibm,
                color=colors.get(_fbx_name(geom["name"]), np.array([0.6, 0.6, 0.6])),
                face_colors=tinted,
            )
        )
    return YBotAsset(rig=rig, meshes=meshes, bone_index=bone_index)


def bone_palette(world: dict[str, np.ndarray], mesh: SkinnedMesh, order: list[str]) -> np.ndarray:
    mats = np.stack([world[name] for name in order], axis=0)
    return mats @ mesh.ibm


def skin_mesh(mesh: SkinnedMesh, palette: np.ndarray) -> np.ndarray:
    """Linear blend skinning. palette is (B, 4, 4) = M_world @ IBM."""
    ones = np.ones((mesh.vertices.shape[0], 1), dtype=np.float64)
    vh = np.concatenate([mesh.vertices, ones], axis=1)
    posed = np.zeros((mesh.vertices.shape[0], 4), dtype=np.float64)
    for b in range(palette.shape[0]):
        w = mesh.weights[:, b]
        if float(w.max()) < 1e-12:
            continue
        posed += w[:, None] * (vh @ palette[b].T)
    return posed[:, :3]


def posed_vertices(
    asset: YBotAsset,
    r_anim: dict[str, np.ndarray],
    hips_translation_cm: np.ndarray,
    lcl_translations_cm: dict[str, np.ndarray] | None = None,
) -> list[np.ndarray]:
    world = forward_kinematics(
        asset.rig,
        r_anim,
        hips_translation_cm=hips_translation_cm,
        lcl_translations_cm=lcl_translations_cm,
    )
    out: list[np.ndarray] = []
    for mesh in asset.meshes:
        palette = bone_palette(world, mesh, asset.rig.order)
        out.append(skin_mesh(mesh, palette))
    return out


def rest_skin_error(asset: YBotAsset) -> float:
    """Identity R_anim must reproduce bind vertices (PreRotation FK + IBM)."""
    world = forward_kinematics(asset.rig, {})
    err = 0.0
    for mesh in asset.meshes:
        posed = skin_mesh(mesh, bone_palette(world, mesh, asset.rig.order))
        err = max(err, float(np.linalg.norm(posed - mesh.vertices, axis=1).max()))
    return err
