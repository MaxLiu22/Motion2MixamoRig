# Blender Extension (maintainer notes)

User install and usage: [`docs/user-guide.md`](user-guide.md).
Building from source and the Advanced (own venv) setup:
[`blender_extension/README.md`](../blender_extension/README.md).

This page is the smoke-test checklist and the out-of-scope list.

## Manual smoke-test checklist

### macOS (Apple Silicon): one-click runtime

Run this on a clean user state: move `~/Motion2MixamoRig` aside first
(`mv ~/Motion2MixamoRig ~/Motion2MixamoRig.bak`) and restore it afterwards.

1. `python scripts/package_blender_extension.py --platform macos-arm64`
2. Install the zip in Blender 4.2+ and enable the add-on; the version in
   **Get Extensions** matches the zip name.
3. Confirm the **Motion2MixamoRig** tab in the 3D Viewport N-panel.
4. Click **⚙** after the title: Setup hides and shows again.
5. **Install Runtime (one click)**: the bar advances and ends with
   "Runtime installed"; External Python and Project Directory (under
   **Advanced**) are filled in.
6. **Choose SMPL-X Model…** → "SMPL-X model: found".
7. **Check Environment** → Ready.
8. The first-run notice shows above **Generate Motion**.
9. Generate a short single-person video on CPU: the download box shows size,
   speed, and time left, then disappears; the job finishes and the GLB is
   auto-imported.
10. Generate again: no download box, no first-run notice.
11. Reinstall the zip, click **Update Runtime**: it finishes without
    re-downloading the weights.
12. Switch **UI Language** to a few languages, including ไทย, नेपाली, and
    العربية, and check that the text renders.
13. **Detect Hands** is off. Turning it on shows the twice-as-long note,
    finger smoothing, and **Choose MANO Hand Model…**.
14. After import, a **Floor Markers** mesh sits on the floor. The checkbox
    under Progress / Result hides it and shows it again.

### macOS (Apple Silicon): own venv

1. Create `.venv`, install Motion2MixamoRig, place SMPL-X.
2. Install the zip and enable the add-on.
3. Under **Advanced**, set External Python to `.venv/bin/python` and Project
   Directory to the repo.
4. Quit Blender, reopen a different `.blend`, and confirm the two paths remain.
5. **Check Environment** → Ready (or a clear Error).
6. Pick a single-person still, a Mixamo FBX, Device **MPS** (or CPU).
7. Generate with preview off. The UI must stay usable (orbit the viewport).
8. Confirm stage/progress/log update, then auto-import of the GLB.
9. Timeline start is 0; end is `n_frames` − 1 from `run.json`; FPS matches.
10. **Open Output Folder** and **View Full Log** work.
11. **Diagnostics** box: red cells match `diagnostics.json`; clicking a cell,
    **Previous** and **Next** move the playhead; during playback the triangle
    stays under the current cell. **Open HTML Report** builds the report on the
    first click (Blender opened from the Dock, so the source video is embedded
    via Homebrew `ffmpeg`) and opens it at once on the second. The report's
    3D view shows fixed 0.5 m floor crosses. The amber lane above the
    intersection tracks takes a dragged range or In / Out. The Notes list on
    the right shows those notes, and **Download notes** saves them with the
    intersection list.
12. Start a second job and click **Cancel**. Only that job should stop.
13. Disable and re-enable the add-on without a crash.

### Windows 10/11 (not tested yet)

Build with `--platform windows-x64`. Known blocker for the one-click runtime:
`cython-bbox` (pulled in by `gvhmr[preproc]`, unused at runtime) has no
Windows wheel and needs a C compiler.

1. One-click runtime: **Install Runtime** works, including paths with spaces
   (`C:\Users\Jane Doe\...`).
2. Own venv: External Python is `.venv\Scripts\python.exe`.
3. **Check Environment**.
4. Run a short single-person video on **CPU** first; the one-click runtime has a
   CPU-only PyTorch, so try **CUDA** only with your own venv.
5. Blender must not freeze during Generate.
6. Confirm auto-import, FPS, and frame range.
7. **Open Output Folder** uses Explorer; **View Full Log** opens the log.
8. Cancel a running job; no other `python.exe` processes should be killed.
9. Uninstall the add-on and confirm `~/Motion2MixamoRig` (or the project's
   `weights/` and `outputs/`) is still there.

## Future work

Not done yet:

- Automatic SMPL-X download (its license requires each user to register)
- Bundling weights inside the extension
- CUDA PyTorch in the one-click runtime on Windows
- A mirror option for slow downloads
- Cloud inference
- Multi-person video
- Writing `mixamo_rotations.npz` onto the current Armature
- Foot lock, root-motion editor, curve cleanup, NLA tools
- Publishing to the Blender Extensions Platform
