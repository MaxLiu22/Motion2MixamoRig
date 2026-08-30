"""Video -> 3D human skeleton (GVHMR world-grounded motion recovery).

Produces skeleton_motion.npz with 24 SMPL joints per frame in a Y-up,
meter-scaled world, plus the root translation/orientation and fps.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .paths import export_gvhmr_env

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


def extract_motion(
    video: Path,
    output_npz: Path,
    *,
    work_dir: Path,
    device: str = "cpu",
    static_camera: bool = True,
    verbose: bool = True,
) -> Path:
    """Run GVHMR on `video` and save skeleton_motion.npz to `output_npz`.

    `work_dir` holds GVHMR's per-video intermediates (2D pose cache, 3D lift).
    Re-running with the same work_dir reuses the expensive passes.
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
    np.savez_compressed(
        output_npz,
        joints_3d=joints_3d,
        joint_names=np.array(SMPL_JOINT_NAMES),
        fps=np.float32(result.fps),
        timestamps=timestamps,
        root_translation=root_translation,
        root_orientation=root_orientation,
        camera=np.array(result.camera),
        video=np.array(str(video)),
    )
    if verbose:
        print(f"saved {output_npz}")
    return output_npz
