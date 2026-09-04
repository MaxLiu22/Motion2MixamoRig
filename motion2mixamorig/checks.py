"""Content checks for user-supplied files, each returning a fix-it hint.

The CLI already checks that files exist. These look *inside* them, because the
common failure mode is not a missing file but a wrong one — an ASCII FBX, an
SMPL model renamed to SMPL-X, a clip OpenCV cannot decode — which would
otherwise surface minutes into a run as a deep traceback.

Each check returns None when the file is usable, else one line saying what is
wrong and what to do about it.
"""

from __future__ import annotations

from pathlib import Path

# Vertex counts identify the body-model family regardless of the file name.
SMPLX_VERTS = 10475
SMPL_VERTS = 6890

FBX_BINARY_MAGIC = b"Kaydara FBX Binary"

# Sampled frames for the person-count check. The pipeline maps one body to one
# rig, so two people in frame is a hard stop — we do not wait for extraction.
_PERSON_SAMPLES = 16
_PERSON_CONF = 0.5
# Ignore postage-stamp extras (audience, posters). A second dancer is larger.
_PERSON_MIN_AREA = 0.015

_yolo = None


def _person_detector():
    """Ultralytics YOLO, reused across checks. Same family GVHMR uses to find people."""
    global _yolo
    if _yolo is not None:
        return _yolo
    from ultralytics import YOLO

    from .paths import WEIGHTS, export_gvhmr_env

    export_gvhmr_env()
    ckpt = WEIGHTS / "yolo" / "yolov8x.pt"
    _yolo = YOLO(str(ckpt) if ckpt.exists() else "yolov8n.pt")
    return _yolo


def _count_people(frame) -> int:
    h, w = frame.shape[:2]
    min_area = _PERSON_MIN_AREA * h * w
    result = _person_detector().predict(
        frame, conf=_PERSON_CONF, classes=[0], verbose=False
    )[0]
    n = 0
    if result.boxes is None:
        return 0
    for box in result.boxes:
        x1, y1, x2, y2 = (float(v) for v in box.xyxy[0])
        if (x2 - x1) * (y2 - y1) >= min_area:
            n += 1
    return n


def check_video(path: Path) -> str | None:
    """Decodable, and a single person on the sampled frames — not a group."""
    import cv2

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return (
            "cannot be decoded as video — convert it to a plain mp4 first, e.g. "
            "ffmpeg -i input -c:v libx264 output.mp4"
        )
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if n_frames <= 0:
        ok, _ = cap.read()
        cap.release()
        if not ok:
            return (
                "cannot be decoded as video — convert it to a plain mp4 first, e.g. "
                "ffmpeg -i input -c:v libx264 output.mp4"
            )
        return "has no readable frame count — re-export the clip as a plain mp4"
    k = min(_PERSON_SAMPLES, n_frames)
    sample = {int(round(i * (n_frames - 1) / max(k - 1, 1))) for i in range(k)}
    counts: list[int] = []
    idx = 0
    while idx <= max(sample):
        ok, frame = cap.read()
        if not ok:
            break
        if idx in sample:
            counts.append(_count_people(frame))
        idx += 1
    cap.release()
    if not counts:
        return "could not read frames to count people — re-export the clip as a plain mp4"
    crowded = [c for c in counts if c >= 2]
    if crowded:
        peak = max(counts)
        return (
            f"shows about {peak} people in frame — this pipeline maps one body "
            "to one Mixamo rig. Use a clip with a single, clearly visible person"
        )
    if max(counts) < 1:
        return (
            "no person was detected — use a clip with one clearly visible dancer, "
            "not an empty or heavily cropped shot"
        )
    return None


def check_image(path: Path) -> str | None:
    """Decodable still, and exactly one person — same rule as check_video."""
    import cv2

    frame = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if frame is None:
        return (
            "cannot be decoded as an image — use a jpg/png/webp still of one person"
        )
    n = _count_people(frame)
    if n >= 2:
        return (
            f"shows about {n} people — this pipeline maps one body "
            "to one Mixamo rig. Use a photo with a single, clearly visible person"
        )
    if n < 1:
        return (
            "no person was detected — use a photo with one clearly visible person, "
            "head to toe in frame"
        )
    return None


def check_smplx(path: Path) -> str | None:
    """SMPLX_NEUTRAL.npz must be the npz variant of SMPL-X (not SMPL, not .pkl)."""
    import numpy as np

    try:
        with np.load(path, allow_pickle=True) as data:
            v_template = data["v_template"]
    except KeyError:
        return "is an .npz but not a body model (no v_template) — re-download SMPLX_NEUTRAL.npz"
    except Exception:
        return (
            "is not a valid .npz — you may have the pickle (.pkl) variant; "
            "download the *npz* SMPL-X model from https://smpl-x.is.tue.mpg.de/"
        )
    n = int(v_template.shape[0])
    if n == SMPL_VERTS:
        return (
            "is the older SMPL model, not SMPL-X — download SMPLX_NEUTRAL.npz "
            "from https://smpl-x.is.tue.mpg.de/"
        )
    if n != SMPLX_VERTS:
        return f"has {n} template vertices, expected {SMPLX_VERTS} (SMPL-X) — re-download SMPLX_NEUTRAL.npz"
    return None


def check_rig(path: Path) -> str | None:
    """The rig must be a binary FBX containing a Mixamo skeleton."""
    from .mixamo.fbx_skeleton import extract_skeleton

    with open(path, "rb") as f:
        head = f.read(len(FBX_BINARY_MAGIC))
    if head != FBX_BINARY_MAGIC:
        return (
            "is not a *binary* FBX — on mixamo.com pick Format: 'FBX Binary(.fbx)' "
            "when downloading the character"
        )
    try:
        bones = {str(b["name"]) for b in extract_skeleton(path)["bones"]}
    except Exception:
        return "could not be parsed as an FBX scene — re-download the character from mixamo.com"
    if "mixamorig:Hips" not in bones:
        return (
            "has no Mixamo skeleton (mixamorig:* bones) — download a *character* "
            "from mixamo.com, T-pose, FBX Binary"
        )
    return None


def check_skeleton_npz(path: Path) -> str | None:
    """--skeleton must point at a skeleton_motion.npz from a previous run."""
    import numpy as np

    try:
        with np.load(path, allow_pickle=True) as data:
            missing = {"joints_3d", "joint_names", "fps"} - set(data.keys())
    except Exception:
        return "is not a valid .npz file"
    if missing:
        return (
            f"is missing {sorted(missing)} — pass the skeleton_motion.npz "
            "found inside a previous run's output directory"
        )
    return None
