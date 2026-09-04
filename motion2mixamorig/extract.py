"""Video or still -> 3D human skeleton (GVHMR world-grounded motion recovery).

Produces skeleton_motion.npz with 24 SMPL joints per frame in a Y-up,
meter-scaled world, plus the root translation/orientation and fps.

A still photo is repeated into a short hold clip first: GVHMR is a temporal
model and a one-frame "video" is too short to recover a stable pose.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import numpy as np

from .paths import VIDEO_SUFFIXES, export_gvhmr_env

# SMPL 24-joint order used by GVHMR (J_regressor).
SMPL_JOINT_NAMES = [
    "pelvis",
    "left_hip",
    "right_hip",
    "spine1",
    "left_knee",
    "right_knee",
    "spine2",
    "left_ankle",
    "right_ankle",
    "spine3",
    "left_foot",
    "right_foot",
    "neck",
    "left_collar",
    "right_collar",
    "head",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hand",
    "right_hand",
]

# GVHMR is a temporal model: a one-frame "video" is too short and often
# unstable. Repeating the still for about a second gives it a static clip
# without inventing motion, and the preview / .glb then hold the pose.
HOLD_FRAMES = 32
HOLD_FPS = 30.0
# Phone photos are often 4000px+; YOLO / RTMPose do not need that, and a
# huge still makes the hold-video encode the slow part of an image run.
HOLD_MAX_SIDE = 1920


def _to_numpy(x):
    if hasattr(x, "detach"):
        return x.detach().cpu().numpy()
    return np.asarray(x)


def joints_world_from_smplx(params, device: str = "cpu") -> np.ndarray:
    """Convert GVHMR SMPL-X params to 24 SMPL joints without the gated SMPL .pkl.

    Official ``result.joints_world`` also loads SMPL faces from
    ``SMPL_NEUTRAL.pkl``. The joint math itself only needs SMPL-X plus the
    shipped ``smplx2smpl`` / ``J_regressor`` maps.
    """
    import torch
    from einops import einsum
    from gvhmr import PROJ_ROOT
    from gvhmr.utils.device import to_device
    from gvhmr.utils.smplx_utils import make_smplx

    if device == "mps":
        device = "cpu"
    torch_device = torch.device(device)
    smplx = make_smplx("supermotion").to(torch_device)
    smplx2smpl = torch.load(
        PROJ_ROOT / "gvhmr/utils/body_model/smplx2smpl_sparse.pt",
        weights_only=False,
    ).to(torch_device)
    j_regressor = torch.load(
        PROJ_ROOT / "gvhmr/utils/body_model/smpl_neutral_J_regressor.pt",
        weights_only=False,
    ).to(torch_device)
    with torch.no_grad():
        out = smplx(**to_device(dict(params), torch_device))
        verts = torch.stack([torch.matmul(smplx2smpl, v) for v in out.vertices])
        joints = einsum(j_regressor, verts, "j v, l v i -> l j i")
    return joints.cpu().numpy().astype(np.float32)


def _stabilize_pose_cache(pose_cache: Path) -> bool:
    """Stabilize GVHMR's 2D-pose cache in place. True if the file changed.

    Idempotent: a cache that was already stabilized comes back unchanged. The
    pre-stabilization data is kept next to it (*_raw) so estimator-vs-
    stabilizer questions stay answerable after the fact.
    """
    import shutil

    import torch

    from .stabilize_kp2d import stabilize_coco17

    current = torch.load(pose_cache, weights_only=False)
    fixed, swaps = stabilize_coco17(current)
    if np.allclose(fixed, _to_numpy(current).astype(np.float32)):
        return False
    raw_backup = pose_cache.with_name(pose_cache.stem + "_raw" + pose_cache.suffix)
    if not raw_backup.exists():
        shutil.copy2(pose_cache, raw_backup)
    torch.save(torch.from_numpy(fixed), pose_cache)
    print(f"stabilized {pose_cache.name}: corrected {int(swaps.sum())}/{len(swaps)} left/right flips")
    return True


def still_to_hold_video(
    image: Path,
    out_mp4: Path,
    *,
    n_frames: int = HOLD_FRAMES,
    fps: float = HOLD_FPS,
) -> Path:
    """Repeat a still as a short silent mp4 so GVHMR can treat it as a clip."""
    import shutil
    import subprocess

    import cv2

    image = Path(image)
    frame = cv2.imread(str(image), cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError(f"cannot decode image: {image}")

    h, w = frame.shape[:2]
    longest = max(h, w)
    if longest > HOLD_MAX_SIDE:
        scale = HOLD_MAX_SIDE / longest
        w = int(round(w * scale))
        h = int(round(h * scale))
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
        h, w = frame.shape[:2]
    w -= w % 2
    h -= h % 2
    if w < 2 or h < 2:
        raise ValueError(f"image is too small: {image}")
    frame = frame[:h, :w]

    out_mp4 = Path(out_mp4)
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is not None:
        cmd = [
            ffmpeg, "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{w}x{h}", "-r", f"{fps:g}",
            "-i", "-",
            "-frames:v", str(n_frames),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-preset", "veryfast", "-movflags", "+faststart",
            str(out_mp4),
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        assert proc.stdin is not None
        for _ in range(n_frames):
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed writing {out_mp4}")
        return out_mp4

    writer = cv2.VideoWriter(
        str(out_mp4), cv2.VideoWriter_fourcc(*"mp4v"), float(fps), (w, h)
    )
    if not writer.isOpened():
        raise RuntimeError(f"Cannot open VideoWriter for {out_mp4}")
    for _ in range(n_frames):
        writer.write(frame)
    writer.release()
    return out_mp4


@contextmanager
def temp_hold_video(image: Path) -> Iterator[Path]:
    """Write the hold clip under the system temp dir; delete it afterwards.

    GVHMR needs a real video file, but that file is not a run artifact and
    must not land in cache/.
    """
    import shutil
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="m2mr-hold-"))
    try:
        yield still_to_hold_video(image, tmp / f"{Path(image).stem}.mp4")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _strip_cache_videos(root: Path) -> None:
    """Drop staged / overlay mp4s from a still-image extract.

    GVHMR always stages ``0_input_video.mp4`` (and may write overlay clips
    under preprocess/). Those are only useful for a video run.
    """
    if not root.is_dir():
        return
    for path in root.rglob("*"):
        if path.suffix.lower() in VIDEO_SUFFIXES and (path.is_file() or path.is_symlink()):
            path.unlink(missing_ok=True)


def extract_motion(
    video: Path,
    output_npz: Path,
    *,
    work_dir: Path,
    device: str = "cpu",
    static_camera: bool = True,
    verbose: bool = True,
    source_image: Path | None = None,
) -> Path:
    """Run GVHMR on `video` and save skeleton_motion.npz to `output_npz`.

    `work_dir` holds GVHMR's per-video intermediates (2D pose cache, 3D lift).
    Re-running with the same work_dir reuses the expensive passes.
    `source_image` is recorded when the clip was built from a still.
    """
    export_gvhmr_env()
    import gvhmr

    video = Path(video).resolve()
    if not video.exists():
        raise FileNotFoundError(video)

    output_dir = Path(work_dir) / video.stem

    def recover():
        return gvhmr.recover(
            str(video),
            static_camera=static_camera,
            device=device,
            pose2d="rtmpose",
            output_dir=str(output_dir),
            output_root=str(work_dir),
            progress=verbose,
        )

    result = recover()

    # RTMPose labels left/right per frame and can swap them when the subject
    # turns away, which spins the recovered 3D heading. Stabilize the 2D cache
    # and redo the 3D lift once if anything was corrected.
    pose_cache = output_dir / "preprocess" / "vitpose.pt"
    if pose_cache.exists() and _stabilize_pose_cache(pose_cache):
        motion_cache = output_dir / "hmr4d_results.pt"
        motion_cache.unlink(missing_ok=True)
        result = recover()

    world = result.smpl_params_world
    joints_3d = joints_world_from_smplx(world, device=device)
    root_translation = _to_numpy(world["transl"]).astype(np.float32)
    root_orientation = _to_numpy(world["global_orient"]).astype(np.float32)
    timestamps = np.arange(len(joints_3d), dtype=np.float64) / float(result.fps)

    output_npz = Path(output_npz)
    output_npz.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(
        joints_3d=joints_3d,
        joint_names=np.array(SMPL_JOINT_NAMES),
        fps=np.float32(result.fps),
        timestamps=timestamps,
        root_translation=root_translation,
        root_orientation=root_orientation,
        camera=np.array(result.camera),
        video=np.array(str(video)),
    )
    if source_image is not None:
        payload["image"] = np.array(str(source_image))
        _strip_cache_videos(output_dir)
    np.savez_compressed(output_npz, **payload)
    if verbose:
        print(f"saved {output_npz}")
    return output_npz
