"""Load the skeleton_motion.npz produced by extract.py.

Human world (GVHMR gravity frame):
    +Y up, +X right, +Z forward (right-handed), units = meters.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class HumanMotion:
    joints_3d: np.ndarray  # (F, J, 3) meters, Y-up world
    joint_names: list[str]
    fps: float
    timestamps: np.ndarray
    root_translation: np.ndarray | None
    path: Path

    @property
    def n_frames(self) -> int:
        return int(self.joints_3d.shape[0])

    def index(self, name: str) -> int:
        try:
            return self.joint_names.index(name)
        except ValueError as exc:
            raise KeyError(f"joint {name!r} not in {self.joint_names}") from exc

    def joint(self, frame: int, name: str) -> np.ndarray:
        return np.asarray(self.joints_3d[frame, self.index(name)], dtype=np.float64)


def load_human_motion(path: Path) -> HumanMotion:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run the extraction step first.")
    data = np.load(path, allow_pickle=True)
    joints = np.asarray(data["joints_3d"], dtype=np.float64)
    if joints.ndim != 3 or joints.shape[-1] != 3:
        raise ValueError(f"joints_3d must be (F, J, 3), got {joints.shape}")
    names = [str(x) for x in data["joint_names"]]
    fps = float(data["fps"]) if "fps" in data.files else 30.0
    if "timestamps" in data.files:
        timestamps = np.asarray(data["timestamps"], dtype=np.float64)
    else:
        timestamps = np.arange(len(joints), dtype=np.float64) / fps
    root = (
        np.asarray(data["root_translation"], dtype=np.float64)
        if "root_translation" in data.files
        else None
    )
    return HumanMotion(
        joints_3d=joints,
        joint_names=names,
        fps=fps,
        timestamps=timestamps,
        root_translation=root,
        path=path,
    )


def source_video_path(motion: HumanMotion) -> Path | None:
    """The input video recorded inside skeleton_motion.npz, if still on disk."""
    npz = np.load(motion.path, allow_pickle=True)
    if "video" in npz.files:
        path = Path(str(npz["video"]))
        if path.exists():
            return path
    return None
