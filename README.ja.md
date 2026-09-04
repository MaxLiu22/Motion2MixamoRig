# Motion2MixamoRig

![Motion2MixamoRig](repo_poster.png)

<p align="center">
  <a href="README.zh-CN.md">中文</a> · <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · 日本語 · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a>
</p>

動画の人物の動き — または静止画のポーズ — を、Adobe Mixamo rig の 3D キャラクターに移します。

ゲーム開発者向け：入力は**一人**の動作動画（または写真）と Mixamo キャラクター。プレビューと、Blender / Unity にそのまま入れられるスキン付きキャラクターファイル（`.glb`）を書き出します。

> Motion2MixamoRig はまだ実験段階です。v0.1.0 はコマンドラインのパイプラインです。このリポジトリの Blender 4.2+ Extension は、同じパイプラインを外部 Python で実行します。アドオンの導入と使い方は [`blender_extension/README.md`](blender_extension/README.md)。

Agent は先に [`AGENTS.md`](AGENTS.md) を読んでください。

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>このリポジトリの <a href="demo.mp4">demo.mp4</a> を開いてください。</sub>
</p>

別のデモ：

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

## 事前準備

Python 3.10+ が必要です。クローン後に仮想環境を作り依存関係を入れると、`m2mr` が使えます：

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# 依存関係と本プロジェクトをインストールします。chumpy（依存チェーン上の古いパッケージ）の
# セットアップが pip を import するため、pip 既定の隔離ビルドでは
# "No module named 'pip'" になります。隔離を切って（--no-build-isolation）
# 先に入れてから本プロジェクトを入れてください。
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

推論ウェイト（GVHMR など）はこの段階ではダウンロードしません。初回の `m2mr run` で `weights/` に入ります（約 5 GB、一度だけ）。

ffmpeg も推奨です（macOS: `brew install ffmpeg`、Ubuntu: `apt install ffmpeg`）。
なくても動きますが、出力動画は**無音**になり、ブラウザでは再生できません。

## 実行前：これらを `assets/` に入れてください

このリポジトリにはこれらのファイルは入っていません。自分で用意してください。SMPL-X のファイル名は下表と一字一句同じである必要があります。FBX、動画、写真の名前は何でも構いません。1 回の実行には SMPL-X、Mixamo キャラクター、そして**動画か写真のどちらか**が必要です。

| 何を | どこへ | どこから |
|---|---|---|
| SMPL-X ボディモデル | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | [SMPL-X](https://smpl-x.is.tue.mpg.de/) で登録してダウンロード |
| Mixamo キャラクター FBX | `assets/mixamo/Y_Bot.fbx` | Adobe アカウントで [Mixamo](https://www.mixamo.com) から Y Bot（または他の Mixamo rig キャラクター）をダウンロード |
| 動作動画 | `assets/video/<your_clip>.mp4` | **一人だけ**、はっきり見え、**頭から足まで全編フレーム内**（複数可、実行ごとに最後に入れたファイルを使用） |
| ポーズ写真（任意） | `assets/image/<your_photo>.jpg` | **一人だけ**、はっきり見え、**頭から足までフレーム内**。`--image` と一緒に使う |

注意：Mixamo のダウンロード名は `Y Bot.fbx`（**スペース**）で、表の `Y_Bot.fbx`（**アンダースコア**）と一字違います。
アンダースコアにすればデフォルト rig になり、`m2mr run` は `--rig` なしでそれを使います。名前を変えなくても構いません——`Y_Bot.fbx` が無いときは `assets/mixamo/` の最初の `.fbx` を使います。

`assets/video/` には動画を複数置けます。`--video` も `--image` も指定しないと、**`assets/video/` に最後に入れた**ファイルを使い、そのフォルダが空なら `assets/image/` の最新の写真に戻ります。
各クリップや写真は一人だけ、**頭から足までフレーム内**に収まっている必要があります。はみ出してはいけません。`m2mr doctor` / `m2mr run` は二人が写っていれば抽出に入らず止まります。

## クイックスタート

結果は `outputs/<実行時刻>_<入力名>/` です。動画入力は `videos/`、写真入力は `images/` に書き出します。

### 1. アセットと環境を確認

足りないものは、どこから取ってどこに置くかと一緒に出ます。

```bash
m2mr doctor
```

### 2. 初回実行：まず画面に出す

フラグなしでは **`assets/video/` に最後に入れたファイル** と `assets/mixamo/Y_Bot.fbx` を使います。

```bash
m2mr run
```

この段階が最も遅いです。初回は約 5 GB の推論ウェイトをダウンロードしてから（一度だけ）、動画から人体モーションを抽出します。
約 30 秒のクリップは CPU で抽出にだいたい 8–15 分、ウェイト済みの同程度なら 3–5 分です。
リターゲットとレンダリングは通常 1–2 分です。次節の `--skeleton` でスケルトンを再利用すると抽出を飛ばし、数十秒で終わります。

### 3. 同じモーション、別キャラクター

Mixamo から別のキャラクターを `assets/mixamo/` に入れてください。**`--rig` だけ変えて再実行しないでください** — 遅い抽出がもう一度走ります。
`--skeleton` で前回のスケルトンを再利用すれば、数分が数十秒になります：

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. 別の動画

`--video` でクリップを選びます。`--rig` と自由に組み合わせられます。

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. 静止画（静的ポーズ）

`--image` は**一人**の写真から**静的な 3D ポーズ**を復元し、動画実行と同じ経路で Mixamo キャラクターに載せます。プレビューは `images/` の 4 枚（動画実行と同じ視点）と、左右比較の周回クリップ `before_after_360_compare.mp4` です。`--video` と同時に指定しないでください。

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

パスなしの `--image` は、`assets/image/` に最後に入れたファイルを使います。

## 出力

各 `m2mr run` は**コマンド開始時刻**でディレクトリを作ります。ルートの 4 ファイルは動画も写真も同じで、プレビューフォルダだけが変わります。

```
outputs/20260829_193205_dance/          # 写真実行は …_pose/
├── run.json                            # 開始時刻、入力、完全なコマンド
├── skeleton_motion.npz                 # 人体 3D スケルトン（--skeleton で再利用）
├── mixamo_rotations.npz                # Mixamo ボーンごとの回転
├── mixamo_character.glb                # スキン付きキャラクター、Blender / Unity にインポート
└── videos/   または   images/          # プレビュー — 入力によって決まる
```

**動画入力**は `videos/` に書き出します（クリップと同じアスペクト比）：

```
videos/
├── human_skeleton.mp4                  # 復元した人体 3D スケルトン
├── mixamo_skeleton.mp4                 # Mixamo rig スケルトン
├── mixamo_character.mp4                # スキン付き Mixamo キャラクター
└── compare.mp4                         # 2×2：元映像（左上）/ Mixamo スケルトン（右上）
                                        #      人体スケルトン（左下）/ キャラクター（右下）
```

**写真入力**は代わりに `images/` に書き出します（同じ 4 ビュー + 周回）：

```
images/
├── human_skeleton.png                  # 復元した人体 3D スケルトン
├── mixamo_skeleton.png                 # Mixamo rig スケルトン
├── mixamo_character.png                # スキン付き Mixamo キャラクター
├── compare.png                         # 2×2：原画（左上）/ Mixamo スケルトン（右上）
│                                       #      人体スケルトン（左下）/ キャラクター（右下）
└── before_after_360_compare.mp4        # 左：原画
                                        # 右：10° で一周する周回
```

`mixamo_character.glb` は Blender で File → Import → glTF 2.0 (.glb/.gltf) で開きます。カメラが空を向いているときはキャラクターのメッシュを選び、View → Frame Selected。頭と手の球の塊はメッシュではなくボーン表示です。Outliner で **Icosphere** と **armature** を非表示にし、スキン付きメッシュは残してください。再生を原寸に合わせるには、`run.json` の `fps` / `n_frames` でシーンの FPS とタイムライン終了フレームを設定します。動画実行は `videos/mixamo_character.mp4`、写真実行は `images/mixamo_character.png` または周回クリップと見比べてください。

## ライセンス

このリポジトリのコードは Apache-2.0 です。自分で取得したアセットにはそれぞれの条件があり、このリポジトリと一緒に再配布してはいけません：

- **SMPL-X**：MPI による提供制限。既定は非商用の研究 / 教育 / 芸術；商用は別契約
- **Mixamo FBX**：製品に入れてよい；元の FBX をアセットパックとして再配布してはいけない
- **GVHMR および他の推論ウェイト**：初回 `m2mr run` で `weights/` に自動ダウンロード、各アップストリームのライセンス

## 連絡先

ご不明点がある場合、ローカル環境の構築でお手伝いが必要な場合、または協業をご相談したい場合は、メールでご連絡ください：
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)
