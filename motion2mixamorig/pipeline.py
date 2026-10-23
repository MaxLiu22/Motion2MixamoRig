"""One `m2mr run`: video or still -> human skeleton -> Mixamo rig -> result videos.

Everything a run produces lands in its own timestamped folder:

    outputs/<YYYYMMDD_HHMMSS>_<source>/
    ├── run.json                what ran, with what inputs, producing what
    ├── skeleton_motion.npz     3D human skeleton (24 SMPL joints per frame)
    ├── mixamo_rotations.npz    per-bone animation rotations for the rig
    ├── mixamo_character.glb    skinned character + animation (Blender / Unity)
    ├── cache/                  extractor intermediates (GVHMR: 2D pose, 3D lift)
    └── videos/ or images/      four result clips (video in) or four stills (photo in)
"""

from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

from . import paths
from .errors import classify_error
from .diagnose import DIAGNOSTICS_JSON, diagnose_run, summary_line
from .extractors import DEFAULT_EXTRACTOR, get_extractor
from .extractors.base import read_extractor_name
from .extractors.hamer import (
    detect_and_append,
    find_body_cache,
    read_hands_name,
    skeleton_from_still,
    skeleton_has_hands,
)
from .mixamo.hand_retarget import build_hand_mapping, load_hand_motion
from .human_motion import HumanMotion, foot_contact_from_cache, load_human_motion
from .mixamo.animation import build_animation
from .mixamo.gltf import write_glb
from .mixamo.kinematics import quat_wxyz
from .mixamo.retarget import verify_rest_fk
from .mixamo.skinned_mesh import load_character_asset, rest_skin_error
from .mixamo.tpose_calibration import load_calibration
from .mixamo.ybot_retarget import build_mapping
from .progress import ProgressWriter
from .run_report import write_failed_report, write_run_json
from .videos import render_run_images, render_run_videos

ROTATION_CONVENTION = (
    "Animation-channel rotations are rest-relative deltas: M_local = T_bind * R_bind * R_anim, "
    "world = parent @ local. Quaternions are wxyz. Bind transforms prefer FBX Pose / "
    "Cluster.TransformLink matrices, then fall back to local TRS."
)


def save_mixamo_rotations(
    anim, mapping, rig_path: Path, out_npz: Path, *, extra_bones: list[str] | None = None
) -> Path:
    """Per-bone animation rotations, both the portable Mixamo Skeleton channel
    and the channel already converted for this rig file."""
    bones = list(mapping.controlled)
    for name in extra_bones or []:
        if name not in bones:
            bones.append(name)
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
    video: Path | None,
    rig: Path,
    *,
    image: Path | None = None,
    device: str = "cpu",
    extractor: str = DEFAULT_EXTRACTOR,
    detect_hands: bool = False,
    hand_smooth_s: float = 0.08,
    skeleton_npz: Path | None = None,
    verbose: bool = True,
    output_dir: Path | None = None,
    progress: ProgressWriter | None = None,
    progress_jsonl: Path | None = None,
    no_preview: bool = False,
    foot_lock: bool = True,
) -> Path:
    """Full pipeline for one video or still + one rig. Returns the run directory.

    `extractor` chooses which method writes skeleton_motion.npz. `skeleton_npz`
    reuses a previous run's file and skips extraction entirely. A still is
    handed to the extractor as-is; GVHMR turns it into a short hold clip.

    `output_dir` writes this run into a caller-chosen folder (used by the
    Blender extension). When omitted, a timestamped directory is created.
    `no_preview` still writes the NPZ/GLB products but skips rendered previews.
    `foot_lock` pins planted feet using GVHMR's foot contact (when available).
    """
    if image is None and video is None:
        raise ValueError("run_pipeline needs a video or an image")
    if image is not None:
        image = Path(image).resolve()
    if video is not None:
        video = Path(video).resolve()
    rig = Path(rig).resolve()
    started = datetime.now()
    t0 = time.time()
    source = image if image is not None else video
    assert source is not None
    if output_dir is not None:
        run_dir = Path(output_dir).resolve()
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        run_dir = paths.new_run_dir(source, started)
    print(f"run directory  {run_dir}")

    writer = progress if progress is not None else ProgressWriter(progress_jsonl)
    stage = "extract"
    try:
        writer.emit("extract", 0.15, "Extracting human motion")
        extract_video = video
        motion_npz = run_dir / "skeleton_motion.npz"
        if skeleton_npz is not None:
            import shutil

            shutil.copy2(skeleton_npz, motion_npz)
            print(f"reusing skeleton from {skeleton_npz}")
        else:
            if image is not None:
                print(f"extracting human pose from {image.name}")
            else:
                assert video is not None
                print(f"extracting human motion from {video.name}")
            get_extractor(extractor).extract(
                source,
                motion_npz,
                work_dir=run_dir / "cache",
                device=device,
                verbose=verbose,
                detect_hands=detect_hands,
            )
        if detect_hands and skeleton_npz is not None and not skeleton_has_hands(motion_npz):
            cache_dir = find_body_cache(Path(skeleton_npz).parent)
            if cache_dir is None:
                raise FileNotFoundError(
                    "hand detection needs the body cache next to the reused skeleton "
                    "(cache/*/0_input_video.mp4, vitpose.pt, bbx.pt)"
                )
            print("detecting hands on the reused skeleton")
            detect_and_append(
                cache_dir,
                motion_npz,
                load_human_motion(motion_npz).n_frames,
                device=device,
                verbose=verbose,
                single_frame=image is not None or skeleton_from_still(motion_npz),
            )
        motion: HumanMotion = load_human_motion(motion_npz)
        if motion.foot_contact is None and skeleton_npz is not None:
            motion.foot_contact = foot_contact_from_cache(Path(skeleton_npz), motion.n_frames)
        print(f"human motion   {motion.n_frames} frames @ {motion.fps:g} fps")

        stage = "retarget"
        writer.emit("retarget", 0.70, "Retargeting animation")
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
        hands = load_hand_motion(motion_npz, smooth_s=hand_smooth_s)
        hand_mapping = None
        if hands is not None:
            hand_mapping = build_hand_mapping(asset.rig, hands.template_joints, verbose=verbose)
        anim = build_animation(
            motion,
            mapping,
            frames,
            verbose=verbose,
            foot_lock=foot_lock,
            asset=asset,
            hands=hands,
            hand_mapping=hand_mapping,
        )

        rotations_npz = run_dir / "mixamo_rotations.npz"
        save_mixamo_rotations(
            anim,
            mapping,
            rig,
            rotations_npz,
            extra_bones=list(hand_mapping.bones) if hand_mapping is not None else None,
        )
        print(f"saved {rotations_npz}")

        stage = "export"
        writer.emit("export", 0.85, "Writing GLB")
        glb_path = run_dir / "mixamo_character.glb"
        write_glb(glb_path, asset, anim.r_anim_rig, anim.hips_cm_rig, anim.fps)
        print(f"saved {glb_path}")

        outputs = {
            "skeleton_motion": motion_npz.name,
            "mixamo_rotations": rotations_npz.name,
            "mixamo_character_glb": glb_path.name,
        }

        # Diagnostics are a report, not a product: a failure here must not fail the run.
        print("diagnosing self-intersection")
        diagnostics = None
        try:
            diag = diagnose_run(run_dir, verbose=False)
            diagnostics = diag["summary"]
            outputs["diagnostics"] = DIAGNOSTICS_JSON
            print(summary_line(diag))
        except Exception as exc:  # noqa: BLE001
            print(f"diagnostics skipped: {exc}")

        if not no_preview:
            stage = "preview"
            writer.emit("preview", 0.90, "Rendering previews")
            if image is not None:
                print("rendering result images")
                previews = render_run_images(
                    anim, asset, calibration, image, run_dir / "images", verbose=verbose
                )
                outputs["images"] = {k: f"images/{v.name}" for k, v in previews.items()}
            else:
                print("rendering result videos")
                assert extract_video is not None
                previews = render_run_videos(
                    anim,
                    asset,
                    calibration,
                    extract_video,
                    run_dir / "videos",
                    original_label="Original Video",
                    verbose=verbose,
                )
                outputs["videos"] = {k: f"videos/{v.name}" for k, v in previews.items()}

        report = {
            "status": "completed",
            "started": started.isoformat(timespec="seconds"),
            "elapsed_s": round(time.time() - t0, 1),
            "command": sys.argv,
            "video": None if image is not None else str(video),
            "image": str(image) if image is not None else None,
            "rig": str(rig),
            "device": device,
            "extractor": (
                read_extractor_name(motion_npz) if skeleton_npz is not None else extractor
            ),
            "hands": read_hands_name(motion_npz),
            "hand_smooth_s": hand_smooth_s if hands is not None else None,
            "finger_bones": 0 if hand_mapping is None else len(hand_mapping.bones),
            "fps": float(motion.fps),
            "n_frames": motion.n_frames,
            "skeleton_reused_from": str(skeleton_npz) if skeleton_npz else None,
            "rest_fk_error": rest_err,
            "rest_skin_error_cm": skin_err,
            "twist_events": len(anim.twist_events),
            "quat_sign_flips": len(anim.sign_events),
            "foot_lock": anim.foot_lock,
            "ground": anim.ground,
            "diagnostics": diagnostics,
            "outputs": outputs,
        }
        write_run_json(run_dir, report)
        writer.emit("done", 1.0, "Completed")
        print(f"done in {report['elapsed_s']}s  ->  {run_dir}")
        return run_dir
    except Exception as exc:
        error_code, message = classify_error(exc)
        write_failed_report(run_dir, stage=stage, error_code=error_code, message=message)
        writer.emit("failed", _failed_progress(stage), message)
        raise


def _failed_progress(stage: str) -> float:
    return {
        "preflight": 0.05,
        "extract": 0.15,
        "retarget": 0.70,
        "export": 0.85,
        "preview": 0.90,
    }.get(stage, 0.0)
