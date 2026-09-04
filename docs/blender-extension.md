# Blender Extension (maintainer notes)

User install and usage: [`blender_extension/README.md`](../blender_extension/README.md).

This page is the smoke-test checklist and the v0.1 out-of-scope list.

## Manual smoke-test checklist

### macOS (Apple Silicon)

1. Create `.venv`, install Motion2MixamoRig, place SMPL-X.
2. `python scripts/package_blender_extension.py`
3. Install the zip in Blender 4.2+ and enable the add-on.
4. Confirm the **Motion2MixamoRig** tab in the 3D Viewport N-panel.
5. Set External Python to `.venv/bin/python` and Project Directory to the repo.
6. Quit Blender, reopen a different `.blend`, and confirm the two paths remain.
7. **Check Environment** → Ready (or a clear Error).
8. Pick a single-person still, a Mixamo FBX, Device **MPS** (or CPU).
9. Generate with preview off. The UI must stay usable (orbit the viewport).
10. Confirm stage/progress/log update, then auto-import of the GLB.
11. Timeline start is 1; end matches `n_frames` in `run.json`; FPS matches.
12. **Open Output Folder** and **View Full Log** work.
13. Start a second job and click **Cancel**. Only that job should stop.
14. Disable and re-enable the add-on without a crash.

### Windows 10/11

1. Same venv install; External Python is `.venv\Scripts\python.exe`.
2. Install the zip; confirm the N-panel tab.
3. Paths with spaces (`C:\Users\Jane Doe\...`) must work for Python, video, and FBX.
4. **Check Environment**.
5. Run a short single-person video on **CPU** first; try **CUDA** only if that
   PyTorch build is installed.
6. Blender must not freeze during Generate.
7. Confirm auto-import, FPS, and frame range.
8. **Open Output Folder** uses Explorer; **View Full Log** opens the log.
9. Cancel a running job; no other `python.exe` processes should be killed.
10. Uninstall the add-on and confirm `weights/` and `outputs/` are still there.

## Future work

Not in v0.1:

- Automatic Python / PyTorch / GVHMR install
- Automatic SMPL-X download
- Bundling weights inside the extension
- Cloud inference
- Multi-person video
- Writing `mixamo_rotations.npz` onto the current Armature
- Foot lock, root-motion editor, curve cleanup, NLA tools
- Publishing to the Blender Extensions Platform
