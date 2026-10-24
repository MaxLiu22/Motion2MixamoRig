# Motion2MixamoRig for Blender — ユーザーガイド

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · 日本語 · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

一人の人物が映った動画を、Blender の中でアニメーション付きの Mixamo キャラクターに変換します。
コーディングもターミナル操作も不要です。

<!-- video: link the tutorial video here -->

> 現時点でテスト済みなのは **macOS（Apple Silicon）** のみです。Windows 版は近日公開です。

## 必要なもの

- **Blender 4.2 以降**
- **インターネット接続**（初回セットアップ時）
- **約 8 GB の空きディスク容量**（ランタイム約 1.3 GB + モデル約 5.6 GB）
- **無料の SMPL-X アカウント**と**無料の Adobe アカウント**（Mixamo 用）。手順 4 と 5 を参照

## 1. アドオンをダウンロード

[最新リリース](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)を開き、
お使いのコンピューター用の zip をダウンロードします：

| お使いのコンピューター | ファイル |
| --- | --- |
| Apple Silicon 搭載の Mac（M1/M2/M3/M4） | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **近日公開** |

たとえば `motion2mixamorig-0.1.8-macos-arm64.zip` の場合、`0.1.8` がアドオンの
バージョン、`macos-arm64` がプラットフォームです。違うものを選ぶと Blender は
インストールを拒否し、想定しているプラットフォームを表示します。

zip は**展開しないでください**。Blender が zip をそのままインストールします。

## 2. Blender にインストール

1. **Edit → Preferences → Get Extensions**
2. 右上の小さな **∨** をクリック → **Install from Disk…**
3. zip を選択します。**Motion2MixamoRig** が有効な状態で一覧に表示されます。
4. Preferences を閉じます。3D Viewport で **N** を押し、右側の
   **Motion2MixamoRig** タブをクリックします。

<!-- screenshot: Install from Disk menu -->

## 3. ランタイムをインストール（初回のみ）

パネルで **ランタイムをインストール（ワンクリック）**（Install Runtime (one click)）をクリックします。

アドオンが専用の Python とライブラリ（約 1.4 GB）を `~/Motion2MixamoRig/` に
ダウンロードします。コンピューター上のほかのものには一切触れません。数分かかり、
プログレスバーに現在のステップが表示されます。

<!-- screenshot: Install Runtime button and progress -->

## 4. SMPL-X ボディモデルを入手

SMPL-X はアドオンが必要とする無料のボディモデルです。ライセンス上、アドオンに
同梱できないため、一度だけご自身でダウンロードしてください：

1. [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) を開いて **Register** します。
   ライセンスに同意し、確認メールで登録を完了します。
2. ログインして **Download** を開き、SMPL-X モデル（**NPZ** 版）をダウンロードします。
3. 展開して **`SMPLX_NEUTRAL.npz`** を探します。
4. Blender で **SMPL-X モデルを選択…**（Choose SMPL-X Model…）をクリックし、そのファイルを
   選びます。パネルに **SMPL-X モデル: 検出済み**（SMPL-X model: found）と表示されます。

<!-- screenshot: SMPL-X download page -->

## 5. Mixamo キャラクターを入手

1. [mixamo.com](https://www.mixamo.com/) を開き、Adobe アカウントでサインインします。
2. **Characters** タブ → キャラクターを選びます（例：**Y Bot**）。
3. **Download** → Format は **FBX Binary (.fbx)**、Pose は **T-pose** → Download。

<!-- screenshot: Mixamo download dialog -->

## 6. モーションを生成

**入力**（Input）ボックスで：

1. **ソースの種類**（Source Type）：**動画**（Video）（単一のポーズなら **画像**（Image））
2. **ソースファイル**（Source File）：使用するクリップ。**映っているのは一人だけで、
   最初から最後まで頭からつま先までフレームに収まっている**必要があります。
3. **Mixamo リグ FBX**（Mixamo Rig FBX）：手順 5 のキャラクター
4. **手を検出**（Detect Hands）はオフです。指を動かしたいときだけオンにします。
   そのあと **MANO ハンドモデルを選択…**（Choose MANO Hand Model…）をクリックし、`MANO_RIGHT.pkl` を選びます。
   このファイルは SMPL-X と同じ手順で入手します。[mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/) で登録し、
   **Models & Code** をダウンロードして解凍します。手を初めて処理するときは、さらに約 **2.7 GB** を一度だけ
   ダウンロードし、体だけの実行のおよそ 2 倍の時間がかかります。オンにすると **Finger Smoothing (seconds)** も出ます。指の動きをなめらかにします。既定は 0.08 秒で、0 にすると検出したままです。
5. **モーションを生成**（Generate Motion）をクリック

完了すると、アニメーション付きのキャラクターが自動的にシーンへインポートされます。着地した足はその位置に留まり、足の裏は Blender の床に置かれます。その床には **床マーカー**（Floor Markers）のメッシュが追加されます（0.5 m ごとの十字）。進行状況 / 結果の **床マーカー**（Floor Markers）チェックボックスで表示と非表示を切り替えます。

### 初回実行は時間がかかります（正常です）

初回は、アドオンが約 **5.6 GB** のモデルをダウンロードします。パネルにダウンロード
サイズ、速度、残り時間が表示されます。モデルのダウンロードは一度だけです。

その後、動画はお使いのコンピューター上で処理されます。Mac の CPU では、
10 秒のクリップで数分かかります。処理中も Blender は操作でき、
**キャンセル**（Cancel）でジョブを停止できます。

## うまくいくコツ

- 一人だけ、全身が映っていて、画面の端で切れていないこと
- カメラを固定し、明るい場所で。ゆったりした服やなびく服より、シンプルな服で
- まずは短いクリップ（5〜20 秒）で試すと早く結果が出ます

## 新しいバージョンに更新

アドオンは頻繁に更新されます。更新手順：

1. [最新リリース](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)から
   最新の zip をダウンロードします。
2. **Get Extensions** → 古い **Motion2MixamoRig** を削除し、Blender を完全に終了
   （**Cmd+Q**）して再起動し、新しい zip をインストールします。
3. パネルで **ランタイムを更新**（Update Runtime）をクリックします。

更新ではダウンロード済みのモデルが残るので、すぐに終わります。インストール済みの
バージョンは **Get Extensions** のアドオン名の横に表示されます。

## パネルの構成

- **タイトル横の ⚙** で **セットアップ**（Setup）ボックスを表示 / 非表示にします。
- **セットアップ**：言語、ランタイム、SMPL-X、**デバイス**（Device。CPU が無難です）、
  **環境を確認**（Check Environment）。
- **入力**：アニメーションにする素材、**ボディモデル**（Body Model。GVHMR）、**手を検出**（Detect Hands）。
- **進行状況 / 結果**（Progress / Result）：進行状況、最近のログ。ジョブ完了後は
  **生成したキャラクターをインポート**（Import Generated Character）、
  **床マーカー**（Floor Markers）チェックボックス、
  **出力フォルダーを開く**（Open Output Folder）、**ログを表示**（View Full Log）。
- **診断**（Diagnostics）：キャラクターの体の部位がめり込んでいる箇所（手が頭に入り込む、腕を組んだときに腕同士がめり込むなど）。バーの赤いセルは問題のあるフレームで、クリックするとそこへ移動します。バーの下の三角は現在のフレームを示し、その下にこのフレームでめり込んでいる部位と深さが表示されます。**前へ** / **次へ**（Previous / Next）で問題間を移動します。**HTML レポートを開く**（Open HTML Report）は、元動画とキャラクターを並べたレポートをブラウザで開きます（初回は作成に約 15 秒かかります）。元の動画を出すには、パソコンに ffmpeg が必要です（Mac では `brew install ffmpeg`）。入っていないと、キャラクターは表示されますが、横の動画は空のままです。キャラクターは 0.5 m ごとの固定の床十字の上に立ち、滑っているかどうかが見えます。赤いトラックの上にある琥珀色のレーンは、目で見て気づいたことを書く場所です。右の **ノート**（Notes）一覧に並び、行をクリックするとそこへ移ります。**ノートをダウンロード**（Download notes）は、これらのメモと交差している時間をまとめて保存します。ファイル名はその動画の名前です。

アドオンは 19 言語に対応しています。**自動（Blender / システム）**（Auto (Blender / System)）は
Blender の言語に従います。セットアップボックスの **UI 言語**（UI Language）で変更できます。

## うまくいかないとき

| 表示される内容 | 対処 |
| --- | --- |
| **ランタイムのインストールに失敗しました**（Runtime installation failed） | インターネット接続を確認し、もう一度ボタンをクリックします。ログ：`~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X モデル: 未検出**（SMPL-X model: missing） | 手順 4 をやり直し、`SMPLX_NEUTRAL.npz` を選びます |
| **MANO ハンドモデル: 未検出**（MANO hand model: missing） | **手を検出**をオンにして、**MANO ハンドモデルを選択…**で `MANO_RIGHT.pkl` を選びます |
| **Mixamo FBX が無効です**（Mixamo FBX invalid） | キャラクターを **FBX Binary**、**T-pose** で再ダウンロードします |
| **入力に複数人が写っています**（Input contains multiple people） | 一人だけが映ったクリップを使います |
| **入力から人物を検出できませんでした**（No person was detected in the input） | 全身が映っていて明るいことを確認します |
| **パイプラインが予期せず終了しました**（Pipeline process exited unexpectedly） | **ログを表示** をクリックします |

サポートを依頼するときは、ログを添付し、使用しているアドオンのバージョンを伝えてください。

## アンインストール

1. **Get Extensions** → **Motion2MixamoRig** を削除します。
2. フォルダー **`~/Motion2MixamoRig`**（ホームフォルダー → `Motion2MixamoRig`）を
   削除します。アドオンを削除してもこのフォルダーは**削除されません**。中には約 7 GB の
   ランタイムとモデル、さらに `app/outputs/` に生成結果が入っています。

## ライセンス

Motion2MixamoRig は**非商用利用のみ**です。商用利用を認めていないライセンスの研究用
モデル（GVHMR や SMPL-X など）に依存しているためです。
[`NOTICE.md`](../../NOTICE.md) を参照してください。
