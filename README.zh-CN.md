# Motion2MixamoRig

中文 · [English](README.md)

把视频里人物的动作，转到 Adobe Mixamo rig 的 3D 角色上。

面向游戏开发者：输入一段**单人**动作视频和一个 Mixamo 角色，输出预览视频，以及可直接丢进 Blender / Unity 的带皮角色文件（`.glb`）。

Agent 请先读 [`AGENTS.md`](AGENTS.md)。

## 前置条件

需要 Python 3.10+。克隆后建虚拟环境并安装依赖，`m2mr` 命令随之可用：

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

推理权重（GVHMR 等）不在这一步下载，首次 `m2mr run` 时自动拉到 `weights/`（约 5 GB，只下这一次）。

建议再装上 ffmpeg（macOS：`brew install ffmpeg`，Ubuntu：`apt install ffmpeg`）。
没有它也能跑，但输出的视频会**没有声音**，编码格式也没法在浏览器里直接播放。

## 使用前：把三样东西放到 `assets/`

本仓库不附带这些文件，需要你自己准备。SMPL-X 的文件名必须和下表一字不差；FBX 和视频叫什么都行。

| 放什么 | 放到哪 | 去哪拿 |
|---|---|---|
| SMPL-X 人体模型 | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | 注册 [SMPL-X](https://smpl-x.is.tue.mpg.de/) 后下载 |
| Mixamo 角色 FBX | `assets/mixamo/Y_Bot.fbx` | 用 Adobe 账号从 [Mixamo](https://www.mixamo.com) 下载 Y Bot（或其他 Mixamo rig 角色） |
| 动作视频 | `assets/video/<your_clip>.mp4` | **只有一个人**、人清晰可见的动作视频（可放多个文件，每次跑用其中一个） |

注意：Mixamo 下载下来的文件叫 `Y Bot.fbx`（中间是**空格**），和上表的 `Y_Bot.fbx`（**下划线**）差一个字符。
改成下划线它就是默认 rig，`m2mr run` 不带 `--rig` 时自动用它；不想改名也行——找不到 `Y_Bot.fbx` 时
会自动用 `assets/mixamo/` 里的第一个 `.fbx`。

`assets/video/` 可以放多个视频文件。不指定 `--video` 时，会用**最后放进这个文件夹**的那一个。
每个视频画面里只能有一个人：`m2mr doctor` / `m2mr run` 会抽样检测，看到两个人就直接停，不会进入提取。

## Quick Start

结果都在 `outputs/<运行时间>_<视频名>/`，看视频打开该目录下的 `videos/`。

### 1. 检查资产和环境

缺什么会告诉你去哪下、放到哪。

```bash
m2mr doctor
```

### 2. 第一次跑：先拿到一个能看的结果

不带参数时，用**最后放进 `assets/video/` 的视频** + `assets/mixamo/Y_Bot.fbx`。

```bash
m2mr run
```

这步最慢。第一次跑会先下载约 5 GB 推理权重（只这一次），然后从视频里提取人体动作。
一段约 30 秒的视频，CPU 上提取大约 8–15 分钟；权重下完之后再跑同类长度，大约 3–5 分钟。
后面的重定向和渲染通常一两分钟。用下一节的 `--skeleton` 复用骨架时，提取整段跳过，几十秒就能出结果。

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

## 输出

每次 `m2mr run` 按**命令启动时间**新建一个目录：

```
outputs/20260829_193205_dance/
├── run.json                    # 启动时间、用的视频 / rig、完整命令
├── skeleton_motion.npz         # 人体 3D 骨架（换 rig 可复用，不必重跑提取）
├── mixamo_rotations.npz        # Mixamo 骨逐帧旋转
├── mixamo_character.glb        # 带皮角色 + 动画，Blender / Unity 可直接导入
└── videos/                     # 比例跟输入视频一致
    ├── human_skeleton.mp4      # 人体骨架
    ├── mixamo_skeleton.mp4     # Mixamo rig 骨架
    ├── mixamo_character.mp4    # Mixamo rig 角色
    └── compare.mp4             # 四宫格：左上原片 / 右上 Mixamo 骨架 / 左下人体骨架 / 右下 Mixamo 角色
```

`mixamo_character.glb` 用 Blender 打开：File → Import → glTF 2.0 (.glb/.gltf)。导入后若镜头对不准，先选中角色，再 View → Frame Selected。头和手上那堆球是骨头的显示形状，不是模型：选中骨架，在 Armature → Viewport Display 里去掉 Shapes。时间轴结束帧改成和视频一样长，再点播放；对照同一次运行的 `videos/mixamo_character.mp4`。

## 许可证

本仓库代码为 Apache-2.0。你自取的资产各有条款，不能随本仓库再分发：

- **SMPL-X**：MPI 门禁，默认非商业科研 / 教育 / 艺术；商用需另谈
- **Mixamo FBX**：可用在成品里，不能把原始 FBX 当资源包发出去
- **GVHMR 等推理权重**：首次 `m2mr run` 自动下载到 `weights/`，遵循各自上游许可

## 联系

若使用中遇到问题、需要协助完成本地部署，或希望洽谈合作，欢迎通过邮箱联系我：
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)
