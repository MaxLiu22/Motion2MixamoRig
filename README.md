# Motion2MixamoRig

<p align="center">
  <a href="#prerequisites"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="docs/user-guide.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](docs/assets/repo_poster.png)

<p align="center">
  <a href="docs/i18n/README.zh-Hans.md">简体中文</a> · <a href="docs/i18n/README.zh-Hant.md">繁體中文</a> · English · <a href="docs/i18n/README.ko.md">한국어</a> · <a href="docs/i18n/README.ja.md">日本語</a> · <a href="docs/i18n/README.de.md">Deutsch</a> · <a href="docs/i18n/README.ru.md">Русский</a> · <a href="docs/i18n/README.ar.md">العربية</a> · <a href="docs/i18n/README.vi.md">Tiếng Việt</a> · <a href="docs/i18n/README.fil.md">Filipino</a> · <a href="docs/i18n/README.th.md">ไทย</a> · <a href="docs/i18n/README.fr.md">Français</a> · <a href="docs/i18n/README.es-MX.md">Español</a> · <a href="docs/i18n/README.tr.md">Türkçe</a> · <a href="docs/i18n/README.ne.md">नेपाली</a> · <a href="docs/i18n/README.id.md">Bahasa Indonesia</a> · <a href="docs/i18n/README.pl.md">Polski</a> · <a href="docs/i18n/README.nl.md">Nederlands</a> · <a href="docs/i18n/README.it.md">Italiano</a> · <a href="docs/i18n/README.pt-BR.md">Português (Brasil)</a> · <a href="docs/i18n/README.uk.md">Українська</a> · <a href="docs/i18n/README.cs.md">Čeština</a> · <a href="docs/i18n/README.hi.md">हिन्दी</a> · <a href="docs/i18n/README.sv.md">Svenska</a>
</p>

Transfer the motion of a person in a video — or the pose in a still photo — onto an Adobe Mixamo-rigged 3D character.

For game developers: give it a **single-person** action video (or a still) and a Mixamo character; it writes preview videos plus a skinned character file (`.glb`) you can drop into Blender or Unity.

> Motion2MixamoRig is currently experimental. Version 0.1.8 is the command-line pipeline. This repository also includes a Blender 4.2+ Extension that runs that same pipeline in an external Python environment. Building the add-on from source: [`blender_extension/README.md`](blender_extension/README.md).

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

Diagnostics report (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

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

Inference weights are not downloaded here. The first `m2mr run` pulls the GVHMR weights into `weights/` (~5 GB, once only). The first `m2mr run --detect-hands` also pulls the HaMeR hand weights into `weights/hamer/` (~2.7 GB, once only).

ffmpeg is recommended (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
The pipeline runs without it, but the output videos will be **silent** and will not play in a browser.

## Before you run: put these in `assets/`

This repository does not ship these files; you have to fetch them. The SMPL-X filename must match the table exactly; FBX, video, and image names can be anything. A run needs SMPL-X, a Mixamo character, and **either** a video **or** a still. Mixamo characters re-exported from Cinema 4D also work; see [`docs/c4d-fbx-support.md`](docs/c4d-fbx-support.md).

| What | Where | Where to get it |
|---|---|---|
| SMPL-X body model | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Register at [SMPL-X](https://smpl-x.is.tue.mpg.de/) and download it |
| Mixamo character FBX | `assets/mixamo/Y_Bot.fbx` | With an Adobe account, download Y Bot (or any other Mixamo-rigged character) from [Mixamo](https://www.mixamo.com) |
| Action video | `assets/video/<your_clip>.mp4` | A clip with **exactly one** clearly visible person, **head to toe in frame the whole time** (you may keep several files; each run uses the most recently added) |
| Pose still (optional) | `assets/image/<your_photo>.jpg` | A photo with **exactly one** clearly visible person, **head to toe in frame**. Use with `--image` |
| MANO right hand (only for `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Register at [MANO](https://mano.is.tue.mpg.de/) and download **Models & Code**. A body-only run does not need this file |

Note: Mixamo's download is named `Y Bot.fbx` (**space**), one character off from `Y_Bot.fbx` (**underscore**) in the table.
Rename it to the underscore form and it becomes the default rig (`m2mr run` without `--rig`). Leaving the space is fine too — if `Y_Bot.fbx` is missing, the first `.fbx` in `assets/mixamo/` is used.

`assets/video/` can hold several videos. Without `--video` or `--image`, the run uses the file **most recently added** to `assets/video/`; if that folder is empty it falls back to the latest still in `assets/image/`.
Each clip or photo must show only one person, **head to toe in frame** — nothing cropped at the edges. `m2mr doctor` / `m2mr run` stop before extraction if two people are in view.

## Quick Start

Results land in `outputs/<run-time>_<source>/`. Video runs write `videos/`; still runs write `images/`.

### 1. Check assets and the environment

Anything missing is printed with where to download it and where to put it.

```bash
m2mr doctor
```

`m2mr doctor` checks the body run. It does not require the MANO hand model. To check the extra file and Python packages used by finger detection:

```bash
m2mr doctor --detect-hands
```

### 2. First run: get something on screen

With no flags, this uses the **latest file in `assets/video/`** and `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

This is the slow step. The first run downloads ~5 GB of inference weights (once only), then extracts human motion from the video.
On CPU, a ~30 second clip takes about 8–15 minutes to extract; later runs of similar length, with weights already there, take about 3–5 minutes.
Retargeting and rendering are usually a minute or two. Reusing a skeleton with `--skeleton` in the next section skips extraction entirely and finishes in tens of seconds.

A planted foot is pinned by default: the ball when the ball is down, the heel only when the toes are up. If a straight leg cannot reach that point, the hips move. The sole is then set on the floor (y = 0). `--no-foot-lock` keeps the raw retarget, so the feet may slide; the sole is still set on the floor.

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

### 6. Check for self-intersection

Every run also checks the finished character for **self-intersection** — one body part going into another, like a hand inside the head — and writes `diagnostics.json`. The terminal prints one line, e.g. `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. The floor is not checked.

To re-check a run, or to see the problems:

```bash
m2mr diagnose outputs/<run>                  # rewrite diagnostics.json
m2mr diagnose outputs/<run> --visualize      # also diagnostics.html: source video beside the character, timeline, clickable issue list
m2mr diagnose outputs/<run> --threshold-cm 2 # report only penetrations deeper than 2 cm (default 1)
```

Each issue in `diagnostics.json` is a pair of body parts with the frame ranges where they intersect, the worst frame, and its depth. Frame numbers count from 0, as the Blender timeline does after a glTF import. Parts joined at a joint (upper arm and forearm, torso and thigh, …) are not compared: their skins overlap around the joint in any pose. `diagnostics.html` embeds the source video (needs `ffmpeg`) and loads three.js from a CDN, so its 3D view needs an internet connection. That view keeps fixed floor markers on y = 0 — a cross every 0.5 m, a larger one each metre, and a green cross at the origin — so you can judge whether the character is moving. The amber lane above the intersection tracks is for notes made by eye (drag a range, or In / Out). The Notes list on the right shows them; click a row to jump to it. **Download notes** saves those notes and the intersection list together. The file is named after the source video and records that video's path.

### 7. Fingers (`--detect-hands`)

A plain `m2mr run` moves the body and leaves the Mixamo finger bones at rest. `--detect-hands` turns on the hand model that travels with the body extractor. With the default extractor, GVHMR, that model is [HaMeR](https://github.com/geopavlakos/hamer). HaMeR crops the wrists from the person and the frames GVHMR already chose. It does not search the clip for a second person.

**This about doubles the runtime.** A clip that finishes in a few minutes without the flag takes about twice that long with `--detect-hands`, because the hand pass runs on top of the body extraction. On a long video, plan for that extra time before you start.

Place `MANO_RIGHT.pkl` as in the table above, then:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

The first `--detect-hands` run downloads the HaMeR weights into `weights/hamer/` (~2.7 GB, once). Finger rotations are written into `skeleton_motion.npz` and drive the 30 Mixamo finger bones on the skinned character. A wrist the body pass did not see clearly stays at rest for that hand.

`--hand-smooth` is how many seconds of smoothing to apply to those rotations. The default is `0.08`. `0` keeps the raw estimate. Smoothing runs whenever the skeleton file already contains hand motion, including a later run that only reuses that file.

Reusing a previous skeleton:

- The file already contains hand motion: `--skeleton` drives the fingers by itself. `--detect-hands` is not required again.
- It does not, but that run's body cache is still beside it (`cache/<clip>/0_input_video.mp4`, plus `preprocess/vitpose.pt` and `preprocess/bbx.pt`): `--skeleton ... --detect-hands` adds the fingers without extracting the body again.
- That cache is gone: run the video or still again with `--detect-hands`.

## Outputs

Each `m2mr run` creates a directory named by **the time the command started**. The files at the root are the same for video and still; only the preview folder changes.

```
outputs/20260829_193205_dance/          # or …_pose/ for a still
├── run.json                            # start time, inputs, full command
├── skeleton_motion.npz                 # 3D human skeleton (reuse with --skeleton)
├── mixamo_rotations.npz                # per-bone Mixamo rotations
├── mixamo_character.glb                # skinned character, import into Blender / Unity
├── diagnostics.json                    # self-intersection report (see Quick Start step 6)
├── diagnostics.html                    # only after `m2mr diagnose <run> --visualize`
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

With `--detect-hands`, `skeleton_motion.npz` also stores the finger rotations, and `mixamo_rotations.npz` / `mixamo_character.glb` include the 30 finger bones. Without that flag, and without hand motion already stored in a reused skeleton, those bones stay at rest.

Open `mixamo_character.glb` in Blender: File → Import → glTF 2.0 (.glb/.gltf). If the camera is framed on empty space, select the character mesh and use View → Frame Selected. The cluster of spheres on the head and hands is bone display, not the mesh: in the Outliner, hide **Icosphere** and the **armature**; leave the skinned mesh visible. Set scene FPS from `run.json` (`fps`) and the timeline to frames 0 to `n_frames` − 1 so playback matches the source and frame numbers match `diagnostics.json`. Compare a video run against `videos/mixamo_character.mp4`, a still run against `images/mixamo_character.png` or the orbit clip.

## License

This repository's code is Apache-2.0. The assets you download have their own terms and must not be redistributed with this repo:

- **SMPL-X**: MPI-gated; default non-commercial research / education / art; commercial use needs a separate deal
- **MANO** (only if you use `--detect-hands`): MPI-gated, same kind of download as SMPL-X; place `MANO_RIGHT.pkl` locally and do not redistribute it
- **Mixamo FBX**: fine in a shipped product; do not redistribute the raw FBX as an asset pack
- **GVHMR weights**: auto-downloaded into `weights/` on the first `m2mr run`, under the upstream license
- **HaMeR**: the inference code in this repository is MIT; the weights download into `weights/hamer/` on the first `m2mr run --detect-hands`, under the upstream release

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
