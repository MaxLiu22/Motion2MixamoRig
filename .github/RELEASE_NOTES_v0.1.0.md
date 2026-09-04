## Motion2MixamoRig v0.1.0

The first versioned release of Motion2MixamoRig.

Motion2MixamoRig transfers human motion from a monocular video—or a pose from a still image—onto an Adobe Mixamo-rigged 3D character.

### Highlights

- Transfer motion from a single-person video to a Mixamo character
- Recover and transfer a static pose from a still image
- Export an animated, skinned `.glb` for Blender and Unity
- Export reusable human skeleton motion as `skeleton_motion.npz`
- Export per-bone Mixamo rotations as `mixamo_rotations.npz`
- Reuse an extracted skeleton with another Mixamo character
- Generate skeleton, character, and comparison previews
- Check the environment and required assets with `m2mr doctor`
- Select CPU, CUDA, or Apple Silicon MPS for motion extraction

### Quick start

```bash
m2mr doctor
m2mr run
```

Use a specific video and character:

```bash
m2mr run \
  --video assets/video/dance.mp4 \
  --rig assets/mixamo/Vampire.fbx
```

Use a still image:

```bash
m2mr run \
  --image assets/image/pose.jpg \
  --rig assets/mixamo/Y_Bot.fbx
```

Reuse previously extracted motion:

```bash
m2mr run \
  --skeleton outputs/<previous-run>/skeleton_motion.npz \
  --rig assets/mixamo/Vampire.fbx
```

### Important notes

* Input currently supports one clearly visible, full-body person.
* The first run downloads approximately 5 GB of inference weights.
* The SMPL-X body model and Mixamo character must be obtained separately under their respective licenses.
* Motion extraction and retargeting are experimental.
* Some motions may exhibit root drift, orientation errors, foot sliding, or unstable rotations.

### Next

A future release is planned to introduce a Blender Extension that runs the Motion2MixamoRig pipeline and imports the generated character directly into Blender.
