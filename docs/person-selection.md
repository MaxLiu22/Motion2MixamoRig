# Person selection prototype

## Scope

Implemented as one unit of work: select a tracked person without changing the 3D estimator.

- Add a candidate gallery for a video or still, with stable labels within a cached analysis.
- Accept an explicit person ID or a click in a native picker.
- Supply the selected track to GVHMR in full-image coordinates, preserving camera geometry.
- Keep source media and model files shared; keep selection and inference caches in the worktree.
- Verify two-person selection, identity gaps, stale caches, CLI validation, and a real extraction/retargeting run.

This changes subject selection only. It does not recover unseen limbs or replace GVHMR.

## Usage

```bash
python -m motion2mixamorig.cli people --video group.mp4 --device mps
python -m motion2mixamorig.cli run --video group.mp4 --select-person --device mps
python -m motion2mixamorig.cli run --image group.jpg --person 2 --device mps
```

Run these from the project root using its Python environment. In a worktree
that links an existing virtualenv, use `.venv/bin/python -m motion2mixamorig.cli`
so Python imports the worktree's code rather than the editable install's original
console entry point. No dependency installation or changes to GVHMR are required.

`people` writes `outputs/person_selection/<source-key>/people.json` and
`people-1.jpg` (additional pages when needed). The native picker shows six tracks
per page. Click a card and press Enter; N/P changes pages and Escape cancels.
`--person ID` uses the cached track without opening a window. IDs belong to that
source's analysis; a different clip or still can have different IDs.

## Tracking and cache behavior

- YOLO/BoT-SORT runs on GVHMR's staged 30fps video. Selection is by track ID,
  not the largest box or the person's order in each frame.
- The tracker can still swap IDs at crossings or fragment a subject into several
  tracks. Separate IDs are not joined automatically. The gallery shows observed
  frame coverage so fragmented tracks are visible before inference.
- Gaps of up to 15 frames are interpolated; short leading/trailing gaps hold the
  nearest box. Longer gaps stop with a trim/select-another-track message. Missing
  detections are not evidence that the model observed the pose.
- Selection caches are keyed by resolved source path, byte size and modification
  time. A replacement source gets a new cache. Delete its selection directory to
  deliberately re-run detection after changing the model or tracker settings.
- Each selected ID/source revision gets its own inference cache. A normal run
  uses the original cache path, preventing reuse of another person's features.
- `selected_person.npz` beside the selected inference cache contains full-frame
  boxes and an observed-frame mask. `skeleton_motion.npz` records the person ID and
  selection summary; `run.json` repeats that summary.
- Reusing a selected skeleton with `--skeleton` preserves its selection metadata
  and accepts a group source for preview. Do not combine reuse with selection flags.

The existing Blender extension is unchanged. It can import the exported GLB,
but initiating person selection currently requires the CLI.

## Verification

Regression command:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
```

Local verification includes a two-person test video made by placing mirrored
copies of an existing exercise clip side by side. Both people were tracked in
all 60 frames. Selecting ID 2 produced a finite `(60, 24, 3)` skeleton, Mixamo
rotation data, and an animated GLB at 30fps using the installed Apple Silicon
environment. A still from that scene also produced two candidate tracks. These
checks verify selection and export; they do not establish 3D pose accuracy or
performance on real people crossing or occluding one another.

The 11 regression tests pass. Additional local checks confirmed that the native
picker returns the chosen ID, a selected group still exports a 32-frame pose,
saved-skeleton reuse preserves person 2 while rendering previews, and a 60fps
source is staged to 210 frames at 30fps before track analysis. The unselected
group-shot guard still rejects the two-person fixture.
