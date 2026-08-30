"""Parse a binary Mixamo FBX and extract the core skeleton.

Reads the binary FBX directly (PreRotation is a Maya/FBX property, so Assimp
cannot be used) and returns the core-bone skeleton as a plain dict — the same
structure `kinematics.rig_from_skeleton_data` consumes.
"""

from __future__ import annotations

import re
import struct
import zlib
from pathlib import Path
from typing import Any

import numpy as np

# Mixamo body chain only: no finger bones. End sites keep bone directions.
CORE_BONE_SUFFIXES = (
    "Hips",
    "Spine",
    "Spine1",
    "Spine2",
    "Neck",
    "Head",
    "HeadTop_End",
    "LeftShoulder",
    "LeftArm",
    "LeftForeArm",
    "LeftHand",
    "RightShoulder",
    "RightArm",
    "RightForeArm",
    "RightHand",
    "LeftUpLeg",
    "LeftLeg",
    "LeftFoot",
    "LeftToeBase",
    "LeftToe_End",
    "RightUpLeg",
    "RightLeg",
    "RightFoot",
    "RightToeBase",
    "RightToe_End",
)

# SMPL-24 (GVHMR skeleton_motion.npz) → Mixamo Y Bot.
HUMAN_TO_MIXAMO = {
    "pelvis": "mixamorig:Hips",
    "left_hip": "mixamorig:LeftUpLeg",
    "right_hip": "mixamorig:RightUpLeg",
    "spine1": "mixamorig:Spine",
    "left_knee": "mixamorig:LeftLeg",
    "right_knee": "mixamorig:RightLeg",
    "spine2": "mixamorig:Spine1",
    "left_ankle": "mixamorig:LeftFoot",
    "right_ankle": "mixamorig:RightFoot",
    "spine3": "mixamorig:Spine2",
    "left_foot": "mixamorig:LeftToeBase",
    "right_foot": "mixamorig:RightToeBase",
    "neck": "mixamorig:Neck",
    "left_collar": "mixamorig:LeftShoulder",
    "right_collar": "mixamorig:RightShoulder",
    "head": "mixamorig:Head",
    "left_shoulder": "mixamorig:LeftArm",
    "right_shoulder": "mixamorig:RightArm",
    "left_elbow": "mixamorig:LeftForeArm",
    "right_elbow": "mixamorig:RightForeArm",
    "left_wrist": "mixamorig:LeftHand",
    "right_wrist": "mixamorig:RightHand",
    "left_hand": "mixamorig:LeftHand",
    "right_hand": "mixamorig:RightHand",
}

# Mixamo bones that have no 1:1 SMPL-24 joint (chain tips / extra spine).
MIXAMO_WITHOUT_HUMAN = (
    "mixamorig:HeadTop_End",
    "mixamorig:LeftToe_End",
    "mixamorig:RightToe_End",
)

_RIG_PREFIX_RE = re.compile(r"^mixamorig\d+:")

FBX_HEADER = b"Kaydara FBX Binary  \x00\x1a\x00"
ARRAY_DTYPE = {
    b"f": ("<f", 4),
    b"d": ("<d", 8),
    b"l": ("<q", 8),
    b"i": ("<i", 4),
    b"b": ("<?", 1),
}


class FbxError(ValueError):
    pass


def _read(buf: memoryview, offset: int, fmt: str) -> tuple[Any, int]:
    size = struct.calcsize(fmt)
    return struct.unpack_from(fmt, buf, offset)[0], offset + size


def _read_array(buf: memoryview, offset: int, type_code: bytes) -> tuple[list[Any], int]:
    length, offset = _read(buf, offset, "<I")
    encoding, offset = _read(buf, offset, "<I")
    compressed_len, offset = _read(buf, offset, "<I")
    dtype, item_size = ARRAY_DTYPE[type_code]
    raw = bytes(buf[offset : offset + compressed_len])
    offset += compressed_len
    if encoding == 1:
        raw = zlib.decompress(raw)
    elif encoding != 0:
        raise FbxError(f"unsupported FBX array encoding {encoding}")
    expected = length * item_size
    if len(raw) != expected:
        raise FbxError(f"array size mismatch: {len(raw)} != {expected}")
    values = list(struct.unpack_from(f"<{length}{dtype[-1]}", raw, 0)) if length else []
    return values, offset


def _read_property(buf: memoryview, offset: int) -> tuple[Any, int]:
    type_code = bytes(buf[offset : offset + 1])
    offset += 1
    if type_code == b"Y":
        return _read(buf, offset, "<h")
    if type_code == b"C":
        value, offset = _read(buf, offset, "<B")
        return bool(value), offset
    if type_code == b"I":
        return _read(buf, offset, "<i")
    if type_code == b"F":
        return _read(buf, offset, "<f")
    if type_code == b"D":
        return _read(buf, offset, "<d")
    if type_code == b"L":
        return _read(buf, offset, "<q")
    if type_code in ARRAY_DTYPE:
        return _read_array(buf, offset, type_code)
    if type_code in (b"S", b"R"):
        length, offset = _read(buf, offset, "<I")
        data = bytes(buf[offset : offset + length])
        offset += length
        if type_code == b"S":
            return data.split(b"\x00")[0].decode("utf-8", errors="replace"), offset
        return data, offset
    raise FbxError(f"unknown FBX property type {type_code!r}")


def _is_null_record(buf: memoryview, offset: int, version: int) -> bool:
    size = 25 if version >= 7500 else 13
    return offset + size <= len(buf) and all(b == 0 for b in buf[offset : offset + size])


def _read_node(buf: memoryview, offset: int, version: int) -> tuple[dict[str, Any] | None, int]:
    start = offset
    if version >= 7500:
        end_offset, offset = _read(buf, offset, "<Q")
        n_props, offset = _read(buf, offset, "<Q")
        _prop_len, offset = _read(buf, offset, "<Q")
    else:
        end_offset, offset = _read(buf, offset, "<I")
        n_props, offset = _read(buf, offset, "<I")
        _prop_len, offset = _read(buf, offset, "<I")
    if end_offset == 0:
        return None, start + (25 if version >= 7500 else 13)
    name_len = buf[offset]
    offset += 1
    name = bytes(buf[offset : offset + name_len]).decode("ascii", errors="replace")
    offset += name_len
    props: list[Any] = []
    for _ in range(n_props):
        value, offset = _read_property(buf, offset)
        props.append(value)
    children: list[dict[str, Any]] = []
    while offset < end_offset:
        if _is_null_record(buf, offset, version):
            offset = end_offset
            break
        child, offset = _read_node(buf, offset, version)
        if child is None:
            break
        children.append(child)
    return {"name": name, "props": props, "children": children}, end_offset


def parse_fbx(path: Path) -> tuple[int, list[dict[str, Any]]]:
    data = path.read_bytes()
    if not data.startswith(FBX_HEADER):
        raise FbxError(f"{path} is not a binary FBX file")
    version = struct.unpack_from("<I", data, 23)[0]
    buf = memoryview(data)
    offset = 27
    nodes: list[dict[str, Any]] = []
    while offset < len(buf):
        if _is_null_record(buf, offset, version):
            break
        node, offset = _read_node(buf, offset, version)
        if node is None:
            break
        nodes.append(node)
    return version, nodes


def _children_named(node: dict[str, Any], name: str) -> list[dict[str, Any]]:
    return [c for c in node["children"] if c["name"] == name]


def _child_named(node: dict[str, Any], name: str) -> dict[str, Any] | None:
    for child in node["children"]:
        if child["name"] == name:
            return child
    return None


def _vec3(value: Any, default: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> np.ndarray:
    if value is None:
        return np.array(default, dtype=np.float64)
    arr = np.asarray(value, dtype=np.float64).reshape(-1)
    if arr.size < 3:
        out = np.array(default, dtype=np.float64)
        out[: arr.size] = arr
        return out
    return arr[:3].copy()


def parse_properties70(node: dict[str, Any]) -> dict[str, Any]:
    props: dict[str, Any] = {}
    block = _child_named(node, "Properties70")
    if block is None:
        return props
    for child in block["children"]:
        if child["name"] != "P" or not child["props"]:
            continue
        raw = child["props"]
        key = str(raw[0])
        values = raw[4:] if len(raw) > 4 else []
        if len(values) == 1:
            props[key] = values[0]
        elif len(values) >= 3 and all(isinstance(v, (int, float)) for v in values[:3]):
            props[key] = [float(v) for v in values[:3]]
        else:
            props[key] = values
    return props


def euler_xyz_deg_to_matrix(euler_deg: np.ndarray) -> np.ndarray:
    """FBX/Maya Euler XYZ: R = Rz @ Ry @ Rx (column vectors)."""
    x, y, z = np.deg2rad(np.asarray(euler_deg, dtype=np.float64)[:3])
    cx, sx = np.cos(x), np.sin(x)
    cy, sy = np.cos(y), np.sin(y)
    cz, sz = np.cos(z), np.sin(z)
    rx = np.array([[1.0, 0.0, 0.0], [0.0, cx, -sx], [0.0, sx, cx]])
    ry = np.array([[cy, 0.0, sy], [0.0, 1.0, 0.0], [-sy, 0.0, cy]])
    rz = np.array([[cz, -sz, 0.0], [sz, cz, 0.0], [0.0, 0.0, 1.0]])
    return rz @ ry @ rx


def matrix_to_quat_wxyz(rmat: np.ndarray) -> np.ndarray:
    m = np.asarray(rmat, dtype=np.float64)
    t = float(np.trace(m))
    if t > 0.0:
        s = 0.5 / np.sqrt(t + 1.0)
        w = 0.25 / s
        x = (m[2, 1] - m[1, 2]) * s
        y = (m[0, 2] - m[2, 0]) * s
        z = (m[1, 0] - m[0, 1]) * s
    else:
        i = int(np.argmax([m[0, 0], m[1, 1], m[2, 2]]))
        if i == 0:
            s = 2.0 * np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2])
            w = (m[2, 1] - m[1, 2]) / s
            x = 0.25 * s
            y = (m[0, 1] + m[1, 0]) / s
            z = (m[0, 2] + m[2, 0]) / s
        elif i == 1:
            s = 2.0 * np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2])
            w = (m[0, 2] - m[2, 0]) / s
            x = (m[0, 1] + m[1, 0]) / s
            y = 0.25 * s
            z = (m[1, 2] + m[2, 1]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1])
            w = (m[1, 0] - m[0, 1]) / s
            x = (m[0, 2] + m[2, 0]) / s
            y = (m[1, 2] + m[2, 1]) / s
            z = 0.25 * s
    q = np.array([w, x, y, z], dtype=np.float64)
    n = float(np.linalg.norm(q))
    if n < 1e-12:
        return np.array([1.0, 0.0, 0.0, 0.0])
    if q[0] < 0:
        q = -q
    return q / n


def make_transform(
    translation: np.ndarray,
    pre_rot_deg: np.ndarray,
    lcl_rot_deg: np.ndarray,
    post_rot_deg: np.ndarray,
    scale: np.ndarray,
    rotation_offset: np.ndarray | None = None,
    rotation_pivot: np.ndarray | None = None,
) -> np.ndarray:
    """Maya/FBX local TRS with PreRotation (pivots/offsets identity on Mixamo).

    M = T * Roff * Rp * Rpre * R * Rpost^{-1} * Rp^{-1} * S
    """
    t = _vec3(translation)
    s = _vec3(scale, (1.0, 1.0, 1.0))
    roff = _vec3(rotation_offset)
    rp = _vec3(rotation_pivot)
    rpre = euler_xyz_deg_to_matrix(pre_rot_deg)
    r = euler_xyz_deg_to_matrix(lcl_rot_deg)
    rpost = euler_xyz_deg_to_matrix(post_rot_deg)
    rot = rpre @ r @ rpost.T

    def translate(vec: np.ndarray) -> np.ndarray:
        m = np.eye(4)
        m[:3, 3] = vec
        return m

    t_mat = translate(t)
    roff_mat = translate(roff)
    rp_mat = translate(rp)
    rp_inv = translate(-rp)
    r_mat = np.eye(4)
    r_mat[:3, :3] = rot
    s_mat = np.diag([float(s[0]), float(s[1]), float(s[2]), 1.0])
    return t_mat @ roff_mat @ rp_mat @ r_mat @ rp_inv @ s_mat


def _tolist(arr: np.ndarray, ndigits: int = 12) -> list[Any]:
    def _round(x: float) -> float:
        v = round(float(x), ndigits)
        return 0.0 if abs(v) < 10 ** (-ndigits) else v

    if arr.ndim == 1:
        return [_round(x) for x in arr]
    return [[_round(x) for x in row] for row in arr]


def _describe_path(path: Path) -> str:
    return str(path)


def normalize_rig_prefix(name: str) -> str:
    """`mixamorig8:Hips` → `mixamorig:Hips`.

    Mixamo appends a digit to the namespace when a character is exported from a
    scene that already held a rig, so the same bone arrives under a different
    name per file. Every bone table in the project keys off the bare prefix.
    """
    return _RIG_PREFIX_RE.sub("mixamorig:", name, count=1)


def bone_suffix(name: str) -> str:
    return name.split(":")[-1]


def is_core_bone(name: str) -> bool:
    return bone_suffix(name) in CORE_BONE_SUFFIXES


def extract_objects(nodes: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    objects: dict[int, dict[str, Any]] = {}
    for node in nodes:
        if node["name"] != "Objects":
            continue
        for child in node["children"]:
            if not child["props"]:
                continue
            uid = int(child["props"][0])
            name = normalize_rig_prefix(str(child["props"][1])) if len(child["props"]) > 1 else ""
            class_name = str(child["props"][2]) if len(child["props"]) > 2 else ""
            objects[uid] = {
                "uid": uid,
                "node_name": child["name"],
                "name": name,
                "class": class_name,
                "props": parse_properties70(child),
                "raw": child,
            }
    return objects


def extract_connections(nodes: list[dict[str, Any]]) -> list[tuple[str, int, int]]:
    links: list[tuple[str, int, int]] = []
    for node in nodes:
        if node["name"] != "Connections":
            continue
        for child in node["children"]:
            if child["name"] != "C" or len(child["props"]) < 3:
                continue
            kind = str(child["props"][0])
            src = int(child["props"][1])
            dst = int(child["props"][2])
            links.append((kind, src, dst))
    return links


def extract_global_settings(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    for node in nodes:
        if node["name"] == "GlobalSettings":
            return parse_properties70(node)
    return {}


def extract_bind_pose(objects: dict[int, dict[str, Any]]) -> dict[int, np.ndarray]:
    poses: dict[int, np.ndarray] = {}
    for obj in objects.values():
        if obj["node_name"] != "Pose":
            continue
        for pose_node in _children_named(obj["raw"], "PoseNode"):
            node_elem = _child_named(pose_node, "Node")
            matrix_elem = _child_named(pose_node, "Matrix")
            if node_elem is None or matrix_elem is None or not matrix_elem["props"]:
                continue
            uid = int(node_elem["props"][0])
            values = matrix_elem["props"][0]
            mat = np.asarray(values, dtype=np.float64).reshape(4, 4).T
            poses[uid] = mat
    return poses


def collect_limb_nodes(objects: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    limbs: dict[int, dict[str, Any]] = {}
    for uid, obj in objects.items():
        if obj["node_name"] != "Model":
            continue
        if obj["class"] != "LimbNode":
            continue
        limbs[uid] = obj
    return limbs


def build_hierarchy(
    limbs: dict[int, dict[str, Any]],
    connections: list[tuple[str, int, int]],
) -> dict[int, int | None]:
    parent_of: dict[int, int | None] = {uid: None for uid in limbs}
    for kind, src, dst in connections:
        if kind != "OO":
            continue
        if src in limbs and dst in limbs:
            parent_of[src] = dst
    return parent_of


def bone_local_matrix(props: dict[str, Any]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    translation = _vec3(props.get("Lcl Translation"))
    lcl_rot = _vec3(props.get("Lcl Rotation"))
    pre_rot = _vec3(props.get("PreRotation"))
    post_rot = _vec3(props.get("PostRotation"))
    scale = _vec3(props.get("Lcl Scaling"), (1.0, 1.0, 1.0))
    rotation_offset = _vec3(props.get("RotationOffset"))
    rotation_pivot = _vec3(props.get("RotationPivot"))
    local = make_transform(
        translation,
        pre_rot,
        lcl_rot,
        post_rot,
        scale,
        rotation_offset=rotation_offset,
        rotation_pivot=rotation_pivot,
    )
    parts = {
        "lcl_translation": translation,
        "lcl_rotation_euler_deg": lcl_rot,
        "pre_rotation_euler_deg": pre_rot,
        "post_rotation_euler_deg": post_rot,
        "lcl_scaling": scale,
        "rotation_offset": rotation_offset,
        "rotation_pivot": rotation_pivot,
    }
    return local, parts


def compose_world(
    parent_of: dict[int, int | None],
    local_of: dict[int, np.ndarray],
) -> dict[int, np.ndarray]:
    world: dict[int, np.ndarray] = {}

    def eval_uid(uid: int) -> np.ndarray:
        if uid in world:
            return world[uid]
        parent = parent_of.get(uid)
        local = local_of[uid]
        if parent is None:
            world[uid] = local.copy()
        else:
            world[uid] = eval_uid(parent) @ local
        return world[uid]

    for uid in local_of:
        eval_uid(uid)
    return world


def unit_to_meters(settings: dict[str, Any]) -> float:
    """FBX default unit is centimeters when UnitScaleFactor == 1."""
    scale = float(settings.get("UnitScaleFactor", 1.0) or 1.0)
    return 0.01 * scale


def axis_name(index: int, sign: int) -> str:
    names = {0: "X", 1: "Y", 2: "Z"}
    prefix = "+" if int(sign) >= 0 else "-"
    return f"{prefix}{names.get(int(index), '?')}"


def extract_skeleton(fbx_path: Path) -> dict[str, Any]:
    version, nodes = parse_fbx(fbx_path)
    objects = extract_objects(nodes)
    connections = extract_connections(nodes)
    settings = extract_global_settings(nodes)
    bind_pose = extract_bind_pose(objects)
    limbs = collect_limb_nodes(objects)
    parent_of = build_hierarchy(limbs, connections)

    local_of: dict[int, np.ndarray] = {}
    parts_of: dict[int, dict[str, np.ndarray]] = {}
    for uid, obj in limbs.items():
        local, parts = bone_local_matrix(obj["props"])
        local_of[uid] = local
        parts_of[uid] = parts
    world_of = compose_world(parent_of, local_of)

    core_uids = [uid for uid, obj in limbs.items() if is_core_bone(obj["name"])]
    children_of: dict[int, list[int]] = {uid: [] for uid in core_uids}
    for uid in core_uids:
        parent = parent_of[uid]
        if parent in children_of:
            children_of[parent].append(uid)

    def sort_children(uids: list[int]) -> list[int]:
        order = {name: i for i, name in enumerate(CORE_BONE_SUFFIXES)}
        return sorted(uids, key=lambda u: order.get(bone_suffix(limbs[u]["name"]), 999))

    roots = [uid for uid in core_uids if parent_of[uid] not in set(core_uids)]
    ordered: list[int] = []

    def walk(uid: int) -> None:
        ordered.append(uid)
        for child in sort_children(children_of[uid]):
            walk(child)

    for root in sort_children(roots):
        walk(root)

    meters_per_fbx = unit_to_meters(settings)
    bones = []
    for uid in ordered:
        obj = limbs[uid]
        parts = parts_of[uid]
        local = local_of[uid]
        world = world_of[uid]
        parent_uid = parent_of[uid]
        parent_name = limbs[parent_uid]["name"] if parent_uid in limbs else None
        child_names = [limbs[c]["name"] for c in sort_children(children_of[uid])]
        bind = bind_pose.get(uid)
        bind_err = None
        if bind is not None:
            bind_err = float(np.linalg.norm(world - bind))
        pre = parts["pre_rotation_euler_deg"]
        bones.append(
            {
                "name": obj["name"],
                "parent": parent_name,
                "children": child_names,
                "pre_rotation_euler_deg": _tolist(pre),
                "pre_rotation_matrix": _tolist(euler_xyz_deg_to_matrix(pre)),
                "lcl_translation": _tolist(parts["lcl_translation"]),
                "lcl_rotation_euler_deg": _tolist(parts["lcl_rotation_euler_deg"]),
                "lcl_scaling": _tolist(parts["lcl_scaling"]),
                "post_rotation_euler_deg": _tolist(parts["post_rotation_euler_deg"]),
                "rest_local": {
                    "matrix": _tolist(local),
                    "translation": _tolist(local[:3, 3]),
                    "rotation_matrix": _tolist(local[:3, :3]),
                    "quaternion_wxyz": _tolist(matrix_to_quat_wxyz(local[:3, :3])),
                    "scale": _tolist(np.array([np.linalg.norm(local[:3, i]) for i in range(3)])),
                },
                "rest_world": {
                    "matrix": _tolist(world),
                    "translation": _tolist(world[:3, 3]),
                    "translation_m": _tolist(world[:3, 3] * meters_per_fbx),
                    "rotation_matrix": _tolist(world[:3, :3]),
                    "quaternion_wxyz": _tolist(matrix_to_quat_wxyz(world[:3, :3])),
                },
                "bind_pose_world_matrix": _tolist(bind) if bind is not None else None,
                "bind_pose_match_error": bind_err,
            }
        )

    hierarchy = [
        {
            "name": limbs[uid]["name"],
            "parent": limbs[parent_of[uid]]["name"] if parent_of[uid] in limbs else None,
            "children": [limbs[c]["name"] for c in sort_children(children_of[uid])],
        }
        for uid in ordered
    ]

    return {
        "source_fbx": _describe_path(fbx_path),
        "fbx_version": version,
        "character": fbx_path.stem,
        "coord_system": {
            "up": axis_name(int(settings.get("UpAxis", 1)), int(settings.get("UpAxisSign", 1))),
            "front": axis_name(int(settings.get("FrontAxis", 2)), int(settings.get("FrontAxisSign", 1))),
            "coord": axis_name(int(settings.get("CoordAxis", 0)), int(settings.get("CoordAxisSign", 1))),
            "handedness": "right",
            "rotation_order": "XYZ",
            "fbx_unit": "centimeter" if abs(float(settings.get("UnitScaleFactor", 1.0)) - 1.0) < 1e-6 else "custom",
            "unit_scale_factor": float(settings.get("UnitScaleFactor", 1.0)),
            "meters_per_fbx_unit": meters_per_fbx,
        },
        "transform_convention": (
            "Maya/FBX: M_local = T * Roff * Rp * Rpre * R * Rpost^{-1} * Rp^{-1} * S; "
            "M_world = M_parent_world * M_local. Euler XYZ in degrees, column-vector matrices."
        ),
        "root": limbs[roots[0]]["name"] if roots else None,
        "bone_count": len(bones),
        "hierarchy": hierarchy,
        "bones": bones,
    }
