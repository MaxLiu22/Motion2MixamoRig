"""Keep COCO-17 left/right identity consistent across time.

RTMPose/ViTPose label left/right independently per frame. When the subject
turns to face away, those labels often swap. GVHMR then reads a jumping 2D
skeleton and spins the 3D heading. This assigns each left/right pair to the
previous frame's positions so anatomical identity is tracked, not re-guessed.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np

# Full COCO-17 left/right permutation (nose stays).
COCO17_SWAP = np.array([0, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15], dtype=np.int64)


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


def stabilize_coco17(kp2d: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (stabilized (F,17,3), per-frame swap flags (F,)).

    A real 180-degree turn drives left-right x through a narrow side view. A
    label flip jumps the sign while the width stays large. Those jumps are
    un-swapped so GVHMR sees one anatomical identity.

    "Narrow" is relative to how wide this subject usually reads: on a mid-spin
    frame the estimator can report the shoulders 50-60 px apart instead of ~0
    (one such borderline frame per turn is common), and a fixed 40 px cut then
    misreads the whole genuine turn as a label flip and un-swaps it away. The
    width is invariant under label swaps, so the scale can be measured on the
    raw input up front.
    """
    src = np.asarray(_as_numpy(kp2d), dtype=np.float64)
    if src.ndim != 3 or src.shape[1] < 17:
        raise ValueError(f"expected (F, 17, 3) COCO-17, got {src.shape}")
    out = src.copy()
    n = len(out)
    narrow = float(np.clip(0.45 * np.median([abs(_lr_x(f)) for f in src]), 40.0, 80.0))
    swapped = np.zeros(n, dtype=np.int32)
    last_sign = np.sign(_lr_x(out[0])) or 1.0
    last_turn = -(10**9)
    for i in range(n):
        raw = src[i]
        width = abs(_lr_x(raw))
        sign = np.sign(_lr_x(raw)) or last_sign
        if width >= 40.0 and sign != last_sign:
            start = max(0, last_turn + 1, i - 18)
            widths = [abs(_lr_x(f)) for f in out[start:i]]
            run = best = 0
            for w in widths:
                run = run + 1 if w < narrow else 0
                best = max(best, run)
            if best >= (1 if last_turn < 0 else 4):
                last_sign = sign
                last_turn = i
            else:
                raw = raw[COCO17_SWAP]
                swapped[i] = 1
        out[i] = raw
        sh = out[i, 5, 0] - out[i, 6, 0]
        hip = out[i, 11, 0] - out[i, 12, 0]
        if abs(sh) >= 40.0 and abs(hip) >= 40.0 and np.sign(sh) != np.sign(hip):
            out[i, [11, 12, 13, 14, 15, 16]] = out[i, [12, 11, 14, 13, 16, 15]]
    return out.astype(np.float32), swapped


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
