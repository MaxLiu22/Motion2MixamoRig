# Motion2MixamoRig for Blender — 使用指南

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · 繁體中文 · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

在 Blender 裡，把一段單人影片變成會動的 Mixamo 角色。
不需要寫程式，也不需要開終端機。

<!-- video: link the tutorial video here -->

> 目前只在 **macOS（Apple Silicon）** 上測試過。Windows 版即將推出。

## 事前準備

- **Blender 4.2 或更新版本**
- **網路連線**（第一次安裝時需要）
- **約 8 GB 的可用磁碟空間**（執行環境約 1.3 GB + 模型約 5.6 GB）
- **一個免費的 SMPL-X 帳號**和**一個免費的 Adobe 帳號**（用於 Mixamo），請見第 4、5 步

## 1. 下載外掛

前往[最新版本](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)，
下載適合你電腦的 zip：

| 你的電腦 | 檔案 |
| --- | --- |
| 搭載 Apple Silicon 的 Mac（M1/M2/M3/M4） | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **即將推出** |

例如 `motion2mixamorig-0.1.8-macos-arm64.zip`：`0.1.8` 是外掛版本，
`macos-arm64` 是平台。如果選錯了，Blender 會拒絕安裝，並告訴你它需要的平台。

**不要**解壓縮。Blender 會直接安裝這個 zip。

## 2. 在 Blender 中安裝

1. **Edit → Preferences → Get Extensions**
2. 點選右上角的小 **∨** → **Install from Disk…**
3. 選擇 zip。**Motion2MixamoRig** 會出現在清單中，並且已啟用。
4. 關閉 Preferences。在 3D Viewport 中按 **N**，然後點選右側的
   **Motion2MixamoRig** 分頁。

<!-- screenshot: Install from Disk menu -->

## 3. 安裝執行環境（只需一次）

在面板中點選 **一鍵安裝執行環境**（Install Runtime (one click)）。

外掛會把它自己的 Python 和函式庫（約 1.4 GB）下載到
`~/Motion2MixamoRig/`，不會動到你電腦上的其他任何東西。整個過程需要幾分鐘，
進度列會顯示目前的步驟。

<!-- screenshot: Install Runtime button and progress -->

## 4. 取得 SMPL-X 人體模型

SMPL-X 是外掛需要的一個免費人體模型。它的授權不允許我們隨外掛散布，
所以需要你自行下載一次：

1. 前往 [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) 並 **Register**。
   同意授權條款，並完成電子郵件確認。
2. 登入後開啟 **Download**，下載 SMPL-X 模型（**NPZ** 版本）。
3. 解壓縮，找到 **`SMPLX_NEUTRAL.npz`**。
4. 回到 Blender，點選 **選擇 SMPL-X 模型檔案…**（Choose SMPL-X Model…），選擇這個檔案。
   面板接著會顯示 **SMPL-X 模型：已就緒**（SMPL-X model: found）。

<!-- screenshot: SMPL-X download page -->

## 5. 取得 Mixamo 角色

1. 前往 [mixamo.com](https://www.mixamo.com/)，用 Adobe 帳號登入。
2. **Characters** 分頁 → 選一個角色（例如 **Y Bot**）。
3. **Download** → Format 選 **FBX Binary (.fbx)**，Pose 選 **T-pose** → Download。

<!-- screenshot: Mixamo download dialog -->

## 6. 產生動作

在 **輸入**（Input）區塊中：

1. **來源類型**（Source Type）：**影片**（Video）；只需要單一姿勢時選 **圖片**（Image）
2. **來源檔案**（Source File）：你的影片片段。畫面中必須**只有一個人，而且從頭到腳
   全程完整入鏡**。
3. **Mixamo 角色 FBX**（Mixamo Rig FBX）：第 5 步下載的角色
4. **偵測手部**（Detect Hands）預設關著。只有想讓手指跟著動時才打開。
   然後點 **選擇 MANO 手部模型…**（Choose MANO Hand Model…），選中 `MANO_RIGHT.pkl`。
   這個檔案和 SMPL-X 一樣要自己下載：在
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/) 註冊，下載 **Models & Code**，
   解壓後找到它。第一次跑手部會再下載約 **2.7 GB**，只下這一次，耗時大約是只跑身體的兩倍。打開後還會出現 **手指平滑（秒）**（Finger Smoothing (seconds)）。它讓手指的動作順一些。預設是 0.08 秒，填 0 就是偵測到什麼樣就什麼樣。
5. 點選 **產生動作**（Generate Motion）

完成後，帶有動畫的角色會自動匯入你的場景。踩實的那隻腳會停在落點上，腳底板貼在 Blender 的地面上。地面上會多一個 **Floor Markers** 網格（每 0.5 公尺一個十字）。進度 / 結果裡的 **地面標記**（Floor Markers）勾選框用來顯示或隱藏它。

### 首次執行會比較久，這是正常的

第一次執行時，外掛會下載約 **5.6 GB** 的模型。面板會顯示下載大小、速度和
剩餘時間。模型只需要下載一次。

之後，影片會在你的電腦上進行處理。在 Mac 的 CPU 上，一段 10 秒的片段需要
幾分鐘。執行期間 Blender 仍然可以正常使用，點選 **取消**（Cancel）可以停止工作。

## 取得好結果的小訣竅

- 畫面中只有一個人，全身可見，沒有被畫面邊緣切到
- 鏡頭穩定、光線充足，衣服盡量簡單，避免寬鬆或飄動的款式
- 先用短片段（5–20 秒）試試看，比較快有結果

## 更新到新版本

外掛會經常更新。更新方式：

1. 從[最新版本](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
   下載最新的 zip。
2. **Get Extensions** → 移除舊的 **Motion2MixamoRig**，完全結束 Blender
   （**Cmd+Q**），重新開啟後安裝新的 zip。
3. 在面板中點選 **更新執行環境**（Update Runtime）。

更新會保留已下載的模型，所以很快就能完成。已安裝的版本會顯示在 **Get Extensions**
中外掛名稱的旁邊。

## 面板說明

- **標題旁的 ⚙** 用來顯示或隱藏 **設定**（Setup）區塊。
- **設定**：語言、執行環境、SMPL-X、**裝置**（Device，選 CPU 最保險），以及
  **檢查環境**（Check Environment）。
- **輸入**：要製作成動畫的素材、**身體模型**（Body Model，目前是 GVHMR），以及 **偵測手部**（Detect Hands）。
- **進度 / 結果**（Progress / Result）：進度、最近的記錄；工作完成後還有
  **匯入產生的角色**（Import Generated Character）、**地面標記**（Floor Markers）勾選框、**開啟輸出資料夾**（Open Output Folder）、
  **檢視完整記錄**（View Full Log）。
- **診斷**（Diagnostics）：角色身體部位互相穿插的地方（例如手穿進頭裡、雙臂交叉時穿進去）。條上的紅格是有問題的影格，點一下就會跳過去。條下方的三角形跟著目前影格移動，再下方列出這一格有哪些部位穿插、深度多少。**上一個問題** / **下一個問題**（Previous / Next）可在問題之間跳轉。**開啟 HTML 報告**（Open HTML Report）會在瀏覽器中開啟報告，原始影片與角色並排顯示（第一次需要產生，大約 15 秒）。左邊的原始影片要電腦上裝了 ffmpeg 才看得到（Mac 上是 `brew install ffmpeg`）。沒裝的話，角色還在，旁邊的影片是空的。角色站在固定的地面十字上，每 0.5 公尺一個，用來看它有沒有在滑。時間軸上方的琥珀色條用來記人眼看出的問題。右邊的 **標註**（Notes）列表會列出這些標註，點一行就跳到那一幀。**下載標註**（Download notes）會把這些標註和穿模時間點一起存成一份檔案，檔名用的是這段影片的名字。

外掛支援 19 種語言。**自動（跟隨 Blender / 系統）**（Auto (Blender / System)）會跟隨
Blender 的語言；可以在設定區塊的 **介面語言**（UI Language）中變更。

## 發生問題時

| 你看到的訊息 | 處理方式 |
| --- | --- |
| **執行環境安裝失敗**（Runtime installation failed） | 檢查網路連線，然後再點一次按鈕。記錄檔：`~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X 模型：缺少**（SMPL-X model: missing） | 重新執行第 4 步，選擇 `SMPLX_NEUTRAL.npz` |
| **MANO 手部模型：缺少**（MANO hand model: missing） | 打開 **偵測手部**，再點 **選擇 MANO 手部模型…**，選中 `MANO_RIGHT.pkl` |
| **Mixamo FBX 無效**（Mixamo FBX invalid） | 重新下載角色，格式選 **FBX Binary**，姿勢選 **T-pose** |
| **輸入中有多個人**（Input contains multiple people） | 改用只有一個人的片段 |
| **輸入中沒有偵測到人**（No person was detected in the input） | 確認全身入鏡且光線充足 |
| **處理程序意外結束**（Pipeline process exited unexpectedly） | 點選 **檢視完整記錄** |

尋求協助時，請附上記錄檔，並說明你使用的外掛版本。

## 解除安裝

1. **Get Extensions** → 移除 **Motion2MixamoRig**。
2. 刪除資料夾 **`~/Motion2MixamoRig`**（你的家目錄 → `Motion2MixamoRig`）。
   移除外掛**不會**刪除這個資料夾；它佔用約 7 GB（執行環境和模型），
   還包含你產生的結果，存放在 `app/outputs/` 中。

## 授權

Motion2MixamoRig **僅限非商業用途**：它所依賴的研究模型（例如 GVHMR 和 SMPL-X）
的授權不允許商業使用。詳見 [`NOTICE.md`](../../NOTICE.md)。
