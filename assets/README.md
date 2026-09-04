# assets

Everything in this folder is supplied by you and is never committed to git
(see the repository `.gitignore`). Licensing is why these cannot ship with the
project: SMPL-X and Mixamo characters must be obtained under your own account.

Run `m2mr doctor` at any time to check what is present and what is missing.

## What goes where

| Path | What | Where to get it |
| --- | --- | --- |
| `body_models/smplx/SMPLX_NEUTRAL.npz` | SMPL-X neutral body model, needed to lift the video into a 3D skeleton | Register at <https://smpl-x.is.tue.mpg.de/>, download the model archive, copy `SMPLX_NEUTRAL.npz` here |
| `mixamo/<Character>.fbx` | The character to drive, e.g. `Y_Bot.fbx` (the default) | <https://www.mixamo.com/> — pick a character, download as **FBX Binary**, **T-pose** |
| `video/<your_clip>.mp4` | The video whose human motion you want to transfer | One clearly visible person only (`.mp4`, `.mov`, …). Group shots are rejected before extraction |
| `image/<your_photo>.jpg` | A still whose pose you want to transfer | One clearly visible person (`.jpg`, `.png`, …). Group photos are rejected before extraction |

`m2mr run` without flags uses the most recently added file in `video/` and
`mixamo/Y_Bot.fbx`; use `--video` / `--image` / `--rig` to pick explicitly.
