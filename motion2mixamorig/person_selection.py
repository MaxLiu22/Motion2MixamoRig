"""Choose one YOLO track and seed GVHMR's bounding-box cache with that subject.

Tracking uses GVHMR's staged video so frame count, image coordinates and camera
intrinsics agree. No source crop or dependency monkey-patch is needed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from . import paths


class PersonSelectionError(ValueError):
    """A subject could not be selected or followed safely."""


def source_key(source: Path) -> str:
    source = Path(source).resolve()
    stat = source.stat()
    signature = f"{source}:{stat.st_size}:{stat.st_mtime_ns}:selection-v1"
    return hashlib.sha256(signature.encode()).hexdigest()[:20]


def stage_video(video: Path, output_dir: Path):
    """Use the installed GVHMR staging path, including its 30fps conversion."""
    paths.export_gvhmr_env()
    from gvhmr.cli.demo import build_demo_cfg

    return build_demo_cfg(
        Path(video), output_root=str(output_dir.parent), static_cam=True,
        use_dpvo=False, f_mm=None, verbose=False, render_scale=None,
        config_overrides=[f"output_dir={output_dir}", "pose2d=rtmpose"],
    )


def collect_tracks(history: list) -> list[dict]:
    """Keep detector identities; never join separate people across a gap."""
    tracks: dict[int, dict] = {}
    for frame_id, detections in enumerate(history):
        for detection in detections:
            person_id = int(detection["id"])
            box = np.asarray(detection["bbx_xyxy"], dtype=float)
            if box.shape != (4,) or not np.isfinite(box).all():
                raise PersonSelectionError("Tracker returned an invalid person box")
            if box[2] <= box[0] or box[3] <= box[1]:
                continue
            track = tracks.setdefault(person_id, {"id": person_id, "frames": [], "boxes": []})
            track["frames"].append(frame_id)
            track["boxes"].append(box.tolist())
    return sorted(tracks.values(), key=lambda t: t["id"])


def interpolate_track(track: dict, n_frames: int, max_gap: int = 15) -> tuple[np.ndarray, np.ndarray]:
    """Fill short detection gaps only, with an explicit observed-frame mask."""
    frames = np.asarray(track["frames"], dtype=int)
    boxes = np.asarray(track["boxes"], dtype=np.float32)
    if (
        n_frames < 1 or not len(frames) or boxes.shape != (len(frames), 4)
        or np.any(np.diff(frames) <= 0) or frames[0] < 0 or frames[-1] >= n_frames
        or not np.isfinite(boxes).all() or np.any(boxes[:, 2:] <= boxes[:, :2])
    ):
        raise PersonSelectionError("Selected track has invalid frame or bounding-box data")
    gaps = np.r_[frames[0], np.diff(frames) - 1, n_frames - frames[-1] - 1]
    longest = int(gaps.max())
    if longest > max_gap:
        raise PersonSelectionError(
            f"Person {track['id']} is untracked for {longest} frames. "
            f"Only gaps up to {max_gap} frames are filled; trim the clip or select another track. "
            "Separate track IDs are not automatically joined."
        )
    timeline = np.arange(n_frames)
    filled = np.column_stack([np.interp(timeline, frames, boxes[:, i]) for i in range(4)])
    observed = np.zeros(n_frames, dtype=bool)
    observed[frames] = True
    return filled.astype(np.float32), observed


def analyze_people(source: Path, *, image: bool = False, device: str = "cpu") -> dict:
    """Cache all tracks separately from inference, without requiring a rig/body model."""
    import cv2

    source = Path(source).resolve()
    key = source_key(source)
    folder = paths.OUTPUTS / "person_selection" / key
    folder.mkdir(parents=True, exist_ok=True)
    manifest = folder / "people.json"
    if manifest.exists():
        data = json.loads(manifest.read_text())
        if data["source_key"] == key and Path(data["video"]).exists():
            return data
    video = source
    if image:
        from .extract import still_to_hold_video

        video = still_to_hold_video(source, folder / "hold.mp4")
    cfg = stage_video(video, folder / "staged")
    staged = Path(cfg.video_path)
    paths.export_gvhmr_env()
    from gvhmr.utils.preproc.tracker import Tracker

    checkpoint = paths.WEIGHTS / "yolo" / "yolov8x.pt"
    if not checkpoint.exists():
        checkpoint = paths.WEIGHTS / "yolo" / "yolov8n.pt"
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
    tracker = Tracker(ckpt=str(checkpoint))
    tracker.device = 0 if device == "cuda" else device
    history = tracker.track(str(staged))
    tracks = collect_tracks(history)
    if not tracks:
        raise PersonSelectionError("No person tracks found; try a clearer frame or clip")
    cap = cv2.VideoCapture(str(staged))
    try:
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    finally:
        cap.release()
    data = {
        "source": str(source), "source_key": key, "video": str(staged),
        "image": image, "fps": 30.0, "n_frames": len(history),
        "width": width, "height": height, "tracks": tracks,
        "directory": str(folder),
    }
    write_gallery(data)
    manifest.write_text(json.dumps(data, indent=2) + "\n")
    return data


def gallery_page(data: dict, page: int = 0, selected: int | None = None) -> np.ndarray:
    """Six context thumbnails per page, retaining the surrounding people."""
    import cv2

    tracks = data["tracks"][page * 6:(page + 1) * 6]
    canvas = np.full((660, 960, 3), (28, 25, 23), dtype=np.uint8)
    cv2.putText(canvas, "Select a person", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (245, 245, 245), 2)
    pages = (len(data["tracks"]) + 5) // 6
    cv2.putText(canvas, f"Click a card, Enter to confirm. N/P: pages {page+1}/{pages}. Esc: cancel.",
                (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (195, 195, 195), 1)
    cap = cv2.VideoCapture(data["video"])
    try:
        for i, track in enumerate(tracks):
            x, y = (i % 3) * 320 + 8, (i // 3) * 280 + 90
            # Largest observed box gives a readable representative frame.
            boxes = np.asarray(track["boxes"])
            areas = np.prod(boxes[:, 2:] - boxes[:, :2], axis=1)
            best = int(np.argmax(areas))
            cap.set(cv2.CAP_PROP_POS_FRAMES, track["frames"][best])
            ok, frame = cap.read()
            if not ok:
                raise PersonSelectionError("Cannot read the selection preview; re-analyze the source")
            color = (100, 230, 155) if track["id"] == selected else (75, 190, 245)
            x1, y1, x2, y2 = np.rint(boxes[best]).astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, max(2, frame.shape[1] // 300))
            scale = min(300 / frame.shape[1], 210 / frame.shape[0])
            thumb = cv2.resize(frame, None, fx=scale, fy=scale)
            ox, oy = x + (304 - thumb.shape[1]) // 2, y + 6
            canvas[oy:oy+thumb.shape[0], ox:ox+thumb.shape[1]] = thumb
            cv2.rectangle(canvas, (x, y), (x+304, y+265), color, 2)
            cv2.putText(canvas, f"Person {track['id']}", (x+10, y+235), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            coverage = 100 * len(track["frames"]) / data["n_frames"]
            cv2.putText(canvas, f"Observed {coverage:.0f}% of frames", (x+10, y+255),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (210, 210, 210), 1)
    finally:
        cap.release()
    return canvas


def write_gallery(data: dict) -> None:
    import cv2

    for page in range((len(data["tracks"]) + 5) // 6):
        path = Path(data["directory"]) / f"people-{page+1}.jpg"
        if not cv2.imwrite(str(path), gallery_page(data, page)):
            raise OSError(f"Could not write {path}")


def pick_person(data: dict) -> int:
    """Native OpenCV picker; CLI --person is available without a display."""
    import cv2

    page, selected = 0, None
    pages = (len(data["tracks"]) + 5) // 6
    previews = {i: gallery_page(data, i) for i in range(pages)}
    window = "Motion2MixamoRig - select person"

    def click(event, x, y, flags, param):
        nonlocal selected
        if event != cv2.EVENT_LBUTTONDOWN:
            return
        col, row = x // 320, (y - 90) // 280
        if 0 <= col < 3 and 0 <= row < 2:
            index = page * 6 + row * 3 + col
            if index < len(data["tracks"]):
                selected = data["tracks"][index]["id"]

    cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(window, click)
    try:
        while True:
            preview = previews[page].copy()
            for i, track in enumerate(data["tracks"][page * 6:(page + 1) * 6]):
                if track["id"] == selected:
                    x, y = (i % 3) * 320 + 8, (i // 3) * 280 + 90
                    cv2.rectangle(preview, (x, y), (x+304, y+265), (100, 230, 155), 4)
            cv2.imshow(window, preview)
            key = cv2.waitKey(50) & 0xFF
            if key in (13, 10) and selected is not None:
                return selected
            if key == 27 or cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
                raise PersonSelectionError("Person selection cancelled")
            if key in (ord("n"), ord("p")):
                page = (page + (1 if key == ord("n") else -1)) % pages
    finally:
        cv2.destroyWindow(window)


def selected_track(data: dict, person_id: int) -> dict:
    for track in data["tracks"]:
        if track["id"] == person_id:
            return track
    choices = ", ".join(str(t["id"]) for t in data["tracks"])
    raise PersonSelectionError(f"Person {person_id} not found. Available IDs: {choices}")


def seed_person_cache(video: Path, output_dir: Path, data: dict, person_id: int) -> dict:
    """Write a selected track into a person-specific GVHMR preprocessing cache."""
    import cv2
    import torch
    from gvhmr.utils.geo.hmr_cam import get_bbx_xys_from_xyxy

    track = selected_track(data, person_id)
    boxes, observed = interpolate_track(track, data["n_frames"])
    cfg = stage_video(video, output_dir)
    cap = cv2.VideoCapture(str(cfg.video_path))
    try:
        actual = (int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    finally:
        cap.release()
    expected = (data["n_frames"], data["width"], data["height"])
    if actual != expected:
        raise PersonSelectionError(f"Selection video dimensions differ: {actual} vs {expected}; re-analyze the source")
    bbox = torch.from_numpy(boxes)
    target = Path(cfg.paths.bbx)
    if not target.exists():
        torch.save({"bbx_xyxy": bbox, "bbx_xys": get_bbx_xys_from_xyxy(bbox, base_enlarge=1.2).float()}, target)
    summary = {
        "person_id": person_id, "source_key": data["source_key"],
        "observed_frames": int(observed.sum()), "total_frames": len(observed),
        "interpolated_frames": int((~observed).sum()),
        "first_observed_frame": track["frames"][0], "last_observed_frame": track["frames"][-1],
        "selection_directory": data["directory"],
    }
    np.savez_compressed(output_dir / "selected_person.npz", boxes_xyxy=boxes, observed=observed, fps=30.0)
    (output_dir / "person_selection.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary
