# Motion2MixamoRig Blender Extension

A Blender **4.2+** add-on that runs Motion2MixamoRig in a **separate Python**,
then imports the generated Mixamo character (`.glb`) into the scene.

Blender’s own interpreter never loads PyTorch, GVHMR, or OpenCV. The panel
launches:

```text
<external-python> -m motion2mixamorig.cli run ...
```

This folder is the add-on source. It does **not** install Python, download
SMPL-X, or bundle inference weights.

## What you need first

Do this in a terminal, not inside Blender. Details (venv, `chumpy`, SMPL-X,
Mixamo FBX) are in the [repository README](../README.md).

1. Clone this repo and install Motion2MixamoRig into a Python 3.10+ venv.
2. Put `SMPLX_NEUTRAL.npz` at `assets/body_models/smplx/`.
3. Download a Mixamo character as **FBX Binary, T-pose**.
4. Confirm `python -m motion2mixamorig.cli doctor` in that venv.

The first successful extraction downloads **about 5 GB** of weights into
`<project>/weights/`. That happens in External Python, not in this add-on.

## Install the add-on

From the repository root:

```bash
python scripts/package_blender_extension.py
```

That writes `dist/motion2mixamorig-0.1.0.zip`. The zip root is
`blender_manifest.toml` + `__init__.py` (no wrapping folder).

In Blender 4.2+:

1. **Edit → Preferences → Get Extensions**
2. Next to **Repositories**, open the small **∨** menu → **Install from Disk…**
   (there is no large “Install from Disk” button)
3. Choose the zip and enable **Motion2MixamoRig**

Command line:

```bash
blender --command extension install-file --repo user_default --enable dist/motion2mixamorig-0.1.0.zip
```

After you change the add-on code, rebuild the zip and install it again. The
copy Blender loaded is not live from this folder.

An offline alert for `extensions.blender.org` is unrelated and can be ignored.

## Open the panel

Get Extensions only lists whether the add-on is installed. The working UI is
the 3D Viewport sidebar:

1. Go to the **3D Viewport**
2. Press **N** (or open the sidebar on the right)
3. Click the **Motion2MixamoRig** tab

That sidebar has **Setup**, **Input**, and **Progress / Result**.

## Setup

Set these in the Setup box, or under **Edit → Preferences → Add-ons → Motion2MixamoRig**:

| Field | What to put |
| --- | --- |
| **UI Language** | Auto follows Blender / the system, or pick a language (same set as the repo README) |
| **External Python** | The venv interpreter, **not** Blender’s Python |
| **Project Directory** | This repository (or the install that has `assets/` and `weights/`) |
| **Device** | CPU, CUDA, or MPS |

| Platform | External Python |
| --- | --- |
| macOS / Linux | `<project>/.venv/bin/python` |
| Windows | `<project>\.venv\Scripts\python.exe` |

Do not `source` or activate the venv from Blender. The add-on calls that
binary directly. External Python, Project Directory, and UI Language persist
across `.blend` files.

Click **Check Environment**. Missing default clips under `assets/video/` is
fine: you pick files in the panel.

## Generate

In **Input**:

1. Source Type: Video or Image
2. Source File: **one** clearly visible person, head to toe
3. Mixamo Rig FBX
4. Leave **Generate Preview Videos** off unless you want extra renders
5. **Generate Motion**

Blender stays interactive. **Progress / Result** shows stage, a bar, recent
log lines, and **Cancel** (only the process this add-on started).

On success the add-on imports `mixamo_character.glb` into a collection
`M2MR_<source-name>`, hides the joint-bubble objects, frames the visible mesh,
and sets timeline FPS / start / end from the clip.

If import fails, generation still succeeded: use **Import Generated Character**.
**Open Output Folder** and **View Full Log** are always available after a job.

Jobs write to:

```text
<project>/outputs/blender_jobs/<job-id>/
```

(`run.json`, `job.log`, `progress.jsonl`, NPZ files, and the GLB.)

## After import

- If the camera looks at empty space: select the character → **View → Frame Selected**.
- The cluster of spheres on joints is bone display, not the mesh. In the
  Outliner, hide **Icosphere** and the **armature** (the row with pose /
  armature / mesh icons). Leave **skinned_mesh** visible; it still deforms.
- Playback speed follows the source clip’s duration (`fps` in `run.json`). If a
  60 fps video is stored as 30 fps, it will play at half speed.

## Devices

| Device | When |
| --- | --- |
| **CPU** | Works everywhere. Slowest. Safest first try. |
| **MPS** | Apple Silicon, if PyTorch MPS works in External Python. |
| **CUDA** | Windows/Linux NVIDIA GPU; drivers must match the PyTorch CUDA build. |

The add-on does not install GPU drivers. If CUDA or MPS is unavailable, the
external process fails; open the full log.

## Common errors

| Message | What to do |
| --- | --- |
| External Python not found | Point Setup at `.venv/bin/python` or `Scripts\python.exe` |
| Motion2MixamoRig package not installed | In that interpreter: `pip install -e .` |
| SMPL-X model missing | Put `SMPLX_NEUTRAL.npz` in `assets/body_models/smplx/` |
| Mixamo FBX invalid | Re-download as **FBX Binary**, T-pose |
| Input contains multiple people | Use a single-person shot |
| CUDA / MPS unavailable | Switch Device to CPU, or install a matching PyTorch |
| Pipeline process exited unexpectedly | **View Full Log**; an empty log means the CLI did not start |
| Result GLB not found | Re-run; check `run.json` in the job folder |
| Generation succeeded, but automatic import failed | **Import Generated Character** |

The panel shows one short line. Full stdout/stderr is in `job.log`.

`register_class(...): already registered` after installing over an enabled
add-on: disable it, **quit Blender fully**, reopen, then install the zip again.

## Uninstall

**Edit → Preferences → Get Extensions** → remove **Motion2MixamoRig**.

That does **not** delete `<project>/weights/`, `assets/`, or `outputs/`
(including `outputs/blender_jobs/`). Remove those folders yourself if you want
them gone.

## Layout

```text
blender_extension/
├── README.md                          # this file
└── motion2mixamorig_blender/          # packed into the zip
    ├── blender_manifest.toml
    ├── __init__.py
    ├── i18n.py
    ├── preferences.py
    ├── panels/
    ├── operators/
    └── services/
```

Packaging: `scripts/package_blender_extension.py`.
Maintainer smoke-tests: [`docs/blender-extension.md`](../docs/blender-extension.md).
