"""Mixamo Y Bot FK that keeps FBX PreRotation as a separate node.

Maya/FBX (and Assimp's extra PreRotation node) compose as:

    M_local = T * Rpre * R_anim
    M_world = M_parent_world * M_local

R_anim is the animated Lcl Rotation. Rpre is rest-only and is never baked
into R_anim. Bone lengths live in T (Lcl Translation) and stay constant.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from .fbx_skeleton import matrix_to_quat_wxyz


def _as_vec3(value: Iterable[float]) -> np.ndarray:
    return np.asarray(list(value)[:3], dtype=np.float64)


def _as_mat3(value) -> np.ndarray:
    return np.asarray(value, dtype=np.float64).reshape(3, 3)


def _as_mat4(value) -> np.ndarray:
    return np.asarray(value, dtype=np.float64).reshape(4, 4)


def normalize(v: np.ndarray, fallback: np.ndarray | None = None) -> np.ndarray:
    v = np.asarray(v, dtype=np.float64).reshape(3)
    n = float(np.linalg.norm(v))
    if n < 1e-10:
        if fallback is None:
            raise ValueError("cannot normalize a near-zero vector")
        return np.asarray(fallback, dtype=np.float64).reshape(3)
    return v / n


def rotation_aligning(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """Shortest rotation R with R @ src = dst (column vectors). Twist-free swing."""
    a = normalize(src, np.array([0.0, 1.0, 0.0]))
    b = normalize(dst, np.array([0.0, 1.0, 0.0]))
    cosine = float(np.clip(a @ b, -1.0, 1.0))
    axis = np.cross(a, b)
    sine = float(np.linalg.norm(axis))
    if cosine > 0.999999:
        return np.eye(3)
    if cosine < -0.999999:
        helper = np.array([1.0, 0.0, 0.0]) if abs(a[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        axis = normalize(np.cross(a, helper))
        return 2.0 * np.outer(axis, axis) - np.eye(3)
    skew = np.array(
        [[0.0, -axis[2], axis[1]], [axis[2], 0.0, -axis[0]], [-axis[1], axis[0], 0.0]],
        dtype=np.float64,
    )
    return np.eye(3) + skew + skew @ skew * ((1.0 - cosine) / (sine * sine))


def orthonormal_frame(left: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Right-handed Mixamo axes: columns = (left=+X, up=+Y, forward=+Z)."""
    up_u = normalize(up, np.array([0.0, 1.0, 0.0]))
    left_rej = left - up_u * float(left @ up_u)
    if float(np.linalg.norm(left_rej)) < 1e-8:
        helper = np.array([1.0, 0.0, 0.0]) if abs(up_u[0]) < 0.9 else np.array([0.0, 0.0, 1.0])
        left_rej = np.cross(helper, up_u)
    left_u = normalize(left_rej)
    fwd = normalize(np.cross(left_u, up_u))
    left_u = normalize(np.cross(up_u, fwd))
    return np.column_stack([left_u, up_u, fwd])


def angle_deg(a: np.ndarray, b: np.ndarray) -> float:
    ua = normalize(a, np.array([0.0, 1.0, 0.0]))
    ub = normalize(b, np.array([0.0, 1.0, 0.0]))
    return float(np.degrees(np.arccos(np.clip(ua @ ub, -1.0, 1.0))))


def mat4(rotation: np.ndarray, translation: np.ndarray) -> np.ndarray:
    out = np.eye(4)
    out[:3, :3] = rotation
    out[:3, 3] = translation
    return out


def rh_axes(lateral: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Right-handed columns (lateral, up, lateral × up)."""
    up_u = normalize(up, np.array([0.0, 1.0, 0.0]))
    lat_rej = lateral - up_u * float(lateral @ up_u)
    if float(np.linalg.norm(lat_rej)) < 1e-8:
        helper = np.array([1.0, 0.0, 0.0]) if abs(up_u[0]) < 0.9 else np.array([0.0, 0.0, 1.0])
        lat_rej = np.cross(helper, up_u)
    lat_u = normalize(lat_rej)
    fwd = normalize(np.cross(lat_u, up_u))
    lat_u = normalize(np.cross(up_u, fwd))
    up_u = normalize(np.cross(fwd, lat_u))
    return np.column_stack([lat_u, up_u, fwd])


def human_body_frame(joints_or_right, up: np.ndarray | None = None) -> np.ndarray:
    """Human torso columns (right, up, chest-forward).

    chest-forward = right × up (matches the source video: f253 faces +X).
    up × right is the back.
    """
    if up is None:
        raise TypeError("human_body_frame(right, up)")
    return rh_axes(joints_or_right, up)


def mixamo_bone_frame(left: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Mixamo rest bone columns (left=+X, up=+Y, chest-forward=+Z)."""
    return rh_axes(left, up)


def body_frame_from_landmarks(right: np.ndarray, up: np.ndarray, chest_hint: np.ndarray) -> np.ndarray:
    """Columns (right, up, forward). Forward is whichever of right×up / up×right matches chest_hint.

    Does not recross `right` from up×forward. That would force det +1 by flipping
    Mixamo's anatomical right onto character left.
    """
    up_u = normalize(up, np.array([0.0, 1.0, 0.0]))
    right_rej = right - up_u * float(np.asarray(right, dtype=np.float64) @ up_u)
    right_u = normalize(right_rej)
    fwd_ru = np.cross(right_u, up_u)
    fwd_ur = np.cross(up_u, right_u)
    hint = np.asarray(chest_hint, dtype=np.float64).reshape(3)
    fwd = fwd_ur if float(hint @ fwd_ur) >= float(hint @ fwd_ru) else fwd_ru
    return np.column_stack([right_u, up_u, normalize(fwd)])


def body_align_from_bases(r_human: np.ndarray, r_mixamo: np.ndarray, *, proper: bool = False) -> np.ndarray:
    """Linear map R with R @ r_human ≈ r_mixamo.

    The anatomical Human→Mixamo map (right→right, up→up, chest→chest) has det −1
    because Mixamo rest +X is character left. `proper=True` polar-projects onto
    SO(3). Identity and rotY(180) are equally close; neither matches all three axes.
    """
    a = np.asarray(r_mixamo, dtype=np.float64) @ np.asarray(r_human, dtype=np.float64).T
    if not proper:
        return a
    u, _, vt = np.linalg.svd(a)
    r = u @ vt
    if float(np.linalg.det(r)) < 0.0:
        u = u.copy()
        u[:, -1] *= -1.0
        r = u @ vt
    return r


# Maps the capture's anatomical triad onto Mixamo's:
#   Human  (right, up, chest) = (+X, +Y, −Z)
#   Mixamo (right, up, chest) = (−X, +Y, +Z)   # rest +X is character left
# Anatomy obeys chest = up × right, so both triads are left-handed and the map
# between them is a proper rotation: rotY(180), det +1, no reflection.
#
# The capture's chest axis is −Z, measured rather than assumed: over all frames
# the toes-anterior and knees-bow-anterior directions agree to 5.4 deg mean and
# both sit ~167 deg from +Z. Taking chest as +Z makes this map the reflection
# diag(-1, 1, 1), which lands the body's front on Mixamo's back and inverts
# laterality — the torso-backward bug.
R_BODY_ALIGN = np.diag([-1.0, 1.0, -1.0])


def human_to_mixamo(p: np.ndarray) -> np.ndarray:
    """Human world (m) → Mixamo FBX world by one global body-frame map.

    Human: +X = anatomical right, +Y = up, −Z = chest-forward.
    Mixamo rest: +X = anatomical left, +Y = up, +Z = chest-forward (toes / FBX front).

        p_mixamo = R_BODY_ALIGN @ p_human = [-x, y, -z]
    """
    p = np.asarray(p, dtype=np.float64)
    return np.asarray(p, dtype=np.float64) @ R_BODY_ALIGN.T


@dataclass
class MixamoBone:
    name: str
    parent: str | None
    children: list[str]
    pre_rotation: np.ndarray
    lcl_translation_cm: np.ndarray
    rest_world: np.ndarray
    rest_local: np.ndarray
    pre_rotation_euler_deg: np.ndarray


@dataclass
class MixamoRig:
    bones: dict[str, MixamoBone]
    order: list[str]
    meters_per_unit: float
    source: Path
    coord_system: dict = field(default_factory=dict)

    @property
    def root(self) -> str:
        return self.order[0]

    def child_offset_cm(self, parent: str, child: str) -> np.ndarray:
        return self.bones[child].lcl_translation_cm.copy()


def rig_from_skeleton_data(data: dict[str, Any], source: Path) -> MixamoRig:
    """Build a MixamoRig from the dict `fbx_skeleton.extract_skeleton` returns."""
    bones: dict[str, MixamoBone] = {}
    for raw in data["bones"]:
        name = str(raw["name"])
        bones[name] = MixamoBone(
            name=name,
            parent=raw["parent"],
            children=list(raw["children"]),
            pre_rotation=_as_mat3(raw["pre_rotation_matrix"]),
            lcl_translation_cm=_as_vec3(raw["lcl_translation"]),
            rest_world=_as_mat4(raw["rest_world"]["matrix"]),
            rest_local=_as_mat4(raw["rest_local"]["matrix"]),
            pre_rotation_euler_deg=_as_vec3(raw["pre_rotation_euler_deg"]),
        )
    return MixamoRig(
        bones=bones,
        order=[b["name"] for b in data["bones"]],
        meters_per_unit=float(data["coord_system"]["meters_per_fbx_unit"]),
        source=Path(source),
        coord_system=dict(data["coord_system"]),
    )


def load_mixamo_rig(path: Path) -> MixamoRig:
    """Load a core-bone rig from a previously exported skeleton JSON."""
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return rig_from_skeleton_data(data, path)


def local_matrix(bone: MixamoBone, r_anim: np.ndarray, translation_cm: np.ndarray | None = None) -> np.ndarray:
    """Assimp-equivalent local node: T * Rpre * R_anim."""
    t = bone.lcl_translation_cm if translation_cm is None else np.asarray(translation_cm, dtype=np.float64)
    return mat4(bone.pre_rotation @ r_anim, t)


def forward_kinematics(
    rig: MixamoRig,
    r_anim: dict[str, np.ndarray] | None = None,
    hips_translation_cm: np.ndarray | None = None,
    lcl_translations_cm: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    """World 4x4 for every bone. Missing R_anim entries stay identity (rest)."""
    anim = r_anim or {}
    extra_t = lcl_translations_cm or {}
    world: dict[str, np.ndarray] = {}
    for name in rig.order:
        bone = rig.bones[name]
        rot = np.asarray(anim.get(name, np.eye(3)), dtype=np.float64)
        if name == rig.root and hips_translation_cm is not None:
            trans = hips_translation_cm
        elif name in extra_t:
            trans = extra_t[name]
        else:
            trans = None
        local = local_matrix(bone, rot, trans)
        if bone.parent is None:
            world[name] = local
        else:
            world[name] = world[bone.parent] @ local
    return world


def world_positions_m(rig: MixamoRig, world: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    scale = rig.meters_per_unit
    return {name: mat[:3, 3] * scale for name, mat in world.items()}


def bone_direction_world(rig: MixamoRig, world: dict[str, np.ndarray], parent: str, child: str) -> np.ndarray:
    """World direction of parent→child. Independent of child's own rotation."""
    offset = rig.child_offset_cm(parent, child)
    return world[parent][:3, :3] @ offset


def anim_from_world_rotation(bone: MixamoBone, r_parent_world: np.ndarray, r_world: np.ndarray) -> np.ndarray:
    """R_anim such that R_parent * Rpre * R_anim = R_world."""
    return bone.pre_rotation.T @ r_parent_world.T @ r_world


def swing_anim_to_direction(
    rig: MixamoRig,
    world: dict[str, np.ndarray],
    bone_name: str,
    child_name: str | None,
    target_dir_world: np.ndarray,
    d_local: np.ndarray | None = None,
) -> np.ndarray:
    """Lcl Rotation that aims this bone's rest axis at target_dir_world.

    Rest axis is the child's Lcl Translation (Mixamo local +Y) after PreRotation:
        R_parent * Rpre * R_anim * d_local = d_target
    """
    bone = rig.bones[bone_name]
    parent_r = np.eye(3) if bone.parent is None else world[bone.parent][:3, :3]
    if d_local is None:
        if child_name is None:
            raise ValueError(f"{bone_name}: need child_name or d_local")
        d_local = rig.child_offset_cm(bone_name, child_name)
    d_in_anim = bone.pre_rotation.T @ parent_r.T @ normalize(target_dir_world)
    return rotation_aligning(d_local, d_in_anim)


def frame_from_primary_secondary(primary: np.ndarray, secondary: np.ndarray) -> np.ndarray:
    """Orthonormal basis: columns = (primary, secondary_ortho, primary × secondary_ortho)."""
    p = normalize(primary, np.array([0.0, 1.0, 0.0]))
    s = secondary - p * float(secondary @ p)
    if float(np.linalg.norm(s)) < 1e-8:
        helper = np.array([0.0, 1.0, 0.0]) if abs(p[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
        s = np.cross(helper, p)
    s = normalize(s)
    t = np.cross(p, s)
    return np.column_stack([p, s, t])


def frame_anim_from_two_vectors(
    bone: MixamoBone,
    r_parent_world: np.ndarray,
    rest_primary_local: np.ndarray,
    rest_secondary_local: np.ndarray,
    tgt_primary_world: np.ndarray,
    tgt_secondary_world: np.ndarray,
) -> np.ndarray:
    """Lcl Rotation mapping rest local (primary, secondary) onto world targets.

    Used for feet: primary = ankle→toe (forward), secondary = world up (twist).
    """
    r_rest_world = r_parent_world @ bone.pre_rotation
    r_rest_frame = frame_from_primary_secondary(
        r_rest_world @ rest_primary_local, r_rest_world @ rest_secondary_local
    )
    r_tgt_frame = frame_from_primary_secondary(tgt_primary_world, tgt_secondary_world)
    r_world = (r_tgt_frame @ r_rest_frame.T) @ r_rest_world
    return bone.pre_rotation.T @ r_parent_world.T @ r_world


def frame_anim_from_axes(
    bone: MixamoBone,
    r_parent_world: np.ndarray,
    rest_left_local: np.ndarray,
    rest_up_local: np.ndarray,
    tgt_left_world: np.ndarray,
    tgt_up_world: np.ndarray,
) -> np.ndarray:
    """Lcl Rotation that maps rest local (left, up) onto the world target axes.

    Used for Hips and Spine2 so clavicle attachments keep a chest twist, not a
    free swing around the spine.
    """
    r_rest_world = r_parent_world @ bone.pre_rotation
    r_rest_frame = orthonormal_frame(r_rest_world @ rest_left_local, r_rest_world @ rest_up_local)
    r_tgt_frame = orthonormal_frame(tgt_left_world, tgt_up_world)
    r_world = (r_tgt_frame @ r_rest_frame.T) @ r_rest_world
    return bone.pre_rotation.T @ r_parent_world.T @ r_world



def quat_wxyz(rmat: np.ndarray) -> np.ndarray:
    return matrix_to_quat_wxyz(rmat)


def local_aim_axis(rig: MixamoRig, bone_name: str) -> np.ndarray:
    """Rest bone axis in the bone's local (pre-R_anim) frame. Mixamo +Y, or the first child offset."""
    bone = rig.bones[bone_name]
    if bone.children:
        return rig.child_offset_cm(bone_name, bone.children[0])
    return np.array([0.0, 1.0, 0.0])


def geodesic_angle_deg(r_a: np.ndarray, r_b: np.ndarray) -> float:
    rel = np.asarray(r_a, dtype=np.float64).T @ np.asarray(r_b, dtype=np.float64)
    cosine = (float(np.trace(rel)) - 1.0) * 0.5
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))


def rotation_180_around(axis: np.ndarray) -> np.ndarray:
    n = normalize(axis, np.array([0.0, 1.0, 0.0]))
    return 2.0 * np.outer(n, n) - np.eye(3)


def pick_closest_aim_twist(
    r_curr: np.ndarray,
    r_prev: np.ndarray | None,
    axis: np.ndarray,
) -> tuple[np.ndarray, bool]:
    """Keep the independent aim. If a 180° twist around the bone axis is closer to r_prev, use it.

    Does not blend or smooth: only the discrete antipodal twist that still aims the same way.
    """
    r_curr = np.asarray(r_curr, dtype=np.float64)
    if r_prev is None:
        return r_curr, False
    r_prev = np.asarray(r_prev, dtype=np.float64)
    r_flip = r_curr @ rotation_180_around(axis)
    if geodesic_angle_deg(r_flip, r_prev) + 1e-9 < geodesic_angle_deg(r_curr, r_prev):
        return r_flip, True
    return r_curr, False


def continue_quaternion(q_curr: np.ndarray, q_prev: np.ndarray | None) -> tuple[np.ndarray, bool]:
    """If dot(q_t, q_{t-1}) < 0, use -q_t. Quaternion double-cover only; same rotation matrix."""
    q = np.asarray(q_curr, dtype=np.float64).reshape(4)
    n = float(np.linalg.norm(q))
    if n < 1e-12:
        q = np.array([1.0, 0.0, 0.0, 0.0])
    else:
        q = q / n
    if q_prev is not None and float(np.dot(q, np.asarray(q_prev, dtype=np.float64).reshape(4))) < 0.0:
        return -q, True
    return q, False
