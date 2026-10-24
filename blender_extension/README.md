# Motion2MixamoRig Blender Extension

A Blender **4.2+** add-on that runs Motion2MixamoRig in a **separate Python**,
then imports the generated Mixamo character (`.glb`) into the scene.

> **Just want to use it?** Download the zip from the
> [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
> and follow the [User Guide](../docs/user-guide.md). This page is for building
> the add-on from source and for running it against your own Python.

Blender’s own interpreter never loads PyTorch, GVHMR, or OpenCV. The panel
launches:

```text
<external-python> -m motion2mixamorig.cli run ...
```

## Two ways to provide that Python

| | One-click runtime (default) | Your own venv (Advanced) |
| --- | --- | --- |
| Who | Anyone, no terminal | Developers working on this repo |
| Python | Downloaded by the add-on | Your `.venv` |
| Code it runs | The copy bundled in the add-on zip | Your checkout (`pip install -e .`) |
| Project directory | `~/Motion2MixamoRig/app` | This repository |
| Set up with | **Install Runtime (one click)** | **Advanced** → External Python / Project Directory |

### One-click runtime

**Install Runtime (one click)** runs `services/runtime_bootstrap.py` with
Blender’s bundled Python. It downloads [uv](https://github.com/astral-sh/uv),
which installs CPython 3.11 and the dependencies (~1.4 GB, including the
`chumpy` no-build-isolation step), then installs the Motion2MixamoRig code that
ships inside the zip:

```text
~/Motion2MixamoRig/
├── app/        Motion2MixamoRig code + assets/ weights/ outputs/
├── venv/       the Python the add-on runs
├── python/     uv-managed CPython
├── tools/      uv
├── cache/      uv download cache
├── logs/       setup.log
└── runtime.json
```

When it finishes, External Python and Project Directory are filled in for you.
**Choose SMPL-X Model…** copies `SMPLX_NEUTRAL.npz` into
`app/assets/body_models/smplx/`.

The first **Generate Motion** downloads ~5.6 GB of weights into
`app/weights/`; the panel shows the size, speed, and time left. Later runs
reuse them.

PyTorch comes from PyPI’s default build: MPS on Apple Silicon, CUDA on Linux,
**CPU only on Windows**. For CUDA on Windows, use your own venv.

Only tested on macOS (Apple Silicon) so far.

### Your own venv (Advanced)

Do this in a terminal. Details (venv, `chumpy`, SMPL-X, Mixamo FBX) are in the
[repository README](../README.md).

1. Clone this repo and install Motion2MixamoRig into a Python 3.11+ venv.
2. Put `SMPLX_NEUTRAL.npz` at `assets/body_models/smplx/`.
3. Confirm `python -m motion2mixamorig.cli doctor` in that venv.
4. In the panel, open **Advanced** and set:

| Field | What to put |
| --- | --- |
| **External Python** | The venv interpreter, **not** Blender’s Python |
| **Project Directory** | This repository (it has `assets/` and `weights/`) |

| Platform | External Python |
| --- | --- |
| macOS / Linux | `<project>/.venv/bin/python` |
| Windows | `<project>\.venv\Scripts\python.exe` |

Do not `source` or activate the venv from Blender. The add-on calls that
binary directly. External Python, Project Directory, and UI Language persist
across `.blend` files.

## Build and install the add-on

From the repository root:

```bash
python scripts/package_blender_extension.py --platform macos-arm64
```

That writes `dist/motion2mixamorig-0.1.8-macos-arm64.zip`. The version comes
from `version` in `blender_manifest.toml` and is the same on every platform;
the platform goes into the file name and into `platforms` in the zip’s copy of
the manifest, so Blender refuses to install it on another OS. The source
manifest has no `platforms` line.

- Platforms: `macos-arm64`, `macos-x64`, `windows-x64`, `windows-arm64`,
  `linux-x64`. Repeat `--platform` to build several zips at once.
- Without `--platform` you get a platform-neutral
  `dist/motion2mixamorig-0.1.8.zip` that installs anywhere. Use it for local
  testing only; releases ship per-platform zips.

The zip root is `blender_manifest.toml` + `__init__.py` (no wrapping folder),
plus `backend/` with the Motion2MixamoRig code that the one-click runtime
installs. Today the add-on code is identical across platforms; per-platform
zips leave room for platform-specific parts later.

In Blender 4.2+:

1. **Edit → Preferences → Get Extensions**
2. Next to **Repositories**, open the small **∨** menu → **Install from Disk…**
   (there is no large “Install from Disk” button)
3. Choose the zip and enable **Motion2MixamoRig**

Command line:

```bash
blender --command extension install-file --repo user_default --enable dist/motion2mixamorig-0.1.8-macos-arm64.zip
```

After you change the add-on code, rebuild the zip and install it again. The
copy Blender loaded is not live from this folder. If you changed
`motion2mixamorig/` and use the one-click runtime, also click
**Update Runtime**: reinstalling the add-on does not touch `~/Motion2MixamoRig`
(weights are kept).

The manifest declares the `network` permission, used by the one-click runtime
setup. An offline alert for `extensions.blender.org` is unrelated and can be
ignored.

## The panel

3D Viewport → **N** → **Motion2MixamoRig** tab. The **⚙** after the title
shows or hides **Setup**; Setup stays visible while the runtime installs.

- **Setup**: UI Language (19 languages; Auto follows Blender / the system),
  Install / Update Runtime, Choose SMPL-X Model, Device, **Check Environment**,
  and **Advanced** (External Python, Project Directory).
- **Input**: Source Type, Source File, Mixamo Rig FBX, **Body Model**,
  **Detect Hands** (off by default; on shows finger smoothing and
  **Choose MANO Hand Model…**), Generate Preview Videos, **Generate Motion**.
- **Progress / Result**: stage, a bar, the first-run download, recent log
  lines, and **Cancel** (only the process this add-on started). After a job,
  **Floor Markers** shows or hides the floor crosses added on import.

## Generate

In **Input**:

1. Source Type: Video or Image
2. Source File: **one** clearly visible person, head to toe
3. Mixamo Rig FBX
4. Leave **Detect Hands** off unless the fingers should move. Turning it on
   needs `MANO_RIGHT.pkl` via **Choose MANO Hand Model…** and about doubles
   the runtime. The first such run also downloads the HaMeR weights (~2.7 GB).
5. Leave **Generate Preview Videos** off unless you want extra renders
6. **Generate Motion**

Blender stays interactive. On success the add-on imports
`mixamo_character.glb` into a collection `M2MR_<source-name>`, hides the
joint-bubble objects, frames the visible mesh, and sets timeline FPS / start /
end from the clip. Import also adds a **Floor Markers** mesh on Blender's
floor (z = 0); the checkbox under Progress / Result shows or hides it.

If import fails, generation still succeeded: use **Import Generated Character**.
**Open Output Folder** and **View Full Log** are always available after a job.

Jobs write to:

```text
<project>/outputs/blender_jobs/<job-id>/
```

(`run.json`, `job.log`, `progress.jsonl`, NPZ files, and the GLB.) With the
one-click runtime, `<project>` is `~/Motion2MixamoRig/app`.

## After import

- If the camera looks at empty space: select the character → **View → Frame Selected**.
- The cluster of spheres on joints is bone display, not the mesh. In the
  Outliner, hide **Icosphere** and the **armature** (the row with pose /
  armature / mesh icons). Leave the **skinned_mesh_…** objects visible (one
  per FBX geometry, e.g. `skinned_mesh_0_Alpha_Surface`); they still deform.
- Playback speed follows the source clip’s duration (`fps` in `run.json`).

## Devices

| Device | When |
| --- | --- |
| **CPU** | Works everywhere. Slowest. Safest first try. |
| **MPS** | Apple Silicon, if PyTorch MPS works in External Python. |
| **CUDA** | NVIDIA GPU; drivers must match the PyTorch CUDA build. |

The add-on does not install GPU drivers. If CUDA or MPS is unavailable, the
external process fails; open the full log.

## Common errors

| Message | What to do |
| --- | --- |
| Runtime installation failed | Check the connection and retry; see `~/Motion2MixamoRig/logs/setup.log` |
| External Python not found | Install the runtime, or point Advanced at `.venv/bin/python` / `Scripts\python.exe` |
| Motion2MixamoRig package not installed | **Update Runtime**, or `pip install -e .` in your venv |
| SMPL-X model missing | **Choose SMPL-X Model…**, or put `SMPLX_NEUTRAL.npz` in `assets/body_models/smplx/` |
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

That does **not** delete `~/Motion2MixamoRig` (one-click runtime, ~7 GB with
weights and outputs) or, for your own venv, `<project>/weights/`, `assets/`,
and `outputs/`. Remove those folders yourself if you want them gone.

## Layout

```text
blender_extension/
├── README.md                          # this file
└── motion2mixamorig_blender/          # packed into the zip
    ├── blender_manifest.toml
    ├── __init__.py
    ├── i18n.py                        # en, zh-CN, ko, ja, de, ru, ar strings; loads locales/
    ├── locales/                       # the other languages (and newer ko/ja/de/ru/ar keys)
    ├── preferences.py
    ├── properties.py
    ├── panels/
    ├── operators/                     # run, cancel, import, runtime setup, SMPL-X
    └── services/                      # process launch, progress, runtime bootstrap, downloads
```

Packaging: `scripts/package_blender_extension.py`.
Maintainer smoke-tests: [`docs/blender-extension.md`](../docs/blender-extension.md).
