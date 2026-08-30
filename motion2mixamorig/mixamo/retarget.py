"""Human → Mixamo per-frame retarget.

FK is T * Rpre * R_anim. Mixamo rest bone lengths are never scaled.
Optional previous-frame rotations pick the 180-degree twist closest to the
last frame and enforce quaternion sign continuity. No temporal smoothing.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .kinematics import (
    MixamoRig,
    anim_from_world_rotation,
    continue_quaternion,
    forward_kinematics,
    frame_anim_from_axes,
    frame_anim_from_two_vectors,
    human_to_mixamo,
    local_aim_axis,
    normalize,
    orthonormal_frame,
    pick_closest_aim_twist,
    quat_wxyz,
    swing_anim_to_direction,
    world_positions_m,
)

CONTROLLED = (
    "mixamorig:Hips",
    "mixamorig:Spine",
    "mixamorig:Spine1",
    "mixamorig:Spine2",
    "mixamorig:Neck",
    "mixamorig:Head",
    "mixamorig:LeftShoulder",
    "mixamorig:RightShoulder",
    "mixamorig:LeftArm",
    "mixamorig:RightArm",
    "mixamorig:LeftForeArm",
    "mixamorig:RightForeArm",
    "mixamorig:LeftHand",
    "mixamorig:RightHand",
    "mixamorig:LeftUpLeg",
    "mixamorig:RightUpLeg",
    "mixamorig:LeftLeg",
    "mixamorig:RightLeg",
    "mixamorig:LeftFoot",
    "mixamorig:RightFoot",
    "mixamorig:LeftToeBase",
    "mixamorig:RightToeBase",
)

# Mixamo bone → (human parent joint, human child joint) used as the aim vector.
# Spine2 uses a chest frame (not a single swing) so clavicle attachments keep the right twist.
#
# Neck/Head must not aim along SMPL neck→head. That vector is a short (~9 cm)
# skull-center offset, often 50–70° from vertical, and flops Mixamo's longer
# neck/head bones. spine3→head is the stable head-up (skull above the chest)
# while still using the Human head joint. Joint mapping remains
# neck→mixamorig:Neck and head→mixamorig:Head.
#
# Mixamo Neck→Head and Head→HeadTop rest translations are not along local +Y
# (they include a forward +Z offset). Aiming that offset at head-up tilts the
# neck/head bones. Neck/Head therefore swing local +Y.
NECK_HEAD = ("mixamorig:Neck", "mixamorig:Head")
NECK_HEAD_AIM_LOCAL = np.array([0.0, 1.0, 0.0])

SWING_TARGETS = {
    "mixamorig:Spine": ("spine1", "spine2"),
    "mixamorig:Spine1": ("spine2", "spine3"),
    "mixamorig:Neck": ("spine3", "head"),
    "mixamorig:Head": ("spine3", "head"),
    "mixamorig:LeftShoulder": ("left_collar", "left_shoulder"),
    "mixamorig:LeftArm": ("left_shoulder", "left_elbow"),
    "mixamorig:LeftForeArm": ("left_elbow", "left_wrist"),
    "mixamorig:RightShoulder": ("right_collar", "right_shoulder"),
    "mixamorig:RightArm": ("right_shoulder", "right_elbow"),
    "mixamorig:RightForeArm": ("right_elbow", "right_wrist"),
    "mixamorig:LeftUpLeg": ("left_hip", "left_knee"),
    "mixamorig:LeftLeg": ("left_knee", "left_ankle"),
    "mixamorig:RightUpLeg": ("right_hip", "right_knee"),
    "mixamorig:RightLeg": ("right_knee", "right_ankle"),
}

SWING_TARGETS_NO_CLAVICLE = {
    "mixamorig:Spine": ("spine1", "spine2"),
    "mixamorig:Spine1": ("spine2", "spine3"),
    "mixamorig:Spine2": ("spine3", "neck"),
    "mixamorig:LeftArm": ("left_shoulder", "left_elbow"),
    "mixamorig:LeftForeArm": ("left_elbow", "left_wrist"),
    "mixamorig:RightArm": ("right_shoulder", "right_elbow"),
    "mixamorig:RightForeArm": ("right_elbow", "right_wrist"),
}

# Child that defines this bone's rest axis (local +Y after PreRotation).
AIM_CHILD = {
    "mixamorig:Spine": "mixamorig:Spine1",
    "mixamorig:Spine1": "mixamorig:Spine2",
    "mixamorig:Spine2": "mixamorig:Neck",
    "mixamorig:Neck": "mixamorig:Head",
    "mixamorig:Head": "mixamorig:HeadTop_End",
    "mixamorig:LeftShoulder": "mixamorig:LeftArm",
    "mixamorig:LeftArm": "mixamorig:LeftForeArm",
    "mixamorig:LeftForeArm": "mixamorig:LeftHand",
    "mixamorig:RightShoulder": "mixamorig:RightArm",
    "mixamorig:RightArm": "mixamorig:RightForeArm",
    "mixamorig:RightForeArm": "mixamorig:RightHand",
    "mixamorig:LeftUpLeg": "mixamorig:LeftLeg",
    "mixamorig:LeftLeg": "mixamorig:LeftFoot",
    "mixamorig:LeftFoot": "mixamorig:LeftToeBase",
    "mixamorig:LeftToeBase": "mixamorig:LeftToe_End",
    "mixamorig:RightUpLeg": "mixamorig:RightLeg",
    "mixamorig:RightLeg": "mixamorig:RightFoot",
    "mixamorig:RightFoot": "mixamorig:RightToeBase",
    "mixamorig:RightToeBase": "mixamorig:RightToe_End",
}


def swing_aim_local(rig: MixamoRig, bone_name: str) -> np.ndarray:
    """Rest axis that swing_anim_to_direction aligns with the Human target."""
    if bone_name in NECK_HEAD:
        return NECK_HEAD_AIM_LOCAL.copy()
    return rig.child_offset_cm(bone_name, AIM_CHILD[bone_name])


MIXAMO_TO_HUMAN = {
    "mixamorig:Hips": "pelvis",
    "mixamorig:Spine": "spine1",
    "mixamorig:Spine1": "spine2",
    "mixamorig:Spine2": "spine3",
    "mixamorig:Neck": "neck",
    "mixamorig:Head": "head",
    "mixamorig:LeftShoulder": "left_collar",
    "mixamorig:LeftArm": "left_shoulder",
    "mixamorig:LeftForeArm": "left_elbow",
    "mixamorig:LeftHand": "left_wrist",
    "mixamorig:RightShoulder": "right_collar",
    "mixamorig:RightArm": "right_shoulder",
    "mixamorig:RightForeArm": "right_elbow",
    "mixamorig:RightHand": "right_wrist",
    "mixamorig:LeftUpLeg": "left_hip",
    "mixamorig:LeftLeg": "left_knee",
    "mixamorig:LeftFoot": "left_ankle",
    "mixamorig:LeftToeBase": "left_foot",
    "mixamorig:RightUpLeg": "right_hip",
    "mixamorig:RightLeg": "right_knee",
    "mixamorig:RightFoot": "right_ankle",
    "mixamorig:RightToeBase": "right_foot",
}

ARM_POSITION_MARKERS = {
    "left_elbow": "mixamorig:LeftForeArm",
    "left_wrist": "mixamorig:LeftHand",
    "right_elbow": "mixamorig:RightForeArm",
    "right_wrist": "mixamorig:RightHand",
}

LEG_POSITION_MARKERS = {
    "left_hip": "mixamorig:LeftUpLeg",
    "left_knee": "mixamorig:LeftLeg",
    "left_ankle": "mixamorig:LeftFoot",
    "right_hip": "mixamorig:RightUpLeg",
    "right_knee": "mixamorig:RightLeg",
    "right_ankle": "mixamorig:RightFoot",
}

LEG_BONES = (
    "mixamorig:LeftUpLeg",
    "mixamorig:LeftLeg",
    "mixamorig:LeftFoot",
    "mixamorig:LeftToeBase",
    "mixamorig:LeftToe_End",
    "mixamorig:RightUpLeg",
    "mixamorig:RightLeg",
    "mixamorig:RightFoot",
    "mixamorig:RightToeBase",
    "mixamorig:RightToe_End",
)

WORLD_UP = np.array([0.0, 1.0, 0.0])
HAND_LOCAL_AXIS = np.array([0.0, 1.0, 0.0])

MIXAMO_EDGES = [
    ("mixamorig:Hips", "mixamorig:Spine"),
    ("mixamorig:Spine", "mixamorig:Spine1"),
    ("mixamorig:Spine1", "mixamorig:Spine2"),
    ("mixamorig:Spine2", "mixamorig:Neck"),
    ("mixamorig:Neck", "mixamorig:Head"),
    ("mixamorig:Head", "mixamorig:HeadTop_End"),
    ("mixamorig:Spine2", "mixamorig:LeftShoulder"),
    ("mixamorig:LeftShoulder", "mixamorig:LeftArm"),
    ("mixamorig:LeftArm", "mixamorig:LeftForeArm"),
    ("mixamorig:LeftForeArm", "mixamorig:LeftHand"),
    ("mixamorig:Spine2", "mixamorig:RightShoulder"),
    ("mixamorig:RightShoulder", "mixamorig:RightArm"),
    ("mixamorig:RightArm", "mixamorig:RightForeArm"),
    ("mixamorig:RightForeArm", "mixamorig:RightHand"),
    ("mixamorig:Hips", "mixamorig:LeftUpLeg"),
    ("mixamorig:LeftUpLeg", "mixamorig:LeftLeg"),
    ("mixamorig:LeftLeg", "mixamorig:LeftFoot"),
    ("mixamorig:LeftFoot", "mixamorig:LeftToeBase"),
    ("mixamorig:LeftToeBase", "mixamorig:LeftToe_End"),
    ("mixamorig:Hips", "mixamorig:RightUpLeg"),
    ("mixamorig:RightUpLeg", "mixamorig:RightLeg"),
    ("mixamorig:RightLeg", "mixamorig:RightFoot"),
    ("mixamorig:RightFoot", "mixamorig:RightToeBase"),
    ("mixamorig:RightToeBase", "mixamorig:RightToe_End"),
]

HUMAN_EDGES = [
    ("pelvis", "spine1"),
    ("spine1", "spine2"),
    ("spine2", "spine3"),
    ("spine3", "neck"),
    ("neck", "head"),
    ("spine3", "left_collar"),
    ("left_collar", "left_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"),
    ("left_wrist", "left_hand"),
    ("spine3", "right_collar"),
    ("right_collar", "right_shoulder"),
    ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"),
    ("right_wrist", "right_hand"),
    ("pelvis", "left_hip"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("left_ankle", "left_foot"),
    ("pelvis", "right_hip"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
    ("right_ankle", "right_foot"),
]

LENGTH_EDGES = [
    ("mixamorig:Spine2", "mixamorig:LeftShoulder"),
    ("mixamorig:LeftShoulder", "mixamorig:LeftArm"),
    ("mixamorig:LeftArm", "mixamorig:LeftForeArm"),
    ("mixamorig:LeftForeArm", "mixamorig:LeftHand"),
    ("mixamorig:Spine2", "mixamorig:RightShoulder"),
    ("mixamorig:RightShoulder", "mixamorig:RightArm"),
    ("mixamorig:RightArm", "mixamorig:RightForeArm"),
    ("mixamorig:RightForeArm", "mixamorig:RightHand"),
    ("mixamorig:Hips", "mixamorig:Spine"),
    ("mixamorig:Spine", "mixamorig:Spine1"),
    ("mixamorig:Spine1", "mixamorig:Spine2"),
    ("mixamorig:Spine2", "mixamorig:Neck"),
    ("mixamorig:Neck", "mixamorig:Head"),
    ("mixamorig:Head", "mixamorig:HeadTop_End"),
    ("mixamorig:Hips", "mixamorig:LeftUpLeg"),
    ("mixamorig:LeftUpLeg", "mixamorig:LeftLeg"),
    ("mixamorig:LeftLeg", "mixamorig:LeftFoot"),
    ("mixamorig:LeftFoot", "mixamorig:LeftToeBase"),
    ("mixamorig:Hips", "mixamorig:RightUpLeg"),
    ("mixamorig:RightUpLeg", "mixamorig:RightLeg"),
    ("mixamorig:RightLeg", "mixamorig:RightFoot"),
    ("mixamorig:RightFoot", "mixamorig:RightToeBase"),
]


@dataclass
class FrameRetarget:
    r_anim: dict[str, np.ndarray]
    q_anim: dict[str, np.ndarray]
    r_anim_raw: dict[str, np.ndarray] = field(default_factory=dict)
    twist_flips: list[str] = field(default_factory=list)
    sign_flips: list[str] = field(default_factory=list)


def joint_mixamo(motion, frame: int, name: str) -> np.ndarray:
    return human_to_mixamo(motion.joint(frame, name))


def human_dir(motion, frame: int, start: str, end: str) -> np.ndarray:
    return joint_mixamo(motion, frame, end) - joint_mixamo(motion, frame, start)


def verify_rest_fk(rig: MixamoRig, atol: float = 1e-4) -> float:
    """Identity R_anim must reproduce the FBX rest pose (PreRotation included)."""
    world = forward_kinematics(rig, {})
    err = 0.0
    for name, bone in rig.bones.items():
        err = max(err, float(np.linalg.norm(world[name] - bone.rest_world)))
    if err > atol:
        raise RuntimeError(f"rest FK mismatch {err:.4g} > {atol} — PreRotation composition is wrong")
    return err


def mixamo_proportioned_from(
    rig: MixamoRig,
    motion,
    frame: int,
    rest_pos: dict[str, np.ndarray],
    root_name: str,
    root_pos_m: np.ndarray,
) -> dict[str, np.ndarray]:
    """Rebuild descendants of root_name with Human directions and Mixamo rest lengths."""
    target: dict[str, np.ndarray] = {root_name: np.asarray(root_pos_m, dtype=np.float64).copy()}
    for name in rig.order:
        if name == root_name:
            continue
        parent = rig.bones[name].parent
        if parent is None or parent not in target:
            continue
        length = float(np.linalg.norm(rest_pos[name] - rest_pos[parent]))
        if name in MIXAMO_TO_HUMAN and parent in MIXAMO_TO_HUMAN:
            direction = human_dir(motion, frame, MIXAMO_TO_HUMAN[parent], MIXAMO_TO_HUMAN[name])
        else:
            direction = rest_pos[name] - rest_pos[parent]
        target[name] = target[parent] + normalize(direction) * length
    return target


def position_errors(
    posed: dict[str, np.ndarray],
    target: dict[str, np.ndarray],
    markers: dict[str, str],
) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for label, bone in markers.items():
        delta = posed[bone] - target[bone]
        out[label] = {
            "error_m": float(np.linalg.norm(delta)),
            "dx": float(delta[0]),
            "dy": float(delta[1]),
            "dz": float(delta[2]),
            "mixamo_bone": bone,
        }
    return out


def _hips_rotation(rig: MixamoRig, motion, frame: int) -> np.ndarray:
    rest_world = forward_kinematics(rig, {})
    rest_pos = world_positions_m(rig, rest_world)
    r_rest_frame = orthonormal_frame(
        rest_pos["mixamorig:LeftUpLeg"] - rest_pos["mixamorig:RightUpLeg"],
        rest_pos["mixamorig:Neck"] - rest_pos["mixamorig:Hips"],
    )
    r_tgt_frame = orthonormal_frame(
        joint_mixamo(motion, frame, "left_hip") - joint_mixamo(motion, frame, "right_hip"),
        joint_mixamo(motion, frame, "neck") - joint_mixamo(motion, frame, "pelvis"),
    )
    r_hips_world = (r_tgt_frame @ r_rest_frame.T) @ rest_world["mixamorig:Hips"][:3, :3]
    return anim_from_world_rotation(rig.bones["mixamorig:Hips"], np.eye(3), r_hips_world)


def _spine2_chest_rotation(rig: MixamoRig, world: dict[str, np.ndarray], motion, frame: int) -> np.ndarray:
    bone = rig.bones["mixamorig:Spine2"]
    parent_r = world[bone.parent][:3, :3] if bone.parent else np.eye(3)
    rest_left = rig.child_offset_cm("mixamorig:Spine2", "mixamorig:LeftShoulder") - rig.child_offset_cm(
        "mixamorig:Spine2", "mixamorig:RightShoulder"
    )
    rest_up = rig.child_offset_cm("mixamorig:Spine2", "mixamorig:Neck")
    return frame_anim_from_axes(
        bone,
        parent_r,
        rest_left,
        rest_up,
        joint_mixamo(motion, frame, "left_collar") - joint_mixamo(motion, frame, "right_collar"),
        joint_mixamo(motion, frame, "neck") - joint_mixamo(motion, frame, "spine3"),
    )


def _foot_rotation(rig: MixamoRig, world: dict[str, np.ndarray], motion, frame: int, side: str) -> np.ndarray:
    foot = f"mixamorig:{side}Foot"
    toe = f"mixamorig:{side}ToeBase"
    bone = rig.bones[foot]
    parent_r = world[bone.parent][:3, :3] if bone.parent else np.eye(3)
    along_local = rig.child_offset_cm(foot, toe)
    r_rest = parent_r @ bone.pre_rotation
    up_local = r_rest.T @ WORLD_UP
    ankle = "left_ankle" if side == "Left" else "right_ankle"
    foot_j = "left_foot" if side == "Left" else "right_foot"
    knee = "left_knee" if side == "Left" else "right_knee"
    tgt_along = human_dir(motion, frame, ankle, foot_j)
    tgt_up = WORLD_UP.copy()
    if abs(float(normalize(tgt_along) @ normalize(tgt_up))) > 0.95:
        tgt_up = human_dir(motion, frame, knee, ankle)
        if bone.parent:
            up_local = r_rest.T @ (parent_r @ rig.child_offset_cm(bone.parent, foot))
    return frame_anim_from_two_vectors(
        bone,
        parent_r,
        along_local,
        up_local,
        tgt_along,
        tgt_up,
    )


def _hand_rotation(rig: MixamoRig, world: dict[str, np.ndarray], motion, frame: int, side: str) -> np.ndarray:
    """Aim Mixamo Hand local +Y along Human wrist→hand. No finger bones in the core rig."""
    hand = f"mixamorig:{side}Hand"
    wrist_j = "left_wrist" if side == "Left" else "right_wrist"
    palm_j = "left_hand" if side == "Left" else "right_hand"
    tgt = human_dir(motion, frame, wrist_j, palm_j)
    if float(np.linalg.norm(tgt)) < 1e-4:
        return np.eye(3)
    return swing_anim_to_direction(rig, world, hand, None, tgt, d_local=HAND_LOCAL_AXIS)


# Bones whose rotation is built from two independent human directions (or is
# constant). They are fully determined by the current frame's data, so there is
# no twist ambiguity for the continuity rule to resolve. Letting the rule
# prefer the 180-degree twist variant anyway lets one transient glitch in the
# extracted data latch permanently: once the previous frame is in the flipped
# state, the flipped variant of every later (correct) rotation stays closest
# to it, and the character finishes the clip facing backwards.
FULLY_DETERMINED = frozenset({
    "mixamorig:Hips",
    "mixamorig:Spine2",
    "mixamorig:LeftFoot",
    "mixamorig:RightFoot",
    "mixamorig:LeftToeBase",
    "mixamorig:RightToeBase",
})


def retarget_one_frame(
    rig: MixamoRig,
    motion,
    frame: int,
    *,
    clavicles: bool = True,
    legs: bool = True,
    prev_r_anim: dict[str, np.ndarray] | None = None,
    prev_q_anim: dict[str, np.ndarray] | None = None,
) -> FrameRetarget:
    hips_t_cm = joint_mixamo(motion, frame, "pelvis") / rig.meters_per_unit
    r_anim = {name: np.eye(3) for name in rig.order}
    q_anim = {name: np.array([1.0, 0.0, 0.0, 0.0]) for name in rig.order}
    twist_flips: list[str] = []
    sign_flips: list[str] = []

    def fk() -> dict[str, np.ndarray]:
        return forward_kinematics(rig, r_anim, hips_translation_cm=hips_t_cm)

    def commit(name: str, rotation: np.ndarray) -> None:
        q_prev = None if prev_q_anim is None else prev_q_anim.get(name)
        if name in FULLY_DETERMINED:
            # Trust the data over history; only the aim-ambiguous bones below
            # get the anti-twist continuity.
            r_pick, did_twist = np.asarray(rotation, dtype=np.float64), False
        else:
            axis = swing_aim_local(rig, name) if name in AIM_CHILD or name in NECK_HEAD else local_aim_axis(rig, name)
            r_prev = None if prev_r_anim is None else prev_r_anim.get(name)
            r_pick, did_twist = pick_closest_aim_twist(rotation, r_prev, axis)
        q = quat_wxyz(r_pick)
        q, did_sign = continue_quaternion(q, q_prev)
        r_anim[name] = r_pick
        q_anim[name] = q
        if did_twist:
            twist_flips.append(name)
        if did_sign:
            sign_flips.append(name)

    def apply_swings(targets: dict[str, tuple[str, str]]) -> None:
        for bone_name, (h_a, h_b) in targets.items():
            rotation = swing_anim_to_direction(
                rig,
                fk(),
                bone_name,
                AIM_CHILD.get(bone_name),
                human_dir(motion, frame, h_a, h_b),
                d_local=swing_aim_local(rig, bone_name),
            )
            commit(bone_name, rotation)

    commit("mixamorig:Hips", _hips_rotation(rig, motion, frame))
    if clavicles:
        apply_swings(
            {
                "mixamorig:Spine": SWING_TARGETS["mixamorig:Spine"],
                "mixamorig:Spine1": SWING_TARGETS["mixamorig:Spine1"],
            }
        )
        commit("mixamorig:Spine2", _spine2_chest_rotation(rig, fk(), motion, frame))
        apply_swings(
            {
                "mixamorig:Neck": SWING_TARGETS["mixamorig:Neck"],
                "mixamorig:Head": SWING_TARGETS["mixamorig:Head"],
                "mixamorig:LeftShoulder": SWING_TARGETS["mixamorig:LeftShoulder"],
                "mixamorig:LeftArm": SWING_TARGETS["mixamorig:LeftArm"],
                "mixamorig:LeftForeArm": SWING_TARGETS["mixamorig:LeftForeArm"],
                "mixamorig:RightShoulder": SWING_TARGETS["mixamorig:RightShoulder"],
                "mixamorig:RightArm": SWING_TARGETS["mixamorig:RightArm"],
                "mixamorig:RightForeArm": SWING_TARGETS["mixamorig:RightForeArm"],
            }
        )
        commit("mixamorig:LeftHand", _hand_rotation(rig, fk(), motion, frame, "Left"))
        commit("mixamorig:RightHand", _hand_rotation(rig, fk(), motion, frame, "Right"))
    else:
        apply_swings(SWING_TARGETS_NO_CLAVICLE)
        apply_swings(
            {
                "mixamorig:Neck": SWING_TARGETS["mixamorig:Neck"],
                "mixamorig:Head": SWING_TARGETS["mixamorig:Head"],
            }
        )
    if legs:
        apply_swings(
            {
                "mixamorig:LeftUpLeg": SWING_TARGETS["mixamorig:LeftUpLeg"],
                "mixamorig:LeftLeg": SWING_TARGETS["mixamorig:LeftLeg"],
                "mixamorig:RightUpLeg": SWING_TARGETS["mixamorig:RightUpLeg"],
                "mixamorig:RightLeg": SWING_TARGETS["mixamorig:RightLeg"],
            }
        )
        commit("mixamorig:LeftFoot", _foot_rotation(rig, fk(), motion, frame, "Left"))
        commit("mixamorig:LeftToeBase", np.eye(3))
        commit("mixamorig:RightFoot", _foot_rotation(rig, fk(), motion, frame, "Right"))
        commit("mixamorig:RightToeBase", np.eye(3))
    r_raw = {name: np.asarray(rot, dtype=np.float64).copy() for name, rot in r_anim.items()}
    return FrameRetarget(
        r_anim=r_anim,
        q_anim=q_anim,
        r_anim_raw=r_raw,
        twist_flips=twist_flips,
        sign_flips=sign_flips,
    )
