"""The `m2mr` command-line entry point: doctor / run.

    m2mr doctor                 check assets, weights and dependencies
    m2mr run                    latest video in assets/video/ + default Y Bot
    m2mr run --video V --rig R  pick the inputs explicitly (flags combine freely)

`m2mr run` performs the same asset checks as `m2mr doctor` before doing any
work, and reports everything that is missing in one pass.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import checks, paths

OK = "[ok]     "
MISS = "[missing]"
BAD = "[invalid]"

SMPLX_HINT = (
    "register at https://smpl-x.is.tue.mpg.de/ , download SMPLX_NEUTRAL.npz, "
    "place it at assets/body_models/smplx/SMPLX_NEUTRAL.npz"
)
RIG_HINT = (
    "download a character from https://www.mixamo.com/ (FBX Binary, T-pose) "
    "into assets/mixamo/ , e.g. Y_Bot.fbx"
)
VIDEO_HINT = (
    "put a *single-person* motion video (.mp4/.mov/...) into assets/video/ "
    "— group shots are rejected before extraction"
)


def _check(label: str, present: bool, hint: str) -> bool:
    print(f"{OK if present else MISS} {label}")
    if not present:
        print(f"          -> {hint}")
    return present


def _check_content(label: str, path: Path, checker) -> bool:
    """Existence is assumed; `checker` inspects the file and returns a hint or None."""
    problem = checker(path)
    print(f"{OK if problem is None else BAD} {label}")
    if problem is not None:
        print(f"          -> {path.name} {problem}")
    return problem is None


def _module_available(name: str) -> bool:
    import importlib.util

    return importlib.util.find_spec(name) is not None


def _available_rigs() -> list[Path]:
    return sorted(paths.MIXAMO_DIR.glob("*.fbx")) if paths.MIXAMO_DIR.is_dir() else []


def doctor() -> int:
    """Check every user-supplied asset and dependency; say where to get what's missing."""
    print(f"project root: {paths.PROJECT_ROOT}\n")

    ok = True
    smplx_label = f"SMPL-X body model  {paths.SMPLX_NEUTRAL.relative_to(paths.PROJECT_ROOT)}"
    if paths.SMPLX_NEUTRAL.exists():
        ok &= _check_content(smplx_label, paths.SMPLX_NEUTRAL, checks.check_smplx)
    else:
        ok &= _check(smplx_label, False, SMPLX_HINT)
    rigs = _available_rigs()
    ok &= _check(
        f"Mixamo rig .fbx    assets/mixamo/  ({len(rigs)} found"
        + (f": {', '.join(r.name for r in rigs[:5])})" if rigs else ")"),
        bool(rigs),
        RIG_HINT,
    )
    for rig in rigs:
        ok &= _check_content(f"  - {rig.name}", rig, checks.check_rig)
    videos = paths.list_videos()
    ok &= _check(
        f"input video        assets/video/  ({len(videos)} found"
        + (f", latest: {videos[0].name})" if videos else ")"),
        bool(videos),
        VIDEO_HINT,
    )
    for video in videos:
        ok &= _check_content(f"  - {video.name}", video, checks.check_video)

    print()
    deps_ok = True
    for module, hint in (
        ("numpy", "pip install -e ."),
        ("cv2", "pip install -e ."),
        ("torch", "pip install -e ."),
        ("gvhmr", "pip install -e ."),
    ):
        deps_ok &= _check(f"python module      {module}", _module_available(module), hint)
    import shutil as _shutil

    _check(
        "ffmpeg (optional)  H.264 output with the source video's audio",
        _shutil.which("ffmpeg") is not None,
        "brew install ffmpeg / apt install ffmpeg — runs fine without, but videos are silent mp4v",
    )

    weights_note = (
        "downloaded automatically into weights/ on the first `m2mr run` (~5 GB)"
    )
    print(f"\ninference weights: {weights_note}")

    if ok and deps_ok:
        print("\neverything in place — try: m2mr run")
        return 0
    print("\nfix the [missing] items above, then re-run: m2mr doctor")
    return 1


def preflight(args: argparse.Namespace) -> tuple[Path, Path, Path | None]:
    """Resolve run inputs, checking everything doctor checks for this run.

    All problems are collected and reported together (same format as doctor)
    instead of failing on the first one. Exits with code 1 if anything is
    missing.
    """
    problems = 0

    def check(label: str, present: bool, hint: str) -> bool:
        nonlocal problems
        if not _check(label, present, hint):
            problems += 1
        return present

    def check_content(label: str, path: Path | None, checker) -> None:
        """Inspect the file's contents, but only when it exists at all."""
        nonlocal problems
        if path is not None and path.exists() and not _check_content(label, path, checker):
            problems += 1

    # Input video: --video wins, else the most recently added file in assets/video/.
    if args.video:
        video = Path(args.video)
        check(f"input video        {video}", video.exists(), "check the --video path")
    else:
        video = paths.latest_video()
        check(
            "input video        assets/video/"
            + (f"  (latest: {video.name})" if video else "  (0 found)"),
            video is not None,
            VIDEO_HINT + ", or pass --video",
        )
    check_content(f"video is usable    {video.name if video else ''}", video, checks.check_video)

    # Rig: --rig wins, else Y_Bot.fbx, else the first .fbx in assets/mixamo/.
    if args.rig:
        rig = Path(args.rig)
        check(f"Mixamo rig .fbx    {rig}", rig.exists(), "check the --rig path")
    else:
        rig = paths.DEFAULT_RIG
        if not rig.exists():
            rigs = _available_rigs()
            rig = rigs[0] if rigs else None
        check(
            "Mixamo rig .fbx    " + (str(rig) if rig else "assets/mixamo/  (0 found)"),
            rig is not None,
            RIG_HINT + ", or pass --rig",
        )
    check_content(f"rig is Mixamo      {rig.name if rig else ''}", rig, checks.check_rig)

    # Skeleton reuse skips extraction; only then is SMPL-X not needed.
    skeleton = Path(args.skeleton) if args.skeleton else None
    if skeleton is not None:
        check(
            f"skeleton npz       {skeleton}",
            skeleton.exists(),
            "check the --skeleton path (a previous run's skeleton_motion.npz)",
        )
        check_content(f"skeleton loads     {skeleton.name}", skeleton, checks.check_skeleton_npz)
    else:
        check(
            f"SMPL-X body model  {paths.SMPLX_NEUTRAL.relative_to(paths.PROJECT_ROOT)}",
            paths.SMPLX_NEUTRAL.exists(),
            SMPLX_HINT,
        )
        check_content(
            "SMPL-X loads       SMPLX_NEUTRAL.npz", paths.SMPLX_NEUTRAL, checks.check_smplx
        )

    if problems:
        print(f"\n{problems} problem(s) — nothing was run. `m2mr doctor` checks everything.")
        sys.exit(1)
    return video, rig, skeleton


def run(args: argparse.Namespace) -> int:
    video, rig, skeleton = preflight(args)
    print()

    from .pipeline import run_pipeline

    run_dir = run_pipeline(video, rig, device=args.device, skeleton_npz=skeleton)
    print(f"\nresults: {run_dir / 'videos'}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="m2mr",
        description="Drive a Mixamo-rigged character with human motion from a video.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="check assets, weights and dependencies")

    p_run = sub.add_parser("run", help="video -> Mixamo rig, results in outputs/")
    p_run.add_argument(
        "--video",
        help="input video (default: the file most recently added to assets/video/)",
    )
    p_run.add_argument(
        "--rig",
        help="Mixamo character .fbx (default: assets/mixamo/Y_Bot.fbx)",
    )
    p_run.add_argument(
        "--skeleton",
        help="reuse a previous run's skeleton_motion.npz and skip video extraction",
    )
    p_run.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda", "mps"],
        help="inference device for the extraction step (default: cpu)",
    )

    args = parser.parse_args()
    if args.command == "doctor":
        sys.exit(doctor())
    sys.exit(run(args))
