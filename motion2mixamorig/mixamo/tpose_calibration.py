"""The single source of truth for the Mixamo Skeleton ↔ character Rig T-pose relationship.

    Mixamo Skeleton T-pose
            ↕  one global calibration
    character Rig rest T-pose

Both the T-pose inspection programs and the animation retargeting import this
module, so there is exactly one Front / Right / Up convention in the project.

Nothing here is a manual correction: the anatomical axes are measured from bone
positions, and the alignment is `B_rig @ B_skel.T` with no polar/SVD det fix and
no per-bone 90/180 patches.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .fbx_skeleton import extract_skeleton
from .kinematics import (
    MixamoRig,
    forward_kinematics,
    normalize,
    rig_from_skeleton_data,
    world_positions_m,
)

# Mixamo skeleton world (validated Human → Mixamo space):
#   +X = anatomical LEFT,  +Y = UP,  +Z = chest-forward (toes / FBX front).
LEFT_DIR = np.array([1.0, 0.0, 0.0])
RIGHT_DIR = np.array([-1.0, 0.0, 0.0])
UP_DIR = np.array([0.0, 1.0, 0.0])
DOWN_DIR = np.array([0.0, -1.0, 0.0])
FWD_DIR = np.array([0.0, 0.0, 1.0])

REQUIRED_BONES = (
    "mixamorig:Hips",
    "mixamorig:Spine",
    "mixamorig:Spine1",
    "mixamorig:Spine2",
    "mixamorig:Neck",
    "mixamorig:Head",
    "mixamorig:LeftShoulder",
    "mixamorig:LeftArm",
    "mixamorig:LeftForeArm",
    "mixamorig:LeftHand",
    "mixamorig:RightShoulder",
    "mixamorig:RightArm",
    "mixamorig:RightForeArm",
    "mixamorig:RightHand",
    "mixamorig:LeftUpLeg",
    "mixamorig:LeftLeg",
    "mixamorig:LeftFoot",
    "mixamorig:RightUpLeg",
    "mixamorig:RightLeg",
    "mixamorig:RightFoot",
)

SPINE_CHAIN = (
    "mixamorig:Spine",
    "mixamorig:Spine1",
    "mixamorig:Spine2",
    "mixamorig:Neck",
    "mixamorig:Head",
    "mixamorig:HeadTop_End",
)
LEFT_ARM_CHAIN = (
    "mixamorig:LeftShoulder",
    "mixamorig:LeftArm",
    "mixamorig:LeftForeArm",
    "mixamorig:LeftHand",
)
RIGHT_ARM_CHAIN = (
    "mixamorig:RightShoulder",
    "mixamorig:RightArm",
    "mixamorig:RightForeArm",
    "mixamorig:RightHand",
)
LEFT_LEG_CHAIN = ("mixamorig:LeftUpLeg", "mixamorig:LeftLeg", "mixamorig:LeftFoot")
RIGHT_LEG_CHAIN = ("mixamorig:RightUpLeg", "mixamorig:RightLeg", "mixamorig:RightFoot")
LEFT_TOE_CHAIN = ("mixamorig:LeftToeBase", "mixamorig:LeftToe_End")
RIGHT_TOE_CHAIN = ("mixamorig:RightToeBase", "mixamorig:RightToe_End")

# Anatomical bone correspondence. Left stays Left, Right stays Right.
# Human joint → Mixamo/Y Bot bone; the two rigs share these bone names.
ANATOMICAL_BONE_MAP = {
    "pelvis": "mixamorig:Hips",
    "spine1": "mixamorig:Spine",
    "spine2": "mixamorig:Spine1",
    "spine3": "mixamorig:Spine2",
    "neck": "mixamorig:Neck",
    "head": "mixamorig:Head",
    "left_collar": "mixamorig:LeftShoulder",
    "left_shoulder": "mixamorig:LeftArm",
    "left_elbow": "mixamorig:LeftForeArm",
    "left_wrist": "mixamorig:LeftHand",
    "right_collar": "mixamorig:RightShoulder",
    "right_shoulder": "mixamorig:RightArm",
    "right_elbow": "mixamorig:RightForeArm",
    "right_wrist": "mixamorig:RightHand",
    "left_hip": "mixamorig:LeftUpLeg",
    "left_knee": "mixamorig:LeftLeg",
    "left_ankle": "mixamorig:LeftFoot",
    "left_foot": "mixamorig:LeftToeBase",
    "right_hip": "mixamorig:RightUpLeg",
    "right_knee": "mixamorig:RightLeg",
    "right_ankle": "mixamorig:RightFoot",
    "right_foot": "mixamorig:RightToeBase",
}


def rest_length(rest: dict[str, np.ndarray], parent: str, child: str) -> float:
    return float(np.linalg.norm(rest[child] - rest[parent]))


def canonical_mixamo_tpose(rig: MixamoRig) -> dict[str, np.ndarray]:
    """Explicit Mixamo-skeleton T-pose. Not an animation frame.

    Uses Mixamo rest bone *lengths* and the validated Mixamo world axes:
    arms along ±X (left = +X), spine +Y, legs −Y, feet +Z. Hip / clavicle
    widths keep the rest lateral offsets so proportions stay Mixamo's.
    """
    rest = world_positions_m(rig, forward_kinematics(rig, {}))
    pos: dict[str, np.ndarray] = {"mixamorig:Hips": np.zeros(3)}

    def place(child: str, parent: str, direction: np.ndarray) -> None:
        length = rest_length(rest, parent, child)
        pos[child] = pos[parent] + normalize(direction) * length

    for child in SPINE_CHAIN:
        parent = rig.bones[child].parent
        place(child, parent, UP_DIR)

    def lateral_then_chain(first: str, chain: tuple[str, ...], side_sign: float, along: np.ndarray) -> None:
        parent = rig.bones[first].parent
        offset = rest[first] - rest[parent]
        lateral = np.array([side_sign * abs(float(offset[0])), float(offset[1]), 0.0])
        if float(np.linalg.norm(lateral)) < 1e-8:
            lateral = np.array([side_sign, 0.0, 0.0])
        place(first, parent, lateral)
        for child in chain[1:]:
            p = rig.bones[child].parent
            place(child, p, along)

    lateral_then_chain("mixamorig:LeftShoulder", LEFT_ARM_CHAIN, +1.0, LEFT_DIR)
    for child in LEFT_ARM_CHAIN[1:]:
        place(child, rig.bones[child].parent, LEFT_DIR)
    lateral_then_chain("mixamorig:RightShoulder", RIGHT_ARM_CHAIN, -1.0, RIGHT_DIR)
    for child in RIGHT_ARM_CHAIN[1:]:
        place(child, rig.bones[child].parent, RIGHT_DIR)

    lateral_then_chain("mixamorig:LeftUpLeg", LEFT_LEG_CHAIN, +1.0, DOWN_DIR)
    for child in LEFT_LEG_CHAIN[1:]:
        place(child, rig.bones[child].parent, DOWN_DIR)
    lateral_then_chain("mixamorig:RightUpLeg", RIGHT_LEG_CHAIN, -1.0, DOWN_DIR)
    for child in RIGHT_LEG_CHAIN[1:]:
        place(child, rig.bones[child].parent, DOWN_DIR)

    for child in LEFT_TOE_CHAIN:
        place(child, rig.bones[child].parent, FWD_DIR)
    for child in RIGHT_TOE_CHAIN:
        place(child, rig.bones[child].parent, FWD_DIR)

    return pos


def rig_rest_from_skeleton_data(data: dict, fbx_path: Path) -> tuple[dict[str, np.ndarray], dict]:
    """Core Mixamo bones from the character FBX rest pose.

    PreRotation is already inside the local matrix. Assimp
    `$AssimpFbx$_PreRotation` helpers are not anatomical bones; extract_skeleton
    applies Maya/FBX `T * Rpre * R * ...` so those extra nodes are not listed.
    """
    pos: dict[str, np.ndarray] = {}
    for bone in data["bones"]:
        pos[str(bone["name"])] = np.asarray(bone["rest_world"]["translation_m"], dtype=np.float64)
    missing = [name for name in REQUIRED_BONES if name not in pos]
    if missing:
        raise RuntimeError(f"{fbx_path.name} is missing required Mixamo bones: {missing}")
    meta = {
        "source_fbx": data.get("source_fbx"),
        "fbx_version": data.get("fbx_version"),
        "coord_system": data.get("coord_system"),
        "transform_convention": data.get("transform_convention"),
        "bone_count": data.get("bone_count"),
        "character": data.get("character"),
    }
    return pos, meta


def hips_origin(pos: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    origin = np.asarray(pos["mixamorig:Hips"], dtype=np.float64)
    return {name: np.asarray(p, dtype=np.float64) - origin for name, p in pos.items()}


def body_height(pos: dict[str, np.ndarray]) -> float:
    return float(np.linalg.norm(pos["mixamorig:Head"] - pos["mixamorig:Hips"]))


def scale_to_height(pos: dict[str, np.ndarray], height: float) -> dict[str, np.ndarray]:
    h = body_height(pos)
    if h < 1e-8:
        raise RuntimeError("degenerate pelvis→head height")
    s = float(height / h)
    return {name: p * s for name, p in pos.items()}


def anatomical_axes(pos: dict[str, np.ndarray], label: str, *, verbose: bool = True) -> dict:
    """Right = right_hip − left_hip, Up = neck − pelvis. Front from the two crosses."""
    left_hip = pos["mixamorig:LeftUpLeg"]
    right_hip = pos["mixamorig:RightUpLeg"]
    pelvis = pos["mixamorig:Hips"]
    neck = pos["mixamorig:Neck"]
    mid_sh = 0.5 * (pos["mixamorig:LeftArm"] + pos["mixamorig:RightArm"])
    toe = pos["mixamorig:LeftToeBase"] - pos["mixamorig:LeftFoot"]
    chest_hint = mid_sh - pelvis
    if float(np.linalg.norm(chest_hint)) < 1e-6:
        chest_hint = toe

    right_raw = right_hip - left_hip
    up_raw = neck - pelvis
    up = normalize(up_raw, UP_DIR)
    right = right_raw - up * float(right_raw @ up)
    right = normalize(right, RIGHT_DIR)

    cross_right_up = np.cross(right, up)
    cross_up_right = np.cross(up, right)
    n_ru = float(np.linalg.norm(cross_right_up))
    n_ur = float(np.linalg.norm(cross_up_right))
    fwd_ru = cross_right_up / n_ru if n_ru > 1e-12 else np.zeros(3)
    fwd_ur = cross_up_right / n_ur if n_ur > 1e-12 else np.zeros(3)

    hint = normalize(chest_hint, FWD_DIR)
    toe_u = normalize(toe, FWD_DIR)
    score_ru = float(hint @ fwd_ru) + float(toe_u @ fwd_ru)
    score_ur = float(hint @ fwd_ur) + float(toe_u @ fwd_ur)
    use_up_cross_right = score_ur >= score_ru
    forward = fwd_ur if use_up_cross_right else fwd_ru
    formula = "up × right" if use_up_cross_right else "right × up"

    basis = np.column_stack([right, up, forward])
    det = float(np.linalg.det(basis))
    if verbose:
        print(f"\n=== {label} anatomical axes ===")
        print(f"  right  (RightUpLeg − LeftUpLeg, ortho to up)  {np.round(right, 6)}")
        print(f"  up     (Neck − Hips)                          {np.round(up, 6)}")
        print(f"  right × up                                    {np.round(fwd_ru, 6)}  chest· = {float(hint @ fwd_ru):+.4f}  toe· = {float(toe_u @ fwd_ru):+.4f}")
        print(f"  up × right                                    {np.round(fwd_ur, 6)}  chest· = {float(hint @ fwd_ur):+.4f}  toe· = {float(toe_u @ fwd_ur):+.4f}")
        print(f"  FRONT chosen                                  {formula}")
        print(f"  forward                                       {np.round(forward, 6)}")
        print(f"  basis columns [Right | Up | Forward]")
        print(f"  det(basis)                                    {det:+.6f}")
        if det < 0.0:
            print("  FLAG  det < 0  — anatomical [Right|Up|Forward] is left-handed in this world.")
            print("         Expected for Mixamo: anatomical right is world −X (world +X is character left).")
            print("         This labels the existing world; it is not a transform we apply.")
        elif abs(det - 1.0) > 1e-3:
            print(f"  FLAG  |det| not 1  — basis is not orthonormal-proper.")
        else:
            print("  det ≈ +1  right-handed orthonormal frame.")
    return {
        "right": right,
        "up": up,
        "forward": forward,
        "basis": basis,
        "det": det,
        "front_formula": formula,
        "cross_right_up": fwd_ru,
        "cross_up_right": fwd_ur,
        "chest_hint": hint,
        "toe_hint": toe_u,
    }


def global_alignment(skel: dict, rig: dict, *, verbose: bool = True) -> dict:
    """R such that R @ skeleton_axis ≈ rig_axis for Right, Up, Forward.

    R = B_rig @ B_skel.T. Not polar-projected. A det −1 result is a reflection
    and is flagged, not silently corrected with a 180° yaw.
    """
    b_s = skel["basis"]
    b_r = rig["basis"]
    r = b_r @ b_s.T
    det = float(np.linalg.det(r))
    if verbose:
        print("\n=== candidate global alignment  R_skeleton_to_rig ===")
        print("  maps  Skeleton Right/Up/Forward  →  Rig Right/Up/Forward")
        print(r)
        print(f"  det(R_skeleton_to_rig) = {det:+.6f}")
        if det < 0.0:
            print("  FLAG  det < 0  — this is a REFLECTION / mirror. Not applied as a rotation.")
            print("  No SVD/polar flip, no rotY(180) substitute.")
        elif abs(det - 1.0) > 5e-3:
            print("  FLAG  det is not +1  — not a proper rotation.")
        else:
            print("  det ≈ +1  proper rotation (no reflection).")
        mapped = r @ b_s
        print("  R @ skeleton_right    ", np.round(mapped[:, 0], 6), "  vs rig", np.round(b_r[:, 0], 6))
        print("  R @ skeleton_up       ", np.round(mapped[:, 1], 6), "  vs rig", np.round(b_r[:, 1], 6))
        print("  R @ skeleton_forward  ", np.round(mapped[:, 2], 6), "  vs rig", np.round(b_r[:, 2], 6))
    return {"R": r, "det": det}


def apply_global(
    pos: dict[str, np.ndarray],
    r: np.ndarray,
    scale: float,
    translation: np.ndarray,
) -> dict[str, np.ndarray]:
    return {name: scale * (r @ p) + translation for name, p in pos.items()}


@dataclass(frozen=True)
class TposeCalibration:
    """Frozen result of the accepted T-pose orientation check.

    `skeleton_axes` / `rig_axes` are the anatomical [Right | Up | Forward] bases
    that produced the accepted FRONT/BACK/LEFT/RIGHT images. `r_skeleton_to_rig`
    maps one onto the other. `height_scale` stretches the Mixamo pelvis→head
    length onto the character rig's for visualisation only.
    """

    skeleton_rig: MixamoRig
    skeleton_tpose: dict[str, np.ndarray]
    rig_rest: dict[str, np.ndarray]
    skeleton_axes: dict
    rig_axes: dict
    r_skeleton_to_rig: np.ndarray
    height_scale: float
    fbx_meta: dict
    fbx_path: Path

    @property
    def forward(self) -> np.ndarray:
        """Anatomical FRONT in the character rig world. Used by the fixed render camera."""
        return np.asarray(self.rig_axes["forward"], dtype=np.float64)

    @property
    def up(self) -> np.ndarray:
        return np.asarray(self.rig_axes["up"], dtype=np.float64)

    @property
    def right(self) -> np.ndarray:
        return np.asarray(self.rig_axes["right"], dtype=np.float64)


def load_calibration(fbx_path: Path, *, verbose: bool = False) -> TposeCalibration:
    """T-pose calibration between the Mixamo core skeleton and the character rig.

    Both sides come from the same character FBX: the core-bone skeleton drives
    the retarget, the full rig receives the motion. Everything is measured from
    the file; nothing is hand-authored.
    """
    fbx_path = Path(fbx_path)
    data = extract_skeleton(fbx_path)
    rig = rig_from_skeleton_data(data, fbx_path)
    skel = hips_origin(canonical_mixamo_tpose(rig))
    rest_raw, fbx_meta = rig_rest_from_skeleton_data(data, fbx_path)
    rest = hips_origin(rest_raw)

    ref_h = body_height(rest)
    skel_n = scale_to_height(skel, ref_h)
    height_scale = float(ref_h / body_height(skel))

    skel_axes = anatomical_axes(skel_n, "Mixamo skeleton T-pose", verbose=verbose)
    rig_axes = anatomical_axes(rest, f"{fbx_path.stem} FBX rest rig", verbose=verbose)
    align = global_alignment(skel_axes, rig_axes, verbose=verbose)

    return TposeCalibration(
        skeleton_rig=rig,
        skeleton_tpose=skel_n,
        rig_rest=rest,
        skeleton_axes=skel_axes,
        rig_axes=rig_axes,
        r_skeleton_to_rig=align["R"],
        height_scale=height_scale,
        fbx_meta=fbx_meta,
        fbx_path=fbx_path,
    )
