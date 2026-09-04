"""Parse progress JSONL written by `m2mr run --progress-jsonl`."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ProgressEvent:
    stage: str
    progress: float
    message: str
    raw: dict[str, Any] = field(default_factory=dict)


def clamp_progress(value: object) -> float:
    try:
        progress = float(value)
    except (TypeError, ValueError):
        return 0.0
    if progress < 0.0:
        return 0.0
    if progress > 1.0:
        return 1.0
    return progress


def parse_progress_jsonl(text: str) -> list[ProgressEvent]:
    """Parse complete JSON objects; skip a truncated final line."""
    events: list[ProgressEvent] = []
    if not text:
        return events
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        events.append(
            ProgressEvent(
                stage=str(data.get("stage", "")),
                progress=clamp_progress(data.get("progress", 0.0)),
                message=str(data.get("message", "")),
                raw=data,
            )
        )
    return events


def read_progress_file(path: str | Path) -> list[ProgressEvent]:
    file_path = Path(path)
    if not file_path.is_file():
        return []
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return []
    return parse_progress_jsonl(text)


def latest_progress(events: list[ProgressEvent]) -> ProgressEvent | None:
    return events[-1] if events else None
