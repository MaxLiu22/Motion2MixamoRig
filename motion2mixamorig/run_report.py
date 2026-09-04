"""Write and merge `run.json` for a single pipeline run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_run_json(run_dir: Path, report: dict[str, Any]) -> Path:
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "run.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path


def write_failed_report(
    run_dir: Path | None,
    *,
    stage: str,
    error_code: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> Path | None:
    """Write a failed `run.json`. Keeps any earlier fields already on disk."""
    if run_dir is None:
        return None
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {}
    existing = run_dir / "run.json"
    if existing.is_file():
        try:
            loaded = json.loads(existing.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                report.update(loaded)
        except (OSError, json.JSONDecodeError):
            pass
    report.update(
        {
            "status": "failed",
            "stage": stage,
            "error_code": error_code,
            "message": message,
        }
    )
    if extra:
        for key, value in extra.items():
            if key not in {"status", "stage", "error_code", "message"}:
                report[key] = value
    return write_run_json(run_dir, report)
