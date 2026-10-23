"""Put the planted sole on y = 0.

Foot lock pins a foot where it already was, and that height is the recovered
skeleton's, not the floor. The character's sole sits a different distance
below the foot bone than the skeleton joint does, and the recovered height
drifts over a clip, so the mesh ends up floating or sunk in Blender.

The sole is the lowest skinned vertex of the planted part: the heel (Foot)
or the ball (ToeBase / Toe_End). On a planted frame the hips translate
vertically so that vertex lands on y = 0. A plant holds the offset of its
lowest frame, so the sole can lift during the step but does not sink.
Airborne frames blend from the previous plant to the next, which keeps a
jump's height and removes the slow drift between steps.
"""

from __future__ import annotations

import numpy as np

from .foot_lock import contact_mask, segments
from .kinematics import forward_kinematics, world_positions_m
from .skinned_mesh import YBotAsset

# Column order matches foot_contact: left heel, left ball, right heel, right ball.
SOLE_BONES = (
    ("mixamorig:LeftFoot",),
    ("mixamorig:LeftToeBase", "mixamorig:LeftToe_End"),
    ("mixamorig:RightFoot",),
    ("mixamorig:RightToeBase", "mixamorig:RightToe_End"),
)


def _skin(vertices: np.ndarray, weights: np.ndarray, palette: np.ndarray) -> np.ndarray:
    ones = np.ones((len(vertices), 1), dtype=np.float64)
    posed = np.zeros((len(vertices), 4), dtype=np.float64)
    homogeneous = np.concatenate([vertices, ones], axis=1)
    for bone in range(palette.shape[0]):
        weight = weights[:, bone]
        if float(weight.max()) < 1e-12:
            continue
        posed += weight[:, None] * (homogeneous @ palette[bone].T)
    return posed[:, :3]


def _sole_vertices(asset: YBotAsset) -> list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """Per mesh: foot vertices, their weights, the inverse binds, and a group id per vertex.

    Group ids are the SOLE_BONES columns. A vertex belongs to the foot bone that
    owns most of its weight.
    """
    out = []
    for mesh in asset.meshes:
        group = np.full(len(mesh.vertices), -1, dtype=int)
        dominant = mesh.weights.argmax(axis=1)
        for column, bones in enumerate(SOLE_BONES):
            owned = np.zeros(len(mesh.vertices), dtype=bool)
            for bone in bones:
                index = asset.bone_index.get(bone)
                if index is None:
                    continue
                owned |= (dominant == index) & (mesh.weights[:, index] > 0.5)
            group[owned] = column
        keep = group >= 0
        if not np.any(keep):
            continue
        out.append((mesh.vertices[keep], mesh.weights[keep], mesh.ibm, group[keep]))
    return out


def sole_heights_m(
    asset: YBotAsset,
    r_anims: list[dict[str, np.ndarray]],
    hips_cm: list[np.ndarray],
    soles: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] | None = None,
) -> np.ndarray:
    """(F, 4) world height of the lowest vertex of each sole group, in metres."""
    if soles is None:
        soles = _sole_vertices(asset)
    n = len(r_anims)
    heights = np.full((n, 4), np.nan)
    scale = asset.rig.meters_per_unit
    order = asset.rig.order
    for i in range(n):
        world = forward_kinematics(asset.rig, r_anims[i], hips_translation_cm=hips_cm[i])
        for vertices, weights, ibm, group in soles:
            palette = np.stack([world[name] for name in order], axis=0) @ ibm
            posed = _skin(vertices, weights, palette)
            for column in range(4):
                picked = posed[group == column]
                if len(picked) == 0:
                    continue
                lowest = float(picked[:, 1].min()) * scale
                if not np.isfinite(heights[i, column]) or lowest < heights[i, column]:
                    heights[i, column] = lowest
    return heights


def support_delta_m(heights_m: np.ndarray, contact: np.ndarray, fps: float) -> np.ndarray:
    """Per-frame vertical hips shift, in metres, that lands the support sole on y = 0.

Planted frames use the lowest planted sole. Each contact holds the shift
that puts the lowest frame of that contact on the floor, so the sole can
lift during the step but does not sink through it. Airborne frames blend
from the previous plant to the next; the clip before the first plant and
after the last holds still.
    """
    n = len(heights_m)
    raw = np.full(n, np.nan)
    supported = np.zeros(n, dtype=bool)
    masks = [contact_mask(contact[:, channel], fps) for channel in range(4)]
    for i in range(n):
        planted = [heights_m[i, column] for column, mask in enumerate(masks) if mask[i] and np.isfinite(heights_m[i, column])]
        if not planted:
            continue
        raw[i] = -min(planted)
        supported[i] = True

    delta = np.zeros(n)
    segs = segments(supported)
    if not segs:
        return delta
    for start, end in segs:
        delta[start:end] = float(np.max(raw[start:end]))
    delta[: segs[0][0]] = delta[segs[0][0]]
    delta[segs[-1][1] :] = delta[segs[-1][1] - 1]
    for (_, left_end), (right_start, _) in zip(segs, segs[1:]):
        gap = np.arange(left_end, right_start)
        if len(gap) == 0:
            continue
        span = right_start - (left_end - 1)
        t = (gap - (left_end - 1)) / span
        delta[gap] = (1.0 - t) * delta[left_end - 1] + t * delta[right_start]
    return delta


def plant_soles(anim, mapping, asset: YBotAsset, contact: np.ndarray) -> dict:
    """Shift both hip tracks so the planted sole sits on y = 0. Rotations stay."""
    soles = _sole_vertices(asset)
    heights = sole_heights_m(asset, anim.r_anim_rig, anim.hips_cm_rig, soles)
    delta_m = support_delta_m(heights, np.asarray(contact, dtype=np.float64), float(anim.fps))
    delta_cm = delta_m / asset.rig.meters_per_unit
    align = mapping.r_world_align
    scale = mapping.translation_scale
    for i, shift_cm in enumerate(delta_cm):
        anim.hips_cm_rig[i] = np.asarray(anim.hips_cm_rig[i], dtype=np.float64) + np.array([0.0, shift_cm, 0.0])
        skeleton_shift = align.T @ np.array([0.0, shift_cm, 0.0]) / scale
        anim.hips_cm_skeleton[i] = np.asarray(anim.hips_cm_skeleton[i], dtype=np.float64) + skeleton_shift

    skel = mapping.skeleton_rig
    anim.mixamo_pos = [
        world_positions_m(skel, forward_kinematics(skel, r, hips_translation_cm=h))
        for r, h in zip(anim.r_anim_skeleton, anim.hips_cm_skeleton)
    ]
    anim.rig_pos = [mapping.ybot_positions_m(r, h) for r, h in zip(anim.r_anim_rig, anim.hips_cm_rig)]

    grounded = sole_heights_m(asset, anim.r_anim_rig, anim.hips_cm_rig, soles)
    supported = np.zeros(len(delta_m), dtype=bool)
    masks = [contact_mask(contact[:, channel], anim.fps) for channel in range(4)]
    residual = []
    for i in range(len(delta_m)):
        planted = [grounded[i, column] for column, mask in enumerate(masks) if mask[i] and np.isfinite(grounded[i, column])]
        if planted:
            supported[i] = True
            residual.append(min(planted) * 100.0)
    return {
        "median_shift_cm": round(float(np.median(np.abs(delta_m)) * 100.0), 2),
        "max_shift_cm": round(float(np.max(np.abs(delta_m)) * 100.0), 2),
        "supported_fraction": round(float(supported.mean()), 3),
        "support_sole_cm": {
            "median": round(float(np.median(residual)), 2) if residual else None,
            "p95_abs": round(float(np.percentile(np.abs(residual), 95)), 2) if residual else None,
        },
    }
