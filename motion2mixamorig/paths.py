"""Single source of truth for project paths: assets, weights, outputs."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ASSETS = PROJECT_ROOT / "assets"
BODY_MODELS = ASSETS / "body_models"
SMPLX_NEUTRAL = BODY_MODELS / "smplx" / "SMPLX_NEUTRAL.npz"
MIXAMO_DIR = ASSETS / "mixamo"
DEFAULT_RIG = MIXAMO_DIR / "Y_Bot.fbx"
VIDEO_DIR = ASSETS / "video"

WEIGHTS = PROJECT_ROOT / "weights"
OUTPUTS = PROJECT_ROOT / "outputs"

VIDEO_SUFFIXES = (".mp4", ".mov", ".avi", ".mkv", ".webm")


def list_videos() -> list[Path]:
    """User-supplied videos in assets/video/, most recently added first."""
    if not VIDEO_DIR.is_dir():
        return []
    videos = [
        p
        for p in VIDEO_DIR.iterdir()
        if p.suffix.lower() in VIDEO_SUFFIXES and not p.name.startswith(".")
    ]
    return sorted(videos, key=lambda p: p.stat().st_mtime, reverse=True)


def latest_video() -> Path | None:
    """The video most recently placed into assets/video/ (by file mtime)."""
    videos = list_videos()
    return videos[0] if videos else None


def new_run_dir(video: Path, now: datetime | None = None) -> Path:
    """Create outputs/<YYYYMMDD_HHMMSS>_<video-stem>/ for one `m2mr run`."""
    stamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUTS / f"{stamp}_{video.stem}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "videos").mkdir(exist_ok=True)
    return run_dir


def export_gvhmr_env() -> None:
    """Point GVHMR at this project's weights/ and assets/ before importing it.

    The gvhmr package resolves its asset roots from these variables at import
    time. Auto-downloaded checkpoints land in weights/; the gated SMPL-X body
    model is read from assets/body_models/ where the user placed it.
    """
    os.environ.setdefault("GVHMR_CHECKPOINTS", str(WEIGHTS))
    os.environ.setdefault("GVHMR_BODY_MODELS", str(BODY_MODELS))
