# Motion2MixamoRig cho Blender — Hướng dẫn sử dụng

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · Tiếng Việt · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Biến video có một người thành nhân vật Mixamo có hoạt ảnh, ngay trong Blender.
Không cần lập trình hay dùng terminal.

<!-- video: link the tutorial video here -->

> Hiện mới được kiểm thử trên **macOS (Apple Silicon)**. Bản Windows sắp ra mắt.

## Bạn cần có

- **Blender 4.2 trở lên**
- **Kết nối internet** cho lần thiết lập đầu tiên
- **Khoảng 8 GB dung lượng ổ đĩa trống** (runtime ~1.3 GB + mô hình ~5.6 GB)
- **Một tài khoản SMPL-X miễn phí** và **một tài khoản Adobe miễn phí** (cho Mixamo); xem bước 4 và 5

## 1. Tải add-on

Vào [bản phát hành mới nhất](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
và tải tệp zip phù hợp với máy của bạn:

| Máy của bạn | Tệp |
| --- | --- |
| Mac dùng Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Sắp có** |

Ví dụ `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` là phiên bản add-on,
`macos-arm64` là nền tảng. Nếu chọn nhầm tệp, Blender sẽ từ chối cài đặt và cho
biết nền tảng mà nó cần.

**Không** giải nén tệp. Blender tự cài tệp zip.

## 2. Cài vào Blender

1. **Edit → Preferences → Get Extensions**
2. Nhấp vào dấu **∨** nhỏ ở góc trên bên phải → **Install from Disk…**
3. Chọn tệp zip. **Motion2MixamoRig** xuất hiện trong danh sách, đã được bật.
4. Đóng Preferences. Trong 3D Viewport, nhấn **N**, rồi nhấp vào tab
   **Motion2MixamoRig** ở bên phải.

<!-- screenshot: Install from Disk menu -->

## 3. Cài runtime (một lần)

Trong bảng điều khiển, nhấp **Cài runtime (một cú nhấp)** (Install Runtime (one click)).

Add-on tải Python và các thư viện riêng của nó (~1.4 GB) vào
`~/Motion2MixamoRig/`. Nó không động đến bất kỳ thứ gì khác trên máy của bạn.
Quá trình này mất vài phút; thanh tiến trình hiển thị bước hiện tại.

<!-- screenshot: Install Runtime button and progress -->

## 4. Lấy mô hình cơ thể SMPL-X

SMPL-X là mô hình cơ thể miễn phí mà add-on cần. Giấy phép của nó không cho phép
chúng tôi phân phối kèm, nên bạn cần tự tải về, chỉ một lần:

1. Mở [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) và **Register**.
   Chấp nhận giấy phép và xác nhận email.
2. Đăng nhập, mở **Download**, và tải mô hình SMPL-X (bản **NPZ**).
3. Giải nén và tìm **`SMPLX_NEUTRAL.npz`**.
4. Trong Blender, nhấp **Chọn mô hình SMPL-X…** (Choose SMPL-X Model…) và chọn tệp
   đó. Bảng điều khiển sẽ hiển thị **Mô hình SMPL-X: đã có** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Lấy nhân vật Mixamo

1. Mở [mixamo.com](https://www.mixamo.com/) và đăng nhập bằng tài khoản Adobe.
2. Tab **Characters** → chọn một nhân vật (ví dụ **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Tạo chuyển động

Trong khung **Đầu vào** (Input):

1. **Loại nguồn** (Source Type): Video (hoặc Ảnh cho một tư thế đơn)
2. **Tệp nguồn** (Source File): clip của bạn. Clip phải có **đúng một người, lọt
   khung từ đầu đến chân trong suốt thời gian**.
3. **Mixamo Rig FBX**: nhân vật từ bước 5
4. **Nhận dạng bàn tay** (Detect Hands) đang tắt. Chỉ bật khi bạn muốn các ngón
   cử động. Rồi nhấp **Chọn mô hình bàn tay MANO…** (Choose MANO Hand Model…) và
   chọn `MANO_RIGHT.pkl`. Lấy tệp này giống SMPL-X: đăng ký tại
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), tải **Models & Code** và giải nén.
   Lần chạy bàn tay đầu tiên tải thêm khoảng **2.7 GB**, một lần, và mất khoảng gấp đôi
   thời gian so với lần chỉ chạy thân người. Khi bật, **Finger Smoothing (seconds)** cũng hiện ra. Nó làm chuyển động ngón tay mượt hơn. Mặc định là 0,08 giây; 0 giữ nguyên kết quả nhận dạng.
5. Nhấp **Tạo chuyển động** (Generate Motion)

Khi hoàn tất, nhân vật có hoạt ảnh sẽ tự động được nhập vào cảnh của bạn. Bàn chân đã đặt xuống đứng yên tại chỗ đáp, và lòng bàn chân nằm trên sàn của Blender. Trên sàn đó có thêm một mesh **Mốc sàn** (Floor Markers) (một dấu cộng mỗi 0,5 m). Ô **Mốc sàn** (Floor Markers) trong Tiến trình / Kết quả dùng để hiện hoặc ẩn nó.

### Lần chạy đầu tiên lâu hơn — điều này là bình thường

Lần đầu, add-on tải khoảng **5.6 GB** mô hình. Bảng điều khiển hiển thị dung
lượng tải, tốc độ và thời gian còn lại. Mô hình chỉ cần tải một lần.

Sau đó, video được xử lý trên máy của bạn. Trên CPU của Mac, một clip 10 giây
mất vài phút. Blender vẫn dùng được trong lúc chạy, và **Hủy** (Cancel) sẽ dừng
tác vụ.

## Mẹo để có kết quả tốt

- Chỉ một người, thấy toàn thân, không bị cắt ở mép khung hình
- Camera ổn định, ánh sáng tốt, quần áo gọn gàng thay vì rộng hoặc bay phấp phới
- Clip ngắn (5–20 giây) chạy nhanh hơn, nên thử trước

## Cập nhật lên phiên bản mới

Add-on được cập nhật thường xuyên. Để cập nhật:

1. Tải tệp zip mới nhất từ
   [bản phát hành mới nhất](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → gỡ **Motion2MixamoRig** cũ, thoát hẳn Blender
   (**Cmd+Q**), mở lại, rồi cài tệp zip mới.
3. Trong bảng điều khiển, nhấp **Cập nhật runtime** (Update Runtime).

Cập nhật vẫn giữ các mô hình đã tải, nên diễn ra nhanh. Phiên bản đã cài được
hiển thị bên cạnh add-on trong **Get Extensions**.

## Bảng điều khiển

- **⚙ cạnh tiêu đề** hiện hoặc ẩn khung **Thiết lập** (Setup).
- **Thiết lập**: ngôn ngữ, runtime, SMPL-X, **Thiết bị** (Device) (CPU là lựa
  chọn an toàn), và **Kiểm tra môi trường** (Check Environment).
- **Đầu vào**: thứ cần tạo hoạt ảnh, **Mô hình cơ thể** (Body Model, GVHMR) và **Nhận dạng bàn tay** (Detect Hands).
- **Tiến trình / Kết quả** (Progress / Result): tiến trình, nhật ký gần đây, và
  sau mỗi tác vụ là **Nhập nhân vật đã tạo** (Import Generated Character), **Mốc sàn** (Floor Markers),
  **Mở thư mục đầu ra** (Open Output Folder), **Xem toàn bộ nhật ký** (View Full Log).
- **Chẩn đoán** (Diagnostics): những chỗ các bộ phận cơ thể của nhân vật đâm
  vào nhau (tay nằm trong đầu, hai tay khoanh lại). Ô đỏ trên thanh là khung
  hình có vấn đề; bấm vào để nhảy tới đó. Tam giác dưới thanh đi theo khung
  hình hiện tại, bên dưới là các bộ phận đang giao cắt và độ sâu. **Trước** /
  **Tiếp** (Previous / Next) nhảy giữa các vấn đề. **Mở báo cáo HTML** (Open
  HTML Report) mở trong trình duyệt một báo cáo có video nguồn bên cạnh nhân
  vật (lần đầu mất khoảng 15 giây để tạo). Video gốc cần ffmpeg trên máy tính (trên Mac: `brew install ffmpeg`). Không có thì nhân vật vẫn hiện, còn video bên cạnh để trống. Nhân vật đứng trên các dấu cộng sàn cố định, mỗi 0,5 m một dấu, để xem nó có đang trượt hay không. Làn màu hổ phách phía trên các dải đỏ dùng để ghi điều bạn thấy bằng mắt. Chúng nằm trong danh sách **Notes** bên phải; bấm một dòng để nhảy tới đó. **Download notes** lưu các ghi chú này cùng thời điểm giao cắt. Tệp được đặt tên theo video nguồn.

Add-on hỗ trợ 19 ngôn ngữ. **Tự động (theo Blender / hệ thống)** (Auto (Blender / System))
đi theo ngôn ngữ của Blender; bạn có thể đổi trong khung **Thiết lập**, tại
**Ngôn ngữ giao diện** (UI Language).

## Nếu có sự cố

| Bạn thấy gì | Cần làm gì |
| --- | --- |
| **Cài runtime thất bại** (Runtime installation failed) | Kiểm tra kết nối internet và nhấp lại nút. Nhật ký: `~/Motion2MixamoRig/logs/setup.log` |
| **Mô hình SMPL-X: thiếu** (SMPL-X model: missing) | Làm lại bước 4 và chọn `SMPLX_NEUTRAL.npz` |
| **Mô hình bàn tay MANO: thiếu** (MANO hand model: missing) | Bật **Nhận dạng bàn tay**, rồi **Chọn mô hình bàn tay MANO…** và chọn `MANO_RIGHT.pkl` |
| **Mixamo FBX không hợp lệ** (Mixamo FBX invalid) | Tải lại nhân vật dưới dạng **FBX Binary**, **T-pose** |
| **Đầu vào có nhiều người** (Input contains multiple people) | Dùng clip chỉ có một người |
| **Không phát hiện người nào trong đầu vào** (No person was detected in the input) | Đảm bảo toàn thân hiện rõ và đủ sáng |
| **Tiến trình pipeline thoát bất ngờ** (Pipeline process exited unexpectedly) | Nhấp **Xem toàn bộ nhật ký** |

Khi cần trợ giúp, hãy đính kèm nhật ký và cho biết bạn đang dùng phiên bản add-on nào.

## Gỡ cài đặt

1. **Get Extensions** → gỡ **Motion2MixamoRig**.
2. Xóa thư mục **`~/Motion2MixamoRig`** (thư mục home của bạn →
   `Motion2MixamoRig`). Gỡ add-on **không** xóa thư mục này; nó chứa khoảng 7 GB
   runtime và mô hình, cùng các kết quả bạn đã tạo trong `app/outputs/`.

## Giấy phép

Motion2MixamoRig **chỉ dành cho mục đích phi thương mại**: nó dựa trên các mô
hình nghiên cứu (như GVHMR và SMPL-X) có giấy phép không cho phép sử dụng thương
mại. Xem [`NOTICE.md`](../../NOTICE.md).
