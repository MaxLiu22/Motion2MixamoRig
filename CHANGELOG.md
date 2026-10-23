# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Self-intersection diagnostics: every `m2mr run` checks the finished `mixamo_character.glb` for one body part going into another and writes `diagnostics.json` (body-part pairs, frame ranges, worst frame, depth in cm) plus a one-line summary; the summary also goes into `run.json`. A failed check does not fail the run. `m2mr diagnose <run>` re-checks a run; `--visualize` also writes `diagnostics.html` with the source video beside the character, a timeline, and a clickable issue list; `--threshold-cm` sets the reporting depth (default 1 cm). Parts joined at a joint are not compared, and stretches of one pair at most 3 frames apart are reported as one range. The floor is not checked.
- Blender add-on: a **Diagnostics** box under Progress shows the job's self-intersections as a 48-cell frame bar (red = intersecting; click a cell to go there), the parts intersecting on the current frame with their depth, and Previous / Next buttons that jump between problem ranges. **Open HTML Report** opens the interactive report in the browser; the first click builds it in the background (`m2mr diagnose --visualize`, about 15 s). Results generated before this version show a note to update the runtime and generate again.

- Italian: a README, a user guide, and the add-on UI (**UI Language → Italiano**; Auto picks it when Blender or the system is set to Italian). The README and the add-on now come in 19 languages.

### Fixed

- Blender add-on: after import the timeline covers the clip as frames 0 to n-1 (was 1 to n), the frame numbers the glTF importer and `diagnostics.json` use.
- Blender add-on: the external Python now finds Homebrew tools such as `ffmpeg` (`/opt/homebrew/bin`, `/usr/local/bin`) when Blender was opened from the Dock or Finder, whose PATH leaves them out. Before, the HTML report could not embed the source video.
- A subject who turned away and back could stay facing away in the recovered 3D motion for the rest of the clip. The 2D left/right stabilizer decided "real turn or label flip" at the single transition frame (it required four consecutive side-view frames after the first turn) and never revisited the decision, so one mislabelled frame or one fast spin locked the wrong facing in. `motion2mixamorig/stabilize_kp2d.py` now cuts the clip into segments at side-view frames and takes the majority of RTMPose's labels inside each segment; only runs of the opposite sign shorter than ~0.33 s count as flips. No facial keypoints are used (hats and masks do not matter) and each person track is handled on its own. On a dance clip with a fast half-second turn, wrong-facing frames went from 320 of 642 to 3. Re-running on an existing cache re-stabilizes from the `vitpose_raw.pt` backup, not from the previous rule's output.

## [0.1.7] - 2026-10-17

Tested on macOS (Apple Silicon) only; Windows and Linux are untested.

### Added

- Mixamo character FBXs re-exported from Cinema 4D are supported: the rest pose comes from the FBX bind matrices (`Pose`, then skin-cluster `TransformLink`, then local transforms) instead of `PreRotation` alone. See `docs/c4d-fbx-support.md`. Contributed by [@yng47](https://github.com/yng47) in [#8](https://github.com/MaxLiu22/Motion2MixamoRig/issues/8).
- The user guide and the README quick start are available in all 18 README languages.

### Changed

- The GLB has one mesh node and skin per FBX geometry, so Blender imports one `skinned_mesh_…` object per mesh piece (Y Bot: two) instead of a single `skinned_mesh`. The armature is still named `mixamo`. Animation and deformation are unchanged.

### Fixed

- GLB export reused the first mesh's inverse-bind matrices for every mesh piece, which could separate or collapse a character whose pieces have different bind matrices. Contributed by [@yng47](https://github.com/yng47) in [#8](https://github.com/MaxLiu22/Motion2MixamoRig/issues/8).
- `rest_skin_error_cm` compares in the same coordinate space as the skinned result, so it no longer reports a false error for meshes with their own bind transform.

## [0.1.6] - 2026-10-17

### Added

- Blender add-on: **Install Runtime (one click)** downloads Python and the dependencies into `~/Motion2MixamoRig`, so the add-on works without a terminal; **Update Runtime** refreshes the code and keeps the weights.
- Blender add-on: **Choose SMPL-X Model…** copies the SMPL-X file into place.
- Blender add-on: first-run notice, and model download progress with speed and time left.
- Blender add-on: UI in 18 languages, matching the README.
- Blender add-on: a ⚙ toggle next to the panel title shows or hides Setup.
- The add-on zip bundles the Motion2MixamoRig code that the one-click runtime installs.
- Per-platform add-on zips: `scripts/package_blender_extension.py --platform <name>` writes `motion2mixamorig-<version>-<platform>.zip` and declares the platform in its manifest, so Blender refuses it on another OS. This release ships `macos-arm64` only.
- User guide for using the add-on without coding (`docs/user-guide.md`), linked from the top of the README.

### Fixed

- The original-video panel of `compare.mp4` played at half speed for non-30 fps clips.
- The fallback YOLO weights were downloaded into the working directory instead of `weights/yolo/`.

## [0.1.5] - 2026-10-15

### Added

- Blender 4.2+ Extension that launches `m2mr` in an external Python environment, streams progress, and imports the generated GLB.
- `m2mr run --output-dir`, `--progress-jsonl`, and `--no-preview` for add-on job control (existing CLI flags unchanged).
- README translations in 17 languages, under `docs/i18n/`.
- Python, Blender, and GitHub stars badges, and a star history chart in the English README.

### Changed

- Python 3.11+ is now required, matching `gvhmr>=1.6`.
- Translated READMEs, the poster, and the demo video moved into `docs/`.

## [0.1.0] - 2026-09-04

### Added

- Retarget single-person motion videos to Mixamo-rigged characters.
- Recover and transfer a static 3D pose from a single-person image.
- Export reusable human skeleton motion as `skeleton_motion.npz`.
- Export per-bone Mixamo rotations as `mixamo_rotations.npz`.
- Export animated, skinned Mixamo characters as `.glb`.
- Generate human skeleton, Mixamo skeleton, character, and comparison previews.
- Reuse previously extracted skeleton motion with `--skeleton`.
- Validate dependencies and user-provided assets with `m2mr doctor`.
- Select CPU, CUDA, or Apple Silicon MPS for motion extraction.

[Unreleased]: https://github.com/MaxLiu22/Motion2MixamoRig/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/MaxLiu22/Motion2MixamoRig/compare/v0.1.0...v0.1.5
[0.1.0]: https://github.com/MaxLiu22/Motion2MixamoRig/releases/tag/v0.1.0
