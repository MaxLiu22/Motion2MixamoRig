"""The skeleton file every extractor must write.

Input is a video or a still. Output is ``skeleton_motion.npz``: 24 SMPL joints,
Y-up metres, one continuous world frame for the whole clip, the order in
``SMPL_JOINT_NAMES``. Retargeting reads that file and does not care which
extractor produced it.

A new extractor maps its own joints into these 24 names, in metres, before
writing. ``root_orientation`` is optional metadata; retargeting uses joint
positions, not that rotation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np

# SMPL 24-joint order. Retargeting looks joints up by these names.
SMPL_JOINT_NAMES = (
    "pelvis",
    "left_hip",
    "right_hip",
    "spine1",
    "left_knee",
    "right_knee",
    "spine2",
    "left_ankle",
    "right_ankle",
    "spine3",
    "left_foot",
    "right_foot",
    "neck",
    "left_collar",
    "right_collar",
    "head",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hand",
    "right_hand",
)


@dataclass(frozen=True)
class CheckResult:
    """One doctor / preflight line owned by an extractor.

    ``section="asset"`` is a file the run needs. ``section="module"`` is a
    Python dependency, reported by ``m2mr doctor``. ``audience`` picks which
    command prints the line: doctor and preflight lay the same fact out
    differently, and ``both`` prints it in each.
    ``invalid`` prints ``[invalid]`` rather than ``[missing]``.
    """

    label: str
    ok: bool
    hint: str = ""
    section: str = "asset"
    audience: str = "both"
    invalid: bool = False


class MotionExtractor(Protocol):
    """Turn a video or a still into ``skeleton_motion.npz``."""

    name: str
    weights_note: str

    def check(self, detect_hands: bool = False) -> list[CheckResult]:
        """Assets and modules this extractor needs, for doctor and preflight.

        ``detect_hands`` adds the hand model paired with this extractor.
        """

    def extract(
        self,
        source: Path,
        output_npz: Path,
        *,
        work_dir: Path,
        device: str = "cpu",
        verbose: bool = True,
        detect_hands: bool = False,
    ) -> Path:
        """Write the shared skeleton file for `source` (a video or a still).

        ``detect_hands`` asks the extractor to append its paired hand model
        into the same file. Preflight rejects the flag when this extractor
        has no paired hand model.
        """


def write_skeleton_npz(
    path: Path,
    *,
    extractor: str,
    joints_3d: np.ndarray,
    fps: float,
    timestamps: np.ndarray | None = None,
    root_translation: np.ndarray | None = None,
    root_orientation: np.ndarray | None = None,
    **extra,
) -> Path:
    """Write the shared skeleton file. Joint names are always ``SMPL_JOINT_NAMES``."""
    joints = np.asarray(joints_3d)
    expected = (len(SMPL_JOINT_NAMES), 3)
    if joints.ndim != 3 or tuple(joints.shape[1:]) != expected:
        raise ValueError(
            f"joints_3d must be (frames, {expected[0]}, 3), got {joints.shape}"
        )
    fps_value = float(fps)
    if not fps_value > 0:
        raise ValueError(f"fps must be positive, got {fps}")
    if timestamps is None:
        stamps = np.arange(len(joints), dtype=np.float64) / fps_value
    else:
        stamps = np.asarray(timestamps, dtype=np.float64)
        if len(stamps) != len(joints):
            raise ValueError(
                f"timestamps length {len(stamps)} does not match {len(joints)} frames"
            )
    payload: dict = {
        "joints_3d": joints,
        "joint_names": np.array(SMPL_JOINT_NAMES),
        "fps": np.float32(fps_value),
        "timestamps": stamps,
        "extractor": np.array(extractor),
    }
    if root_translation is not None:
        payload["root_translation"] = np.asarray(root_translation)
    if root_orientation is not None:
        payload["root_orientation"] = np.asarray(root_orientation)
    for key, value in extra.items():
        if value is not None:
            payload[key] = value
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **payload)
    return path


def read_extractor_name(path: Path) -> str | None:
    """The extractor recorded in a skeleton file, if this pipeline wrote it."""
    with np.load(path, allow_pickle=True) as data:
        if "extractor" not in data.files:
            return None
        return str(data["extractor"])
