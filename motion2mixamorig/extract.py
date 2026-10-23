"""Clip timing helpers shared by extraction and preview rendering.

Motion recovery lives in ``motion2mixamorig.extractors``. Preview rendering
reads the container frame rate from here so a 60 fps source is not played
back at the model's own rate.
"""

from __future__ import annotations

from pathlib import Path


def video_duration_seconds(path: Path) -> float | None:
    """Wall-clock length of a clip. Prefers ffprobe; OpenCV is the fallback."""
    import os
    import subprocess

    try:
        completed = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=duration:format=duration",
                "-of",
                "json",
                os.fspath(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=8,
        )
        if completed.returncode == 0 and completed.stdout.strip():
            import json

            payload = json.loads(completed.stdout)
            streams = payload.get("streams") or []
            candidates = []
            if streams and streams[0].get("duration"):
                candidates.append(streams[0]["duration"])
            fmt = payload.get("format") or {}
            if fmt.get("duration"):
                candidates.append(fmt["duration"])
            for raw in candidates:
                duration = float(raw)
                if duration > 0:
                    return duration
    except (OSError, subprocess.TimeoutExpired, ValueError):
        pass
    try:
        import cv2

        cap = cv2.VideoCapture(os.fspath(path))
        try:
            fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
            count = float(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        finally:
            cap.release()
        if fps > 1e-6 and count > 0:
            return count / fps
    except Exception:
        pass
    return None


def video_native_fps(path: Path) -> float | None:
    """Container frame rate (e.g. 60000/1001). None if it cannot be read."""
    import os
    import subprocess

    try:
        completed = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=avg_frame_rate,r_frame_rate",
                "-of",
                "json",
                os.fspath(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=8,
        )
        if completed.returncode == 0 and completed.stdout.strip():
            import json

            streams = json.loads(completed.stdout).get("streams") or []
            if streams:
                rate = streams[0].get("avg_frame_rate") or streams[0].get("r_frame_rate") or "0/1"
                num, _, den = str(rate).partition("/")
                fps = float(num) / float(den or 1)
                if fps > 0:
                    return fps
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError):
        pass
    try:
        import cv2

        cap = cv2.VideoCapture(os.fspath(path))
        try:
            fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
        finally:
            cap.release()
        if fps > 1e-6:
            return fps
    except Exception:
        pass
    return None


def playback_fps(video: Path, n_motion_frames: int, fallback: float = 30.0) -> float:
    """FPS that plays `n_motion_frames` in the source clip's real duration.

    GVHMR always reports 30 fps (the model rate). If staging fails to resample a
    60 fps source, keeping that 30 would stretch the clip to ~2× length.
    """
    n = max(1, int(n_motion_frames))
    duration = video_duration_seconds(video)
    native = video_native_fps(video)
    if duration and duration > 1e-6:
        implied_source_frames = native * duration if native else None
        if (
            implied_source_frames is not None
            and abs(implied_source_frames - n) <= 2
            and native
            and native > 0
        ):
            return float(native)
        return n / duration
    if native and native > 0:
        return float(native)
    return float(fallback) if fallback > 0 else 30.0


def foot_contact_from_raw(raw):
    """(F, 4) static probability of left ankle, left foot, right ankle, right foot.

    GVHMR's static_conf_logits channels are [L_ankle, L_foot, R_ankle, R_foot,
    L_wrist, R_wrist]; only the feet are kept.
    """
    import numpy as np

    try:
        logits = raw["net_outputs"]["static_conf_logits"]
    except (KeyError, TypeError):
        return None
    if hasattr(logits, "detach"):
        logits = logits.detach().cpu().numpy()
    logits = np.asarray(logits, dtype=np.float64).reshape(-1, logits.shape[-1])
    if logits.shape[-1] < 4:
        return None
    return (1.0 / (1.0 + np.exp(-logits[:, :4]))).astype(np.float32)

