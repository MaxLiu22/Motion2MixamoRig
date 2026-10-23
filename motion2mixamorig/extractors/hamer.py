"""HaMeR finger pass for a body extractor that already chose the person and the frames.

The body cache supplies COCO-17 wrists (GVHMR's ``vitpose.pt``) and the staged
video those coordinates were measured on (``0_input_video.mp4``). This module
crops each wrist and appends MANO finger rotations to ``skeleton_motion.npz``.
It does not run its own person detector.
"""

from __future__ import annotations

import importlib.util
import time
from pathlib import Path

import numpy as np

from .. import paths
from .base import CheckResult

# MANO's 15 articulated joints, parent-relative, in MANO kintree order.
HAND_JOINT_NAMES = (
    "index1", "index2", "index3",
    "middle1", "middle2", "middle3",
    "pinky1", "pinky2", "pinky3",
    "ring1", "ring2", "ring3",
    "thumb1", "thumb2", "thumb3",
)
HAND_POSE_CONVENTION = (
    "MANO parent-relative rotation matrices relative to the flat MANO template "
    "(no hand_mean added); index 0 = left hand (mirrored back from HaMeR's "
    "right-hand prediction), index 1 = right hand."
)
HAND_MODEL_NAME = "hamer"

# Released hamer.ckpt configuration.
IMAGE_SIZE = 256
BBOX_SHAPE = (192, 256)
IMAGE_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGE_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
FOCAL_LENGTH = 5000.0
RESCALE_FACTOR = 2.0
BATCH = 8

# COCO-17. GVHMR's vitpose cache is (frames, 17, 3) in the staged video's pixels.
LEFT_ELBOW, LEFT_WRIST = 7, 9
RIGHT_ELBOW, RIGHT_WRIST = 8, 10
WRIST_CONF = 0.3
STAGED_VIDEO_NAME = "0_input_video.mp4"

HAMER_URL = "https://www.cs.utexas.edu/~pavlakos/hamer/data/hamer_demo_data.tar.gz"
HAMER_MEMBERS = {
    "_DATA/hamer_ckpts/checkpoints/hamer.ckpt": "hamer.ckpt",
    "_DATA/data/mano_mean_params.npz": "mano_mean_params.npz",
}
MANO_HINT = (
    "register at https://mano.is.tue.mpg.de/ , download 'Models & Code' (mano_v1_2.zip), "
    "place models/MANO_RIGHT.pkl at assets/body_models/mano/MANO_RIGHT.pkl"
)
HAND_WEIGHTS_NOTE = (
    "HaMeR hand weights (~2.7 GB) download into weights/hamer/ on the first "
    "`m2mr run --detect-hands`"
)
_MIRROR = np.diag([-1.0, 1.0, 1.0]).astype(np.float32)


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def mano_present() -> bool:
    return paths.MANO_RIGHT_NPZ.exists() or paths.MANO_RIGHT_PKL.exists()


def hand_requirements() -> list[CheckResult]:
    """MANO and the Python modules the finger pass imports."""
    label = f"MANO hand model    {paths.MANO_DIR.relative_to(paths.PROJECT_ROOT)}/MANO_RIGHT.pkl"
    results = [
        CheckResult(
            label,
            mano_present(),
            MANO_HINT,
            section="hand",
            audience="both",
        )
    ]
    for module in ("smplx", "timm", "skimage"):
        results.append(
            CheckResult(
                f"python module      {module}",
                _module_available(module),
                "pip install -e .",
                section="hand",
                audience="both",
            )
        )
    return results


def skeleton_from_still(path: Path) -> bool:
    """True when the skeleton file was recovered from a photo, not a video."""
    with np.load(path, allow_pickle=True) as data:
        if "image" not in data.files:
            return False
        value = np.asarray(data["image"]).reshape(-1)
        if value.size == 0:
            return False
        text = str(value[0])
        return bool(text) and text.lower() != "none"


def skeleton_has_hands(path: Path) -> bool:
    with np.load(path, allow_pickle=True) as data:
        return "hand_pose" in data.files and "hand_valid" in data.files


def read_hands_name(path: Path) -> str | None:
    """``hands`` on new files; ``hands_extractor`` on files written by the earlier hand pass."""
    with np.load(path, allow_pickle=True) as data:
        for key in ("hands", "hands_extractor"):
            if key not in data.files:
                continue
            text = str(np.asarray(data[key]).reshape(-1)[0]) if np.asarray(data[key]).size else ""
            if text and text.lower() != "none":
                return text
        return None


def find_body_cache(run_dir: Path) -> Path | None:
    """The GVHMR output folder that holds the staged video and vitpose cache."""
    cache = Path(run_dir) / "cache"
    if not cache.is_dir():
        return None
    found = []
    for pose in cache.glob(f"*/preprocess/vitpose.pt"):
        folder = pose.parent.parent
        if (folder / STAGED_VIDEO_NAME).is_file() and (folder / "preprocess" / "bbx.pt").is_file():
            found.append(folder)
    if len(found) == 1:
        return found[0]
    return None


def convert_mano_pkl(pkl: Path, npz: Path) -> Path:
    """MANO_RIGHT.pkl (chumpy pickle) -> MANO_RIGHT.npz that smplx can load."""
    import inspect
    import pickle

    if not hasattr(inspect, "getargspec"):
        inspect.getargspec = inspect.getfullargspec  # type: ignore[attr-defined]
    for name, typ in (
        ("bool", bool), ("int", int), ("float", float), ("complex", complex),
        ("object", object), ("unicode", str), ("str", str),
    ):
        if not hasattr(np, name):
            setattr(np, name, typ)
    with open(pkl, "rb") as fh:
        data = pickle.load(fh, encoding="latin1")
    out: dict[str, np.ndarray] = {}
    for key, value in data.items():
        if hasattr(value, "r"):
            value = np.asarray(value.r)
        elif hasattr(value, "toarray"):
            value = value.toarray()
        if isinstance(value, (int, float, str, list, tuple, np.ndarray)):
            out[key] = np.asarray(value)
    npz = Path(npz)
    npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez(npz, **out)
    return npz


def ensure_mano_npz() -> Path:
    if paths.MANO_RIGHT_NPZ.exists():
        return paths.MANO_RIGHT_NPZ
    if paths.MANO_RIGHT_PKL.exists():
        print(f"converting {paths.MANO_RIGHT_PKL.name} -> {paths.MANO_RIGHT_NPZ.name} (one time)")
        return convert_mano_pkl(paths.MANO_RIGHT_PKL, paths.MANO_RIGHT_NPZ)
    raise FileNotFoundError(f"MANO model missing: {MANO_HINT}")


def ensure_hamer_weights(verbose: bool = True) -> None:
    """Stream the official bundle and keep only the checkpoint and mean params."""
    if paths.HAMER_CKPT.exists() and paths.HAMER_MEAN_PARAMS.exists():
        return
    import tarfile
    import urllib.request

    paths.HAMER_WEIGHTS.mkdir(parents=True, exist_ok=True)
    if verbose:
        print(f"downloading HaMeR weights (bundle ~6 GB, keeping ~2.7 GB) -> {paths.HAMER_WEIGHTS}")
    wanted = dict(HAMER_MEMBERS)
    with urllib.request.urlopen(HAMER_URL) as resp:
        with tarfile.open(fileobj=resp, mode="r|gz") as tar:
            for member in tar:
                target = wanted.pop(member.name, None)
                if target is None:
                    continue
                src = tar.extractfile(member)
                assert src is not None
                tmp = paths.HAMER_WEIGHTS / (target + ".part")
                with open(tmp, "wb") as dst:
                    while chunk := src.read(1 << 24):
                        dst.write(chunk)
                tmp.replace(paths.HAMER_WEIGHTS / target)
                if verbose:
                    print(f"  saved {target}")
                if not wanted:
                    break
    if wanted:
        raise RuntimeError(f"HaMeR bundle did not contain {sorted(wanted)}")


def _as_numpy(value) -> np.ndarray:
    if hasattr(value, "detach"):
        value = value.detach().cpu().numpy()
    return np.asarray(value)


def wrist_box(frame_kp: np.ndarray, body_xyxy: np.ndarray, *, left: bool) -> np.ndarray | None:
    """A square crop around one COCO wrist, in the staged video's pixels.

    The side length follows the elbow-to-wrist distance when the elbow is
    visible, otherwise a fraction of the body box. HaMeR then expands it.
    """
    elbow_i, wrist_i = (LEFT_ELBOW, LEFT_WRIST) if left else (RIGHT_ELBOW, RIGHT_WRIST)
    wrist = np.asarray(frame_kp[wrist_i], dtype=np.float64)
    if wrist.shape[0] < 3 or float(wrist[2]) < WRIST_CONF:
        return None
    elbow = np.asarray(frame_kp[elbow_i], dtype=np.float64)
    if elbow.shape[0] >= 3 and float(elbow[2]) >= WRIST_CONF:
        length = float(np.linalg.norm(wrist[:2] - elbow[:2]))
        side = max(length * 1.2, 20.0)
    else:
        box = np.asarray(body_xyxy, dtype=np.float64)
        side = max(0.18 * max(float(box[2] - box[0]), float(box[3] - box[1])), 20.0)
    half = side / 2.0
    center = wrist[:2]
    return np.array(
        [center[0] - half, center[1] - half, center[0] + half, center[1] + half],
        dtype=np.float32,
    )


class HamerHandModel:
    """HaMeR ViT-H + MANO head, inference only."""

    def __init__(self, device: str = "cpu", verbose: bool = True) -> None:
        import torch

        from ..vendor.hamer.mano_head import MANOTransformerDecoderHead
        from ..vendor.hamer.vit import ViT

        ensure_hamer_weights(verbose=verbose)
        ensure_mano_npz()
        self.device = torch.device(device)
        t0 = time.time()
        self.backbone = ViT(
            img_size=(256, 192), patch_size=16, embed_dim=1280, depth=32, num_heads=16,
            ratio=1, use_checkpoint=False, mlp_ratio=4, qkv_bias=True, drop_path_rate=0.55,
        )
        self.head = MANOTransformerDecoderHead(str(paths.HAMER_MEAN_PARAMS))
        state = torch.load(paths.HAMER_CKPT, map_location="cpu", weights_only=False)
        state = state.get("state_dict", state)
        self.backbone.load_state_dict({k[9:]: v for k, v in state.items() if k.startswith("backbone.")})
        self.head.load_state_dict({k[10:]: v for k, v in state.items() if k.startswith("mano_head.")})
        for module in (self.backbone, self.head):
            module.to(self.device).eval()
        if verbose:
            print(f"HaMeR loaded in {time.time() - t0:.1f}s on {self.device}")

    def crop(self, img_bgr: np.ndarray, box_xyxy: np.ndarray, is_right: bool) -> tuple[np.ndarray, np.ndarray, float]:
        """One normalised (3, 256, 256) RGB patch. Left hands are mirrored."""
        from skimage.filters import gaussian

        from ..vendor.hamer.crop import expand_to_aspect_ratio, generate_image_patch_cv2
        import cv2

        box = np.asarray(box_xyxy, dtype=np.float32)
        center = (box[2:4] + box[0:2]) / 2.0
        scale = RESCALE_FACTOR * (box[2:4] - box[0:2]) / 200.0
        size = float(expand_to_aspect_ratio(scale * 200, target_aspect_ratio=BBOX_SHAPE).max())
        img = img_bgr
        down = size / IMAGE_SIZE / 2.0
        if down > 1.1:
            img = gaussian(img, sigma=(down - 1) / 2, channel_axis=2, preserve_range=True)
        patch, _ = generate_image_patch_cv2(
            img, float(center[0]), float(center[1]), size, size, IMAGE_SIZE, IMAGE_SIZE,
            not is_right, 1.0, 0, border_mode=cv2.BORDER_CONSTANT,
        )
        patch = patch[:, :, ::-1].astype(np.float32) / 255.0
        patch = (patch - IMAGE_MEAN) / IMAGE_STD
        return np.ascontiguousarray(patch.transpose(2, 0, 1)), center, size

    def predict(self, patches: np.ndarray, is_right: np.ndarray) -> np.ndarray:
        """MANO joint rotations for a batch. Left hands are mirrored back."""
        import torch

        x = torch.from_numpy(np.asarray(patches, dtype=np.float32)).to(self.device)
        with torch.no_grad():
            feats = self.backbone(x[:, :, :, 32:-32])
            params, _cam = self.head(feats)
        hp = params["hand_pose"].float().cpu().numpy()
        for i in np.flatnonzero(~np.asarray(is_right, dtype=bool)):
            hp[i] = _MIRROR @ hp[i] @ _MIRROR
        return hp.reshape(x.shape[0], 15, 3, 3).astype(np.float32)


def _load_pose_and_boxes(cache_dir: Path, n_frames: int) -> tuple[np.ndarray, np.ndarray]:
    import torch

    pose_path = cache_dir / "preprocess" / "vitpose.pt"
    box_path = cache_dir / "preprocess" / "bbx.pt"
    video_path = cache_dir / STAGED_VIDEO_NAME
    if not pose_path.is_file() or not box_path.is_file() or not video_path.is_file():
        raise FileNotFoundError(
            f"hand detection needs {STAGED_VIDEO_NAME}, vitpose.pt and bbx.pt under {cache_dir}"
        )
    kp = _as_numpy(torch.load(pose_path, weights_only=False))
    bbx = torch.load(box_path, weights_only=False)["bbx_xyxy"]
    boxes = _as_numpy(bbx)
    if kp.ndim != 3 or kp.shape[1] < 17 or kp.shape[-1] < 3:
        raise ValueError(f"vitpose cache must be (frames, 17, 3), got {getattr(kp, 'shape', None)}")
    if len(kp) != n_frames or len(boxes) != n_frames:
        raise ValueError(
            f"body cache has {len(kp)} pose frames and {len(boxes)} boxes, "
            f"but the skeleton has {n_frames}"
        )
    return kp, boxes


def _blank_pose(n: int) -> np.ndarray:
    return np.tile(np.eye(3, dtype=np.float32), (n, 2, 15, 1, 1))


def detect_on_cache(
    cache_dir: Path,
    n_frames: int,
    *,
    device: str = "cpu",
    verbose: bool = True,
    single_frame: bool = False,
) -> dict[str, np.ndarray]:
    """Finger rotations aligned with the body skeleton's frames."""
    import cv2

    kp, boxes = _load_pose_and_boxes(cache_dir, n_frames)
    video_path = cache_dir / STAGED_VIDEO_NAME
    use_n = 1 if single_frame else n_frames
    pose = _blank_pose(use_n)
    valid = np.zeros((use_n, 2), dtype=bool)
    model: HamerHandModel | None = None
    pending: list[tuple[int, int, np.ndarray, bool]] = []

    def flush() -> None:
        if not pending:
            return
        assert model is not None
        rotations = model.predict(
            np.stack([item[2] for item in pending]),
            np.array([item[3] for item in pending]),
        )
        for i, (frame, side, *_rest) in enumerate(pending):
            pose[frame, side] = rotations[i]
            valid[frame, side] = True
        pending.clear()

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"cannot open staged video {video_path}")
    t0 = time.time()
    try:
        for frame_i in range(use_n):
            ok, frame = cap.read()
            if not ok:
                raise ValueError(
                    f"{video_path.name} ended at frame {frame_i}, expected {use_n}"
                )
            for side, is_right in ((0, False), (1, True)):
                box = wrist_box(kp[frame_i], boxes[frame_i], left=not is_right)
                if box is None:
                    continue
                if model is None:
                    model = HamerHandModel(device=device, verbose=verbose)
                patch, _center, _size = model.crop(frame, box, is_right)
                pending.append((frame_i, side, patch, is_right))
            if len(pending) >= BATCH:
                flush()
            if verbose and use_n > 1 and (frame_i == 0 or (frame_i + 1) % 30 == 0 or frame_i == use_n - 1):
                seen = valid[: frame_i + 1].sum(axis=0)
                print(
                    f"  hands  frame {frame_i + 1}/{use_n}  "
                    f"left {int(seen[0])}  right {int(seen[1])}  {time.time() - t0:.0f}s"
                )
        flush()
    finally:
        cap.release()
    if single_frame and n_frames != 1:
        pose = np.repeat(pose, n_frames, axis=0)
        valid = np.repeat(valid, n_frames, axis=0)
    if verbose:
        seen = valid.sum(axis=0)
        print(
            f"hands done     {n_frames} frames, left seen {int(seen[0])}, "
            f"right seen {int(seen[1])}, {time.time() - t0:.0f}s"
        )
    with np.load(ensure_mano_npz()) as mano:
        template = np.asarray(mano["J"], dtype=np.float32)
    return {
        "hand_pose": pose,
        "hand_valid": valid,
        "hand_template_joints": template,
        "hands": np.array(HAND_MODEL_NAME),
        "hand_pose_convention": np.array(HAND_POSE_CONVENTION),
    }


def append_hands(skeleton_npz: Path, arrays: dict[str, np.ndarray]) -> Path:
    """Add the finger arrays to an existing skeleton file."""
    skeleton_npz = Path(skeleton_npz)
    with np.load(skeleton_npz, allow_pickle=True) as data:
        payload = {key: data[key] for key in data.files}
    payload.update(arrays)
    np.savez_compressed(skeleton_npz, **payload)
    return skeleton_npz


def detect_and_append(
    cache_dir: Path,
    skeleton_npz: Path,
    n_frames: int,
    *,
    device: str = "cpu",
    verbose: bool = True,
    single_frame: bool = False,
) -> Path:
    arrays = detect_on_cache(
        cache_dir,
        n_frames,
        device=device,
        verbose=verbose,
        single_frame=single_frame,
    )
    return append_hands(skeleton_npz, arrays)
