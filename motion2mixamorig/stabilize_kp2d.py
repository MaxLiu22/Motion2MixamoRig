"""Keep COCO-17 left/right identity consistent across time (segment majority).

RTMPose / ViTPose decide left and right from appearance, one frame at a time,
with no memory. Whether the subject faces the camera or away is implied by
those labels: the left shoulder drawn on the image's right means the subject
faces the camera. Per frame the estimator is right most of the time but it
mislabels isolated frames, and one mislabelled frame makes GVHMR spin the 3D
body around for that frame.

The *facing sign* of a frame is ``sign(x_left - x_right)`` of the shoulders
(hips when the shoulders are collapsed). Two facts drive the rule:

* a real 180-degree turn passes through a side view, where the facing sign
  changes while the shoulder width is near zero ("narrow" frames);
* a label flip is isolated: a few frames with the opposite sign, surrounded by
  frames that agree with each other, at full shoulder width.

So the clip is cut into *wide segments* at the narrow frames. Inside a wide
segment the facing sign cannot genuinely change, so runs of the minority sign
shorter than ``MIN_TURN_FRAMES`` are flips and get swapped back; a longer run
is treated as a real turn that happened too fast to show a side view and is
left alone. Narrow frames between two segments that agree are forced to that
sign (a flip can happen in a near-side view as well); narrow frames between
two segments that disagree are a turn in progress and keep the estimator's
labels. Nothing here looks at the face, so hats and masks do not matter, and
every decision rests on the whole segment rather than on one transition
frame, so one bad frame cannot lock the rest of the clip into the wrong state.

Each person's track is stabilized on its own, so people in the same clip may
face different ways.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np

# Full COCO-17 left/right permutation (nose stays).
COCO17_SWAP = np.array([0, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15], dtype=np.int64)

# A frame is "narrow" (side view) below this fraction of the subject's usual
# shoulder width, clamped to a pixel range so tiny or huge subjects behave.
NARROW_SCALE = 0.45
NARROW_MIN_PX = 40.0
NARROW_MAX_PX = 80.0
# Inside a wide segment, a run of the opposite facing sign at least this long
# (frames at 30 fps, ~0.33 s) is a real turn with no side view, not a flip.
MIN_TURN_FRAMES = 10
# Narrow frames narrower than this are too ambiguous to touch.
NARROW_FORCE_MIN_PX = 12.0


def _as_numpy(x) -> np.ndarray:
    if hasattr(x, "detach"):
        return x.detach().cpu().numpy()
    return np.asarray(x)


def _lr_x(frame: np.ndarray) -> float:
    """Shoulder left-minus-right in image x. Hips if shoulders are collapsed."""
    sh = float(frame[5, 0] - frame[6, 0])
    if abs(sh) >= 40.0:
        return sh
    return float(frame[11, 0] - frame[12, 0])


def facing_sign(frame: np.ndarray) -> float:
    """+1 when the labels say the subject faces the camera, -1 away, 0 undecided."""
    return float(np.sign(_lr_x(frame)))


def _runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """Maximal runs of True as inclusive (start, end) pairs."""
    out: list[tuple[int, int]] = []
    i, n = 0, len(mask)
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        out.append((i, j - 1))
        i = j
    return out


def _sign_runs(signs: np.ndarray) -> list[tuple[int, int, float]]:
    """Runs of equal sign as (start, end, sign)."""
    out: list[tuple[int, int, float]] = []
    i, n = 0, len(signs)
    while i < n:
        j = i
        while j < n and signs[j] == signs[i]:
            j += 1
        out.append((i, j - 1, float(signs[i])))
        i = j
    return out


def _denoise_segment(signs: np.ndarray, min_turn: int) -> np.ndarray:
    """Flip every run shorter than `min_turn` into its neighbours, shortest first.

    Works on a copy of the wide segment's signs (all non-zero). Stops when every
    remaining run is at least `min_turn` long or the segment is one run.
    """
    out = signs.copy()
    while True:
        runs = _sign_runs(out)
        if len(runs) < 2:
            return out
        short = [r for r in runs if (r[1] - r[0] + 1) < min_turn]
        if not short:
            return out
        a, b, s = min(short, key=lambda r: (r[1] - r[0], r[0]))
        out[a : b + 1] = -s


def stabilize_coco17(
    kp2d: np.ndarray, *, min_turn_frames: int = MIN_TURN_FRAMES
) -> tuple[np.ndarray, np.ndarray]:
    """Return (stabilized (F,17,3), per-frame swap flags (F,))."""
    src = np.asarray(_as_numpy(kp2d), dtype=np.float64)
    if src.ndim != 3 or src.shape[1] < 17:
        raise ValueError(f"expected (F, 17, 3) COCO-17, got {src.shape}")
    n = len(src)
    widths = np.array([_lr_x(f) for f in src])
    raw_sign = np.sign(widths)
    narrow_px = float(np.clip(NARROW_SCALE * np.median(np.abs(widths)), NARROW_MIN_PX, NARROW_MAX_PX))
    wide = (np.abs(widths) >= narrow_px) & (raw_sign != 0)

    target = raw_sign.copy()
    # 1) wide segments: the facing sign is constant inside, short minority runs are flips
    for a, b in _runs(wide):
        target[a : b + 1] = _denoise_segment(raw_sign[a : b + 1], min_turn_frames)
    # 2) narrow frames: forced to the sign both neighbouring segments agree on
    for a, b in _runs(~wide):
        before = target[a - 1] if a > 0 else None
        after = target[b + 1] if b + 1 < n else None
        if before is None and after is None:
            continue
        if before is not None and after is not None and before != after:
            continue  # a turn in progress: keep the estimator's labels
        force = before if before is not None else after
        for i in range(a, b + 1):
            if abs(widths[i]) >= NARROW_FORCE_MIN_PX and raw_sign[i] != 0 and raw_sign[i] != force:
                target[i] = force

    swapped = (target != raw_sign) & (raw_sign != 0)
    out = src.copy()
    for i in np.flatnonzero(swapped):
        out[i] = src[i][COCO17_SWAP]
    # 3) hips must agree with the shoulders within a frame
    for i in range(n):
        sh = out[i, 5, 0] - out[i, 6, 0]
        hip = out[i, 11, 0] - out[i, 12, 0]
        if abs(sh) >= 40.0 and abs(hip) >= 40.0 and np.sign(sh) != np.sign(hip):
            out[i, [11, 12, 13, 14, 15, 16]] = out[i, [12, 11, 14, 13, 16, 15]]
    return out.astype(np.float32), swapped.astype(np.int32)


def facing_segments(kp2d: np.ndarray) -> list[tuple[int, int, str]]:
    """Human-readable (start, end, 'front'|'back'|'side') runs of a stabilized sequence."""
    src = np.asarray(_as_numpy(kp2d), dtype=np.float64)
    widths = np.array([_lr_x(f) for f in src])
    narrow_px = float(np.clip(NARROW_SCALE * np.median(np.abs(widths)), NARROW_MIN_PX, NARROW_MAX_PX))
    labels = np.where(np.abs(widths) < narrow_px, 0.0, np.sign(widths))
    names = {1.0: "front", -1.0: "back", 0.0: "side"}
    return [(a, b, names[s]) for a, b, s in _sign_runs(labels)]


def stabilize_cache(path: Path) -> np.ndarray:
    """Stabilize a GVHMR 2D-pose cache file in place (keeping a *_raw backup)."""
    import torch

    raw = path.with_name(path.stem + "_raw" + path.suffix)
    src = raw if raw.exists() else path
    if not src.exists():
        raise FileNotFoundError(path)
    if src == path and not raw.exists():
        shutil.copy2(path, raw)
    tensor = torch.load(src, weights_only=False)
    fixed, swaps = stabilize_coco17(tensor)
    print(f"stabilized {path.name}: corrected {int(swaps.sum())}/{len(swaps)} left/right flips")
    torch.save(torch.from_numpy(fixed), path)
    return fixed
