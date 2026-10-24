# Motion2MixamoRig

<p align="center">
  <a href="#前置需求"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.zh-Hant.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · 繁體中文 · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

把影片中人物的動作，或一張照片裡的姿勢，轉移到用 Adobe Mixamo rig 好的 3D 角色上。

給遊戲開發者：輸入一段**單人**動作影片（或一張人物照片）和一個 Mixamo 角色，就會輸出預覽影片，以及可以直接放進 Blender / Unity 的已蒙皮角色檔（`.glb`）。

> Motion2MixamoRig 目前仍在實驗階段。v0.1.8 是命令列工作流程。本儲存庫另外提供一個 Blender 4.2+ Extension，會在外部的 Python 環境中執行同一條 pipeline。從原始碼建置外掛：[`blender_extension/README.md`](../../blender_extension/README.md)。

## 兩種使用方式

### 🎨 在 Blender 中使用 — 不需要寫程式

1. 從[最新版本](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)下載適合你平台的 zip，例如 `motion2mixamorig-<version>-macos-arm64.zip`。
2. 在 Blender 中：**Edit → Preferences → Get Extensions → ∨ → Install from Disk…**，選擇這個 zip。
3. 3D Viewport → 按 **N** → **Motion2MixamoRig** 分頁 → **一鍵安裝執行環境**（Install Runtime (one click)）。
4. **選擇 SMPL-X 模型檔案…**（Choose SMPL-X Model…）（可免費下載），再選擇一個 Mixamo 角色 FBX。
5. 選擇一段單人影片 → **產生動作**（Generate Motion）。

逐步說明、使用訣竅與更新方式請見 **[使用指南](user-guide.zh-Hant.md)**。已在 macOS（Apple Silicon）上測試。

### 💻 命令列 — 給開發者

clone 儲存庫，自行執行 pipeline：從[前置需求](#前置需求)開始。

Agent 請先閱讀 [`AGENTS.md`](../../AGENTS.md)。

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>開啟本儲存庫中的 <a href="../assets/demo.mp4">demo.mp4</a>。</sub>
</p>

另一個 demo：

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

診斷報告（`diagnostics.html`）：

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## 前置需求

需要 Python 3.11+。clone 之後建立虛擬環境並安裝相依套件，就可以使用 `m2mr` 指令：

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# 安裝相依套件與本專案。chumpy（相依鏈中的舊套件）的建置腳本會 import pip，
# 在 pip 預設的隔離建置環境中一定會出現 "No module named 'pip'"，
# 所以要先關閉隔離（--no-build-isolation）單獨安裝它，再安裝本專案。
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

推論權重（GVHMR 等）不會在這一步下載，第一次執行 `m2mr run` 時會自動下載到 `weights/`（約 5 GB，只需下載一次）。第一次執行 `m2mr run --detect-hands` 時，還會把 HaMeR 手部權重下載到 `weights/hamer/`（約 2.7 GB，只需下載一次）。

建議另外安裝 ffmpeg（macOS：`brew install ffmpeg`，Ubuntu：`apt install ffmpeg`）。
沒有它也能執行，但輸出的影片會**沒有聲音**，編碼格式也無法直接在瀏覽器中播放。

## 執行前：把這些檔案放到 `assets/`

本儲存庫不附帶這些檔案，需要你自行準備。SMPL-X 的檔名必須和下表完全一致；FBX、影片和照片的檔名可以隨意。每次執行需要 SMPL-X、一個 Mixamo 角色，以及**影片或照片二選一**。 在 Cinema 4D 中重新匯出的 Mixamo 角色 FBX 也能使用，詳見 [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md)。

| 放什麼 | 放在哪裡 | 去哪裡取得 |
|---|---|---|
| SMPL-X 人體模型 | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | 在 [SMPL-X](https://smpl-x.is.tue.mpg.de/) 註冊後下載 |
| Mixamo 角色 FBX | `assets/mixamo/Y_Bot.fbx` | 用 Adobe 帳號從 [Mixamo](https://www.mixamo.com) 下載 Y Bot（或其他用 Mixamo rig 好的角色） |
| 動作影片 | `assets/video/<your_clip>.mp4` | **只有一個人**、人物清楚可見、**從頭到腳全程都在畫面內**（可以放多個檔案，每次執行會使用最新加入的那一個） |
| 姿勢照片（選用） | `assets/image/<your_photo>.jpg` | **只有一個人**、人物清楚可見、**從頭到腳都在畫面內**。搭配 `--image` 使用 |
| MANO 右手模型（只有 `--detect-hands` 才需要） | `assets/body_models/mano/MANO_RIGHT.pkl` | 在 [MANO](https://mano.is.tue.mpg.de/) 註冊後下載 **Models & Code**。只跑身體時不需要這個檔案 |

注意：從 Mixamo 下載的檔名是 `Y Bot.fbx`（中間是**空格**），和上表的 `Y_Bot.fbx`（**底線**）差一個字元。
改成底線後它就是預設 rig，`m2mr run` 不加 `--rig` 時會自動使用它；不改名也可以——找不到 `Y_Bot.fbx` 時，
會自動使用 `assets/mixamo/` 中的第一個 `.fbx`。

`assets/video/` 可以放多個影片檔。沒有指定 `--video` 或 `--image` 時，會使用**最後放進 `assets/video/` 的影片**；如果這個資料夾是空的，就改用 `assets/image/` 中最新的一張照片。
每段影片或每張照片中只能有一個人，而且人物必須**從頭到腳都在畫面內**，不能被裁切。`m2mr doctor` / `m2mr run` 偵測到兩個人時會直接停止，不會進入擷取步驟。

## 快速開始

結果都會放在 `outputs/<執行時間>_<輸入名稱>/`。影片輸入會寫到 `videos/`，照片輸入會寫到 `images/`。

### 1. 檢查資源與環境

缺少什麼會告訴你去哪裡下載、放到哪裡。

```bash
m2mr doctor
```

`m2mr doctor` 檢查的是身體這一路，不要求 MANO 手部模型。要連手指偵測用的檔案和 Python 套件一起查：

```bash
m2mr doctor --detect-hands
```

### 2. 第一次執行：先得到一個看得到的結果

不加任何參數時，會使用**最後放進 `assets/video/` 的影片** + `assets/mixamo/Y_Bot.fbx`。

```bash
m2mr run
```

這一步最慢。第一次執行會先下載約 5 GB 的推論權重（只需一次），接著從影片中擷取人體動作。
一段約 30 秒的影片，在 CPU 上擷取大約需要 8–15 分鐘；權重下載完成後，再處理類似長度的影片大約需要 3–5 分鐘。
後面的重定向與算繪通常只需一兩分鐘。使用下一節的 `--skeleton` 重複利用骨架時，會完全跳過擷取，幾十秒就能得到結果。

踩實的腳預設會釘住：腳掌著地時鎖腳掌，只有腳尖抬起來才鎖腳跟。腿伸直還夠不到時，髖部會跟著挪。然後腳底板會被放到地面上（y = 0）。`--no-foot-lock` 保留原始重定向，腳可能會滑；腳底板仍然會放到地面上。

### 3. 同一段動作，換一個角色

從 Mixamo 下載其他角色放進 `assets/mixamo/`。**不要只改 `--rig` 就重新執行**——這樣最慢的
動作擷取會整個重來一次。使用 `--skeleton` 重複利用上一次執行擷取好的骨架，幾分鐘的事就變成幾十秒：

```bash
m2mr run --skeleton outputs/<上次的執行目錄>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. 換一段影片

`--video` 用來指定使用哪一段影片，可以和 `--rig` 任意搭配。

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. 使用一張照片（靜態姿勢）

`--image` 會從**單人照片**還原出一個靜態的 3D 姿勢，再用和影片相同的流程轉移到 Mixamo 角色上。預覽是 `images/` 中的四張靜態圖（種類和影片執行相同），另外還有一段左右對照的環繞影片 `before_after_360_compare.mp4`。不要和 `--video` 一起使用。

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` 不加路徑時，會使用 `assets/image/` 中最後放進去的那一張。

### 6. 檢查穿模

每次執行還會檢查產生的角色有沒有**穿模**——一個身體部位穿進另一個部位，例如手穿進頭裡——並寫出 `diagnostics.json`。終端機會印出一行，例如 `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`。不檢查與地面的穿插。

想重新檢查某次執行，或直接看問題在哪裡：

```bash
m2mr diagnose outputs/<run>                  # 重寫 diagnostics.json
m2mr diagnose outputs/<run> --visualize      # 另外產生 diagnostics.html：原始影片與角色並排、時間軸、可點選的問題清單
m2mr diagnose outputs/<run> --threshold-cm 2 # 只回報深度超過 2 cm 的穿插（預設 1）
```

`diagnostics.json` 中每個問題是一對身體部位，附上兩者穿插的影格範圍、最嚴重的影格及其深度。影格編號從 0 開始，與 glTF 匯入 Blender 後的時間軸一致。以關節相連的部位（上臂與前臂、軀幹與大腿……）不互相比較：不論什麼姿勢，關節附近的皮膚都會重疊。`diagnostics.html` 會嵌入原始影片（需要 `ffmpeg`），並從 CDN 載入 three.js，因此 3D 檢視需要網路連線。這個 3D 檢視在 y = 0 上畫著固定的地面標記：每 0.5 公尺一個十字，整公尺的更大，原點是綠色，用來判斷角色有沒有在動。穿模軌道上方的琥珀色條用來記人眼看出的問題（拖出一段，或用 **In** / **Out**）。右邊的 **標註**（Notes）列表會列出這些標註，點一行就跳到那一幀。**下載標註**（Download notes）會把這些標註和穿模紀錄一起存成一份檔案。檔名用的是這段影片的名字，裡面也寫著這段影片的路徑。

### 7. 手指（`--detect-hands`）

一般的 `m2mr run` 只動身體，Mixamo 的手指骨停在靜息姿勢。`--detect-hands` 打開和身體擷取器配套的手部模型。預設擷取器 GVHMR 用的是 [HaMeR](https://github.com/geopavlakos/hamer)。HaMeR 用 GVHMR 已經選定的人和影格去裁手腕，不會再在片子裡另找一個人。

**耗時大約翻倍。** 不加這個開關幾分鐘能跑完的片段，加上之後大約要兩倍時間，因為手部是在身體擷取之上再跑一遍。長影片開跑之前先把這段時間算進去。

按上面的表放好 `MANO_RIGHT.pkl`，然後：

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

第一次帶 `--detect-hands` 會把 HaMeR 權重下載到 `weights/hamer/`（約 2.7 GB，只這一次）。手指旋轉寫進 `skeleton_motion.npz`，並驅動帶皮角色上的 30 根 Mixamo 手指骨。身體那一步沒看清的那隻手腕，這隻手就保持靜息。

`--hand-smooth` 是這些旋轉要平滑多少秒。預設 `0.08`。`0` 保留原始估計。只要骨架檔案裡已經有手部動作，平滑就會做，包括後來只重複利用這個檔案的那次執行。

重複利用以前的骨架時：

- 檔案裡已經有手部動作：`--skeleton` 自己就會驅動手指，不必再加 `--detect-hands`。
- 沒有，但這邊還留著那次的身體快取（`cache/<clip>/0_input_video.mp4`，以及 `preprocess/vitpose.pt` 和 `preprocess/bbx.pt`）：`--skeleton ... --detect-hands` 可以補上手指，不用重新擷取身體。
- 快取已經沒了：用 `--detect-hands` 把影片或照片再跑一遍。

## 輸出

每次執行 `m2mr run` 都會依**指令開始執行的時間**建立一個新目錄。根目錄的檔案在影片和照片輸入時都相同，只有預覽資料夾會不同。

```
outputs/20260829_193205_dance/          # 照片執行則是 …_pose/
├── run.json                            # 開始時間、輸入、完整指令
├── skeleton_motion.npz                 # 人體 3D 骨架（可用 --skeleton 重複利用）
├── mixamo_rotations.npz                # Mixamo 每根骨骼的旋轉
├── mixamo_character.glb                # 已蒙皮角色，可匯入 Blender / Unity
├── diagnostics.json                    # 穿模報告（見快速開始第 6 步）
├── diagnostics.html                    # 只有執行 `m2mr diagnose <run> --visualize` 之後才有
└── videos/   或   images/              # 預覽 — 取決於這次輸入的是影片還是照片
```

**影片輸入**會寫到 `videos/`（長寬比和原始片段相同）：

```
videos/
├── human_skeleton.mp4                  # 還原出的人體 3D 骨架
├── mixamo_skeleton.mp4                 # Mixamo rig 骨架
├── mixamo_character.mp4                # 已蒙皮的 Mixamo 角色
└── compare.mp4                         # 四格對照：左上原始影片 / 右上 Mixamo 骨架
                                        #         左下人體骨架 / 右下角色
```

**照片輸入**則會寫到 `images/`（四種圖和上面一一對應，另外加一段環繞影片）：

```
images/
├── human_skeleton.png                  # 還原出的人體 3D 骨架
├── mixamo_skeleton.png                 # Mixamo rig 骨架
├── mixamo_character.png                # 已蒙皮的 Mixamo 角色
├── compare.png                         # 四格對照：左上原始照片 / 右上 Mixamo 骨架
│                                       #         左下人體骨架 / 右下角色
└── before_after_360_compare.mp4        # 左：原始照片
                                        # 右：每 10° 環繞角色一圈
```

帶上 `--detect-hands` 時，`skeleton_motion.npz` 裡還有手指旋轉，`mixamo_rotations.npz` 和 `mixamo_character.glb` 會包含那 30 根手指骨。沒有這個開關、重複利用的骨架裡也沒有手部動作時，這些骨頭停在靜息姿勢。

用 Blender 開啟 `mixamo_character.glb`：File → Import → glTF 2.0 (.glb/.gltf)。匯入後如果鏡頭沒有對準角色，請選取角色網格，再使用 View → Frame Selected。頭部和手上那一堆球是骨骼的顯示形狀，不是模型本身：在 Outliner 中隱藏 **Icosphere** 和骨架（armature），保留已蒙皮的網格。場景 FPS 請依照 `run.json` 中的 `fps` 設定，時間軸設為第 0 影格到第 `n_frames` − 1 影格，播放長度才會和原始影片一致，影格編號也才會和 `diagnostics.json` 對得上。影片執行請對照 `videos/mixamo_character.mp4`，照片執行請對照 `images/mixamo_character.png` 或那段環繞影片。

## 授權

本儲存庫的程式碼採用 Apache-2.0 授權。你自行取得的資源各有其條款，不可隨本儲存庫重新散布：

- **SMPL-X**：需經 MPI 授權取得，預設僅限非商業的研究 / 教育 / 藝術用途；商業使用需另行洽談
- **MANO**（只有用 `--detect-hands` 時）：同樣需經 MPI 授權，下載方式和 SMPL-X 一樣；把 `MANO_RIGHT.pkl` 放在本機，不要再散布
- **Mixamo FBX**：可以用在發行的產品中，但不可將原始 FBX 當成素材包散布
- **GVHMR 等推論權重**：第一次執行 `m2mr run` 時會自動下載到 `weights/`，並遵循各自上游專案的授權
- **HaMeR**：本儲存庫裡的推論程式碼是 MIT；權重在第一次 `m2mr run --detect-hands` 時下載到 `weights/hamer/`，遵循上游發布條款

## 聯絡方式

如果在使用中遇到問題、需要協助完成本機環境建置，或希望洽談合作，歡迎透過電子郵件與我聯絡：
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
