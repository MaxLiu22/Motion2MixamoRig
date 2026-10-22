# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- `m2mr run --detect-hands` turns on the hand model that travels with the body extractor. With the default extractor, GVHMR, that model is HaMeR: it crops the wrists from the person and the frames GVHMR already chose, writes the finger rotations into `skeleton_motion.npz`, and drives the 30 Mixamo finger bones on the skinned character. Off by default; a plain `m2mr run` leaves those bones at rest. A wrist the body pass did not see clearly stays at rest for that hand.
- The flag needs `assets/body_models/mano/MANO_RIGHT.pkl` (register at https://mano.is.tue.mpg.de/ and download Models & Code). The first `m2mr run --detect-hands` downloads the HaMeR weights into `weights/hamer/` (~2.7 GB, once). `m2mr doctor --detect-hands` checks that file and the extra Python packages; `m2mr doctor` without the flag does not.
- A run with `--detect-hands` takes about twice as long as the same clip without it. The extra time is the hand pass on top of the body extraction.
- `--hand-smooth SECONDS` smooths the finger rotations (default `0.08`; `0` keeps the raw estimate). It applies whenever the skeleton file already contains hand motion, including a later `--skeleton` reuse. A reused skeleton that already has hand motion drives the fingers without `--detect-hands`. If it does not, `--detect-hands` can add them only while that run's body cache is still beside the file; otherwise run the video or still again with the flag.
- The README quick start documents `--detect-hands`, the MANO file, the extra runtime, and how reuse behaves.
- Blender add-on: the Input section has a **Body Model** menu (`--set-extractor`, currently GVHMR) and **Detect Hands** (`--detect-hands`, off by default). Turning hands on shows the about-twice runtime, finger smoothing, and **Choose MANO Hand Model…**. **Check Environment** runs `m2mr doctor` with the same two choices.

### Fixed

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
