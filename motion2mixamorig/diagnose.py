"""Self-intersection diagnostics for a skinned, animated character GLB.

Reads `mixamo_character.glb` itself (any skinned glTF with Mixamo bone names),
poses every frame with the file's own skin (linear blend skinning, as a glTF
viewer would) and reports where one body part goes into another:

    diagnostics.json
        issues: one entry per body-part pair, with the frame ranges where the
        penetration exceeds the threshold, the worst frame, and its depth.

Only self-intersection is checked. Floor contact needs a defined floor, which
this tool does not have yet.

Frame numbers are Blender frame numbers after import: frame = time x fps, so
the first animation frame is frame 0.
"""

from __future__ import annotations

import json
import re
import struct
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import numpy as np

SCHEMA = "m2mr-diagnostics-v1"
DEFAULT_THRESHOLD_CM = 1.0
DIAGNOSTICS_JSON = "diagnostics.json"
DIAGNOSTICS_HTML = "diagnostics.html"

# Mixamo bone (namespace stripped) -> body part. Fingers go with the hand.
_PART_OF_BONE = {
    "Hips": "torso", "Spine": "torso", "Spine1": "torso", "Spine2": "torso",
    "LeftShoulder": "torso", "RightShoulder": "torso",
    "Neck": "head", "Head": "head", "HeadTop_End": "head",
    "LeftEye": "head", "RightEye": "head",
    "LeftArm": "left_upper_arm", "LeftForeArm": "left_forearm", "LeftHand": "left_hand",
    "RightArm": "right_upper_arm", "RightForeArm": "right_forearm", "RightHand": "right_hand",
    "LeftUpLeg": "left_thigh", "LeftLeg": "left_shin",
    "LeftFoot": "left_foot", "LeftToeBase": "left_foot", "LeftToe_End": "left_foot",
    "RightUpLeg": "right_thigh", "RightLeg": "right_shin",
    "RightFoot": "right_foot", "RightToeBase": "right_foot", "RightToe_End": "right_foot",
}
PARTS = (
    "head", "torso",
    "left_upper_arm", "left_forearm", "left_hand",
    "right_upper_arm", "right_forearm", "right_hand",
    "left_thigh", "left_shin", "left_foot",
    "right_thigh", "right_shin", "right_foot",
)
# Parts joined at a joint are not compared: their skins meet, blend, or (on
# segmented rigs such as Y Bot) overlap at the joint even in the rest pose.
_ADJACENT = {
    frozenset(p) for p in [
        ("head", "torso"),
        ("torso", "left_upper_arm"), ("left_upper_arm", "left_forearm"), ("left_forearm", "left_hand"),
        ("torso", "right_upper_arm"), ("right_upper_arm", "right_forearm"), ("right_forearm", "right_hand"),
        ("torso", "left_thigh"), ("left_thigh", "left_shin"), ("left_shin", "left_foot"),
        ("torso", "right_thigh"), ("right_thigh", "right_shin"), ("right_shin", "right_foot"),
    ]
}
# A vertex counts as inside another part when it sits behind that part's
# surface (against its normal) and roughly in front of the nearest surface
# point, not off to the side of a thin edge.
_MAX_REACH_M = 0.15
_MIN_LATERAL_M = 0.02
# Two stretches of one pair this many frames apart or fewer are reported as one.
_MERGE_GAP = 3


def part_of_bone(name: str) -> str | None:
    """'mixamorig:LeftHandIndex2' / 'mixamorig1:LeftArm' / 'LeftArm' -> body part."""
    base = re.sub(r"^mixamorig\d*[:_]?", "", name, flags=re.IGNORECASE)
    if base in _PART_OF_BONE:
        return _PART_OF_BONE[base]
    for side in ("Left", "Right"):
        if base.startswith(side + "Hand"):
            return f"{side.lower()}_hand"
    return None


# --------------------------------------------------------------------------- GLB


_COMPONENT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
_WIDTH = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def read_glb(path: Path) -> tuple[dict, bytes]:
    data = Path(path).read_bytes()
    magic, version, _ = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67 or version != 2:
        raise ValueError(f"{path} is not a glTF 2.0 binary (.glb)")
    offset, gltf, binary = 12, None, b""
    while offset < len(data):
        length, kind = struct.unpack_from("<II", data, offset)
        chunk = data[offset + 8: offset + 8 + length]
        if kind == 0x4E4F534A:
            gltf = json.loads(chunk)
        elif kind == 0x004E4942:
            binary = chunk
        offset += 8 + length
    if gltf is None:
        raise ValueError(f"{path} has no JSON chunk")
    return gltf, binary


def _accessor(gltf: dict, binary: bytes, index: int) -> np.ndarray:
    acc = gltf["accessors"][index]
    view = gltf["bufferViews"][acc["bufferView"]]
    dtype = np.dtype(_COMPONENT[acc["componentType"]])
    width = _WIDTH[acc["type"]]
    count = acc["count"]
    start = view.get("byteOffset", 0) + acc.get("byteOffset", 0)
    stride = view.get("byteStride") or dtype.itemsize * width
    raw = np.frombuffer(binary, dtype=np.uint8, count=stride * (count - 1) + dtype.itemsize * width, offset=start)
    rows = np.lib.stride_tricks.as_strided(raw, shape=(count, dtype.itemsize * width), strides=(stride, 1))
    out = np.ascontiguousarray(rows).view(dtype).reshape(count, width)
    if acc.get("normalized") and dtype.kind in "iu":
        out = out.astype(np.float64) / np.iinfo(dtype).max
    if acc["type"] == "MAT4":
        out = out.reshape(count, 4, 4).transpose(0, 2, 1)  # column-major -> row-major
    return out


def _quat_xyzw_to_mat(q: np.ndarray) -> np.ndarray:
    x, y, z, w = (q / np.linalg.norm(q, axis=-1, keepdims=True)).T
    return np.stack([
        1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w),
        2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w),
        2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y),
    ], axis=-1).reshape(q.shape[:-1] + (3, 3))


@dataclass
class _Primitive:
    mesh_node: int
    skin: int
    positions: np.ndarray  # (V, 3) bind space, metres
    joints: np.ndarray  # (V, 4) skin-joint indices
    weights: np.ndarray  # (V, 4)
    faces: np.ndarray  # (F, 3)
    part: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.int16))  # index into PARTS, -1 = none


class SkinnedClip:
    """The node hierarchy, skins, skinned primitives, and first animation of a GLB."""

    def __init__(self, path: Path) -> None:
        gltf, binary = read_glb(path)
        self.path = Path(path)
        nodes = gltf.get("nodes", [])
        self.names = [n.get("name", f"node_{i}") for i, n in enumerate(nodes)]
        self.parent = [-1] * len(nodes)
        for i, n in enumerate(nodes):
            for c in n.get("children", []):
                self.parent[c] = i
        self.order = self._topological()
        self.rest_t = np.array([n.get("translation", [0, 0, 0]) for n in nodes], dtype=np.float64).reshape(-1, 3)
        self.rest_r = np.array([n.get("rotation", [0, 0, 0, 1]) for n in nodes], dtype=np.float64).reshape(-1, 4)
        self.rest_s = np.array([n.get("scale", [1, 1, 1]) for n in nodes], dtype=np.float64).reshape(-1, 3)
        for i, n in enumerate(nodes):
            if "matrix" in n:
                raise ValueError(f"node {self.names[i]!r} uses a matrix; only TRS nodes are supported")

        self.skins = []
        for skin in gltf.get("skins", []):
            ibm = (_accessor(gltf, binary, skin["inverseBindMatrices"]).astype(np.float64)
                   if "inverseBindMatrices" in skin else np.repeat(np.eye(4)[None], len(skin["joints"]), axis=0))
            self.skins.append((list(skin["joints"]), ibm))

        self.primitives: list[_Primitive] = []
        for ni, node in enumerate(nodes):
            if "mesh" not in node or "skin" not in node:
                continue
            for prim in gltf["meshes"][node["mesh"]]["primitives"]:
                attrs = prim["attributes"]
                if "JOINTS_0" not in attrs or "WEIGHTS_0" not in attrs:
                    continue
                pos = _accessor(gltf, binary, attrs["POSITION"]).astype(np.float64)
                faces = (_accessor(gltf, binary, prim["indices"]).reshape(-1, 3).astype(np.int64)
                         if "indices" in prim else np.arange(len(pos)).reshape(-1, 3))
                self.primitives.append(_Primitive(
                    mesh_node=ni,
                    skin=node["skin"],
                    positions=pos,
                    joints=_accessor(gltf, binary, attrs["JOINTS_0"]).astype(np.int64),
                    weights=_accessor(gltf, binary, attrs["WEIGHTS_0"]).astype(np.float64),
                    faces=faces,
                ))
        if not self.primitives:
            raise ValueError(f"{path} has no skinned mesh")

        self.times = np.zeros(1)
        self.tracks: dict[tuple[int, str], np.ndarray] = {}
        anims = gltf.get("animations", [])
        if anims:
            anim = anims[0]
            inputs = {s["input"] for s in anim["samplers"]}
            self.times = max((_accessor(gltf, binary, i).reshape(-1).astype(np.float64) for i in inputs), key=len)
            for ch in anim["channels"]:
                path_ = ch["target"]["path"]
                if path_ not in ("translation", "rotation", "scale") or "node" not in ch["target"]:
                    continue
                sampler = anim["samplers"][ch["sampler"]]
                t = _accessor(gltf, binary, sampler["input"]).reshape(-1).astype(np.float64)
                v = _accessor(gltf, binary, sampler["output"]).astype(np.float64)
                if len(t) != len(self.times) or not np.allclose(t, self.times):
                    v = np.stack([np.interp(self.times, t, v[:, k]) for k in range(v.shape[1])], axis=1)
                self.tracks[(ch["target"]["node"], path_)] = v
        self.n_frames = len(self.times)
        dt = np.diff(self.times)
        self.fps = float(1.0 / np.median(dt)) if len(dt) and np.median(dt) > 0 else 30.0
        self._label_parts()

    def _topological(self) -> list[int]:
        order, seen = [], set()

        def visit(i: int) -> None:
            if i in seen:
                return
            if self.parent[i] >= 0:
                visit(self.parent[i])
            seen.add(i)
            order.append(i)

        for i in range(len(self.parent)):
            visit(i)
        return order

    def _label_parts(self) -> None:
        for prim in self.primitives:
            joint_nodes, _ = self.skins[prim.skin]
            part_of_joint = np.array(
                [PARTS.index(p) if (p := part_of_bone(self.names[j])) else -1 for j in joint_nodes], dtype=np.int16
            )
            share = np.zeros((len(prim.positions), len(PARTS)))
            parts = part_of_joint[prim.joints]
            for k in range(prim.joints.shape[1]):
                ok = parts[:, k] >= 0
                np.add.at(share, (np.nonzero(ok)[0], parts[ok, k]), prim.weights[ok, k])
            prim.part = np.where(share.max(axis=1) > 0, share.argmax(axis=1), -1).astype(np.int16)

    def node_world(self, frame: int | None) -> np.ndarray:
        """(N, 4, 4) world matrices; frame None = rest pose (no animation)."""
        n = len(self.names)
        t, r, s = self.rest_t.copy(), self.rest_r.copy(), self.rest_s.copy()
        if frame is not None:
            for (node, path_), values in self.tracks.items():
                {"translation": t, "rotation": r, "scale": s}[path_][node] = values[frame]
        local = np.repeat(np.eye(4)[None], n, axis=0)
        local[:, :3, :3] = _quat_xyzw_to_mat(r) * s[:, None, :]
        local[:, :3, 3] = t
        world = np.empty_like(local)
        for i in self.order:
            p = self.parent[i]
            world[i] = local[i] if p < 0 else world[p] @ local[i]
        return world

    def skinned_positions(self, frame: int | None) -> list[np.ndarray]:
        world = self.node_world(frame)
        out = []
        for prim in self.primitives:
            joint_nodes, ibm = self.skins[prim.skin]
            palette = world[joint_nodes] @ ibm  # (J, 4, 4)
            m = np.einsum("vk,vkij->vij", prim.weights, palette[prim.joints])
            out.append(np.einsum("vij,vj->vi", m[:, :3, :3], prim.positions) + m[:, :3, 3])
        return out


# ---------------------------------------------------------------- intersection


def _vertex_normals(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
    p0, p1, p2 = vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]]
    face_n = np.cross(p1 - p0, p2 - p0)
    normals = np.zeros_like(vertices)
    for i in range(3):
        np.add.at(normals, faces[:, i], face_n)
    return normals / np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-12)


def _frame_depths(clip: SkinnedClip, frame: int | None) -> dict[tuple[int, int], float]:
    """Deepest penetration (metres) per unordered part pair in one frame."""
    from scipy.spatial import cKDTree

    posed = clip.skinned_positions(frame)
    pts = np.concatenate(posed)
    nrm = np.concatenate([_vertex_normals(v, p.faces) for v, p in zip(posed, clip.primitives)])
    part = np.concatenate([p.part for p in clip.primitives])

    groups = {}
    for k in range(len(PARTS)):
        idx = np.nonzero(part == k)[0]
        if len(idx):
            groups[k] = {"idx": idx, "lo": pts[idx].min(0), "hi": pts[idx].max(0)}
    trees: dict[int, cKDTree] = {}

    def inside(a: int, b: int) -> float:
        """How deep part a's vertices go into part b's surface."""
        src, dst = groups[a]["idx"], groups[b]["idx"]
        lo, hi = groups[b]["lo"] - 0.01, groups[b]["hi"] + 0.01
        near = src[np.all((pts[src] >= lo) & (pts[src] <= hi), axis=1)]
        if not len(near):
            return 0.0
        if b not in trees:
            trees[b] = cKDTree(pts[dst])
        dist, j = trees[b].query(pts[near], distance_upper_bound=_MAX_REACH_M)
        ok = np.isfinite(dist)
        if not ok.any():
            return 0.0
        p, q = pts[near[ok]], pts[dst[j[ok]]]
        n = nrm[dst[j[ok]]]
        d = p - q
        along = np.einsum("ij,ij->i", d, n)
        lateral = np.linalg.norm(d - along[:, None] * n, axis=1)
        depth = -along
        hit = (depth > 0) & (lateral <= np.maximum(_MIN_LATERAL_M, depth))
        return float(depth[hit].max()) if hit.any() else 0.0

    out: dict[tuple[int, int], float] = {}
    keys = sorted(groups)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            ga, gb = groups[a], groups[b]
            if np.any(ga["hi"] < gb["lo"] - 0.01) or np.any(gb["hi"] < ga["lo"] - 0.01):
                continue
            if frozenset((PARTS[a], PARTS[b])) in _ADJACENT:
                continue
            depth = max(inside(a, b), inside(b, a))
            if depth > 0:
                out[(a, b)] = depth
    return out


def _ranges(frames: list[int]) -> list[list[int]]:
    """Sorted frames -> [first, last] stretches; gaps of up to _MERGE_GAP frames are bridged."""
    out: list[list[int]] = []
    for f in frames:
        if out and f - out[-1][1] <= _MERGE_GAP + 1:
            out[-1][1] = f
        else:
            out.append([f, f])
    return out


def diagnose_glb(glb_path: Path, *, threshold_cm: float = DEFAULT_THRESHOLD_CM, verbose: bool = False) -> dict:
    """Self-intersection report for every frame of the GLB's first animation."""
    clip = SkinnedClip(glb_path)
    limit_m = threshold_cm / 100.0
    rest = {pair for pair, d in _frame_depths(clip, None).items() if d > limit_m}

    per_pair: dict[tuple[int, int], dict[int, float]] = {}
    for f in range(clip.n_frames):
        for pair, depth in _frame_depths(clip, f).items():
            if depth > limit_m:
                per_pair.setdefault(pair, {})[f] = depth
        if verbose and ((f + 1) % 200 == 0 or f + 1 == clip.n_frames):
            print(f"  diagnose {f + 1}/{clip.n_frames}")

    issues = []
    for (a, b), depths in per_pair.items():
        frames = sorted(depths)
        worst = max(frames, key=depths.get)
        issues.append({
            "kind": "self_intersection",
            "parts": [PARTS[a], PARTS[b]],
            "ranges": _ranges(frames),
            "frame_count": len(frames),
            "worst_frame": worst,
            "max_depth_cm": round(depths[worst] * 100.0, 2),
            "also_in_rest_pose": (a, b) in rest,
        })
    issues.sort(key=lambda i: (-i["max_depth_cm"], i["parts"]))
    all_frames = sorted({f for (_, _), depths in per_pair.items() for f in depths})

    return {
        "schema": SCHEMA,
        "source": clip.path.name,
        "generated": datetime.now().isoformat(timespec="seconds"),
        "frame_count": clip.n_frames,
        "fps": round(clip.fps, 3),
        "threshold_cm": threshold_cm,
        "summary": {
            "self_intersection": {
                "issue_count": len(issues),
                "frame_count": len(all_frames),
                "ranges": _ranges(all_frames),
                "max_depth_cm": max((i["max_depth_cm"] for i in issues), default=0.0),
            }
        },
        "issues": issues,
        "method": {
            "checks": "Self-intersection only. Floor contact is not checked.",
            "geometry": "Every frame of the GLB's first animation, posed with the file's own skin "
                        "(top-4 joint weights, linear blend skinning) — the mesh a glTF viewer shows.",
            "parts": "Vertices are grouped into 14 body parts by the Mixamo bones that carry most of "
                     "their skin weight; fingers belong to the hand.",
            "test": "A vertex is inside another part when it lies behind that part's nearest surface "
                    "vertex, against its normal. Depth is that distance, so it is approximate to about "
                    "the mesh's vertex spacing.",
            "neighbours": "Parts joined at a joint (e.g. upper arm and forearm, torso and thigh) are "
                          "not compared with each other: their skins meet at the joint.",
            "ranges": f"Stretches of one pair at most {_MERGE_GAP} frames apart are reported as one range.",
            "rest_pose": "Pairs that already intersect in the rest pose are labelled "
                         "also_in_rest_pose, not removed.",
            "frames": "Frame numbers match Blender after import (frame = time x fps); the first "
                      "animation frame is frame 0.",
        },
    }


def summary_line(report: dict) -> str:
    s = report["summary"]["self_intersection"]
    if not s["issue_count"]:
        return f"diagnostics: no self-intersection deeper than {report['threshold_cm']:g} cm"
    return (f"diagnostics: {s['issue_count']} self-intersection(s) over {s['frame_count']} of "
            f"{report['frame_count']} frames, deepest {s['max_depth_cm']:g} cm")


def diagnose_run(run_dir: Path, *, threshold_cm: float = DEFAULT_THRESHOLD_CM,
                 visualize: bool = False, verbose: bool = True) -> dict:
    """Diagnose <run_dir>/mixamo_character.glb; write diagnostics.json (and .html)."""
    run_dir = Path(run_dir)
    glb = run_dir / "mixamo_character.glb"
    if not glb.is_file():
        raise FileNotFoundError(f"{glb} not found — pass a run folder from `m2mr run`")
    report = diagnose_glb(glb, threshold_cm=threshold_cm, verbose=verbose)
    (run_dir / DIAGNOSTICS_JSON).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if visualize:
        from .diagnose_report import write_html_report

        write_html_report(run_dir / DIAGNOSTICS_HTML, glb, report, SkinnedClip(glb))
    return report
