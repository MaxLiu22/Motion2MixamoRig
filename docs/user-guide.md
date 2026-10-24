# Motion2MixamoRig for Blender — User Guide

<p align="center">
  <a href="i18n/user-guide.zh-Hans.md">简体中文</a> · <a href="i18n/user-guide.zh-Hant.md">繁體中文</a> · English · <a href="i18n/user-guide.ko.md">한국어</a> · <a href="i18n/user-guide.ja.md">日本語</a> · <a href="i18n/user-guide.de.md">Deutsch</a> · <a href="i18n/user-guide.ru.md">Русский</a> · <a href="i18n/user-guide.ar.md">العربية</a> · <a href="i18n/user-guide.vi.md">Tiếng Việt</a> · <a href="i18n/user-guide.fil.md">Filipino</a> · <a href="i18n/user-guide.th.md">ไทย</a> · <a href="i18n/user-guide.fr.md">Français</a> · <a href="i18n/user-guide.es-MX.md">Español</a> · <a href="i18n/user-guide.tr.md">Türkçe</a> · <a href="i18n/user-guide.ne.md">नेपाली</a> · <a href="i18n/user-guide.id.md">Bahasa Indonesia</a> · <a href="i18n/user-guide.pl.md">Polski</a> · <a href="i18n/user-guide.nl.md">Nederlands</a> · <a href="i18n/user-guide.it.md">Italiano</a> · <a href="i18n/user-guide.pt-BR.md">Português (Brasil)</a> · <a href="i18n/user-guide.uk.md">Українська</a> · <a href="i18n/user-guide.cs.md">Čeština</a> · <a href="i18n/user-guide.hi.md">हिन्दी</a> · <a href="i18n/user-guide.sv.md">Svenska</a>
</p>

Turn a video of one person into an animated Mixamo character, inside Blender.
No coding or terminal needed.

<!-- video: link the tutorial video here -->

> Tested on **macOS (Apple Silicon)** so far. A Windows build is coming soon.

## What you need

- **Blender 4.2 or newer**
- **An internet connection** for the first setup
- **About 8 GB of free disk space** (runtime ~1.3 GB + models ~5.6 GB)
- **A free SMPL-X account** and **a free Adobe account** (for Mixamo); see steps 4 and 5

## 1. Download the add-on

Go to the [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
and download the zip for your computer:

| Your computer | File |
| --- | --- |
| Mac with Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Coming soon** |

For example `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` is the add-on
version, `macos-arm64` the platform. If you pick the wrong one, Blender refuses
to install it and names the platform it expected.

Do **not** unzip it. Blender installs the zip itself.

## 2. Install it in Blender

1. **Edit → Preferences → Get Extensions**
2. Click the small **∨** at the top right → **Install from Disk…**
3. Choose the zip. **Motion2MixamoRig** appears in the list, enabled.
4. Close Preferences. In the 3D Viewport press **N**, then click the
   **Motion2MixamoRig** tab on the right.

<!-- screenshot: Install from Disk menu -->

## 3. Install the runtime (one time)

In the panel, click **Install Runtime (one click)**.

The add-on downloads its own Python and libraries (~1.4 GB) into
`~/Motion2MixamoRig/`. It does not touch anything else on your computer. This
takes a few minutes; the progress bar shows the current step.

<!-- screenshot: Install Runtime button and progress -->

## 4. Get the SMPL-X body model

SMPL-X is a free body model the add-on needs. Its license does not allow us to
ship it, so you download it yourself, once:

1. Open [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) and **Register**.
   Accept the license and confirm the email.
2. Log in, open **Download**, and download the SMPL-X model (the **NPZ**
   version).
3. Unzip it and find **`SMPLX_NEUTRAL.npz`**.
4. In Blender, click **Choose SMPL-X Model…** and pick that file. The panel
   then shows **SMPL-X model: found**.

<!-- screenshot: SMPL-X download page -->

## 5. Get a Mixamo character

1. Open [mixamo.com](https://www.mixamo.com/) and sign in with an Adobe account.
2. **Characters** tab → pick a character (for example **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Generate motion

In the **Input** box:

1. **Source Type**: Video (or Image for a single pose)
2. **Source File**: your clip. It must show **exactly one person, head to toe
   in frame the whole time**.
3. **Mixamo Rig FBX**: the character from step 5
4. **Detect Hands** is off. Turn it on only when you want the fingers to move.
   Then click **Choose MANO Hand Model…** and pick `MANO_RIGHT.pkl`. Get that
   file the same way as SMPL-X: register at
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), download **Models & Code**,
   and unzip it. The first hand run downloads about **2.7 GB** more, once, and
   takes about twice as long as a body-only run. With hands on, **Finger
   Smoothing (seconds)** appears. It softens the finger motion. The default is
   0.08 seconds; 0 keeps what was detected.
5. Click **Generate Motion**

When it finishes, the animated character is imported into your scene
automatically. A planted foot stays where it landed, and the sole is set on
Blender's floor. A **Floor Markers** mesh is added on that floor (a cross
every 0.5 m). The **Floor Markers** checkbox under Progress / Result shows or
hides it.

### The first run takes longer — this is normal

The first time, the add-on downloads about **5.6 GB** of models. The panel
shows the download size, speed, and time left. Models download only once.

After that, the video is processed on your computer. On a Mac CPU, a
10-second clip takes a few minutes. Blender stays usable while it runs, and
**Cancel** stops the job.

## Tips for good results

- One person only, full body visible, not cut off at the edges
- Steady camera, good light, plain clothes rather than loose or flowing ones
- Short clips (5–20 seconds) are faster to try first

## Update to a new version

The add-on is updated often. To update:

1. Download the newest zip from the
   [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → remove the old **Motion2MixamoRig**, quit Blender
   fully (**Cmd+Q**), reopen, and install the new zip.
3. In the panel, click **Update Runtime**.

Updating keeps the downloaded models, so it is quick. Your installed version is
shown next to the add-on in **Get Extensions**.

## The panel

- **⚙ next to the title** shows or hides the **Setup** box.
- **Setup**: language, runtime, SMPL-X, device (CPU is the safe choice), and
  **Check Environment**.
- **Input**: what to animate, **Body Model** (GVHMR), and **Detect Hands**.
- **Progress / Result**: progress, recent log, and after a job
  **Import Generated Character**, the **Floor Markers** checkbox,
  **Open Output Folder**, **View Full Log**.
- **Diagnostics**: where the character's body parts go into each other (a
  hand inside the head, crossed arms). Red cells in the bar are frames with a
  problem; click one to go there. The triangle under the bar follows the
  current frame, and below it are the parts that intersect and how deep.
  **Previous** / **Next** jump between problems. **Open HTML Report** opens a
  report in your web browser with the source video beside the character (the
  first time it takes about 15 seconds to build). That video needs ffmpeg
  installed on the computer (on a Mac, `brew install ffmpeg`); without it the
  pane stays blank. The character stands on
  fixed floor crosses, one every 0.5 m, so you can see whether it is sliding.
  The amber lane above the red tracks is for notes you make by eye. Those notes
  are listed under **Notes** on the right; click one to jump to it.   **Download
  notes** saves those notes together with the intersection times. The file is
  named after the source video.

The add-on speaks 19 languages. **Auto** follows Blender's language; change it
in the Setup box under **UI Language**.

## If something goes wrong

| What you see | What to do |
| --- | --- |
| Runtime installation failed | Check your internet connection and click the button again. Log: `~/Motion2MixamoRig/logs/setup.log` |
| SMPL-X model: missing | Do step 4 again and pick `SMPLX_NEUTRAL.npz` |
| MANO hand model: missing | Turn on **Detect Hands**, then **Choose MANO Hand Model…** and pick `MANO_RIGHT.pkl` |
| Mixamo FBX invalid | Download the character again as **FBX Binary**, **T-pose** |
| Input contains multiple people | Use a clip with only one person |
| No person was detected | Make sure the whole body is visible and well lit |
| Pipeline process exited unexpectedly | Click **View Full Log** |

When you ask for help, attach the log and say which add-on version you use.

## Uninstall

1. **Get Extensions** → remove **Motion2MixamoRig**.
2. Delete the folder **`~/Motion2MixamoRig`** (your home folder →
   `Motion2MixamoRig`). Removing the add-on does **not** delete it, and it
   holds about 7 GB of runtime and models, plus your generated results in
   `app/outputs/`.

## License

Motion2MixamoRig is for **non-commercial use only**: it relies on research
models (such as GVHMR and SMPL-X) whose licenses do not allow commercial use.
See [`NOTICE.md`](../NOTICE.md).
