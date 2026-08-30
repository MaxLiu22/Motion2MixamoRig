"""Render the four result videos of a run, all in the input video's aspect ratio.

    videos/human_skeleton.mp4     3D human skeleton recovered from the video
    videos/mixamo_skeleton.mp4    retargeted Mixamo Skeleton
    videos/mixamo_character.mp4   skinned character mesh
    videos/compare.mp4            2x2 grid: original | mixamo skeleton
                                            human    | character

The three rendered panels share one perspective camera and one floor grid, so
they read as views into the same space: an orthographic camera cannot show a
floor receding to a vanishing point, and without a floor and a contact shadow
the figure just hangs in black. All of it is fitted once over the whole clip;
nothing is re-centred per frame.

Frames are streamed straight into ffmpeg (which also muxes the source video's
audio into every output), so memory stays flat no matter how long the clip is.
When ffmpeg is missing the videos still get written via OpenCV, just silent.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np

from .mixamo.animation import RetargetedAnimation, all_points, skin_frames
from .mixamo.render import (
    DARK_THEME,
    GRID_THEME,
    MESH_COLORS_BGR,
    Ground,
    blank_panel,
    build_perspective_camera,
    draw_mesh,
    draw_shadow,
    draw_skeleton,
    fit_letterbox,
    ground_backdrop,
    label_panel,
)
from .mixamo.retarget import HUMAN_EDGES, MIXAMO_EDGES

# Rendered panel height in pixels; width follows the input video's aspect.
PANEL_H = 720
MAX_PANEL_W = 1280

# Frames sampled only to bound the mesh for the camera fit and the floor
# height; never all kept, or the streaming render would gain nothing.
CAMERA_MESH_SAMPLES = 60
# Fraction of the panel the whole clip's motion is fitted into.
CAMERA_FILL = 0.94
# Pinhole view matching the Mixamo viewport the look was taken from. Level
# (elevation 0): a pinhole camera standing above the floor still sees it
# recede, and tilting down makes the chest overhang the hips.
CAMERA_FOV_DEG = 28.0
CAMERA_AZIMUTH_DEG = 0.0
CAMERA_ELEVATION_DEG = 0.0
# The sole wanders over ~20 cm across a clip, mostly on lifted-leg frames, so
# the floor goes at a low percentile of it rather than the minimum. Higher and
# the character sinks in on many frames; lower and it visibly floats on all.
FLOOR_PERCENTILE = 10.0
# The character keeps its own texture colours, and a navy or black outfit
# against a black backdrop has no silhouette: its panel gets the lifted
# backdrop and a little more ambient fill than the white-on-black skeletons.
CHARACTER_AMBIENT = 0.34


def video_size(video: Path) -> tuple[int, int]:
    import cv2

    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video}")
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return w, h


def panel_size(video: Path) -> tuple[int, int]:
    """Panel with the same aspect ratio as the input video, even dimensions."""
    w, h = video_size(video)
    pw = int(round(PANEL_H * w / max(h, 1)))
    pw = min(max(pw, 2), MAX_PANEL_W)
    return pw + pw % 2, PANEL_H + PANEL_H % 2


class _OriginalReader:
    """Sequential reader that letterboxes each requested source frame."""

    def __init__(self, src: Path, width: int, height: int):
        import cv2

        self.blank = blank_panel(width, height)
        self.width, self.height = width, height
        self.cap = cv2.VideoCapture(str(src))
        self.next_idx = 0

    def frame(self, idx: int) -> np.ndarray:
        out = None
        while self.cap.isOpened() and self.next_idx <= idx:
            ok, frame = self.cap.read()
            if not ok:
                break
            if self.next_idx == idx:
                out = fit_letterbox(frame, self.width, self.height)
            self.next_idx += 1
        return self.blank.copy() if out is None else out

    def close(self) -> None:
        self.cap.release()


class _StreamWriter:
    """Raw BGR frames piped into ffmpeg, which encodes H.264 and muxes the
    source video's audio over the rendered frame window.

    Falls back to a plain (silent) OpenCV writer when ffmpeg is unavailable.
    """

    def __init__(
        self,
        out_path: Path,
        fps: float,
        width: int,
        height: int,
        *,
        audio_src: Path | None = None,
        audio_start_s: float = 0.0,
        audio_dur_s: float | None = None,
    ):
        self.out_path = Path(out_path)
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self.proc = None
        self.writer = None
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg is not None:
            cmd = [
                ffmpeg, "-y", "-loglevel", "error",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{width}x{height}", "-r", f"{fps}",
                "-i", "-",
            ]
            if audio_src is not None and Path(audio_src).exists():
                cmd += ["-ss", f"{audio_start_s:.6f}"]
                if audio_dur_s is not None:
                    cmd += ["-t", f"{audio_dur_s:.6f}"]
                # `0:v` is the rendered frames, `1:a:0?` the source audio if
                # it has any; -shortest stops the audio with the last frame.
                cmd += ["-i", str(audio_src), "-map", "0:v:0", "-map", "1:a:0?",
                        "-c:a", "aac", "-b:a", "192k", "-shortest"]
            cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-preset", "medium", "-movflags", "+faststart",
                    str(self.out_path)]
            self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        else:
            import cv2

            self.writer = cv2.VideoWriter(
                str(self.out_path), cv2.VideoWriter_fourcc(*"mp4v"),
                float(fps), (width, height),
            )
            if not self.writer.isOpened():
                raise RuntimeError(f"Cannot open VideoWriter for {self.out_path}")

    def write(self, frame: np.ndarray) -> None:
        if self.proc is not None:
            self.proc.stdin.write(frame.tobytes())
        else:
            self.writer.write(frame)

    def close(self) -> Path:
        if self.proc is not None:
            self.proc.stdin.close()
            if self.proc.wait() != 0:
                raise RuntimeError(f"ffmpeg failed encoding {self.out_path}")
        if self.writer is not None:
            self.writer.release()
        return self.out_path


def _grid2x2(tl: np.ndarray, tr: np.ndarray, bl: np.ndarray, br: np.ndarray) -> np.ndarray:
    return np.vstack([np.hstack([tl, tr]), np.hstack([bl, br])])


def render_run_videos(
    anim: RetargetedAnimation,
    asset,
    calibration,
    source_video: Path,
    out_dir: Path,
    *,
    verbose: bool = True,
) -> dict[str, Path]:
    """Write the four result videos into `out_dir` (videos/ of a run)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    width, height = panel_size(source_video)
    fps = anim.fps

    # One camera and one floor over human joints, Mixamo joints and the mesh,
    # so the three rendered panels agree on where everything stands. Human,
    # Mixamo Skeleton and character all live in the calibrated rig world, so
    # the shared anatomical axes come from the calibration.
    axes = calibration.rig_axes
    stride = max(1, anim.n // CAMERA_MESH_SAMPLES)
    probe = skin_frames(asset, anim, list(range(0, anim.n, stride)))
    frames_pts = [np.concatenate(v, axis=0) for v in probe]
    del probe
    soles = np.array([float(pts[:, 1].min()) for pts in frames_pts])
    mesh_pts = np.concatenate(frames_pts, axis=0)
    del frames_pts

    cam = build_perspective_camera(
        axes,
        np.concatenate(
            [all_points(anim.human_pos), all_points(anim.mixamo_pos), mesh_pts],
            axis=0,
        ),
        width,
        height,
        fov_deg=CAMERA_FOV_DEG,
        azimuth_deg=CAMERA_AZIMUTH_DEG,
        elevation_deg=CAMERA_ELEVATION_DEG,
        fill=CAMERA_FILL,
    )
    del mesh_pts
    hips = np.stack([anim.mixamo_pos[i]["mixamorig:Hips"] for i in range(anim.n)])
    ground = Ground(
        y=float(np.percentile(soles, FLOOR_PERCENTILE)),
        cx=float(np.median(hips[:, 0])),
        cz=float(np.median(hips[:, 2])),
    )
    if verbose:
        print(f"  camera eye {np.round(cam.eye, 3)}  fov {cam.fov_deg:.1f} deg"
              f"  floor y {ground.y:+.4f} m")

    # Camera and floor are both fixed, so the floor is drawn once per theme
    # and every frame starts as a copy of it.
    backdrop_dark = ground_backdrop(cam, ground, width, height, DARK_THEME)
    backdrop_grid = ground_backdrop(cam, ground, width, height, GRID_THEME)

    faces = [m.faces for m in asset.meshes]
    colors = [
        m.face_colors
        if m.face_colors is not None
        else MESH_COLORS_BGR.get(m.name, np.array([150.0, 150.0, 150.0]))
        for m in asset.meshes
    ]

    audio_start = anim.frames[0] / fps
    audio_dur = anim.n / fps

    def writer(name: str, w: int, h: int) -> _StreamWriter:
        return _StreamWriter(
            out_dir / name, fps, w, h,
            audio_src=source_video,
            audio_start_s=audio_start,
            audio_dur_s=audio_dur,
        )

    character = calibration.fbx_path.stem
    writers = {
        "human_skeleton": writer("human_skeleton.mp4", width, height),
        "mixamo_skeleton": writer("mixamo_skeleton.mp4", width, height),
        "mixamo_character": writer("mixamo_character.mp4", width, height),
        "compare": writer("compare.mp4", 2 * width, 2 * height),
    }
    originals = _OriginalReader(source_video, width, height)
    try:
        for i in range(anim.n):
            t = anim.frames[i] / fps
            stamp = f"f{anim.frames[i]}  t={t:.2f}s"

            p_hum = backdrop_dark.copy()
            pos = anim.human_pos[i]
            draw_shadow(p_hum, cam, np.stack(list(pos.values())), ground, DARK_THEME)
            draw_skeleton(p_hum, pos, HUMAN_EDGES, cam, 2, DARK_THEME.joint)
            label_panel(p_hum, f"Human Skeleton  {stamp}")

            p_mix = backdrop_dark.copy()
            pos = anim.mixamo_pos[i]
            draw_shadow(p_mix, cam, np.stack(list(pos.values())), ground, DARK_THEME)
            draw_skeleton(p_mix, pos, MIXAMO_EDGES, cam, 3, DARK_THEME.joint)
            label_panel(p_mix, f"Mixamo Skeleton  {stamp}")

            p_char = backdrop_grid.copy()
            verts = skin_frames(asset, anim, [i])[0]
            draw_shadow(p_char, cam, np.concatenate(verts, axis=0), ground, GRID_THEME)
            draw_mesh(p_char, verts, faces, colors, cam, CHARACTER_AMBIENT)
            label_panel(p_char, f"{character}  {stamp}")

            p_orig = originals.frame(anim.frames[i])
            label_panel(p_orig, f"Original Video  {stamp}")

            writers["human_skeleton"].write(p_hum)
            writers["mixamo_skeleton"].write(p_mix)
            writers["mixamo_character"].write(p_char)
            writers["compare"].write(_grid2x2(p_orig, p_mix, p_hum, p_char))

            if verbose and (i == 0 or (i + 1) % 100 == 0 or i == anim.n - 1):
                print(f"  render {i + 1}/{anim.n}")
    finally:
        originals.close()

    out = {name: w.close() for name, w in writers.items()}
    if verbose:
        for path in out.values():
            print(f"saved {path}")
    return out
