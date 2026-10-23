"""Per-frame retarget of a whole clip: Human -> Mixamo Skeleton -> character rig.

    human skeleton_motion.npz
            |  retarget_one_frame (swing/aim, no bone scaling, no IK)
    Mixamo Skeleton R_anim
            |  rest-relative transfer from the T-pose calibration
    character rig R_anim  ->  FK  ->  linear blend skinning

When the motion carries foot contact, planted feet are pinned on both the
Mixamo Skeleton and the character rig (foot_lock.py) after the transfer, and
the hips then shift vertically so the planted sole sits on y = 0 (ground.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .foot_lock import lock_feet
from .ground import plant_soles
from .hand_retarget import HandMapping, HandMotion
from .kinematics import forward_kinematics, world_positions_m
from .retarget import joint_mixamo, retarget_one_frame
from .skinned_mesh import YBotAsset, bone_palette, skin_mesh
from .ybot_retarget import YBotMapping


@dataclass
class RetargetedAnimation:
    frames: list[int]
    fps: float
    r_anim_skeleton: list[dict[str, np.ndarray]]
    r_anim_rig: list[dict[str, np.ndarray]]
    hips_cm_skeleton: list[np.ndarray]
    hips_cm_rig: list[np.ndarray]
    mixamo_pos: list[dict[str, np.ndarray]]
    rig_pos: list[dict[str, np.ndarray]]
    human_pos: list[dict[str, np.ndarray]]
    twist_events: list[dict] = field(default_factory=list)
    sign_events: list[dict] = field(default_factory=list)
    foot_lock: dict | None = None
    ground: dict | None = None

    @property
    def n(self) -> int:
        return len(self.frames)


def build_animation(
    motion,
    mapping: YBotMapping,
    frames: list[int],
    *,
    verbose: bool = True,
    foot_lock: bool = True,
    asset: YBotAsset | None = None,
    hands: HandMotion | None = None,
    hand_mapping: HandMapping | None = None,
) -> RetargetedAnimation:
    """Retarget Human -> Mixamo, then carry the rest-relative motion onto the rig."""
    skel = mapping.skeleton_rig
    anim = RetargetedAnimation(
        frames=frames,
        fps=float(motion.fps),
        r_anim_skeleton=[],
        r_anim_rig=[],
        hips_cm_skeleton=[],
        hips_cm_rig=[],
        mixamo_pos=[],
        rig_pos=[],
        human_pos=[],
    )
    r_prev = q_prev = None
    for i, frame in enumerate(frames):
        result = retarget_one_frame(skel, motion, frame, prev_r_anim=r_prev, prev_q_anim=q_prev)
        hips_cm = joint_mixamo(motion, frame, "pelvis") / skel.meters_per_unit

        mix_pos = world_positions_m(
            skel, forward_kinematics(skel, result.r_anim, hips_translation_cm=hips_cm)
        )
        r_rig = mapping.apply_rest_relative_rotations(result.r_anim)
        if hands is not None and hand_mapping is not None and frame < hands.n_frames:
            r_rig.update(hand_mapping.finger_rotations(hands.pose[frame], hands.valid[frame]))
        hips_rig = mapping.hips_translation_cm(hips_cm)
        rig_pos = mapping.ybot_positions_m(r_rig, hips_rig)

        anim.r_anim_skeleton.append(result.r_anim)
        anim.r_anim_rig.append(r_rig)
        anim.hips_cm_skeleton.append(hips_cm)
        anim.hips_cm_rig.append(hips_rig)
        anim.mixamo_pos.append(mix_pos)
        anim.rig_pos.append(rig_pos)
        anim.human_pos.append({n: joint_mixamo(motion, frame, n) for n in motion.joint_names})
        if result.twist_flips:
            anim.twist_events.append({"frame": frame, "bones": result.twist_flips})
        if result.sign_flips:
            anim.sign_events.append({"frame": frame, "bones": result.sign_flips})

        r_prev, q_prev = result.r_anim_raw, result.q_anim
        if verbose and (i == 0 or (i + 1) % 200 == 0 or i == len(frames) - 1):
            print(f"  retarget {i + 1}/{len(frames)}")

    contact = getattr(motion, "foot_contact", None)
    contact_frames = None if contact is None else np.asarray(contact)[list(frames)]
    if foot_lock and contact_frames is not None and len(frames) > 1:
        anim.r_anim_skeleton, _ = lock_feet(
            skel, anim.r_anim_skeleton, anim.hips_cm_skeleton, contact_frames, anim.fps
        )
        anim.r_anim_rig, stats = lock_feet(
            mapping.ybot_rig, anim.r_anim_rig, anim.hips_cm_rig, contact_frames, anim.fps
        )
        anim.mixamo_pos = [
            world_positions_m(skel, forward_kinematics(skel, r, hips_translation_cm=h))
            for r, h in zip(anim.r_anim_skeleton, anim.hips_cm_skeleton)
        ]
        anim.rig_pos = [mapping.ybot_positions_m(r, h) for r, h in zip(anim.r_anim_rig, anim.hips_cm_rig)]
        anim.foot_lock = stats.as_dict()
        if verbose:
            print(
                f"  foot lock: mean correction {stats.mean_correction_cm:.1f} cm, "
                f"max {stats.max_correction_cm:.1f} cm, "
                f"hips shifted on {stats.hip_shift_frames} frames "
                f"(mean {stats.mean_hip_shift_cm:.1f} cm, max {stats.max_hip_shift_cm:.1f} cm), "
                f"out of reach {stats.unreachable_frames} frames"
            )
    elif verbose and foot_lock:
        print("  foot lock: no foot contact in the skeleton; skipped")
    if asset is not None and contact_frames is not None and len(frames) > 1:
        anim.ground = plant_soles(anim, mapping, asset, contact_frames)
        if verbose and anim.ground is not None:
            sole = anim.ground["support_sole_cm"]
            print(
                f"  ground: hips shifted median {anim.ground['median_shift_cm']:.1f} cm, "
                f"max {anim.ground['max_shift_cm']:.1f} cm, "
                f"support sole median {sole['median']} cm"
            )
    return anim


def skin_frames(
    asset: YBotAsset, anim: RetargetedAnimation, indices: list[int]
) -> list[list[np.ndarray]]:
    """Linear blend skinning of the character mesh (meters) for the given indices."""
    out: list[list[np.ndarray]] = []
    scale = asset.rig.meters_per_unit
    for i in indices:
        world = forward_kinematics(
            asset.rig, anim.r_anim_rig[i], hips_translation_cm=anim.hips_cm_rig[i]
        )
        out.append(
            [
                skin_mesh(mesh, bone_palette(world, mesh, asset.rig.order)) * scale
                for mesh in asset.meshes
            ]
        )
    return out


def core_bones_only(pos: dict[str, np.ndarray], edges) -> dict[str, np.ndarray]:
    """Drop the finger chains so the rig panel draws the same graph as the edges."""
    keep = {name for edge in edges for name in edge}
    return {name: p for name, p in pos.items() if name in keep}


def all_points(seq: list[dict[str, np.ndarray]]) -> np.ndarray:
    return np.stack([p for pos in seq for p in pos.values()])
