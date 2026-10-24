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
m2mr run --no-foot-lock ...                                        # keep the raw retarget (planted feet are pinned by default)
m2mr run --set-extractor gvhmr --detect-hands --hand-smooth 0.08  # HaMeR fingers; needs assets/body_models/mano/MANO_RIGHT.pkl
m2mr doctor --detect-hands                                         # also check the MANO file and HaMeR packages
m2mr diagnose outputs/<run> [--visualize] [--threshold-cm N]      # re-check self-intersection -> diagnostics.json (+ .html)
```

`--video` / `--image` and `--rig` combine freely (not `--video` with `--image`).
Extraction is the slow step; reuse it with `--skeleton` when only the rig changes.

## After a generation

When an agent finishes a motion for the user (`m2mr run`, or a Blender job), the message that says it is done also names the quality report. That file is `diagnostics.json` in the run directory: which body parts intersect, on which frames, and how deep. A failed check does not fail the run. If the file is missing, say so and offer `m2mr diagnose <run>`. If they want the picture, `m2mr diagnose <run> --visualize` writes `diagnostics.html`; in Blender, **Open HTML Report** does the same. Tell them they can open it if they want. Do not start a revision until they ask.

The same message can offer to mark the stretches that still look wrong. Do that with them through Review notes: the amber lane in `diagnostics.html`, or a `<video stem>_review.json` written from the frames they point out. They hand that JSON back with the character or the skeleton (`mixamo_character.glb`, `mixamo_rotations.npz`, `skeleton_motion.npz`). The agent then builds a new version of the Mixamo animation for those ranges only, in a new directory, and leaves the previous run untouched. Rotations stay quaternion wxyz, the convention string inside `mixamo_rotations.npz`. Import the new `mixamo_character.glb` into Blender for them to watch: hide **Icosphere** and the armature, leave the skinned meshes. Tell them where the new `diagnostics.json` is, the same way as the first report. Pairs with `also_in_rest_pose` already intersect before the motion starts; say that instead of posing those frames away.

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
2. Build `dist/motion2mixamorig-0.1.8-<platform>.zip` with
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
   **Advanced**. Input: **Body Model**, and **Detect Hands** (off by default;
   on shows finger smoothing and **Choose MANO Hand Model…**).
5. After add-on **code** changes they must rebuild the zip and reinstall.
   The installed copy is not live from this repo. With the one-click runtime,
   changes to `motion2mixamorig/` also need **Update Runtime** (weights are
   kept). If `already registered` / `EnumProperty could not register`
   appears: disable, **quit Blender fully**, reopen, install again.
6. Jobs write `<project>/outputs/blender_jobs/<job-id>/`. After import, hide
   **Icosphere** and the **armature** in the Outliner; leave the
   **skinned_mesh_…** objects (one per FBX geometry) visible. Import also
   adds a **Floor Markers** mesh on Blender's floor (z=0): 0.5 m crosses
   over the hips' travel, metre marks larger, origin green. The next import
   into that collection replaces it. The result panel's **Floor Markers**
   checkbox shows or hides that mesh. FPS must match the source clip duration (a 60 fps video tagged as
 30 fps plays at half speed). The timeline runs 0..n-1, the frames
 `diagnostics.json` uses; the **Diagnostics** box under Progress reads it
 (frame bar, Previous / Next, **Open HTML Report** builds `diagnostics.html`
 on first click).

Smoke-test checklist: [`docs/blender-extension.md`](docs/blender-extension.md).

## Outputs

Each run writes `outputs/<YYYYMMDD_HHMMSS>_<source>/`:

- `run.json` — inputs, timings, output listing
- `skeleton_motion.npz` — 3D human skeleton (24 SMPL joints, Y-up meters) + `foot_contact` (F, 4: left ankle, left foot, right ankle, right foot static probability from GVHMR; older runs read it from `cache/*/hmr4d_results.pt`)
- `mixamo_rotations.npz` — per-bone animation rotations (quaternion wxyz; convention string inside)
- `mixamo_character.glb` — skinned character + clip (glTF 2.0; Blender: File → Import → glTF 2.0)
- `diagnostics.json` — self-intersection report on the GLB (body-part pairs, frame ranges, depth in cm; frames counted from 0); summary also in `run.json`. Parts joined at a joint are not compared. No floor check. `m2mr diagnose <run> [--visualize] [--threshold-cm N]` re-checks a run; `--visualize` adds `diagnostics.html`. The report's 3D view keeps fixed floor markers on y=0 (0.5 m crosses, larger metre marks, green origin) so movement can be judged against the floor. Eye notes on that motion are a separate file; see Review notes.
- Video in: `videos/human_skeleton.mp4`, `videos/mixamo_skeleton.mp4`, `videos/mixamo_character.mp4`, `videos/compare.mp4` (2x2: original / mixamo skeleton / human skeleton / character)
- Photo in: the same four views as PNG under `images/`, plus `images/before_after_360_compare.mp4` (left original / right 10° orbit of the rig)

## Review notes

Problems only the eye can see (a sliding foot, a popped knee, a hand that misses the body) are not in `diagnostics.json`. They go in a review file, schema `m2mr-review-v1`, so a later pass can revise that run's `mixamo_rotations.npz`, `skeleton_motion.npz`, or the animation in `mixamo_character.glb`. The file does not contain the mesh or the npz bytes.

In `diagnostics.html` the amber lane above the intersection tracks is that pass. Drag a range, or set **In** and **Out**, and write what is wrong. The **Notes** list on the right shows the same notes; click a row to jump to its first frame. **Download notes** saves `<video stem>_review.json`. The browser keeps the notes in `localStorage` under the run folder and the source video or still, so a different report does not show them. Regenerating this report's HTML does not drop them.

An agent automating the pass does not need the browser. Write `<run>/<video stem>_review.json` directly. Read `run.json` for the clip and the rig, and `diagnostics.json` for the intersections. Frame 0 is the first frame, the same index as Blender and `diagnostics.json`. Ranges are inclusive. `start_s` and `end_s` are `frame / fps`, rounded to 3 decimals.

Keys and every fixed string are English. `manual_annotations[].note` is the reviewer's own words and is stored exactly as typed, in whatever language they used. A still uses `image` and `image_name` and leaves `video` null.

`self_intersections` is `diagnostics.json` → `issues`. `self_intersection_summary` is `diagnostics.json` → `summary.self_intersection`. Copy them; do not rephrase part names. Pairs with `also_in_rest_pose` already intersect before the motion starts.

```json
{
  "schema": "m2mr-review-v1",
  "purpose": "Human notes on one Mixamo motion, plus the automatic self-intersection report. The clip is the file named in video, or in image for a still. Frame 0 is the first frame, matching Blender and diagnostics.json. Revise mixamo_rotations.npz, skeleton_motion.npz, or the animation in mixamo_character.glb so these ranges improve. Pairs with also_in_rest_pose already intersect before the motion starts. Each note is stored exactly as the reviewer typed it.",
  "run": "20261024_032240_beat_it_shotaro_test_input_compatible",
  "video": "/absolute/path/to/assets/video/beat_it_shotaro_test_input_compatible.mp4",
  "video_name": "beat_it_shotaro_test_input_compatible.mp4",
  "image": null,
  "image_name": null,
  "rig": "/absolute/path/to/assets/mixamo/Y_Bot.fbx",
  "rig_name": "Y_Bot.fbx",
  "source_glb": "mixamo_character.glb",
  "fps": 30,
  "frame_count": 554,
  "threshold_cm": 1.0,
  "generated": "2026-10-24T03:31:54",
  "files": ["mixamo_character.glb", "mixamo_rotations.npz", "skeleton_motion.npz", "diagnostics.json"],
  "manual_annotations": [
    {"id": "n1", "start_frame": 380, "end_frame": 410, "start_s": 12.667, "end_s": 13.667, "note": "left foot slides"}
  ],
  "self_intersection_summary": {"issue_count": 16, "frame_count": 56, "ranges": [[47, 48]], "max_depth_cm": 7.37},
  "self_intersections": [
    {"kind": "self_intersection", "parts": ["left_hand", "left_thigh"], "ranges": [[372, 373], [378, 381]], "frame_count": 6, "worst_frame": 380, "max_depth_cm": 7.37, "also_in_rest_pose": false}
  ]
}
```

The `ranges` inside `self_intersection_summary` and the `self_intersections` array above are shortened. Copy both lists in full from that run's `diagnostics.json`.

Handing this file back with the GLB or the skeleton is the revision pass in After a generation. The agent writes a new version and imports that GLB into Blender; it does not overwrite the run this file describes.

## Code map

- `motion2mixamorig/paths.py` — all filesystem locations
- `motion2mixamorig/extract.py` — clip timing helpers, plus `foot_contact_from_raw`
- `motion2mixamorig/extractors/` — body extractors (`gvhmr`) and the HaMeR finger pass (`hamer.py`, `--detect-hands`)
- `motion2mixamorig/mixamo/hand_retarget.py` — MANO finger rotations onto the 30 Mixamo finger bones
- `motion2mixamorig/mixamo/` — FBX parsing, FK, retargeting, skinning, rendering
- `motion2mixamorig/mixamo/foot_lock.py` — pins planted feet (ball first, else heel) with two-bone leg IK, shifting the hips when a straight leg cannot reach; summary in `run.json` → `foot_lock`
- `motion2mixamorig/mixamo/ground.py` — shifts the hips so the planted sole sits on y = 0; summary in `run.json` → `ground`
- `motion2mixamorig/diagnose.py` — self-intersection check on the GLB -> `diagnostics.json`
- `motion2mixamorig/diagnose_report.py` — `diagnostics.html` (`--visualize`); review lane and `m2mr-review-v1` (see Review notes)
- `motion2mixamorig/pipeline.py` — one run end to end
- `motion2mixamorig/cli.py` — `m2mr doctor` / `m2mr run`
- `blender_extension/motion2mixamorig_blender/` — Blender 4.2+ Extension (UI + external process)
- `blender_extension/README.md` — build the add-on, one-click runtime internals, own-venv setup
- `docs/user-guide.md` — add-on guide for non-programmers
- `docs/blender-extension.md` — maintainer smoke-test checklist
- `docs/c4d-fbx-support.md` — how Cinema 4D-exported FBX rigs are read (bind-matrix rest pose, one GLB skin per mesh)
- `scripts/package_blender_extension.py` — build `dist/motion2mixamorig-0.1.8-<platform>.zip`
