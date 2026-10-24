## Motion2MixamoRig v0.1.8

Motion2MixamoRig transfers human motion from a monocular video—or a pose from a still image—onto an Adobe Mixamo-rigged 3D character.

This release checks the finished character for self-intersection, can drive the fingers, and pins planted feet to the floor.

### Highlights

- **Self-intersection diagnostics**: every run writes `diagnostics.json` (which parts intersect, on which frames, and how deep). `m2mr diagnose <run> --visualize` also writes `diagnostics.html`, with the source video beside the character, a timeline, and a clickable issue list. In Blender, the Diagnostics box under Progress jumps between problem frames, and **Open HTML Report** builds that page.
- **Fingers**: `m2mr run --detect-hands` uses HaMeR to drive the 30 Mixamo finger bones. It is off by default. It needs `MANO_RIGHT.pkl`. The first run downloads about 2.7 GB of hand weights, and the clip takes about twice as long.
- **Planted feet**: a planted foot stays where it landed (the ball when the ball is down, the heel only when the toes are up). The sole is then set on the floor. `--no-foot-lock` keeps the raw retarget, so the feet may slide; the sole is still set on the floor.
- **Floor markers** on the report and in the Blender viewport, so movement can be judged against the floor.
- **Review notes**: in `diagnostics.html`, mark a stretch that still looks wrong. **Download notes** saves those notes with the intersection list for a later pass.
- **Documentation**: the README and the user guide are in 24 languages. The add-on UI is in 19, including Italian. The download table lists Windows as coming soon.

### What you will notice

- After import, the timeline runs from frame 0 to n−1, the same numbers as `diagnostics.json`.
- A person who turned away and back is less likely to stay facing the wrong way for the rest of the clip.
- **Open HTML Report** can find a Homebrew `ffmpeg` when Blender was opened from the Dock or Finder, so the source video is included.

### Install the Blender add-on

1. Download `motion2mixamorig-0.1.8-macos-arm64.zip` from the assets below (do not unzip it). This release has a macOS (Apple Silicon) build only. A Windows build is coming soon.
2. In Blender 4.2+: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**
3. Follow the [User Guide](https://github.com/MaxLiu22/Motion2MixamoRig/blob/v0.1.8/docs/user-guide.md).

Updating from v0.1.7: remove the old add-on, quit Blender fully, install this zip, then click **Update Runtime**. Downloaded models are kept. The new checks, the finger pass, and the foot pin live in the runtime, so this step is required.

### Important notes

* Tested on macOS (Apple Silicon) only. A Windows build is coming soon.
* Input currently supports one clearly visible, full-body person.
* The SMPL-X body model and the Mixamo character must be obtained separately under their respective licenses. `--detect-hands` also needs the MANO right-hand model.
* Non-commercial use only, because of upstream model licenses (see `NOTICE.md`).

Full changelog: [v0.1.7...v0.1.8](https://github.com/MaxLiu22/Motion2MixamoRig/compare/v0.1.7...v0.1.8)
