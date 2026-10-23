"""GVHMR extractor: a video or still -> skeleton_motion.npz.

A still is repeated into a short hold clip first. GVHMR is a temporal model
and a one-frame "video" is too short to recover a stable pose. Torch and
``gvhmr`` are imported only when a check or an extract actually needs them.
"""

from __future__ import annotations

import importlib.util
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import numpy as np

from .. import paths
from ..extract import foot_contact_from_raw, playback_fps
from .base import CheckResult, write_skeleton_npz

# GVHMR is a temporal model: a one-frame "video" is too short and often
# unstable. Repeating the still for about a second gives it a static clip
# without inventing motion, and the preview / .glb then hold the pose.
HOLD_FRAMES = 32
HOLD_FPS = 30.0
# Phone photos are often 4000px+; YOLO / RTMPose do not need that, and a
# huge still makes the hold-video encode the slow part of an image run.
HOLD_MAX_SIDE = 1920

SMPLX_HINT = (
    "register at https://smpl-x.is.tue.mpg.de/ , download SMPLX_NEUTRAL.npz, "
    "place it at assets/body_models/smplx/SMPLX_NEUTRAL.npz"
)


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


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

    from ..stabilize_kp2d import stabilize_coco17

    current = torch.load(pose_cache, weights_only=False)
    # Always stabilize the estimator's own output: a cache written by an older
    # rule must not be stabilized a second time on top of its earlier swaps.
    raw_backup = pose_cache.with_name(pose_cache.stem + "_raw" + pose_cache.suffix)
    source = torch.load(raw_backup, weights_only=False) if raw_backup.exists() else current
    fixed, swaps = stabilize_coco17(source)
    if np.allclose(fixed, _to_numpy(current).astype(np.float32)):
        return False
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
        if path.suffix.lower() in paths.VIDEO_SUFFIXES and (path.is_file() or path.is_symlink()):
            path.unlink(missing_ok=True)


def _smplx_checks() -> list[CheckResult]:
    """SMPL-X lines in the shape doctor and preflight already print."""
    from .. import checks

    label = f"SMPL-X body model  {paths.SMPLX_NEUTRAL.relative_to(paths.PROJECT_ROOT)}"
    if not paths.SMPLX_NEUTRAL.exists():
        return [
            CheckResult(label, False, SMPLX_HINT, section="asset", audience="doctor"),
            CheckResult(label, False, SMPLX_HINT, section="asset", audience="preflight"),
        ]
    problem = checks.check_smplx(paths.SMPLX_NEUTRAL)
    if problem is None:
        return [
            CheckResult(label, True, section="asset", audience="doctor"),
            CheckResult(label, True, section="asset", audience="preflight"),
            CheckResult(
                "SMPL-X loads       SMPLX_NEUTRAL.npz",
                True,
                section="asset",
                audience="preflight",
            ),
        ]
    hint = f"{paths.SMPLX_NEUTRAL.name} {problem}"
    return [
        CheckResult(label, False, hint, section="asset", audience="doctor", invalid=True),
        CheckResult(label, True, section="asset", audience="preflight"),
        CheckResult(
            "SMPL-X loads       SMPLX_NEUTRAL.npz",
            False,
            hint,
            section="asset",
            audience="preflight",
            invalid=True,
        ),
    ]


class GvhmrExtractor:
    """Recover a world-grounded skeleton with GVHMR."""

    name = "gvhmr"
    hand_model = "hamer"
    weights_note = "downloaded automatically into weights/ on the first `m2mr run` (~5 GB)"
    hand_weights_note = (
        "HaMeR hand weights (~2.7 GB) download into weights/hamer/ on the first "
        "`m2mr run --detect-hands`"
    )

    def check(self, detect_hands: bool = False) -> list[CheckResult]:
        from .hamer import hand_requirements

        results = _smplx_checks()
        for module in ("torch", "gvhmr"):
            results.append(
                CheckResult(
                    f"python module      {module}",
                    _module_available(module),
                    "pip install -e .",
                    section="module",
                    audience="doctor",
                )
            )
        if detect_hands:
            results.extend(hand_requirements())
        return results

    def extract(
        self,
        source: Path,
        output_npz: Path,
        *,
        work_dir: Path,
        device: str = "cpu",
        verbose: bool = True,
        detect_hands: bool = False,
    ) -> Path:
        source = Path(source)
        if paths.is_image(source):
            with temp_hold_video(source) as hold:
                return _extract_video(
                    hold,
                    output_npz,
                    work_dir=work_dir,
                    device=device,
                    verbose=verbose,
                    source_image=source,
                    detect_hands=detect_hands,
                )
        return _extract_video(
            source,
            output_npz,
            work_dir=work_dir,
            device=device,
            verbose=verbose,
            detect_hands=detect_hands,
        )


def _extract_video(
    video: Path,
    output_npz: Path,
    *,
    work_dir: Path,
    device: str = "cpu",
    static_camera: bool = True,
    verbose: bool = True,
    source_image: Path | None = None,
    detect_hands: bool = False,
) -> Path:
    """Run GVHMR on `video` and save skeleton_motion.npz to `output_npz`.

    `work_dir` holds GVHMR's per-video intermediates (2D pose cache, 3D lift).
    Re-running with the same work_dir reuses the expensive passes.
    `source_image` is recorded when the clip was built from a still.
    """
    paths.export_gvhmr_env()
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

    # RTMPose labels left/right per frame and mislabels isolated frames, which
    # spins the recovered 3D heading for those frames. Stabilize the 2D cache
    # (segment majority, see stabilize_kp2d.py) and redo the 3D lift once if
    # anything was corrected.
    pose_cache = output_dir / "preprocess" / "vitpose.pt"
    if pose_cache.exists() and _stabilize_pose_cache(pose_cache):
        motion_cache = output_dir / "hmr4d_results.pt"
        motion_cache.unlink(missing_ok=True)
        result = recover()

    world = result.smpl_params_world
    joints_3d = joints_world_from_smplx(world, device=device)
    root_translation = _to_numpy(world["transl"]).astype(np.float32)
    root_orientation = _to_numpy(world["global_orient"]).astype(np.float32)
    reported = float(getattr(result, "fps", 0) or 0)
    fps = playback_fps(video, len(joints_3d), fallback=reported or HOLD_FPS)
    if verbose and reported > 0 and abs(fps - reported) > 1.5:
        print(
            f"source is {fps:.3g} fps ({len(joints_3d)} frames); "
            f"GVHMR reported {reported:g} fps — using the source rate so playback matches the video"
        )
    timestamps = np.arange(len(joints_3d), dtype=np.float64) / float(fps)
    image = None if source_image is None else np.array(str(source_image))
    contact = foot_contact_from_raw(getattr(result, "raw", None))
    if contact is not None and len(contact) != len(joints_3d):
        contact = None
    written = write_skeleton_npz(
        output_npz,
        extractor=GvhmrExtractor.name,
        joints_3d=joints_3d,
        fps=fps,
        timestamps=timestamps,
        root_translation=root_translation,
        root_orientation=root_orientation,
        camera=np.array(result.camera),
        video=np.array(str(video)),
        image=image,
        foot_contact=contact,
    )
    if verbose:
        print(f"saved {written}")
    if detect_hands:
        from .hamer import detect_and_append

        if verbose:
            print("detecting hands")
        detect_and_append(
            output_dir,
            written,
            len(joints_3d),
            device=device,
            verbose=verbose,
            single_frame=source_image is not None,
        )
    if source_image is not None:
        _strip_cache_videos(output_dir)
    return written
