# Motion2MixamoRig for Blender — 使用指南

<p align="center">
  简体中文 · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

在 Blender 里，把一段单人视频变成会动的 Mixamo 角色。
不用写代码，也不用开终端。

<!-- video: link the tutorial video here -->

> 目前只在 **macOS（Apple Silicon）** 上测试过。Windows 版即将推出。

## 准备工作

- **Blender 4.2 或更新版本**
- **网络连接**（首次安装时需要）
- **约 8 GB 可用磁盘空间**（运行环境约 1.3 GB + 模型约 5.6 GB）
- **一个免费的 SMPL-X 账号**和**一个免费的 Adobe 账号**（用于 Mixamo），见第 4、5 步

## 1. 下载插件

打开[最新版本](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)，
下载适合你电脑的 zip：

| 你的电脑 | 文件 |
| --- | --- |
| Apple Silicon 芯片的 Mac（M1/M2/M3/M4） | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **即将推出** |

例如 `motion2mixamorig-0.1.8-macos-arm64.zip`：`0.1.8` 是插件版本，
`macos-arm64` 是平台。选错了的话，Blender 会拒绝安装，并提示它需要的平台。

**不要**解压。Blender 会直接安装这个 zip。

## 2. 在 Blender 里安装

1. **Edit → Preferences → Get Extensions**
2. 点击右上角的小 **∨** → **Install from Disk…**
3. 选中 zip。**Motion2MixamoRig** 会出现在列表里，并且已启用。
4. 关闭 Preferences。在 3D Viewport 里按 **N**，然后点击右侧的
   **Motion2MixamoRig** 标签页。

<!-- screenshot: Install from Disk menu -->

## 3. 安装运行环境（只需一次）

在面板里点击 **一键安装运行环境**（Install Runtime (one click)）。

插件会把它自己的 Python 和依赖库（约 1.4 GB）下载到
`~/Motion2MixamoRig/`，不会动你电脑上的其他任何东西。整个过程需要几分钟，
进度条会显示当前步骤。

<!-- screenshot: Install Runtime button and progress -->

## 4. 获取 SMPL-X 人体模型

SMPL-X 是插件需要的一个免费人体模型。它的许可证不允许我们随插件分发，
所以需要你自己下载一次：

1. 打开 [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) 并 **Register**。
   接受许可证，并完成邮件确认。
2. 登录，打开 **Download**，下载 SMPL-X 模型（**NPZ** 版本）。
3. 解压，找到 **`SMPLX_NEUTRAL.npz`**。
4. 回到 Blender，点击 **选择 SMPL-X 模型文件…**（Choose SMPL-X Model…），选中这个文件。
   面板随后会显示 **SMPL-X 模型：已就绪**（SMPL-X model: found）。

<!-- screenshot: SMPL-X download page -->

## 5. 获取 Mixamo 角色

1. 打开 [mixamo.com](https://www.mixamo.com/)，用 Adobe 账号登录。
2. **Characters** 标签页 → 选一个角色（例如 **Y Bot**）。
3. **Download** → Format 选 **FBX Binary (.fbx)**，Pose 选 **T-pose** → Download。

<!-- screenshot: Mixamo download dialog -->

## 6. 生成动作

在 **输入**（Input）框里：

1. **来源类型**（Source Type）：**视频**（Video）；只要单个姿态就选 **图片**（Image）
2. **来源文件**（Source File）：你的视频片段。画面里必须**只有一个人，而且从头到脚
   始终完整入镜**。
3. **Mixamo 角色 FBX**（Mixamo Rig FBX）：第 5 步下载的角色
4. **检测手部**（Detect Hands）默认关着。只有想让手指跟着动时才打开。
   然后点 **选择 MANO 手部模型…**（Choose MANO Hand Model…），选中 `MANO_RIGHT.pkl`。
   这个文件和 SMPL-X 一样要自己下载：在
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/) 注册，下载 **Models & Code**，
   解压后找到它。第一次跑手部会再下载约 **2.7 GB**，只下这一次，耗时大约是只跑身体的两倍。打开后还会出现 **手指平滑（秒）**（Finger Smoothing (seconds)）。它让手指的动作顺一些。默认是 0.08 秒，填 0 就是检测到什么样就什么样。
5. 点击 **生成动作**（Generate Motion）

完成后，带动画的角色会自动导入到你的场景里。踩实的那只脚会停在落点上，
脚底板贴在 Blender 的地面上。地面上会多一个 **Floor Markers** 网格
（每 0.5 米一个十字）。进度 / 结果里的 **地面标记**（Floor Markers）勾选框用来显示或隐藏它。

### 首次运行会比较久，属于正常现象

第一次运行时，插件会下载约 **5.6 GB** 的模型。面板会显示下载大小、速度和
剩余时间。模型只需下载一次。

之后，视频会在你的电脑上本地处理。在 Mac 的 CPU 上，一段 10 秒的片段需要
几分钟。运行期间 Blender 仍可正常使用，点击 **取消**（Cancel）可以停止任务。

## 获得好效果的小建议

- 画面里只有一个人，全身可见，没有被画面边缘截断
- 镜头稳定、光线充足，衣服尽量简洁，避免宽松或飘动的款式
- 先用短片段（5–20 秒）试，出结果更快

## 更新到新版本

插件更新很频繁。更新方法：

1. 从[最新版本](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
   下载最新的 zip。
2. **Get Extensions** → 移除旧的 **Motion2MixamoRig**，完全退出 Blender
   （**Cmd+Q**），重新打开，再安装新的 zip。
3. 在面板里点击 **更新运行环境**（Update Runtime）。

更新会保留已下载的模型，所以很快。已安装的版本号显示在 **Get Extensions**
里插件名称的旁边。

## 面板说明

- **标题旁的 ⚙** 用来显示或隐藏 **设置**（Setup）框。
- **设置**：语言、运行环境、SMPL-X、**设备**（Device，选 CPU 最稳妥），以及
  **检查环境**（Check Environment）。
- **输入**：要做成动画的素材、**身体模型**（Body Model，目前是 GVHMR），以及 **检测手部**（Detect Hands）。
- **进度 / 结果**（Progress / Result）：进度、最近的日志；任务完成后还有
  **导入生成的角色**（Import Generated Character）、**地面标记**（Floor Markers）勾选框、
  **打开输出文件夹**（Open Output Folder）、**查看完整日志**（View Full Log）。
- **诊断**（Diagnostics）：角色身体部位互相穿插的地方（比如手插进头里、双臂交叉时穿进去）。条上的红格是有问题的帧，点一下就跳过去。条下面的三角跟着当前帧走，再下面列出这一帧哪些部位穿插、有多深。**上一个问题** / **下一个问题**（Previous / Next）在问题之间跳转。**打开 HTML 报告**（Open HTML Report）会在浏览器里打开一份报告，原视频和角色并排显示（第一次要生成，大约 15 秒）。左边的原视频要电脑上装了 ffmpeg 才看得到（Mac 上是 `brew install ffmpeg`）。没装的话，角色还在，旁边的视频是空的。角色站在固定的地面十字上，每 0.5 米一个，用来看它有没有在滑。时间轴上方的琥珀色条用来记人眼看出的问题。右边的 **标注**（Notes）列表会列出这些标注，点一行就跳到那一帧。**下载标注**（Download notes）会把这些标注和穿模时间点一起存成一份文件，文件名用的是这段视频的名字。

插件支持 19 种语言。**自动（跟随 Blender / 系统）**（Auto (Blender / System)）会跟随
Blender 的语言；可以在设置框的 **界面语言**（UI Language）里修改。

## 遇到问题时

| 你看到的提示 | 怎么办 |
| --- | --- |
| **运行环境安装失败**（Runtime installation failed） | 检查网络连接，然后再点一次按钮。日志：`~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X 模型：缺失**（SMPL-X model: missing） | 重新做第 4 步，选中 `SMPLX_NEUTRAL.npz` |
| **MANO 手部模型：缺失**（MANO hand model: missing） | 打开 **检测手部**，再点 **选择 MANO 手部模型…**，选中 `MANO_RIGHT.pkl` |
| **Mixamo FBX 无效**（Mixamo FBX invalid） | 重新下载角色，格式选 **FBX Binary**，姿势选 **T-pose** |
| **输入里有多个人**（Input contains multiple people） | 换一段只有一个人的片段 |
| **输入里没有检测到人**（No person was detected in the input） | 确保全身可见、光线充足 |
| **流水线进程意外退出**（Pipeline process exited unexpectedly） | 点击 **查看完整日志** |

求助时，请附上日志，并说明你使用的插件版本。

## 卸载

1. **Get Extensions** → 移除 **Motion2MixamoRig**。
2. 删除文件夹 **`~/Motion2MixamoRig`**（你的主目录 → `Motion2MixamoRig`）。
   移除插件**不会**删除这个文件夹；它占用约 7 GB（运行环境和模型），
   另外还有你生成的结果，保存在 `app/outputs/` 里。

## 许可证

Motion2MixamoRig **仅限非商业用途**：它依赖的研究模型（如 GVHMR 和 SMPL-X）
的许可证不允许商业使用。详见 [`NOTICE.md`](../../NOTICE.md)。
