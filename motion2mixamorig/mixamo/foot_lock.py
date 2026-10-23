"""Keep planted feet still on a retargeted rig.

GVHMR predicts, per frame, how confident it is that each of four foot joints
is static: left/right ankle (heel side) and left/right foot (ball of the foot).
Heel and ball are locked independently, so a flat foot, a heel raise pivoting
on the ball, and a heel strike with the toes up each keep the part that is
actually on the ground in place.

Per contact segment the locked point is pinned at its mean position over the
segment. The correction (pinned minus raw) fades out over a short window on
both sides of the segment so the swing leg does not pop. Each frame then:

    ankle target = raw ankle + ball correction while the ball is planted,
                   else + heel correction (heel strike, toes up)
    UpLeg / Leg  = analytic two-bone IK to the ankle target, knee kept in the
                   plane of the original bend

The ball wins when both are planted: the two anchors come from different
segments and are not a rigid foot length apart, so forcing both would twist
the foot. The foot keeps its original world orientation, so a heel raise
still pivots about the pinned ball.

When a straight leg still cannot reach its anchor, the hips translate by the
smallest move that brings every planted hip joint into reach. Both hip joints
share that translation. Nothing is snapped to a floor here: only drift during
contact is removed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .kinematics import (
    MixamoRig,
    anim_from_world_rotation,
    forward_kinematics,
    normalize,
    rotation_aligning,
)

# Column order of `foot_contact` in skeleton_motion.npz (GVHMR static_conf_logits[..., :4]).
CONTACT_CHANNELS = ("left_ankle", "left_foot", "right_ankle", "right_foot")
SIDES = (("Left", 0, 1), ("Right", 2, 3))

ENTER_CONF = 0.8
EXIT_CONF = 0.5
MIN_CONTACT_S = 0.1
BLEND_S = 0.15


@dataclass
class FootLockStats:
    planted_fraction: dict[str, float]
    segments: dict[str, int]
    mean_correction_cm: float
    max_correction_cm: float
    unreachable_frames: int
    hip_shift_frames: int
    mean_hip_shift_cm: float
    max_hip_shift_cm: float

    def as_dict(self) -> dict:
        return {
            "planted_fraction": {k: round(v, 3) for k, v in self.planted_fraction.items()},
            "segments": dict(self.segments),
            "mean_correction_cm": round(self.mean_correction_cm, 2),
            "max_correction_cm": round(self.max_correction_cm, 2),
            "unreachable_frames": self.unreachable_frames,
            "hip_shift_frames": self.hip_shift_frames,
            "mean_hip_shift_cm": round(self.mean_hip_shift_cm, 2),
            "max_hip_shift_cm": round(self.max_hip_shift_cm, 2),
        }


def contact_mask(conf: np.ndarray, fps: float) -> np.ndarray:
    """Hysteresis on one confidence channel, then drop contacts shorter than MIN_CONTACT_S."""
    conf = np.asarray(conf, dtype=np.float64)
    mask = np.zeros(len(conf), dtype=bool)
    on = False
    for i, c in enumerate(conf):
        on = c >= EXIT_CONF if on else c >= ENTER_CONF
        mask[i] = on
    min_len = max(2, int(round(MIN_CONTACT_S * fps)))
    for s, e in segments(mask):
        if e - s < min_len:
            mask[s:e] = False
    return mask


def segments(mask: np.ndarray) -> list[tuple[int, int]]:
    """[start, end) runs of True."""
    padded = np.concatenate([[False], np.asarray(mask, dtype=bool), [False]])
    edges = np.flatnonzero(padded[1:] != padded[:-1])
    return [(int(s), int(e)) for s, e in zip(edges[::2], edges[1::2])]


def _fade(distance: int, blend: int) -> float:
    """1 next to a contact, 0 at `blend` frames away (smoothstep)."""
    x = min(1.0, distance / float(blend))
    return 1.0 - x * x * (3.0 - 2.0 * x)


def correction_track(raw: np.ndarray, mask: np.ndarray, blend: int) -> tuple[np.ndarray, np.ndarray]:
    """Per-frame offset that pins `raw` (F, 3) during contact, plus its weight in [0, 1]."""
    n = len(raw)
    offset = np.zeros((n, 3))
    weight = np.zeros(n)
    segs = segments(mask)
    for s, e in segs:
        offset[s:e] = raw[s:e].mean(axis=0) - raw[s:e]
        weight[s:e] = 1.0
    bounds = [(None, None)] + segs + [(None, None)]
    for (_, prev_end), (next_start, _) in zip(bounds[:-1], bounds[1:]):
        lo = 0 if prev_end is None else prev_end
        hi = n if next_start is None else next_start
        for t in range(lo, hi):
            a = _fade(t - prev_end + 1, blend) if prev_end is not None else 0.0
            b = _fade(next_start - t, blend) if next_start is not None else 0.0
            if a + b > 1.0:
                a, b = a / (a + b), b / (a + b)
            if a == 0.0 and b == 0.0:
                continue
            o_prev = offset[prev_end - 1] if prev_end is not None else 0.0
            o_next = offset[next_start] if next_start is not None else 0.0
            offset[t] = a * o_prev + b * o_next
            weight[t] = max(a, b)
    return offset, weight


def _project_ball(point: np.ndarray, center: np.ndarray, radius: float) -> np.ndarray:
    """Closest point to `point` that lies inside the ball."""
    delta = np.asarray(point, dtype=np.float64) - center
    dist = float(np.linalg.norm(delta))
    if dist <= radius or dist < 1e-12:
        return np.asarray(point, dtype=np.float64).copy()
    return center + delta * (radius / dist)


def _equal_shortfall(center_a: np.ndarray, radius_a: float, center_b: np.ndarray, radius_b: float) -> np.ndarray:
    """Where two non-overlapping balls meet once each radius grows by the same amount."""
    span = center_b - center_a
    dist = float(np.linalg.norm(span))
    if dist < 1e-12:
        return center_a.copy()
    along = float(np.clip((dist + radius_a - radius_b) * 0.5, 0.0, dist))
    return center_a + span * (along / dist)


def hip_reach_delta(constraints: list[tuple[np.ndarray, float]]) -> np.ndarray:
    """Smallest shared translation that puts every hip joint within reach of its target.

    Each entry is `(target - hip_joint, reach)`. Both hip joints move by the same
    vector, so the unknown is that translation and zero means the body stays put.
    A target already in reach contributes a ball that contains the origin.
    """
    balls = [(np.asarray(center, dtype=np.float64), float(radius)) for center, radius in constraints if radius > 0.0]
    if not balls:
        return np.zeros(3)
    if len(balls) == 1:
        return _project_ball(np.zeros(3), balls[0][0], balls[0][1])

    (center_a, radius_a), (center_b, radius_b) = balls[:2]
    dist = float(np.linalg.norm(center_b - center_a))
    if dist > radius_a + radius_b + 1e-6:
        return _equal_shortfall(center_a, radius_a, center_b, radius_b)
    if dist < abs(radius_a - radius_b) - 1e-6:
        if radius_a <= radius_b:
            return _project_ball(np.zeros(3), center_a, radius_a)
        return _project_ball(np.zeros(3), center_b, radius_b)

    # Dykstra: Euclidean projection of the origin onto the intersection.
    point = np.zeros(3)
    slack = [np.zeros(3), np.zeros(3)]
    for _ in range(24):
        for index, (center, radius) in enumerate(balls[:2]):
            previous = point.copy()
            point = _project_ball(previous + slack[index], center, radius)
            slack[index] = previous + slack[index] - point
    return point


def two_bone_ik(
    hip: np.ndarray,
    knee: np.ndarray,
    ankle: np.ndarray,
    target: np.ndarray,
    pole_hint: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, bool]:
    """World-space swings for the thigh and shin that put the ankle on `target`.

    The knee stays in the plane of the original bend (or of `pole_hint` when
    the leg is straight). Out-of-reach targets are clamped to full extension.
    """
    l1 = float(np.linalg.norm(knee - hip))
    l2 = float(np.linalg.norm(ankle - knee))
    v = target - hip
    dist = float(np.linalg.norm(v))
    u = normalize(v, normalize(ankle - hip))
    reach = (l1 + l2) * 0.9999
    unreachable = dist > reach
    dist = float(np.clip(dist, abs(l1 - l2) + 1e-6, reach))

    pole = (knee - hip) - u * float((knee - hip) @ u)
    if np.linalg.norm(pole) < 1e-3 * l1:
        pole = pole_hint - u * float(pole_hint @ u)
    pole = normalize(pole, np.array([0.0, 0.0, 1.0]))

    cos_a = float(np.clip((l1 * l1 + dist * dist - l2 * l2) / (2.0 * l1 * dist), -1.0, 1.0))
    sin_a = float(np.sqrt(max(0.0, 1.0 - cos_a * cos_a)))
    knee_new = hip + l1 * (cos_a * u + sin_a * pole)
    ankle_new = hip + dist * u

    r_thigh = rotation_aligning(knee - hip, knee_new - hip)
    r_shin = rotation_aligning(r_thigh @ (ankle - knee), ankle_new - knee_new)
    return r_thigh, r_shin, unreachable


def lock_feet(
    rig: MixamoRig,
    r_anims: list[dict[str, np.ndarray]],
    hips_cm: list[np.ndarray],
    contact: np.ndarray,
    fps: float,
) -> tuple[list[dict[str, np.ndarray]], FootLockStats]:
    """Return new per-frame R_anim dicts with the planted feet pinned.

    `contact` is (F, 4) in CONTACT_CHANNELS order, aligned with `r_anims`.
    Leg rotations change, and `hips_cm` is shifted in place when a straight
    leg cannot reach its anchor.
    """
    n = len(r_anims)
    contact = np.asarray(contact, dtype=np.float64)
    if contact.shape != (n, 4):
        raise ValueError(f"foot contact must be ({n}, 4), got {contact.shape}")
    blend = max(2, int(round(BLEND_S * fps)))

    worlds = [forward_kinematics(rig, r_anims[i], hips_translation_cm=hips_cm[i]) for i in range(n)]

    tracks = {}
    planted: dict[str, float] = {}
    seg_count: dict[str, int] = {}
    for side, heel_ch, ball_ch in SIDES:
        foot, toe = f"mixamorig:{side}Foot", f"mixamorig:{side}ToeBase"
        ankle_raw = np.stack([w[foot][:3, 3] for w in worlds])
        ball_raw = np.stack([w[toe][:3, 3] for w in worlds])
        heel_mask = contact_mask(contact[:, heel_ch], fps)
        ball_mask = contact_mask(contact[:, ball_ch], fps)
        tracks[side] = (
            correction_track(ankle_raw, heel_mask, blend),
            correction_track(ball_raw, ball_mask, blend),
        )
        for label, mask in ((CONTACT_CHANNELS[heel_ch], heel_mask), (CONTACT_CHANNELS[ball_ch], ball_mask)):
            planted[label] = float(mask.mean()) if n else 0.0
            seg_count[label] = len(segments(mask))

    out = [dict(r) for r in r_anims]
    corrections: list[float] = []
    hip_shifts: list[float] = []
    unreachable = 0
    # Stay just inside two_bone_ik's own reach clamp so the shifted hip counts as reachable.
    reach_scale = 0.999
    for i in range(n):
        world = worlds[i]
        planted_legs = []
        for side, _, _ in SIDES:
            (off_h, w_h), (off_b, w_b) = tracks[side]
            if w_h[i] == 0.0 and w_b[i] == 0.0:
                continue
            up, leg, foot, toe = (f"mixamorig:{side}{b}" for b in ("UpLeg", "Leg", "Foot", "ToeBase"))
            hip_p = world[up][:3, 3]
            knee_p = world[leg][:3, 3]
            ankle_p = world[foot][:3, 3]
            ball_p = world[toe][:3, 3]
            ankle_off = w_b[i] * off_b[i] + (1.0 - w_b[i]) * off_h[i]
            reach = (float(np.linalg.norm(knee_p - hip_p)) + float(np.linalg.norm(ankle_p - knee_p))) * reach_scale
            planted_legs.append(
                {
                    "up": up,
                    "leg": leg,
                    "foot": foot,
                    "hip": hip_p,
                    "knee": knee_p,
                    "ankle": ankle_p,
                    "target": ankle_p + ankle_off,
                    "pole": ball_p - ankle_p,
                    "reach": reach,
                    "correction_cm": float(np.linalg.norm(ankle_off)) * rig.meters_per_unit * 100.0,
                }
            )
        delta = hip_reach_delta([(leg["target"] - leg["hip"], leg["reach"]) for leg in planted_legs])
        shift_cm = float(np.linalg.norm(delta)) * rig.meters_per_unit * 100.0
        if shift_cm > 0.0:
            hips_cm[i] = np.asarray(hips_cm[i], dtype=np.float64) + delta
        if shift_cm > 0.01:
            hip_shifts.append(shift_cm)
        for leg in planted_legs:
            r_thigh, r_shin, miss = two_bone_ik(
                leg["hip"] + delta,
                leg["knee"] + delta,
                leg["ankle"] + delta,
                leg["target"],
                leg["pole"],
            )
            unreachable += int(miss)
            corrections.append(leg["correction_cm"])
            parent_r = world[rig.bones[leg["up"]].parent][:3, :3]
            w_up = r_thigh @ world[leg["up"]][:3, :3]
            w_leg = r_shin @ r_thigh @ world[leg["leg"]][:3, :3]
            w_foot = world[leg["foot"]][:3, :3]
            out[i][leg["up"]] = anim_from_world_rotation(rig.bones[leg["up"]], parent_r, w_up)
            out[i][leg["leg"]] = anim_from_world_rotation(rig.bones[leg["leg"]], w_up, w_leg)
            out[i][leg["foot"]] = anim_from_world_rotation(rig.bones[leg["foot"]], w_leg, w_foot)

    stats = FootLockStats(
        planted_fraction=planted,
        segments=seg_count,
        mean_correction_cm=float(np.mean(corrections)) if corrections else 0.0,
        max_correction_cm=float(np.max(corrections)) if corrections else 0.0,
        unreachable_frames=unreachable,
        hip_shift_frames=len(hip_shifts),
        mean_hip_shift_cm=float(np.mean(hip_shifts)) if hip_shifts else 0.0,
        max_hip_shift_cm=float(np.max(hip_shifts)) if hip_shifts else 0.0,
    )
    return out, stats
