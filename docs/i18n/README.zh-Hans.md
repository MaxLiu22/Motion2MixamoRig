# Motion2MixamoRig

<p align="center">
  <a href="#前置条件"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.zh-Hans.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  简体中文 · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

把视频里人物的动作，或一张照片里的姿态，转到 Adobe Mixamo rig 的 3D 角色上。

面向游戏开发者：输入一段**单人**动作视频（或一张人物照片）和一个 Mixamo 角色，输出预览视频，以及可直接丢进 Blender / Unity 的带皮角色文件（`.glb`）。

> Motion2MixamoRig 目前仍处于实验阶段。v0.1.8 是命令行工作流。本仓库另有一个 Blender 4.2+ Extension，在外部 Python 里跑同一条 pipeline。从源码构建插件：[`blender_extension/README.md`](../../blender_extension/README.md)。

## 两种用法

### 🎨 在 Blender 里用 — 无需写代码

1. 从[最新版本](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)下载对应平台的 zip，例如 `motion2mixamorig-<version>-macos-arm64.zip`。
2. 在 Blender 里：**Edit → Preferences → Get Extensions → ∨ → Install from Disk…**，选中这个 zip。
3. 3D Viewport → 按 **N** → **Motion2MixamoRig** 标签页 → **一键安装运行环境**（Install Runtime (one click)）。
4. **选择 SMPL-X 模型文件…**（Choose SMPL-X Model…）（可免费下载），再选一个 Mixamo 角色 FBX。
5. 选一段单人视频 → **生成动作**（Generate Motion）。

分步说明、使用技巧和更新方法见 **[使用指南](user-guide.zh-Hans.md)**。已在 macOS（Apple Silicon）上测试。

### 💻 命令行 — 面向开发者

克隆仓库，自己运行 pipeline：从[前置条件](#前置条件)开始。

Agent 请先读 [`AGENTS.md`](../../AGENTS.md)。

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>打开本仓库中的 <a href="../assets/demo.mp4">demo.mp4</a>。</sub>
</p>

另一个 demo：

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

诊断报告（`diagnostics.html`）：

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## 前置条件

需要 Python 3.11+。克隆后建虚拟环境并安装依赖，`m2mr` 命令随之可用：

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# 安装依赖和本项目。chumpy（依赖链里的老包）的构建脚本会 import pip，
# 在 pip 默认的隔离构建环境里必然报 "No module named 'pip'"，
# 所以先关掉隔离（--no-build-isolation）单独装它，再装本项目。
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

推理权重（GVHMR 等）不在这一步下载，首次 `m2mr run` 时自动拉到 `weights/`（约 5 GB，只下这一次）。首次 `m2mr run --detect-hands` 还会把 HaMeR 手部权重量下载到 `weights/hamer/`（约 2.7 GB，只下这一次）。

建议再装上 ffmpeg（macOS：`brew install ffmpeg`，Ubuntu：`apt install ffmpeg`）。
没有它也能跑，但输出的视频会**没有声音**，编码格式也没法在浏览器里直接播放。

## 使用前：把这些东西放到 `assets/`

本仓库不附带这些文件，需要你自己准备。SMPL-X 的文件名必须和下表一字不差；FBX、视频和照片叫什么都行。一次运行需要 SMPL-X、一个 Mixamo 角色，以及**视频或照片二选一**。 在 Cinema 4D 里重新导出的 Mixamo 角色 FBX 也可以使用，详见 [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md)。

| 放什么 | 放到哪 | 去哪拿 |
|---|---|---|
| SMPL-X 人体模型 | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | 注册 [SMPL-X](https://smpl-x.is.tue.mpg.de/) 后下载 |
| Mixamo 角色 FBX | `assets/mixamo/Y_Bot.fbx` | 用 Adobe 账号从 [Mixamo](https://www.mixamo.com) 下载 Y Bot（或其他 Mixamo rig 角色） |
| 动作视频 | `assets/video/<your_clip>.mp4` | **只有一个人**、人清晰可见、**从头到脚全程都在画框内**（可放多个文件，每次跑用最新的那一个） |
| 姿态照片（可选） | `assets/image/<your_photo>.jpg` | **只有一个人**、人清晰可见、**从头到脚都在画框内**。配合 `--image` 使用 |
| MANO 右手模型（只有 `--detect-hands` 才需要） | `assets/body_models/mano/MANO_RIGHT.pkl` | 在 [MANO](https://mano.is.tue.mpg.de/) 注册后下载 **Models & Code**。只跑身体时不需要这个文件 |

注意：Mixamo 下载下来的文件叫 `Y Bot.fbx`（中间是**空格**），和上表的 `Y_Bot.fbx`（**下划线**）差一个字符。
改成下划线它就是默认 rig，`m2mr run` 不带 `--rig` 时自动用它；不想改名也行——找不到 `Y_Bot.fbx` 时
会自动用 `assets/mixamo/` 里的第一个 `.fbx`。

`assets/video/` 可以放多个视频文件。不指定 `--video` 或 `--image` 时，会用**最后放进 `assets/video/` 的视频**；这个文件夹是空的，就退回到 `assets/image/` 里最新的一张照片。
每个视频或照片画面里只能有一个人，而且人物必须**从头到脚都在画框内**，不能出画。`m2mr doctor` / `m2mr run` 检测到两个人就直接停，不会进入提取。

## Quick Start

结果都在 `outputs/<运行时间>_<输入名>/`。视频输入写 `videos/`，照片输入写 `images/`。

### 1. 检查资产和环境

缺什么会告诉你去哪下、放到哪。

```bash
m2mr doctor
```

`m2mr doctor` 检查的是身体这一路，不要求 MANO 手部模型。要连手指检测用的文件和 Python 包一起查：

```bash
m2mr doctor --detect-hands
```

### 2. 第一次跑：先拿到一个能看的结果

不带参数时，用**最后放进 `assets/video/` 的视频** + `assets/mixamo/Y_Bot.fbx`。

```bash
m2mr run
```

这步最慢。第一次跑会先下载约 5 GB 推理权重（只这一次），然后从视频里提取人体动作。
一段约 30 秒的视频，CPU 上提取大约 8–15 分钟；权重下完之后再跑同类长度，大约 3–5 分钟。
后面的重定向和渲染通常一两分钟。用下一节的 `--skeleton` 复用骨架时，提取整段跳过，几十秒就能出结果。

踩实的脚默认会钉住：脚掌着地时锁脚掌，只有脚尖抬起来才锁脚跟。腿伸直还够不到时，髋部会跟着挪。然后脚底板会被放到地面上（y = 0）。`--no-foot-lock` 保留原始重定向，脚可能会滑；脚底板仍然会放到地面上。

### 3. 同一段动作，换个角色

从 Mixamo 下载别的角色丢进 `assets/mixamo/`。**别直接只改 `--rig` 重跑**——那样最慢的
动作提取会原样再来一遍。用 `--skeleton` 复用上一次运行提取好的骨架，几分钟的事变成几十秒：

```bash
m2mr run --skeleton outputs/<上次的运行目录>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. 换视频

`--video` 指定用哪一段，和 `--rig` 可任意组合。

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. 用一张照片（静态姿态）

`--image` 从**单人照片**恢复一个静态 3D 姿态，再按和视频相同的路径转到 Mixamo 角色上。预览是 `images/` 里的四张静帧（种类和视频 run 一样），外加左右对比绕转视频 `before_after_360_compare.mp4`。不要和 `--video` 一起用。

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` 不带路径时，用 `assets/image/` 里最后放进去的那一张。

### 6. 检查穿模

每次运行还会检查生成的角色有没有**穿模**——一个身体部位插进另一个部位里，比如手插进了头——并写出 `diagnostics.json`。终端会打印一行，例如 `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`。不检查和地面的穿插。

想重新检查某次运行，或者直观地看问题在哪：

```bash
m2mr diagnose outputs/<run>                  # 重写 diagnostics.json
m2mr diagnose outputs/<run> --visualize      # 另外生成 diagnostics.html：原视频和角色并排、时间轴、可点击的问题列表
m2mr diagnose outputs/<run> --threshold-cm 2 # 只报告深于 2 cm 的穿插（默认 1）
```

`diagnostics.json` 里每个问题是一对身体部位，附带它们穿插的帧范围、最严重的一帧和深度。帧号从 0 开始，和 glTF 导入 Blender 后的时间轴一致。由关节连着的部位（上臂和前臂、躯干和大腿……）不互相比较：无论什么姿势，关节附近的皮肤都会重叠。`diagnostics.html` 会嵌入原视频（需要 `ffmpeg`），three.js 从 CDN 加载，所以 3D 视图需要联网。这个 3D 视图在 y = 0 上画着固定的地面标记：每 0.5 米一个十字，整米的更大，原点是绿色，用来判断角色有没有在动。穿模轨道上方的琥珀色条用来记人眼看出的问题（拖出一段，或用 **In** / **Out**）。右边的 **标注**（Notes）列表会列出这些标注，点一行就跳到那一帧。**下载标注**（Download notes）会把这些标注和穿模记录一起存成一份文件。文件名用的是这段视频的名字，里面也写着这段视频的路径。

### 7. 手指（`--detect-hands`）

普通的 `m2mr run` 只动身体，Mixamo 的手指骨停在静息姿势。`--detect-hands` 打开和身体提取器配套的手部模型。默认提取器 GVHMR 用的是 [HaMeR](https://github.com/geopavlakos/hamer)。HaMeR 用 GVHMR 已经选定的人和帧去裁手腕，不会再在片子里另找一个人。

**耗时大约翻倍。** 不加这个开关几分钟能跑完的片段，加上之后大约要两倍时间，因为手部是在身体提取之上再跑一遍。长视频开跑之前先把这段时间算进去。

按上面的表放好 `MANO_RIGHT.pkl`，然后：

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

第一次带 `--detect-hands` 会把 HaMeR 权重下载到 `weights/hamer/`（约 2.7 GB，只这一次）。手指旋转写进 `skeleton_motion.npz`，并驱动带皮角色上的 30 根 Mixamo 手指骨。身体那一步没看清的那只手腕，这只手就保持静息。

`--hand-smooth` 是这些旋转要平滑多少秒。默认 `0.08`。`0` 保留原始估计。只要骨架文件里已经有手部动作，平滑就会做，包括后来只复用这个文件的那次运行。

复用以前的骨架时：

- 文件里已经有手部动作：`--skeleton` 自己就会驱动手指，不必再加 `--detect-hands`。
- 没有，但这边还留着那次的身体缓存（`cache/<片段>/0_input_video.mp4`，以及 `preprocess/vitpose.pt` 和 `preprocess/bbx.pt`）：`--skeleton ... --detect-hands` 可以补上手指，不用重新提取身体。
- 缓存已经没了：用 `--detect-hands` 把视频或照片再跑一遍。

## 输出

每次 `m2mr run` 按**命令启动时间**新建一个目录。根目录的文件视频和照片都一样，只有预览文件夹会变。

```
outputs/20260829_193205_dance/          # 照片 run 则是 …_pose/
├── run.json                            # 启动时间、输入、完整命令
├── skeleton_motion.npz                 # 人体 3D 骨架（可用 --skeleton 复用）
├── mixamo_rotations.npz                # Mixamo 骨骼逐帧旋转
├── mixamo_character.glb                # 带皮角色，Blender / Unity 可导入
├── diagnostics.json                    # 穿模报告（见 Quick Start 第 6 步）
├── diagnostics.html                    # 只在运行 `m2mr diagnose <run> --visualize` 之后才有
└── videos/   或   images/              # 预览 — 取决于这次输入是视频还是照片
```

**视频输入**写 `videos/`（比例跟片段一致）：

```
videos/
├── human_skeleton.mp4                  # 提取出的人体 3D 骨架
├── mixamo_skeleton.mp4                 # Mixamo rig 骨架
├── mixamo_character.mp4                # 带皮 Mixamo 角色
└── compare.mp4                         # 四宫格：左上原片 / 右上 Mixamo 骨架
                                        #         左下人体骨架 / 右下角色
```

**照片输入**则写 `images/`（四种图和上面一一对应，外加一条绕转）：

```
images/
├── human_skeleton.png                  # 提取出的人体 3D 骨架
├── mixamo_skeleton.png                 # Mixamo rig 骨架
├── mixamo_character.png                # 带皮 Mixamo 角色
├── compare.png                         # 四宫格：左上原图 / 右上 Mixamo 骨架
│                                       #         左下人体骨架 / 右下角色
└── before_after_360_compare.mp4        # 左：原图
                                        # 右：10° 俯视绕角色转一圈
```

带上 `--detect-hands` 时，`skeleton_motion.npz` 里还有手指旋转，`mixamo_rotations.npz` 和 `mixamo_character.glb` 会包含那 30 根手指骨。没有这个开关、复用的骨架里也没有手部动作时，这些骨头停在静息姿势。

`mixamo_character.glb` 用 Blender 打开：File → Import → glTF 2.0 (.glb/.gltf)。导入后若镜头对不准，选中角色网格，再 View → Frame Selected。头和手上那堆球是骨头的显示形状，不是模型：在 Outliner 里隐藏 **Icosphere** 和骨架（armature），留下带皮网格。场景 FPS 按 `run.json` 里的 `fps` 设置，时间轴设为第 0 帧到第 `n_frames` − 1 帧，这样播放才会和原片一样长，帧号也和 `diagnostics.json` 对得上。视频 run 对照 `videos/mixamo_character.mp4`，照片 run 对照 `images/mixamo_character.png` 或那条绕转视频。

## 许可证

本仓库代码为 Apache-2.0。你自取的资产各有条款，不能随本仓库再分发：

- **SMPL-X**：MPI 门禁，默认非商业科研 / 教育 / 艺术；商用需另谈
- **MANO**（只有用 `--detect-hands` 时）：同样是 MPI 门禁，下载方式和 SMPL-X 一样；把 `MANO_RIGHT.pkl` 放在本地，不要再分发
- **Mixamo FBX**：可用在成品里，不能把原始 FBX 当资源包发出去
- **GVHMR 等推理权重**：首次 `m2mr run` 自动下载到 `weights/`，遵循各自上游许可
- **HaMeR**：本仓库里的推理代码是 MIT；权重在首次 `m2mr run --detect-hands` 时下载到 `weights/hamer/`，遵循上游发布条款

## 联系

若使用中遇到问题、需要协助完成本地部署，或希望洽谈合作，欢迎通过邮箱联系我：
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
