"""Read a job's `diagnostics.json` (written by `m2mr run`) and lay it out on a frame axis.

No Blender imports. Frame numbers in the report are Blender frame numbers after
import (the clip starts at frame 0), so they work with `scene.frame_set` as is.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DIAGNOSTICS_JSON = "diagnostics.json"

_cache: dict[str, tuple[float, dict | None]] = {}


def load_diagnostics(run_dir: str | Path) -> dict | None:
    """The parsed report, or None when the run has none or it is unreadable.

    Cached by modification time, so it is cheap to call from a panel draw.
    """
    if not run_dir:
        return None
    path = Path(run_dir).expanduser() / DIAGNOSTICS_JSON
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return None
    key = str(path)
    hit = _cache.get(key)
    if hit is not None and hit[0] == mtime:
        return hit[1]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        report = data if isinstance(data, dict) and isinstance(data.get("issues"), list) else None
    except (OSError, ValueError):
        report = None
    if report is not None:
        report["_problem_frames"] = problem_frames(report)
    _cache[key] = (mtime, report)
    return report


def problem_frames(report: dict) -> list[int]:
    """Every frame with at least one intersection, sorted."""
    frames: set[int] = set()
    for issue in report.get("issues", []):
        for a, b in issue.get("ranges", []):
            frames.update(range(int(a), int(b) + 1))
    return sorted(frames)


def issues_at(report: dict, frame: int) -> list[dict]:
    return [i for i in report.get("issues", []) if any(a <= frame <= b for a, b in i.get("ranges", []))]


@dataclass
class Cell:
    start: int  # first frame this cell covers
    end: int  # last frame this cell covers
    target: int  # frame to jump to: the first problem frame in the cell, else its start
    hit: bool  # any intersection in the cell


def frame_cells(report: dict, count: int) -> list[Cell]:
    """Split frames 0 .. n-1 into `count` equal cells for the panel's frame bar."""
    n = max(1, int(report.get("frame_count", 1)))
    count = max(1, min(count, n))
    bad = report.get("_problem_frames") or problem_frames(report)
    cells, k = [], 0
    for c in range(count):
        start, end = c * n // count, (c + 1) * n // count - 1
        while k < len(bad) and bad[k] < start:
            k += 1
        first = bad[k] if k < len(bad) and bad[k] <= end else None
        cells.append(Cell(start, end, first if first is not None else start, first is not None))
    return cells


def step_problem(report: dict, frame: int, direction: int) -> int | None:
    """Start of the next (+1) or previous (-1) problem stretch from `frame`, or None."""
    bad = report.get("_problem_frames") or problem_frames(report)
    starts = [f for i, f in enumerate(bad) if i == 0 or bad[i - 1] != f - 1]
    if direction > 0:
        return next((f for f in starts if f > frame), None)
    return next((f for f in reversed(starts) if f < frame), None)
