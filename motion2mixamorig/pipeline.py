"""One `m2mr run`: video -> human skeleton -> Mixamo rig -> result videos.

Everything a run produces lands in its own timestamped folder:

    outputs/<YYYYMMDD_HHMMSS>_<video>/
    ├── run.json                what ran, with what inputs, producing what
    ├── skeleton_motion.npz     3D human skeleton (24 SMPL joints per frame)
    ├── mixamo_rotations.npz    per-bone animation rotations for the rig
    ├── mixamo_character.glb    skinned character + animation (Blender / Unity)
    ├── cache/                  GVHMR intermediates (2D pose, 3D lift)
    └── videos/                 the four result videos
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

from . import paths
from .human_motion import HumanMotion, load_human_motion
from .mixamo.animation import build_animation
from .mixamo.gltf import write_glb
from .mixamo.kinematics import quat_wxyz
from .mixamo.retarget import verify_rest_fk
from .mixamo.skinned_mesh import load_character_asset, rest_skin_error
from .mixamo.tpose_calibration import load_calibration
from .mixamo.ybot_retarget import build_mapping
from .videos import render_run_videos

ROTATION_CONVENTION = (
    "Animation-channel rotations: M_local = T * Rpre * R_anim, world = parent @ local. "
    "Quaternions are wxyz. FBX rest translations (T, Rpre) come from the rig file."
)


def save_mixamo_rotations(anim, mapping, rig_path: Path, out_npz: Path) -> Path:
    """Per-bone animation rotations, both the portable Mixamo Skeleton channel
    and the channel already converted for this rig file."""
    bones = list(mapping.controlled)
    n = anim.n
    q_skel = np.zeros((n, len(bones), 4), dtype=np.float64)
    q_rig = np.zeros((n, len(bones), 4), dtype=np.float64)
    for i in range(n):
        for b, name in enumerate(bones):
            q_skel[i, b] = quat_wxyz(anim.r_anim_skeleton[i].get(name, np.eye(3)))
            q_rig[i, b] = quat_wxyz(anim.r_anim_rig[i].get(name, np.eye(3)))
    out_npz = Path(out_npz)
    out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_npz,
        bone_names=np.array(bones),
        quat_wxyz_skeleton=q_skel,
        quat_wxyz_rig=q_rig,
        hips_translation_cm_skeleton=np.stack(anim.hips_cm_skeleton),
        hips_translation_cm_rig=np.stack(anim.hips_cm_rig),
        frames=np.array(anim.frames, dtype=np.int64),
        fps=np.float64(anim.fps),
        rig=np.array(str(rig_path)),
        convention=np.array(ROTATION_CONVENTION),
    )
    return out_npz


def run_pipeline(
    video: Path,
    rig: Path,
    *,
    device: str = "cpu",
    skeleton_npz: Path | None = None,
    verbose: bool = True,
) -> Path:
    """Full pipeline for one video + one rig. Returns the run directory.

    `skeleton_npz` reuses a previous run's skeleton_motion.npz and skips the
    (slow) video extraction entirely.
    """
    video = Path(video).resolve()
    rig = Path(rig).resolve()
    started = datetime.now()
    t0 = time.time()
    run_dir = paths.new_run_dir(video, started)
    print(f"run directory  {run_dir}")

    motion_npz = run_dir / "skeleton_motion.npz"
    if skeleton_npz is not None:
        import shutil

        shutil.copy2(skeleton_npz, motion_npz)
        print(f"reusing skeleton from {skeleton_npz}")
    else:
        from .extract import extract_motion

        print(f"extracting human motion from {video.name}")
        extract_motion(
            video,
            motion_npz,
            work_dir=run_dir / "cache",
            device=device,
            verbose=verbose,
        )
    motion: HumanMotion = load_human_motion(motion_npz)
    print(f"human motion   {motion.n_frames} frames @ {motion.fps:g} fps")

    print(f"calibrating rig {rig.name}")
    calibration = load_calibration(rig)
    rest_err = verify_rest_fk(calibration.skeleton_rig)
    mapping = build_mapping(calibration, verbose=verbose)
    asset = load_character_asset(rig, textures=True)
    skin_err = rest_skin_error(asset)
    if verbose:
        print(f"rest FK error  {rest_err:.3e}   rest skin error {skin_err:.3e} cm")

    print("retargeting")
    frames = list(range(motion.n_frames))
    anim = build_animation(motion, mapping, frames, verbose=verbose)

    rotations_npz = run_dir / "mixamo_rotations.npz"
    save_mixamo_rotations(anim, mapping, rig, rotations_npz)
    print(f"saved {rotations_npz}")

    glb_path = run_dir / "mixamo_character.glb"
    write_glb(glb_path, asset, anim.r_anim_rig, anim.hips_cm_rig, anim.fps)
    print(f"saved {glb_path}")

    print("rendering result videos")
    videos = render_run_videos(
        anim, asset, calibration, video, run_dir / "videos", verbose=verbose
    )

    report = {
        "started": started.isoformat(timespec="seconds"),
        "elapsed_s": round(time.time() - t0, 1),
        "command": sys.argv,
        "video": str(video),
        "rig": str(rig),
        "device": device,
        "fps": float(motion.fps),
        "n_frames": motion.n_frames,
        "skeleton_reused_from": str(skeleton_npz) if skeleton_npz else None,
        "rest_fk_error": rest_err,
        "rest_skin_error_cm": skin_err,
        "twist_events": len(anim.twist_events),
        "quat_sign_flips": len(anim.sign_events),
        "outputs": {
            "skeleton_motion": motion_npz.name,
            "mixamo_rotations": rotations_npz.name,
            "mixamo_character_glb": glb_path.name,
            "videos": {k: f"videos/{v.name}" for k, v in videos.items()},
        },
    }
    (run_dir / "run.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"done in {report['elapsed_s']}s  ->  {run_dir}")
    return run_dir
