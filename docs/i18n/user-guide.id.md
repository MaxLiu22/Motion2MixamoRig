# Motion2MixamoRig untuk Blender — Panduan Pengguna

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · Bahasa Indonesia · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Ubah video satu orang menjadi karakter Mixamo yang beranimasi, langsung di Blender.
Tanpa coding dan tanpa terminal.

<!-- video: link the tutorial video here -->

> Sejauh ini baru diuji di **macOS (Apple Silicon)**. Versi Windows segera hadir.

## Yang kamu butuhkan

- **Blender 4.2 atau lebih baru**
- **Koneksi internet** untuk penyiapan pertama
- **Ruang disk kosong sekitar 8 GB** (runtime ~1,3 GB + model ~5,6 GB)
- **Akun SMPL-X gratis** dan **akun Adobe gratis** (untuk Mixamo); lihat langkah 4 dan 5

## 1. Unduh add-on

Buka [rilis terbaru](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
dan unduh zip untuk komputermu:

| Komputermu | File |
| --- | --- |
| Mac dengan Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Segera hadir** |

Contohnya `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` adalah versi
add-on, `macos-arm64` adalah platformnya. Kalau kamu salah pilih, Blender akan
menolak memasangnya dan menyebutkan platform yang seharusnya.

**Jangan** di-unzip. Blender akan memasang zip itu sendiri.

## 2. Pasang di Blender

1. **Edit → Preferences → Get Extensions**
2. Klik **∨** kecil di kanan atas → **Install from Disk…**
3. Pilih zip-nya. **Motion2MixamoRig** muncul di daftar dalam keadaan aktif.
4. Tutup Preferences. Di 3D Viewport tekan **N**, lalu klik tab
   **Motion2MixamoRig** di sebelah kanan.

<!-- screenshot: Install from Disk menu -->

## 3. Pasang runtime (sekali saja)

Di panel, klik **Pasang Runtime (sekali klik)** (Install Runtime (one click)).

Add-on akan mengunduh Python dan library-nya sendiri (~1,4 GB) ke
`~/Motion2MixamoRig/`. Add-on tidak menyentuh apa pun yang lain di komputermu.
Prosesnya beberapa menit; progress bar menampilkan langkah yang sedang berjalan.

<!-- screenshot: Install Runtime button and progress -->

## 4. Ambil model tubuh SMPL-X

SMPL-X adalah model tubuh gratis yang dibutuhkan add-on ini. Lisensinya tidak
mengizinkan kami menyertakannya, jadi kamu perlu mengunduhnya sendiri, sekali saja:

1. Buka [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) lalu **Register**.
   Setujui lisensinya dan konfirmasi email-nya.
2. Login, buka **Download**, lalu unduh model SMPL-X (versi **NPZ**).
3. Unzip dan cari **`SMPLX_NEUTRAL.npz`**.
4. Di Blender, klik **Pilih Model SMPL-X…** (Choose SMPL-X Model…) lalu pilih
   file itu. Panel kemudian menampilkan **Model SMPL-X: ditemukan** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Ambil karakter Mixamo

1. Buka [mixamo.com](https://www.mixamo.com/) dan login dengan akun Adobe.
2. Tab **Characters** → pilih karakter (misalnya **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Buat gerakan

Di kotak **Input**:

1. **Jenis Sumber** (Source Type): Video (atau **Gambar** (Image) untuk satu pose)
2. **File Sumber** (Source File): klipmu. Klip harus menampilkan **tepat satu
   orang, dari kepala sampai kaki masuk frame sepanjang waktu**.
3. **Mixamo Rig FBX**: karakter dari langkah 5
4. **Deteksi tangan** (Detect Hands) mati. Nyalakan hanya jika jari harus bergerak.
   Lalu klik **Pilih model tangan MANO…** (Choose MANO Hand Model…) dan pilih
   `MANO_RIGHT.pkl`. Berkas itu diambil seperti SMPL-X: daftar di
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), unduh **Models & Code**, lalu
   ekstrak. Proses tangan yang pertama mengunduh sekitar **2,7 GB** lagi, sekali, dan
   makan waktu kira-kira dua kali proses tubuh saja. Saat menyala, **Finger Smoothing (seconds)** muncul. Ia menghaluskan gerakan jari. Nilai bawaannya 0,08 detik; 0 mempertahankan yang terdeteksi.
5. Klik **Buat Gerakan** (Generate Motion)

Setelah selesai, karakter yang sudah beranimasi otomatis diimpor ke scene-mu. Kaki yang menapak tetap di tempat ia mendarat, dan telapak kaki diletakkan di lantai Blender. Di lantai itu ditambahkan mesh **Penanda lantai** (Floor Markers) (satu silang setiap 0,5 m). Kotak **Penanda lantai** (Floor Markers) di Progres / Hasil menampilkan atau menyembunyikannya.

### Proses pertama butuh waktu lebih lama — ini normal

Pada proses pertama, add-on mengunduh model sekitar **5,6 GB**. Panel
menampilkan ukuran unduhan, kecepatan, dan sisa waktu. Model hanya diunduh sekali.

Setelah itu, video diproses di komputermu. Di CPU Mac, klip 10 detik butuh
beberapa menit. Blender tetap bisa dipakai selama proses berjalan, dan
**Batal** (Cancel) menghentikan prosesnya.

## Tips agar hasilnya bagus

- Hanya satu orang, seluruh tubuh terlihat, tidak terpotong di tepi frame
- Kamera stabil, pencahayaan bagus, pakaian sederhana, bukan yang longgar atau berkibar
- Klip pendek (5–20 detik) lebih cepat untuk dicoba dulu

## Update ke versi baru

Add-on ini sering diperbarui. Cara update:

1. Unduh zip terbaru dari
   [rilis terbaru](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → hapus **Motion2MixamoRig** yang lama, tutup Blender
   sepenuhnya (**Cmd+Q**), buka lagi, lalu pasang zip yang baru.
3. Di panel, klik **Perbarui Runtime** (Update Runtime).

Update tetap menyimpan model yang sudah diunduh, jadi prosesnya cepat. Versi yang
terpasang ditampilkan di samping add-on di **Get Extensions**.

## Panel

- **⚙ di samping judul** menampilkan atau menyembunyikan kotak **Penyiapan** (Setup).
- **Penyiapan**: bahasa, runtime, SMPL-X, **Perangkat** (Device) (CPU adalah
  pilihan yang aman), dan **Periksa Lingkungan** (Check Environment).
- **Input**: apa yang mau dianimasikan, **Model tubuh** (Body Model, GVHMR), dan **Deteksi tangan** (Detect Hands).
- **Progres / Hasil** (Progress / Result): progres, log terbaru, dan setelah proses selesai
  **Impor Karakter Hasil** (Import Generated Character), **Penanda lantai** (Floor Markers), **Buka Folder Output**
  (Open Output Folder), **Lihat Log Lengkap** (View Full Log).
- **Diagnostik** (Diagnostics): tempat bagian tubuh karakter saling masuk
  (tangan di dalam kepala, lengan bersilang). Sel merah di bilah adalah frame
  yang bermasalah; klik salah satunya untuk pergi ke sana. Segitiga di bawah
  bilah mengikuti frame saat ini, dan di bawahnya tampil bagian yang saling
  tembus serta seberapa dalam. **Sebelumnya** / **Berikutnya** (Previous /
  Next) melompat antarmasalah. **Buka Laporan HTML** (Open HTML Report)
  membuka laporan di browser dengan video sumber di samping karakter (pertama
  kali butuh sekitar 15 detik untuk membuatnya). Video asli membutuhkan ffmpeg di komputer (di Mac: `brew install ffmpeg`). Tanpa itu karakternya ada, dan video di sebelahnya kosong. Karakter berdiri di atas silang lantai yang tetap, satu setiap 0,5 m, supaya terlihat apakah ia meluncur. Lajur amber di atas jalur merah untuk catatan yang kamu lihat dengan mata. Daftar **Notes** di kanan menampilkannya; klik satu baris untuk meloncat ke sana. **Download notes** menyimpan catatan itu bersama waktu perpotongan. Berkas dinamai sesuai video sumber.

Add-on ini tersedia dalam 19 bahasa. **Otomatis (ikut Blender / sistem)** (Auto)
mengikuti bahasa Blender; ubah di kotak Penyiapan pada **Bahasa Antarmuka** (UI Language).

## Kalau ada masalah

| Yang kamu lihat | Yang harus dilakukan |
| --- | --- |
| **Pemasangan runtime gagal** (Runtime installation failed) | Periksa koneksi internetmu lalu klik tombolnya lagi. Log: `~/Motion2MixamoRig/logs/setup.log` |
| **Model SMPL-X: tidak ada** (SMPL-X model: missing) | Ulangi langkah 4 dan pilih `SMPLX_NEUTRAL.npz` |
| **Model tangan MANO: tidak ada** (MANO hand model: missing) | Nyalakan **Deteksi tangan**, lalu **Pilih model tangan MANO…** dan pilih `MANO_RIGHT.pkl` |
| **Mixamo FBX tidak valid** (Mixamo FBX invalid) | Unduh lagi karakternya sebagai **FBX Binary**, **T-pose** |
| **Input berisi lebih dari satu orang** (Input contains multiple people) | Pakai klip yang hanya berisi satu orang |
| **Tidak ada orang yang terdeteksi di input** (No person was detected in the input) | Pastikan seluruh tubuh terlihat dan pencahayaannya cukup |
| **Proses pipeline berhenti tiba-tiba** (Pipeline process exited unexpectedly) | Klik **Lihat Log Lengkap** |

Saat minta bantuan, lampirkan log-nya dan sebutkan versi add-on yang kamu pakai.

## Uninstall

1. **Get Extensions** → hapus **Motion2MixamoRig**.
2. Hapus folder **`~/Motion2MixamoRig`** (folder home-mu →
   `Motion2MixamoRig`). Menghapus add-on **tidak** ikut menghapus folder ini,
   padahal isinya sekitar 7 GB runtime dan model, ditambah hasil yang sudah kamu
   buat di `app/outputs/`.

## Lisensi

Motion2MixamoRig **hanya untuk penggunaan non-komersial**: add-on ini memakai
model riset (seperti GVHMR dan SMPL-X) yang lisensinya tidak mengizinkan
penggunaan komersial. Lihat [`NOTICE.md`](../../NOTICE.md).
