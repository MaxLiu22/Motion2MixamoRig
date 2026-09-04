"""Read `run.json` and turn fps / frame counts into Blender-friendly values."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunResult:
    status: str
    run_dir: Path
    fps: float | None = None
    n_frames: int | None = None
    glb_path: Path | None = None
    error_code: str | None = None
    message: str | None = None
    stage: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


def resolve_run_path(run_dir: Path, value: object) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if path.is_absolute():
        return path
    return run_dir / path


def blender_frame_settings(fps: float, n_frames: int) -> dict[str, float | int]:
    """Map a fractional fps onto Blender's integer `fps` + `fps_base`."""
    rate = float(fps)
    frames = max(1, int(n_frames))
    if abs(rate - round(rate)) < 1e-6:
        fps_int = max(1, int(round(rate)))
        fps_base = 1.0
    else:
        fps_int = max(1, int(round(rate)))
        fps_base = fps_int / rate if rate > 0 else 1.0
    return {
        "fps": fps_int,
        "fps_base": float(fps_base),
        "frame_start": 1,
        "frame_end": frames,
    }


def read_run_json(run_dir: str | Path) -> RunResult:
    directory = Path(run_dir)
    path = directory / "run.json"
    if not path.is_file():
        return RunResult(
            status="missing",
            run_dir=directory,
            error_code="JSON_INVALID",
            message="Result JSON is invalid",
        )
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return RunResult(
            status="invalid",
            run_dir=directory,
            error_code="JSON_INVALID",
            message="Result JSON is invalid",
        )
    if not isinstance(raw, dict):
        return RunResult(
            status="invalid",
            run_dir=directory,
            error_code="JSON_INVALID",
            message="Result JSON is invalid",
        )

    outputs = raw.get("outputs") if isinstance(raw.get("outputs"), dict) else {}
    glb = resolve_run_path(directory, outputs.get("mixamo_character_glb"))
    fps = _as_float(raw.get("fps"))
    n_frames = _as_int(raw.get("n_frames"))
    status = str(raw.get("status") or "")
    error_code = raw.get("error_code")
    message = raw.get("message")
    stage = raw.get("stage")

    if status == "failed":
        return RunResult(
            status="failed",
            run_dir=directory,
            fps=fps,
            n_frames=n_frames,
            glb_path=glb if glb is not None and glb.is_file() else None,
            error_code=str(error_code) if error_code else "PIPELINE_FAILED",
            message=str(message) if message else "Motion2MixamoRig pipeline failed",
            stage=str(stage) if stage else None,
            raw=raw,
        )

    if status == "completed" or (glb is not None and glb.is_file()):
        if glb is None or not glb.is_file():
            return RunResult(
                status="glb_missing",
                run_dir=directory,
                fps=fps,
                n_frames=n_frames,
                glb_path=None,
                error_code="GLB_MISSING",
                message="Result GLB not found",
                stage=str(stage) if stage else None,
                raw=raw,
            )
        return RunResult(
            status="completed",
            run_dir=directory,
            fps=fps,
            n_frames=n_frames,
            glb_path=glb,
            error_code=None,
            message=None,
            stage="done",
            raw=raw,
        )

    return RunResult(
        status=status or "unknown",
        run_dir=directory,
        fps=fps,
        n_frames=n_frames,
        glb_path=glb if glb is not None and glb.is_file() else None,
        error_code=str(error_code) if error_code else None,
        message=str(message) if message else None,
        stage=str(stage) if stage else None,
        raw=raw,
    )


def _as_float(value: object) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _as_int(value: object) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None
