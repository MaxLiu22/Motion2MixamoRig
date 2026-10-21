# Motion2MixamoRig

<p align="center">
  <a href="#prerequisites"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="docs/user-guide.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](docs/assets/repo_poster.png)

<p align="center">
  <a href="docs/i18n/README.zh-Hans.md">简体中文</a> · <a href="docs/i18n/README.zh-Hant.md">繁體中文</a> · English · <a href="docs/i18n/README.ko.md">한국어</a> · <a href="docs/i18n/README.ja.md">日本語</a> · <a href="docs/i18n/README.de.md">Deutsch</a> · <a href="docs/i18n/README.ru.md">Русский</a> · <a href="docs/i18n/README.ar.md">العربية</a> · <a href="docs/i18n/README.vi.md">Tiếng Việt</a> · <a href="docs/i18n/README.fil.md">Filipino</a> · <a href="docs/i18n/README.th.md">ไทย</a> · <a href="docs/i18n/README.fr.md">Français</a> · <a href="docs/i18n/README.es-MX.md">Español</a> · <a href="docs/i18n/README.tr.md">Türkçe</a> · <a href="docs/i18n/README.ne.md">नेपाली</a> · <a href="docs/i18n/README.id.md">Bahasa Indonesia</a> · <a href="docs/i18n/README.pl.md">Polski</a> · <a href="docs/i18n/README.nl.md">Nederlands</a>
</p>

Transfer the motion of a person in a video — or the pose in a still photo — onto an Adobe Mixamo-rigged 3D character.

For game developers: give it an action video (or a still) and a Mixamo character; it writes preview videos plus a skinned character file (`.glb`) you can drop into Blender or Unity. For group footage, the CLI can select a person with `--select-person`.

> Motion2MixamoRig is currently experimental. Version 0.1.7 is the command-line pipeline. This repository also includes a Blender 4.2+ Extension that runs that same pipeline in an external Python environment. Building the add-on from source: [`blender_extension/README.md`](blender_extension/README.md).

## Two ways to use it

### 🎨 In Blender — no coding

1. Download the zip for your platform, e.g. `motion2mixamorig-<version>-macos-arm64.zip`, from the [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. In Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, pick the zip.
3. 3D Viewport → press **N** → **Motion2MixamoRig** tab → **Install Runtime (one click)**.
4. **Choose SMPL-X Model…** (a free download) and pick a Mixamo character FBX.
5. Choose a video of one person → **Generate Motion**.

Step-by-step instructions, tips, and updating: **[User Guide](docs/user-guide.md)**. Tested on macOS (Apple Silicon).

### 💻 Command line — for developers

Clone the repository and run the pipeline yourself: start at [Prerequisites](#prerequisites).

Agents should start with [`AGENTS.md`](AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Open <a href="docs/assets/demo.mp4">demo.mp4</a> in this repository.</sub>
</p>

Another demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

## Prerequisites

Python 3.11+. After cloning, create a virtualenv and install dependencies; the `m2mr` command is then available:

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

## Before you run: put these in `assets/`

This repository does not ship these files; you have to fetch them. The SMPL-X filename must match the table exactly; FBX, video, and image names can be anything. A run needs SMPL-X, a Mixamo character, and **either** a video **or** a still. Mixamo characters re-exported from Cinema 4D also work; see [`docs/c4d-fbx-support.md`](docs/c4d-fbx-support.md).

| What | Where | Where to get it |
|---|---|---|
| SMPL-X body model | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Register at [SMPL-X](https://smpl-x.is.tue.mpg.de/) and download it |
| Mixamo character FBX | `assets/mixamo/Y_Bot.fbx` | With an Adobe account, download Y Bot (or any other Mixamo-rigged character) from [Mixamo](https://www.mixamo.com) |
| Action video | `assets/video/<your_clip>.mp4` | One clearly visible person, or choose a subject with `--select-person`. Full-body visibility is recommended. Each run uses the most recently added clip unless `--video` is given. |
| Pose still (optional) | `assets/image/<your_photo>.jpg` | Use with `--image`; choose a subject in a group with `--select-person`. Full-body visibility is recommended. |

Note: Mixamo's download is named `Y Bot.fbx` (**space**), one character off from `Y_Bot.fbx` (**underscore**) in the table.
Rename it to the underscore form and it becomes the default rig (`m2mr run` without `--rig`). Leaving the space is fine too — if `Y_Bot.fbx` is missing, the first `.fbx` in `assets/mixamo/` is used.

`assets/video/` can hold several videos. Without `--video` or `--image`, the run uses the file **most recently added** to `assets/video/`; if that folder is empty it falls back to the latest still in `assets/image/`.
Without explicit selection, `m2mr doctor` / `m2mr run` stop before extraction if two people are in view. Use the CLI's `--select-person` or `--person ID` to process a group shot. Keep the selected subject's full body visible for the best results; cropped or hidden limbs remain estimates.

## Quick Start

### Choose a person in a group shot

The CLI prototype can select a subject before pose extraction:

```bash
# Analyze all tracks and write numbered thumbnails; no 3D inference yet.
m2mr people --video group.mp4 --device mps

# Click a candidate, then press Enter to run on that person.
m2mr run --video group.mp4 --select-person --device mps

# Or use an ID from the gallery without opening a window.
m2mr run --video group.mp4 --person 2 --device mps
```

The same options work with `--image group.jpg`. Selection keeps the full input
frame and supplies the chosen person's boxes to GVHMR. It does not change the
3D estimator or reliably reconstruct body parts that are outside the image.
The Blender extension does not yet expose this picker. See
[`docs/person-selection.md`](docs/person-selection.md) for details.

Results land in `outputs/<run-time>_<source>/`. Video runs write `videos/`; still runs write `images/`.

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

### 5. A still photo (static pose)

`--image` recovers a **static 3D pose** from a photo of one person, then retargets it onto the Mixamo character the same way a video run does. Previews are four stills in `images/` (same views as the video run), plus a left/right orbit clip `before_after_360_compare.mp4`. Do not pass `--video` at the same time.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` with no path uses the file most recently added to `assets/image/`.

## Outputs

Each `m2mr run` creates a directory named by **the time the command started**. The four files at the root are the same for video and still; only the preview folder changes.

```
outputs/20260829_193205_dance/          # or …_pose/ for a still
├── run.json                            # start time, inputs, full command
├── skeleton_motion.npz                 # 3D human skeleton (reuse with --skeleton)
├── mixamo_rotations.npz                # per-bone Mixamo rotations
├── mixamo_character.glb                # skinned character, import into Blender / Unity
└── videos/   or   images/              # previews — which one depends on the input
```

**Video input** writes `videos/` (same aspect ratio as the clip):

```
videos/
├── human_skeleton.mp4                  # recovered 3D human skeleton
├── mixamo_skeleton.mp4                 # Mixamo rig skeleton
├── mixamo_character.mp4                # skinned Mixamo character
└── compare.mp4                         # 2×2: original (TL) / Mixamo skeleton (TR)
                                        #      human skeleton (BL) / character (BR)
```

**Still input** writes `images/` instead (same four views, plus a turntable):

```
images/
├── human_skeleton.png                  # recovered 3D human skeleton
├── mixamo_skeleton.png                 # Mixamo rig skeleton
├── mixamo_character.png                # skinned Mixamo character
├── compare.png                         # 2×2: original (TL) / Mixamo skeleton (TR)
│                                       #      human skeleton (BL) / character (BR)
└── before_after_360_compare.mp4        # left: original photo
                                        # right: 10° orbit of the rig (one full turn)
```

Open `mixamo_character.glb` in Blender: File → Import → glTF 2.0 (.glb/.gltf). If the camera is framed on empty space, select the character mesh and use View → Frame Selected. The cluster of spheres on the head and hands is bone display, not the mesh: in the Outliner, hide **Icosphere** and the **armature**; leave the skinned mesh visible. Set scene FPS and the timeline end frame from `run.json` (`fps`, `n_frames`) so playback matches the source. Compare a video run against `videos/mixamo_character.mp4`, a still run against `images/mixamo_character.png` or the orbit clip.

## License

This repository's code is Apache-2.0. The assets you download have their own terms and must not be redistributed with this repo:

- **SMPL-X**: MPI-gated; default non-commercial research / education / art; commercial use needs a separate deal
- **Mixamo FBX**: fine in a shipped product; do not redistribute the raw FBX as an asset pack
- **GVHMR and other inference weights**: auto-downloaded into `weights/` on the first `m2mr run`, under each upstream license

## Contact

If you run into a problem, need help finishing a local setup, or would like to talk about working together, email:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
