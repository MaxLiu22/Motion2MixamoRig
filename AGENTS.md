# AGENTS.md

Motion2MixamoRig drives an Adobe Mixamo-rigged 3D character with human motion
extracted from a monocular video, or a static 3D pose from a still photo.
CLI: `m2mr`.

## Setup

```bash
# chumpy (legacy dep of gvhmr) breaks under PEP 517 build isolation
# ("No module named 'pip'"); install it without isolation first.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

These must be supplied by the user (all git-ignored, licensing-gated).
A run needs SMPL-X, a Mixamo character, and either a video or a still:

| What | Where to put it | Source |
| --- | --- | --- |
| SMPL-X body model | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | https://smpl-x.is.tue.mpg.de/ (registration) |
| Mixamo character | `assets/mixamo/<Name>.fbx` (FBX Binary, T-pose) | https://www.mixamo.com/ (Adobe account) |
| Input video | `assets/video/<name>.mp4` | one clearly visible person (group shots fail preflight) |
| Input still | `assets/image/<name>.jpg` | one clearly visible person, head to toe (optional; `--image`) |

Inference weights (~5 GB) auto-download into `weights/` on the first run.

## Commands

```bash
m2mr doctor        # verify assets + dependencies; prints what is missing and where to get it
m2mr run           # latest video in assets/video/ + assets/mixamo/Y_Bot.fbx
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Y_Bot.fbx
m2mr run --skeleton outputs/<run>/skeleton_motion.npz --rig ...   # reuse extraction, swap rig
m2mr run --output-dir DIR --progress-jsonl FILE --no-preview      # Blender Extension / automation
```

`--video` / `--image` and `--rig` combine freely (not `--video` with `--image`).
Extraction is the slow step; reuse it with `--skeleton` when only the rig changes.

## Blender Extension

The add-on is a thin UI. It must **not** import PyTorch / GVHMR / OpenCV in
Blender’s Python. It launches an external Python:

```text
<external-python> -m motion2mixamorig.cli run ...
```

That Python is either the **one-click runtime** the add-on installs into
`~/Motion2MixamoRig` (default; project directory `~/Motion2MixamoRig/app`), or
the user’s own venv set under **Advanced**.

- Non-programmers: [`docs/user-guide.md`](docs/user-guide.md) (release zip,
  one-click runtime, no terminal).
- Building from source / own venv:
  [`blender_extension/README.md`](blender_extension/README.md).

When helping a user:

1. One-click path: download the zip from the latest GitHub release, install
   it, click **Install Runtime (one click)**, then **Choose SMPL-X Model…**.
   Own-venv path: the same venv + SMPL-X + Mixamo FBX as the CLI (see Setup
   above).
2. Build `dist/motion2mixamorig-0.1.7-<platform>.zip` with
   `python scripts/package_blender_extension.py --platform macos-arm64` (one
   zip per platform; the platform is declared in the zip's manifest, the
   version is shared; the zip bundles `motion2mixamorig/` under `backend/`
   for the one-click runtime). Without `--platform`: a neutral test build.
3. In Blender 4.2+: **Edit → Preferences → Get Extensions**, then the **∨**
   next to Repositories → **Install from Disk…** (no large button). Enable it.
4. The panel is **3D Viewport → N sidebar → Motion2MixamoRig**, not Get
   Extensions. The **⚙** after the title shows / hides Setup. Setup: UI
   Language, Install / Update Runtime, Choose SMPL-X Model, Device,
   **Check Environment**; External Python and Project Directory are under
   **Advanced**.
5. After add-on **code** changes they must rebuild the zip and reinstall.
   The installed copy is not live from this repo. With the one-click runtime,
   changes to `motion2mixamorig/` also need **Update Runtime** (weights are
   kept). If `already registered` / `EnumProperty could not register`
   appears: disable, **quit Blender fully**, reopen, install again.
6. Jobs write `<project>/outputs/blender_jobs/<job-id>/`. After import, hide
   **Icosphere** and the **armature** in the Outliner; leave the
   **skinned_mesh_…** objects (one per FBX geometry) visible. FPS must match the source clip duration (a 60 fps video tagged as
   30 fps plays at half speed).

Smoke-test checklist: [`docs/blender-extension.md`](docs/blender-extension.md).

## Outputs

Each run writes `outputs/<YYYYMMDD_HHMMSS>_<source>/`:

- `run.json` — inputs, timings, output listing
- `skeleton_motion.npz` — 3D human skeleton (24 SMPL joints, Y-up meters)
- `mixamo_rotations.npz` — per-bone animation rotations (quaternion wxyz; convention string inside)
- `mixamo_character.glb` — skinned character + clip (glTF 2.0; Blender: File → Import → glTF 2.0)
- `diagnostics.json` — self-intersection report on the GLB (body-part pairs, frame ranges, depth in cm; frames = Blender frame numbers, first = 0). `m2mr diagnose <run> [--visualize] [--threshold-cm N]` re-checks a run; `--visualize` adds `diagnostics.html`. No floor check.
- Video in: `videos/human_skeleton.mp4`, `videos/mixamo_skeleton.mp4`, `videos/mixamo_character.mp4`, `videos/compare.mp4` (2x2: original / mixamo skeleton / human skeleton / character)
- Photo in: the same four views as PNG under `images/`, plus `images/before_after_360_compare.mp4` (left original / right 10° orbit of the rig)

## Code map

- `motion2mixamorig/paths.py` — all filesystem locations
- `motion2mixamorig/extract.py` — video or still -> 3D human skeleton (GVHMR)
- `motion2mixamorig/mixamo/` — FBX parsing, FK, retargeting, skinning, rendering
- `motion2mixamorig/pipeline.py` — one run end to end
- `motion2mixamorig/cli.py` — `m2mr doctor` / `m2mr run`
- `blender_extension/motion2mixamorig_blender/` — Blender 4.2+ Extension (UI + external process)
- `blender_extension/README.md` — build the add-on, one-click runtime internals, own-venv setup
- `docs/user-guide.md` — add-on guide for non-programmers
- `docs/blender-extension.md` — maintainer smoke-test checklist
- `docs/c4d-fbx-support.md` — how Cinema 4D-exported FBX rigs are read (bind-matrix rest pose, one GLB skin per mesh)
- `scripts/package_blender_extension.py` — build `dist/motion2mixamorig-0.1.7-<platform>.zip`
