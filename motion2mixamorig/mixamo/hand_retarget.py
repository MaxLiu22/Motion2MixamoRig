"""MANO finger rotations (HaMeR hand pass) -> Mixamo finger bones.

MANO joint rotations are parent-relative and expressed in the hand model's own
axes, because every MANO rest frame is the identity. A Mixamo finger bone's
animation channel is also parent-relative, but expressed in that bone's own
rest frame (`M_local = T_bind * R_bind * R_anim`). The transfer is therefore a
pure basis change, measured from the two rest poses and never authored:

    R_anim[b] = D_bᵀ · (C · R_mano[j] · Cᵀ) · D_b

    C   : MANO hand axes -> the Mixamo Hand bone's rest frame, from the hand
          frames (wrist->middle1, index1-pinky1) of both rest poses
    D_b : finger bone b's rest world rotation relative to the Hand bone's

HaMeR is a single-image model, so the raw rotations jitter frame to frame;
`load_hand_motion` smooths them with a validity-weighted Gaussian over time
and fills short detection gaps from the neighbouring frames.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..extractors.hamer import HAND_JOINT_NAMES
from .kinematics import MixamoRig, forward_kinematics, normalize

SIDES = ("Left", "Right")  # hand_pose[:, 0] is the left hand, [:, 1] the right
# MANO joint order: 0 wrist, 1-3 index, 4-6 middle, 7-9 pinky, 10-12 ring, 13-15 thumb.
MANO_WRIST, MANO_INDEX1, MANO_MIDDLE1, MANO_PINKY1 = 0, 1, 4, 7
_FINGER = {"index": "Index", "middle": "Middle", "pinky": "Pinky", "ring": "Ring", "thumb": "Thumb"}
DEFAULT_SMOOTH_S = 0.08


def finger_bone(side: str, joint: str) -> str:
    """'index2' on the left -> 'mixamorig:LeftHandIndex2'."""
    return f"mixamorig:{side}Hand{_FINGER[joint[:-1]]}{joint[-1]}"


def _hand_frame(wrist: np.ndarray, middle1: np.ndarray, index1: np.ndarray, pinky1: np.ndarray) -> np.ndarray:
    """Columns: along the fingers, pinky->index, and their cross product (palm normal)."""
    e1 = normalize(middle1 - wrist)
    lateral = index1 - pinky1
    e2 = normalize(lateral - e1 * float(lateral @ e1))
    return np.stack([e1, e2, np.cross(e1, e2)], axis=1)


def _mano_frame(template_joints: np.ndarray, side: str) -> np.ndarray:
    j = np.asarray(template_joints, dtype=np.float64)
    if side == "Left":
        j = j * np.array([-1.0, 1.0, 1.0])  # the hand pass mirrors left hands the same way
    return _hand_frame(j[MANO_WRIST], j[MANO_MIDDLE1], j[MANO_INDEX1], j[MANO_PINKY1])


@dataclass(frozen=True)
class HandMapping:
    rig: MixamoRig
    basis: dict[str, np.ndarray]  # side -> C
    bone_rest: dict[str, np.ndarray]  # finger bone -> D_b
    bones: tuple[str, ...]

    def finger_rotations(self, hand_pose: np.ndarray, valid: np.ndarray) -> dict[str, np.ndarray]:
        """R_anim per finger bone for one frame; undetected hands stay at rest."""
        out: dict[str, np.ndarray] = {}
        for s, side in enumerate(SIDES):
            if not bool(valid[s]) or side not in self.basis:
                continue
            c = self.basis[side]
            for k, joint in enumerate(HAND_JOINT_NAMES):
                bone = finger_bone(side, joint)
                d = self.bone_rest.get(bone)
                if d is None:
                    continue
                r = c @ np.asarray(hand_pose[s, k], dtype=np.float64) @ c.T
                out[bone] = d.T @ r @ d
        return out


def build_hand_mapping(rig: MixamoRig, mano_template_joints: np.ndarray, *, verbose: bool = True) -> HandMapping:
    """Measure C per side and D_b per finger bone from the rig's rest pose and MANO's template."""
    world = forward_kinematics(rig, {})
    rot = {n: np.asarray(m[:3, :3], dtype=np.float64) for n, m in world.items()}
    pos = {n: np.asarray(m[:3, 3], dtype=np.float64) for n, m in world.items()}
    basis: dict[str, np.ndarray] = {}
    bone_rest: dict[str, np.ndarray] = {}
    bones: list[str] = []
    for side in SIDES:
        hand = f"mixamorig:{side}Hand"
        needed = [hand] + [finger_bone(side, j) for j in HAND_JOINT_NAMES]
        if any(b not in rig.bones for b in needed):
            if verbose:
                missing = [b for b in needed if b not in rig.bones]
                print(f"  {side.lower()} hand: rig has no finger chain ({missing[0]} ...), fingers stay at rest")
            continue
        h = rot[hand]
        mix = _hand_frame(
            h.T @ pos[hand], h.T @ pos[finger_bone(side, "middle1")],
            h.T @ pos[finger_bone(side, "index1")], h.T @ pos[finger_bone(side, "pinky1")],
        )
        basis[side] = mix @ _mano_frame(mano_template_joints, side).T
        for joint in HAND_JOINT_NAMES:
            bone = finger_bone(side, joint)
            bone_rest[bone] = h.T @ rot[bone]
            bones.append(bone)
    if verbose and basis:
        angles = {s: float(np.degrees(np.arccos(np.clip((np.trace(c) - 1) / 2, -1, 1)))) for s, c in basis.items()}
        print(f"  finger bones            {len(bones)}  (MANO -> Mixamo basis change "
              + ", ".join(f"{s.lower()} {a:.1f} deg" for s, a in angles.items()) + ")")
    return HandMapping(rig=rig, basis=basis, bone_rest=bone_rest, bones=tuple(bones))


# ---------------------------------------------------------------- hand motion + smoothing


@dataclass
class HandMotion:
    pose: np.ndarray  # (F, 2, 15, 3, 3)
    valid: np.ndarray  # (F, 2)
    template_joints: np.ndarray  # (16, 3) MANO right-hand rest joints
    fps: float
    smoothed_s: float

    @property
    def n_frames(self) -> int:
        return int(self.pose.shape[0])


def _quat_from_rotmat(r: np.ndarray) -> np.ndarray:
    """(..., 3, 3) -> (..., 4) wxyz, batch-safe."""
    r = np.asarray(r, dtype=np.float64)
    shape = r.shape[:-2]
    r = r.reshape(-1, 3, 3)
    m00, m11, m22 = r[..., 0, 0], r[..., 1, 1], r[..., 2, 2]
    t = m00 + m11 + m22
    q = np.empty(r.shape[:-2] + (4,))
    # branch on the largest diagonal term for stability
    s = np.sqrt(np.maximum(t + 1.0, 0.0)) * 2
    q[..., 0] = 0.25 * s
    q[..., 1] = (r[..., 2, 1] - r[..., 1, 2]) / np.where(s > 1e-9, s, 1)
    q[..., 2] = (r[..., 0, 2] - r[..., 2, 0]) / np.where(s > 1e-9, s, 1)
    q[..., 3] = (r[..., 1, 0] - r[..., 0, 1]) / np.where(s > 1e-9, s, 1)
    bad = t <= -0.5  # near 180 deg: fall back to the per-element formula
    if np.any(bad):
        for idx in zip(*np.nonzero(bad)):
            q[idx] = _quat_from_rotmat_single(r[idx])
    q /= np.linalg.norm(q, axis=-1, keepdims=True)
    return q.reshape(shape + (4,))


def _quat_from_rotmat_single(r: np.ndarray) -> np.ndarray:
    diag = np.array([r[0, 0], r[1, 1], r[2, 2]])
    i = int(np.argmax(diag))
    j, k = (i + 1) % 3, (i + 2) % 3
    s = np.sqrt(max(diag[i] - diag[j] - diag[k] + 1.0, 1e-12)) * 2
    q = np.empty(4)
    q[0] = (r[k, j] - r[j, k]) / s
    q[1 + i] = 0.25 * s
    q[1 + j] = (r[j, i] + r[i, j]) / s
    q[1 + k] = (r[k, i] + r[i, k]) / s
    return q


def _rotmat_from_quat(q: np.ndarray) -> np.ndarray:
    w, x, y, z = (q[..., i] for i in range(4))
    r = np.empty(q.shape[:-1] + (3, 3))
    r[..., 0, 0] = 1 - 2 * (y * y + z * z)
    r[..., 0, 1] = 2 * (x * y - z * w)
    r[..., 0, 2] = 2 * (x * z + y * w)
    r[..., 1, 0] = 2 * (x * y + z * w)
    r[..., 1, 1] = 1 - 2 * (x * x + z * z)
    r[..., 1, 2] = 2 * (y * z - x * w)
    r[..., 2, 0] = 2 * (x * z - y * w)
    r[..., 2, 1] = 2 * (y * z + x * w)
    r[..., 2, 2] = 1 - 2 * (x * x + y * y)
    return r


def smooth_hand_pose(pose: np.ndarray, valid: np.ndarray, fps: float, sigma_s: float = DEFAULT_SMOOTH_S) -> tuple[np.ndarray, np.ndarray]:
    """Validity-weighted Gaussian smoothing of each joint rotation over time.

    Frames without a detection take the weighted mean of their valid
    neighbours inside the window; frames with no valid neighbour at all stay at
    rest and are reported invalid. Returns (pose, valid) with the same shapes.
    """
    pose = np.asarray(pose, dtype=np.float64)
    valid = np.asarray(valid, dtype=bool)
    n = pose.shape[0]
    if sigma_s <= 0 or n < 2:
        return pose.copy(), valid.copy()
    sigma = max(float(sigma_s) * float(fps), 1e-6)
    radius = int(np.ceil(3 * sigma))
    offsets = np.arange(-radius, radius + 1)
    kernel = np.exp(-0.5 * (offsets / sigma) ** 2)
    out = np.tile(np.eye(3), pose.shape[:-2] + (1, 1))
    out_valid = np.zeros_like(valid)
    for s in range(pose.shape[1]):
        if not valid[:, s].any():
            continue
        q = _quat_from_rotmat(pose[:, s])  # (F, 15, 4)
        # hemisphere continuity along time so averaging does not cancel out
        for f in range(1, n):
            flip = np.sum(q[f] * q[f - 1], axis=-1) < 0
            q[f, flip] *= -1
        w_valid = valid[:, s].astype(np.float64)
        acc = np.zeros_like(q)
        wsum = np.zeros(n)
        for off, k in zip(offsets, kernel):
            src = np.arange(n) + off
            ok = (src >= 0) & (src < n)
            w = np.zeros(n)
            w[ok] = k * w_valid[src[ok]]
            acc[ok] += w[ok, None, None] * q[src[ok]]
            wsum += w
        has = wsum > 1e-9
        mean = acc[has] / wsum[has, None, None]
        mean /= np.linalg.norm(mean, axis=-1, keepdims=True)
        out[has, s] = _rotmat_from_quat(mean)
        out_valid[:, s] = has
    return out, out_valid


def load_hand_motion(skeleton_npz: Path, *, smooth_s: float = DEFAULT_SMOOTH_S) -> HandMotion | None:
    """Finger rotations from a skeleton file, smoothed. None when the file has no hands."""
    with np.load(Path(skeleton_npz), allow_pickle=True) as data:
        if "hand_pose" not in data.files or "hand_valid" not in data.files:
            return None
        pose = np.asarray(data["hand_pose"], dtype=np.float64)
        valid = np.asarray(data["hand_valid"], dtype=bool)
        fps = float(data["fps"]) if "fps" in data.files else 30.0
        if "hand_template_joints" in data.files:
            template = np.asarray(data["hand_template_joints"], dtype=np.float64)
        else:
            from ..extractors.hamer import ensure_mano_npz

            with np.load(ensure_mano_npz()) as mano:
                template = np.asarray(mano["J"], dtype=np.float64)
    pose, valid = smooth_hand_pose(pose, valid, fps, smooth_s)
    return HandMotion(pose=pose, valid=valid, template_joints=template, fps=fps, smoothed_s=float(smooth_s))
