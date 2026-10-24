# Motion2MixamoRig

<p align="center">
  <a href="#yêu-cầu"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.vi.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · Tiếng Việt · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Chuyển chuyển động của một người trong video — hoặc tư thế trong một bức ảnh tĩnh — sang nhân vật 3D đã được rig bằng Adobe Mixamo.

Dành cho nhà phát triển game: đưa vào một video hành động có **một người duy nhất** (hoặc một ảnh tĩnh) cùng một nhân vật Mixamo; công cụ sẽ xuất các video xem trước và một tệp nhân vật đã skin (`.glb`) để bạn kéo thẳng vào Blender hoặc Unity.

> Motion2MixamoRig hiện vẫn đang ở giai đoạn thử nghiệm. Phiên bản 0.1.8 là pipeline dòng lệnh. Kho mã này cũng có một Blender 4.2+ Extension chạy chính pipeline đó trong một môi trường Python bên ngoài. Tự build add-on từ mã nguồn: [`blender_extension/README.md`](../../blender_extension/README.md).

## Hai cách sử dụng

### 🎨 Trong Blender — không cần lập trình

1. Tải tệp zip cho nền tảng của bạn, ví dụ `motion2mixamorig-<version>-macos-arm64.zip`, từ [bản phát hành mới nhất](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. Trong Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, chọn tệp zip.
3. 3D Viewport → nhấn **N** → tab **Motion2MixamoRig** → **Cài runtime (một cú nhấp)** (Install Runtime (one click)).
4. **Chọn mô hình SMPL-X…** (Choose SMPL-X Model…) (tải miễn phí) và chọn một tệp FBX nhân vật Mixamo.
5. Chọn một video có một người → **Tạo chuyển động** (Generate Motion).

Hướng dẫn từng bước, mẹo và cách cập nhật: **[Hướng dẫn sử dụng](user-guide.vi.md)**. Đã kiểm thử trên macOS (Apple Silicon).

### 💻 Dòng lệnh — dành cho nhà phát triển

Clone kho mã và tự chạy pipeline: bắt đầu từ [Yêu cầu](#yêu-cầu).

Agent nên bắt đầu từ [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Mở <a href="../assets/demo.mp4">demo.mp4</a> trong kho mã này.</sub>
</p>

Một bản demo khác:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Báo cáo chẩn đoán (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Yêu cầu

Python 3.11+. Sau khi clone, hãy tạo virtualenv và cài các phụ thuộc; khi đó lệnh `m2mr` sẽ dùng được:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Cài các phụ thuộc và dự án này. chumpy (một gói cũ trong chuỗi phụ thuộc)
# import pip trong script setup của nó, nên sẽ báo lỗi "No module named 'pip'"
# trong môi trường build cô lập mặc định của pip. Hãy cài nó trước với chế độ
# cô lập đã tắt, rồi mới cài dự án này.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Trọng số suy luận (GVHMR, v.v.) không được tải ở bước này. Lần `m2mr run` đầu tiên sẽ tự tải chúng về `weights/` (~5 GB, chỉ một lần). Lần `m2mr run --detect-hands` đầu tiên cũng tải trọng số bàn tay HaMeR về `weights/hamer/` (~2,7 GB, chỉ một lần).

Nên cài thêm ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Pipeline vẫn chạy được khi không có nó, nhưng video đầu ra sẽ **không có tiếng** và không phát được trong trình duyệt.

## Trước khi chạy: đặt các tệp này vào `assets/`

Kho mã này không kèm các tệp dưới đây; bạn phải tự tải về. Tên tệp SMPL-X phải khớp chính xác với bảng; tên tệp FBX, video và ảnh thì tùy ý. Mỗi lần chạy cần SMPL-X, một nhân vật Mixamo, và **hoặc** một video **hoặc** một ảnh tĩnh. Nhân vật Mixamo được xuất lại từ Cinema 4D cũng dùng được; xem [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Tệp | Vị trí | Nơi tải |
|---|---|---|
| Mô hình cơ thể SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Đăng ký tại [SMPL-X](https://smpl-x.is.tue.mpg.de/) rồi tải về |
| FBX nhân vật Mixamo | `assets/mixamo/Y_Bot.fbx` | Dùng tài khoản Adobe để tải Y Bot (hoặc bất kỳ nhân vật nào đã rig bằng Mixamo) từ [Mixamo](https://www.mixamo.com) |
| Video hành động | `assets/video/<your_clip>.mp4` | Một đoạn video có **đúng một** người nhìn rõ, **từ đầu đến chân luôn nằm trong khung hình** (có thể để nhiều tệp; mỗi lần chạy dùng tệp được thêm vào gần nhất) |
| Ảnh tư thế (tùy chọn) | `assets/image/<your_photo>.jpg` | Một bức ảnh có **đúng một** người nhìn rõ, **từ đầu đến chân nằm trong khung hình**. Dùng với `--image` |
| Bàn tay phải MANO (chỉ khi dùng `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Đăng ký tại [MANO](https://mano.is.tue.mpg.de/) và tải **Models & Code**. Một lần chạy chỉ có thân người không cần tệp này |

Lưu ý: tệp tải từ Mixamo có tên `Y Bot.fbx` (**dấu cách**), khác đúng một ký tự so với `Y_Bot.fbx` (**dấu gạch dưới**) trong bảng.
Đổi tên sang dạng gạch dưới thì nó sẽ thành rig mặc định (`m2mr run` không cần `--rig`). Giữ nguyên dấu cách cũng được — nếu không có `Y_Bot.fbx`, tệp `.fbx` đầu tiên trong `assets/mixamo/` sẽ được dùng.

`assets/video/` có thể chứa nhiều video. Khi không có `--video` hoặc `--image`, lần chạy sẽ dùng tệp **được thêm vào gần nhất** trong `assets/video/`; nếu thư mục đó trống, nó sẽ chuyển sang ảnh tĩnh mới nhất trong `assets/image/`.
Mỗi video hoặc ảnh chỉ được có một người, **từ đầu đến chân nằm trong khung hình** — không bị cắt ở mép. `m2mr doctor` / `m2mr run` sẽ dừng trước bước trích xuất nếu có hai người trong khung hình.

## Bắt đầu nhanh

Kết quả nằm trong `outputs/<run-time>_<source>/`. Lần chạy với video ghi vào `videos/`; lần chạy với ảnh tĩnh ghi vào `images/`.

### 1. Kiểm tra tài nguyên và môi trường

Mọi thứ còn thiếu sẽ được in ra kèm nơi tải và nơi đặt tệp.

```bash
m2mr doctor
```

`m2mr doctor` kiểm tra lần chạy thân người. Nó không yêu cầu mô hình bàn tay MANO. Để kiểm tra cả tệp bổ sung và các gói Python dùng cho nhận dạng ngón tay:

```bash
m2mr doctor --detect-hands
```

### 2. Lần chạy đầu tiên: có kết quả trên màn hình

Không có tham số nào, lệnh này dùng **tệp mới nhất trong `assets/video/`** và `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Đây là bước chậm. Lần chạy đầu tiên tải ~5 GB trọng số suy luận (chỉ một lần), sau đó trích xuất chuyển động người từ video.
Trên CPU, một đoạn video ~30 giây mất khoảng 8–15 phút để trích xuất; các lần chạy sau với độ dài tương tự, khi trọng số đã có sẵn, mất khoảng 3–5 phút.
Retarget và render thường mất một hai phút. Dùng lại khung xương bằng `--skeleton` ở phần tiếp theo sẽ bỏ qua hoàn toàn bước trích xuất và xong trong vài chục giây.

Bàn chân đã đặt xuống được ghim theo mặc định: phần trước bàn chân khi phần đó chạm đất, gót chỉ khi các ngón nhấc lên. Nếu chân duỗi thẳng vẫn không với tới, hông sẽ dịch. Sau đó lòng bàn chân được đặt lên sàn (y = 0). `--no-foot-lock` giữ nguyên retarget thô, nên bàn chân có thể trượt; lòng bàn chân vẫn được đặt lên sàn.

### 3. Cùng chuyển động, nhân vật khác

Tải thêm một nhân vật khác từ Mixamo vào `assets/mixamo/`. **Đừng chạy lại chỉ với `--rig`** — như vậy sẽ lặp lại bước trích xuất chậm.
Truyền `--skeleton` để dùng lại khung xương từ lần chạy trước; vài phút sẽ rút xuống còn vài chục giây:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Một video khác

`--video` chọn đoạn video. Có thể kết hợp tự do với `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Một ảnh tĩnh (tư thế tĩnh)

`--image` khôi phục một **tư thế 3D tĩnh** từ ảnh chụp một người, rồi retarget nó lên nhân vật Mixamo giống như lần chạy với video. Bản xem trước gồm bốn ảnh tĩnh trong `images/` (cùng các góc nhìn như lần chạy video), cùng một đoạn quay quanh trái/phải `before_after_360_compare.mp4`. Không truyền `--video` cùng lúc.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` không kèm đường dẫn sẽ dùng tệp được thêm vào gần nhất trong `assets/image/`.

### 6. Kiểm tra tự giao cắt

Mỗi lần chạy còn kiểm tra nhân vật hoàn chỉnh xem có **tự giao cắt** không — một bộ phận cơ thể đi vào bộ phận khác, như tay nằm trong đầu — và ghi `diagnostics.json`. Terminal in ra một dòng, ví dụ `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Sàn không được kiểm tra.

Để kiểm tra lại một lần chạy, hoặc để xem các vấn đề:

```bash
m2mr diagnose outputs/<run>                  # ghi lại diagnostics.json
m2mr diagnose outputs/<run> --visualize      # thêm diagnostics.html: video nguồn cạnh nhân vật, timeline, danh sách vấn đề có thể bấm
m2mr diagnose outputs/<run> --threshold-cm 2 # chỉ báo các chỗ xuyên sâu hơn 2 cm (mặc định 1)
```

Mỗi vấn đề trong `diagnostics.json` là một cặp bộ phận cơ thể, kèm các khoảng khung hình mà chúng giao cắt, khung hình tệ nhất và độ sâu của nó. Số khung hình đếm từ 0, giống timeline của Blender sau khi nhập glTF. Các bộ phận nối với nhau bằng khớp (cánh tay trên và cẳng tay, thân và đùi, …) không được so sánh: da của chúng chồng lên nhau quanh khớp ở mọi tư thế. `diagnostics.html` nhúng video nguồn (cần `ffmpeg`) và tải three.js từ CDN, nên chế độ xem 3D cần kết nối internet. Chế độ xem này vẽ các mốc sàn cố định trên y = 0: một dấu cộng mỗi 0,5 m, một dấu lớn hơn mỗi mét, và một dấu xanh lục tại gốc tọa độ, để xem nhân vật có đang di chuyển hay không. Làn màu hổ phách phía trên các dải giao cắt dùng để ghi điều chỉ mắt mới thấy (kéo một khoảng, hoặc **In** / **Out**). Danh sách **Notes** bên phải hiện chúng; bấm một dòng để nhảy tới đó. **Download notes** lưu các ghi chú này cùng danh sách giao cắt. Tệp được đặt tên theo video nguồn và ghi đường dẫn của video đó.

### 7. Ngón tay (`--detect-hands`)

Một `m2mr run` thông thường chỉ cử động thân người và để xương ngón tay Mixamo ở tư thế nghỉ. `--detect-hands` bật mô hình bàn tay đi cùng bộ trích xuất thân. Với bộ trích xuất mặc định, GVHMR, mô hình đó là [HaMeR](https://github.com/geopavlakos/hamer). HaMeR cắt cổ tay từ người và các khung hình mà GVHMR đã chọn. Nó không tìm thêm người thứ hai trong clip.

**Thời gian tăng khoảng gấp đôi.** Clip nào không có cờ thì xong trong vài phút, có `--detect-hands` thì mất khoảng gấp đôi, vì lượt bàn tay chạy chồng lên bước trích xuất thân. Với video dài, hãy tính thời gian này trước khi bắt đầu.

Đặt `MANO_RIGHT.pkl` như bảng ở trên, rồi:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Lần chạy `--detect-hands` đầu tiên tải trọng số HaMeR về `weights/hamer/` (~2,7 GB, một lần). Góc xoay ngón tay được ghi vào `skeleton_motion.npz` và điều khiển 30 xương ngón tay Mixamo trên nhân vật đã skin. Cổ tay nào bước thân không nhìn rõ thì bàn tay đó giữ nguyên tư thế nghỉ.

`--hand-smooth` là số giây làm mượt áp lên các góc xoay đó. Mặc định là `0.08`. `0` giữ ước lượng thô. Việc làm mượt chạy mỗi khi tệp khung xương đã có chuyển động bàn tay, kể cả lần chạy sau chỉ dùng lại tệp đó.

Khi dùng lại một khung xương trước đó:

- Tệp đã có chuyển động bàn tay: `--skeleton` tự điều khiển các ngón. Không cần `--detect-hands` lần nữa.
- Chưa có, nhưng bộ nhớ đệm thân của lần chạy đó vẫn nằm cạnh (`cache/<clip>/0_input_video.mp4`, cùng `preprocess/vitpose.pt` và `preprocess/bbx.pt`): `--skeleton ... --detect-hands` thêm các ngón mà không trích xuất lại thân.
- Bộ nhớ đệm đó đã mất: chạy lại video hoặc ảnh với `--detect-hands`.

## Đầu ra

Mỗi lần `m2mr run` tạo một thư mục được đặt tên theo **thời điểm lệnh bắt đầu**. Các tệp ở thư mục gốc giống nhau cho video và ảnh tĩnh; chỉ thư mục xem trước là khác.

```
outputs/20260829_193205_dance/          # hoặc …_pose/ với ảnh tĩnh
├── run.json                            # thời điểm bắt đầu, đầu vào, lệnh đầy đủ
├── skeleton_motion.npz                 # khung xương người 3D (dùng lại với --skeleton)
├── mixamo_rotations.npz                # góc xoay Mixamo theo từng xương
├── mixamo_character.glb                # nhân vật đã skin, nhập vào Blender / Unity
├── diagnostics.json                    # báo cáo tự giao cắt (xem bước 6 của Bắt đầu nhanh)
├── diagnostics.html                    # chỉ có sau `m2mr diagnose <run> --visualize`
└── videos/   hoặc   images/            # bản xem trước — tùy theo đầu vào
```

**Đầu vào video** ghi ra `videos/` (cùng tỉ lệ khung hình với đoạn video):

```
videos/
├── human_skeleton.mp4                  # khung xương người 3D đã khôi phục
├── mixamo_skeleton.mp4                 # khung xương rig Mixamo
├── mixamo_character.mp4                # nhân vật Mixamo đã skin
└── compare.mp4                         # 2×2: bản gốc (trên trái) / khung xương Mixamo (trên phải)
                                        #      khung xương người (dưới trái) / nhân vật (dưới phải)
```

**Đầu vào ảnh tĩnh** thay vào đó ghi ra `images/` (cùng bốn góc nhìn, cộng thêm một vòng xoay):

```
images/
├── human_skeleton.png                  # khung xương người 3D đã khôi phục
├── mixamo_skeleton.png                 # khung xương rig Mixamo
├── mixamo_character.png                # nhân vật Mixamo đã skin
├── compare.png                         # 2×2: bản gốc (trên trái) / khung xương Mixamo (trên phải)
│                                       #      khung xương người (dưới trái) / nhân vật (dưới phải)
└── before_after_360_compare.mp4        # trái: ảnh gốc
                                        # phải: quay quanh rig mỗi bước 10° (trọn một vòng)
```

Khi có `--detect-hands`, `skeleton_motion.npz` còn lưu góc xoay các ngón, còn `mixamo_rotations.npz` và `mixamo_character.glb` gồm 30 xương ngón tay. Không có cờ này, và khung xương dùng lại cũng không có chuyển động bàn tay, những xương đó giữ nguyên tư thế nghỉ.

Mở `mixamo_character.glb` trong Blender: File → Import → glTF 2.0 (.glb/.gltf). Nếu camera đang hướng vào khoảng trống, hãy chọn mesh nhân vật rồi dùng View → Frame Selected. Cụm hình cầu trên đầu và tay là phần hiển thị xương, không phải mesh: trong Outliner, ẩn **Icosphere** và **armature**; giữ mesh đã skin ở trạng thái hiển thị. Đặt FPS của scene theo `run.json` (`fps`) và timeline từ khung hình 0 đến `n_frames` − 1 để phát lại khớp với nguồn và số khung hình khớp với `diagnostics.json`. So sánh lần chạy video với `videos/mixamo_character.mp4`, lần chạy ảnh tĩnh với `images/mixamo_character.png` hoặc đoạn quay quanh.

## Giấy phép

Mã nguồn của kho này theo giấy phép Apache-2.0. Các tài nguyên bạn tự tải về có điều khoản riêng và không được phân phối lại cùng kho mã này:

- **SMPL-X**: truy cập qua MPI; mặc định chỉ dùng cho nghiên cứu / giáo dục / nghệ thuật phi thương mại; sử dụng thương mại cần thỏa thuận riêng
- **MANO** (chỉ khi dùng `--detect-hands`): truy cập qua MPI, cách tải giống SMPL-X; để `MANO_RIGHT.pkl` ở máy và đừng phân phối lại
- **Mixamo FBX**: được dùng trong sản phẩm phát hành; không phân phối lại FBX gốc dưới dạng gói tài nguyên
- **GVHMR và các trọng số suy luận khác**: tự động tải về `weights/` trong lần `m2mr run` đầu tiên, theo giấy phép của từng dự án gốc
- **HaMeR**: mã suy luận trong kho này là MIT; trọng số được tải vào `weights/hamer/` ở lần `m2mr run --detect-hands` đầu tiên, theo điều khoản phát hành của dự án gốc

## Liên hệ

Nếu bạn gặp vấn đề, cần hỗ trợ hoàn tất cài đặt cục bộ, hoặc muốn trao đổi về hợp tác, hãy gửi email tới:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
