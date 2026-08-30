# AGENTS.md

Motion2MixamoRig drives an Adobe Mixamo-rigged 3D character with human motion
extracted from a monocular video. CLI: `m2mr`.

## Setup

```bash
# chumpy (legacy dep of gvhmr) breaks under PEP 517 build isolation
# ("No module named 'pip'"); install it without isolation first.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Three things must be supplied by the user (all git-ignored, licensing-gated):

| What | Where to put it | Source |
| --- | --- | --- |
| SMPL-X body model | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | https://smpl-x.is.tue.mpg.de/ (registration) |
| Mixamo character | `assets/mixamo/<Name>.fbx` (FBX Binary, T-pose) | https://www.mixamo.com/ (Adobe account) |
| Input video | `assets/video/<name>.mp4` | one clearly visible person (group shots fail preflight) |

Inference weights (~5 GB) auto-download into `weights/` on the first run.

## Commands

```bash
m2mr doctor        # verify assets + dependencies; prints what is missing and where to get it
m2mr run           # latest video in assets/video/ + assets/mixamo/Y_Bot.fbx
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
m2mr run --skeleton outputs/<run>/skeleton_motion.npz --rig ...   # reuse extraction, swap rig
```

`--video` and `--rig` combine freely. Extraction is the slow step; reuse it
with `--skeleton` when only the rig changes.

## Outputs

Each run writes `outputs/<YYYYMMDD_HHMMSS>_<video>/`:

- `run.json` — inputs, timings, output listing
- `skeleton_motion.npz` — 3D human skeleton (24 SMPL joints, Y-up meters)
- `mixamo_rotations.npz` — per-bone animation rotations (quaternion wxyz; convention string inside)
- `mixamo_character.glb` — skinned character + clip (glTF 2.0; Blender: File → Import → glTF 2.0)
- `videos/human_skeleton.mp4`, `videos/mixamo_skeleton.mp4`, `videos/mixamo_character.mp4`, `videos/compare.mp4` (2x2: original / mixamo skeleton / human skeleton / character)

## Code map

- `motion2mixamorig/paths.py` — all filesystem locations
- `motion2mixamorig/extract.py` — video -> 3D human skeleton (GVHMR)
- `motion2mixamorig/mixamo/` — FBX parsing, FK, retargeting, skinning, rendering
- `motion2mixamorig/pipeline.py` — one run end to end
- `motion2mixamorig/cli.py` — `m2mr doctor` / `m2mr run`
