# Motion2MixamoRig

<p align="center">
  <a href="#事前準備"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.ja.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · 日本語 · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

動画の人物の動き — または静止画のポーズ — を、Adobe Mixamo rig の 3D キャラクターに移します。

ゲーム開発者向け：入力は**一人**の動作動画（または写真）と Mixamo キャラクター。プレビューと、Blender / Unity にそのまま入れられるスキン付きキャラクターファイル（`.glb`）を書き出します。

> Motion2MixamoRig はまだ実験段階です。v0.1.8 はコマンドラインのパイプラインです。このリポジトリの Blender 4.2+ Extension は、同じパイプラインを外部 Python で実行します。アドオンをソースからビルドする方法：[`blender_extension/README.md`](../../blender_extension/README.md)。

## 2 つの使い方

### 🎨 Blender で使う — コーディング不要

1. [最新リリース](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)から、お使いのプラットフォーム用の zip（例：`motion2mixamorig-<version>-macos-arm64.zip`）をダウンロードします。
2. Blender で **Edit → Preferences → Get Extensions → ∨ → Install from Disk…** を開き、zip を選びます。
3. 3D Viewport → **N** を押す → **Motion2MixamoRig** タブ → **ランタイムをインストール（ワンクリック）**（Install Runtime (one click)）。
4. **SMPL-X モデルを選択…**（Choose SMPL-X Model…）（無料でダウンロード可能）し、Mixamo キャラクターの FBX を選びます。
5. 一人が映った動画を選ぶ → **モーションを生成**（Generate Motion）。

手順の詳細、コツ、更新方法は **[ユーザーガイド](user-guide.ja.md)** を参照してください。macOS（Apple Silicon）でテスト済みです。

### 💻 コマンドライン — 開発者向け

リポジトリをクローンしてパイプラインを自分で実行します：[事前準備](#事前準備)から始めてください。

Agent は先に [`AGENTS.md`](../../AGENTS.md) を読んでください。

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>このリポジトリの <a href="../assets/demo.mp4">demo.mp4</a> を開いてください。</sub>
</p>

別のデモ：

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

診断レポート（`diagnostics.html`）：

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## 事前準備

Python 3.11+ が必要です。クローン後に仮想環境を作り依存関係を入れると、`m2mr` が使えます：

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

推論ウェイト（GVHMR など）はこの段階ではダウンロードしません。初回の `m2mr run` で `weights/` に入ります（約 5 GB、一度だけ）。初回の `m2mr run --detect-hands` では、HaMeR の手のウェイトも `weights/hamer/` に入ります（約 2.7 GB、一度だけ）。

ffmpeg も推奨です（macOS: `brew install ffmpeg`、Ubuntu: `apt install ffmpeg`）。
なくても動きますが、出力動画は**無音**になり、ブラウザでは再生できません。

## 実行前：これらを `assets/` に入れてください

このリポジトリにはこれらのファイルは入っていません。自分で用意してください。SMPL-X のファイル名は下表と一字一句同じである必要があります。FBX、動画、写真の名前は何でも構いません。1 回の実行には SMPL-X、Mixamo キャラクター、そして**動画か写真のどちらか**が必要です。 Cinema 4D で再エクスポートした Mixamo キャラクターの FBX も使えます。詳しくは [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md) を参照してください。

| 何を | どこへ | どこから |
|---|---|---|
| SMPL-X ボディモデル | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | [SMPL-X](https://smpl-x.is.tue.mpg.de/) で登録してダウンロード |
| Mixamo キャラクター FBX | `assets/mixamo/Y_Bot.fbx` | Adobe アカウントで [Mixamo](https://www.mixamo.com) から Y Bot（または他の Mixamo rig キャラクター）をダウンロード |
| 動作動画 | `assets/video/<your_clip>.mp4` | **一人だけ**、はっきり見え、**頭から足まで全編フレーム内**（複数可、実行ごとに最後に入れたファイルを使用） |
| ポーズ写真（任意） | `assets/image/<your_photo>.jpg` | **一人だけ**、はっきり見え、**頭から足までフレーム内**。`--image` と一緒に使う |
| MANO 右手（`--detect-hands` のときだけ） | `assets/body_models/mano/MANO_RIGHT.pkl` | [MANO](https://mano.is.tue.mpg.de/) で登録し、**Models & Code** をダウンロード。体だけの実行には不要 |

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

`m2mr doctor` が確認するのは体の実行です。MANO の手モデルは要求しません。指の検出に使う追加ファイルと Python パッケージも確認するには：

```bash
m2mr doctor --detect-hands
```

### 2. 初回実行：まず画面に出す

フラグなしでは **`assets/video/` に最後に入れたファイル** と `assets/mixamo/Y_Bot.fbx` を使います。

```bash
m2mr run
```

この段階が最も遅いです。初回は約 5 GB の推論ウェイトをダウンロードしてから（一度だけ）、動画から人体モーションを抽出します。
約 30 秒のクリップは CPU で抽出にだいたい 8–15 分、ウェイト済みの同程度なら 3–5 分です。
リターゲットとレンダリングは通常 1–2 分です。次節の `--skeleton` でスケルトンを再利用すると抽出を飛ばし、数十秒で終わります。

着地した足は既定で固定されます。足の裏が地面についているときは足の裏を、つま先が上がっているときだけかかとを固定します。脚を伸ばしても届かないときは腰が動きます。そのあと足の裏が地面（y = 0）に置かれます。`--no-foot-lock` は生のリターゲットを残すので、足が滑ることがあります。足の裏はそれでも地面に置かれます。

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

### 6. 自己交差（めり込み）をチェック

各実行では、完成したキャラクターの**自己交差**（ある体の部位が別の部位にめり込むこと。例：手が頭に入り込む）もチェックし、`diagnostics.json` を書き出します。ターミナルには `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm` のような 1 行が表示されます。床とのめり込みはチェックしません。

実行を再チェックする、または問題を目で確認するには：

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json を書き直す
m2mr diagnose outputs/<run> --visualize      # diagnostics.html も出力：元動画とキャラクターを並べて表示、タイムライン、クリックできる問題一覧
m2mr diagnose outputs/<run> --threshold-cm 2 # 2 cm より深いめり込みだけを報告（既定 1）
```

`diagnostics.json` の各問題は体の部位のペアで、交差しているフレーム範囲、最もひどいフレームとその深さを含みます。フレーム番号は glTF を Blender にインポートしたときのタイムラインと同じく 0 から数えます。関節でつながった部位（上腕と前腕、胴体と太ももなど）は比較しません。どんなポーズでも関節まわりで皮膚が重なるためです。`diagnostics.html` は元動画を埋め込み（`ffmpeg` が必要）、three.js を CDN から読み込むため、3D ビューにはインターネット接続が必要です。この 3D ビューは y = 0 に固定の床マーカーを描きます。0.5 m ごとに十字、1 m ごとに大きい十字、原点は緑で、キャラクターが動いているかを判断できます。交差トラックの上にある琥珀色のレーンは、目で見て気づいた問題を書く場所です（範囲をドラッグするか、**In** / **Out**）。右の **ノート**（Notes）一覧に並び、行をクリックするとその先頭フレームへ移ります。**ノートをダウンロード**（Download notes）は、これらのメモと交差の一覧をまとめて保存します。ファイル名はその動画の名前で、動画のパスも記録されます。

### 7. 指（`--detect-hands`）

普通の `m2mr run` は体だけを動かし、Mixamo の指のボーンはレストのままです。`--detect-hands` は、体の抽出器と一緒に動く手のモデルをオンにします。既定の抽出器 GVHMR では、そのモデルは [HaMeR](https://github.com/geopavlakos/hamer) です。HaMeR は、GVHMR がすでに選んだ人とフレームから手首を切り出します。クリップの中から別の人を探し直すことはありません。

**所要時間はおよそ 2 倍になります。** フラグなしで数分で終わるクリップは、`--detect-hands` を付けるとおよそその 2 倍かかります。手の処理が体の抽出の上に乗るためです。長い動画では、始める前にこの時間を見込んでください。

上の表のとおり `MANO_RIGHT.pkl` を置いてから：

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

最初の `--detect-hands` 実行は、HaMeR のウェイトを `weights/hamer/` にダウンロードします（約 2.7 GB、一度だけ）。指の回転は `skeleton_motion.npz` に書き込まれ、スキン付きキャラクターの Mixamo 指ボーン 30 本を駆動します。体の処理で手首がはっきり見えなかった手は、レストのままです。

`--hand-smooth` は、これらの回転に何秒分の平滑化をかけるかです。既定は `0.08` です。`0` は生の推定を残します。スケルトンファイルにすでに手の動きが入っていれば平滑化は行われます。後からそのファイルだけを再利用する実行も含みます。

以前のスケルトンを再利用するとき：

- ファイルにすでに手の動きがある：`--skeleton` だけで指が動きます。`--detect-hands` はもう要りません。
- 手の動きはないが、その実行の体のキャッシュがまだ横にある（`cache/<clip>/0_input_video.mp4` と `preprocess/vitpose.pt`、`preprocess/bbx.pt`）：`--skeleton ... --detect-hands` で、体を再抽出せずに指を足せます。
- そのキャッシュが無い：動画または写真を `--detect-hands` 付きでもう一度実行します。

## 出力

各 `m2mr run` は**コマンド開始時刻**でディレクトリを作ります。ルートのファイルは動画も写真も同じで、プレビューフォルダだけが変わります。

```
outputs/20260829_193205_dance/          # 写真実行は …_pose/
├── run.json                            # 開始時刻、入力、完全なコマンド
├── skeleton_motion.npz                 # 人体 3D スケルトン（--skeleton で再利用）
├── mixamo_rotations.npz                # Mixamo ボーンごとの回転
├── mixamo_character.glb                # スキン付きキャラクター、Blender / Unity にインポート
├── diagnostics.json                    # 自己交差レポート（クイックスタートの手順 6 を参照）
├── diagnostics.html                    # `m2mr diagnose <run> --visualize` の実行後のみ
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

`--detect-hands` を付けると、`skeleton_motion.npz` に指の回転も入り、`mixamo_rotations.npz` と `mixamo_character.glb` には 30 本の指のボーンが含まれます。このフラグがなく、再利用するスケルトンにも手の動きが無いときは、それらのボーンはレストのままです。

`mixamo_character.glb` は Blender で File → Import → glTF 2.0 (.glb/.gltf) で開きます。カメラが空を向いているときはキャラクターのメッシュを選び、View → Frame Selected。頭と手の球の塊はメッシュではなくボーン表示です。Outliner で **Icosphere** と **armature** を非表示にし、スキン付きメッシュは残してください。再生を元の長さに合わせ、フレーム番号を `diagnostics.json` とそろえるには、シーンの FPS を `run.json` の `fps` に、タイムラインを 0 〜 `n_frames` − 1 フレームに設定します。動画実行は `videos/mixamo_character.mp4`、写真実行は `images/mixamo_character.png` または周回クリップと見比べてください。

## ライセンス

このリポジトリのコードは Apache-2.0 です。自分で取得したアセットにはそれぞれの条件があり、このリポジトリと一緒に再配布してはいけません：

- **SMPL-X**：MPI による提供制限。既定は非商用の研究 / 教育 / 芸術；商用は別契約
- **MANO**（`--detect-hands` を使うときだけ）：SMPL-X と同じく MPI の提供制限。`MANO_RIGHT.pkl` は手元に置き、再配布しない
- **Mixamo FBX**：製品に入れてよい；元の FBX をアセットパックとして再配布してはいけない
- **GVHMR および他の推論ウェイト**：初回 `m2mr run` で `weights/` に自動ダウンロード、各アップストリームのライセンス
- **HaMeR**：このリポジトリ内の推論コードは MIT。ウェイトは初回の `m2mr run --detect-hands` で `weights/hamer/` に入り、アップストリームの公開条件に従う

## 連絡先

ご不明点がある場合、ローカル環境の構築でお手伝いが必要な場合、または協業をご相談したい場合は、メールでご連絡ください：
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
