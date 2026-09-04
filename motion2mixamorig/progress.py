"""Machine-readable progress events for `m2mr run` and the Blender extension."""

from __future__ import annotations

import json
import os
from pathlib import Path


class ProgressWriter:
    """Append one JSON object per line and flush immediately.

    `path=None` is a no-op so the CLI stays quiet when `--progress-jsonl` is
    omitted. Creating a writer truncates an existing file so each run starts
    clean.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("", encoding="utf-8")

    def emit(self, stage: str, progress: float, message: str) -> dict:
        event = {
            "stage": str(stage),
            "progress": _clamp_progress(progress),
            "message": str(message),
        }
        if self.path is None:
            return event
        line = json.dumps(event, ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
        return event


def _clamp_progress(value: object) -> float:
    try:
        progress = float(value)
    except (TypeError, ValueError):
        return 0.0
    if progress < 0.0:
        return 0.0
    if progress > 1.0:
        return 1.0
    return progress
