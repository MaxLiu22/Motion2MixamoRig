# Motion2MixamoRig

![Motion2MixamoRig](repo_poster.png)

<p align="center">
  <a href="README.zh-CN.md">中文</a> · English
</p>

Transfer the motion of a person in a video onto an Adobe Mixamo-rigged 3D character.

For game developers: give it a **single-person** action video and a Mixamo character; it writes preview videos plus a skinned character file (`.glb`) you can drop into Blender or Unity.

Agents should start with [`AGENTS.md`](AGENTS.md).

## Prerequisites

Python 3.10+. After cloning, create a virtualenv and install dependencies; the `m2mr` command is then available:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Install dependencies and this project. chumpy (a legacy package on the
# dependency chain) imports pip in its setup script, which fails with
# "No module named 'pip'" under pip's default isolated build. Install it
# first with isolation turned off, then install this project.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Inference weights (GVHMR and so on) are not downloaded here. The first `m2mr run` pulls them into `weights/` (~5 GB, once only).

ffmpeg is recommended (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
The pipeline runs without it, but the output videos will be **silent** and will not play in a browser.

## Before you run: put three things in `assets/`

This repository does not ship these files; you have to fetch them. The SMPL-X filename must match the table exactly; FBX and video names can be anything.

| What | Where | Where to get it |
|---|---|---|
| SMPL-X body model | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Register at [SMPL-X](https://smpl-x.is.tue.mpg.de/) and download it |
| Mixamo character FBX | `assets/mixamo/Y_Bot.fbx` | With an Adobe account, download Y Bot (or any other Mixamo-rigged character) from [Mixamo](https://www.mixamo.com) |
| Action video | `assets/video/<your_clip>.mp4` | A clip with **exactly one** clearly visible person (you may keep several files; each run uses one) |

Note: Mixamo's download is named `Y Bot.fbx` (**space**), one character off from `Y_Bot.fbx` (**underscore**) in the table.
Rename it to the underscore form and it becomes the default rig (`m2mr run` without `--rig`). Leaving the space is fine too — if `Y_Bot.fbx` is missing, the first `.fbx` in `assets/mixamo/` is used.

`assets/video/` can hold several videos. Without `--video`, the run uses the file **most recently added** to that folder.
Each clip must show only one person: `m2mr doctor` / `m2mr run` sample the frames and stop before extraction if two people are in view.

## Quick Start

Results land in `outputs/<run-time>_<video>/`. Open that folder's `videos/` to watch them.

### 1. Check assets and the environment

Anything missing is printed with where to download it and where to put it.

```bash
m2mr doctor
```

### 2. First run: get something on screen

With no flags, this uses the **latest file in `assets/video/`** and `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

This is the slow step. The first run downloads ~5 GB of inference weights (once only), then extracts human motion from the video.
On CPU, a ~30 second clip takes about 8–15 minutes to extract; later runs of similar length, with weights already there, take about 3–5 minutes.
Retargeting and rendering are usually a minute or two. Reusing a skeleton with `--skeleton` in the next section skips extraction entirely and finishes in tens of seconds.

### 3. Same motion, different character

Download another character from Mixamo into `assets/mixamo/`. **Do not rerun with only `--rig`** — that repeats the slow extraction.
Pass `--skeleton` to reuse the skeleton from a previous run; minutes become tens of seconds:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. A different video

`--video` picks the clip. It combines freely with `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

## Outputs

Each `m2mr run` creates a directory named by **the time the command started**:

```
outputs/20260829_193205_dance/
├── run.json                    # start time, video / rig used, full command
├── skeleton_motion.npz         # 3D human skeleton (reuse when swapping rigs; no re-extract)
├── mixamo_rotations.npz        # per-bone Mixamo rotations
├── mixamo_character.glb        # skinned character + animation, import into Blender / Unity
└── videos/                     # same aspect ratio as the input
    ├── human_skeleton.mp4      # human skeleton
    ├── mixamo_skeleton.mp4     # Mixamo rig skeleton
    ├── mixamo_character.mp4    # Mixamo rig character
    └── compare.mp4             # 2×2: original (TL) / Mixamo skeleton (TR) / human skeleton (BL) / character (BR)
```

Open `mixamo_character.glb` in Blender: File → Import → glTF 2.0 (.glb/.gltf). If the camera is framed on empty space, select the character and use View → Frame Selected. The cluster of spheres on the head and hands is the bone display, not the mesh: select the armature and turn off Shapes under Armature → Viewport Display. Set the timeline end frame to the clip length, then play. Compare against `videos/mixamo_character.mp4` from the same run.

## License

This repository's code is Apache-2.0. The assets you download have their own terms and must not be redistributed with this repo:

- **SMPL-X**: MPI-gated; default non-commercial research / education / art; commercial use needs a separate deal
- **Mixamo FBX**: fine in a shipped product; do not redistribute the raw FBX as an asset pack
- **GVHMR and other inference weights**: auto-downloaded into `weights/` on the first `m2mr run`, under each upstream license

## Contact

If you run into a problem, need help finishing a local setup, or would like to talk about working together, email:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)
