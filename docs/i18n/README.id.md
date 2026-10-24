# Motion2MixamoRig

<p align="center">
  <a href="#prasyarat"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.id.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · Bahasa Indonesia · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Pindahkan gerakan seseorang dalam video — atau pose dalam sebuah foto — ke karakter 3D yang sudah di-rig dengan Adobe Mixamo.

Untuk developer game: berikan video aksi dengan **satu orang saja** (atau sebuah foto) dan satu karakter Mixamo; alat ini akan menghasilkan video pratinjau serta file karakter yang sudah di-skin (`.glb`) yang bisa langsung kamu masukkan ke Blender atau Unity.

> Motion2MixamoRig saat ini masih eksperimental. Versi 0.1.8 adalah pipeline baris perintah. Repositori ini juga menyertakan Blender 4.2+ Extension yang menjalankan pipeline yang sama di lingkungan Python eksternal. Membangun add-on dari source: [`blender_extension/README.md`](../../blender_extension/README.md).

## Dua cara memakainya

### 🎨 Di Blender — tanpa coding

1. Unduh zip untuk platformmu, misalnya `motion2mixamorig-<version>-macos-arm64.zip`, dari [rilis terbaru](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. Di Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, pilih zip-nya.
3. 3D Viewport → tekan **N** → tab **Motion2MixamoRig** → **Pasang Runtime (sekali klik)** (Install Runtime (one click)).
4. **Pilih Model SMPL-X…** (Choose SMPL-X Model…) (unduhan gratis) dan pilih FBX karakter Mixamo.
5. Pilih video satu orang → **Buat Gerakan** (Generate Motion).

Petunjuk langkah demi langkah, tips, dan cara update: **[Panduan Pengguna](user-guide.id.md)**. Sudah diuji di macOS (Apple Silicon).

### 💻 Baris perintah — untuk developer

Clone repositori ini dan jalankan pipeline-nya sendiri: mulai dari [Prasyarat](#prasyarat).

Agent sebaiknya mulai dari [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Buka <a href="../assets/demo.mp4">demo.mp4</a> di repositori ini.</sub>
</p>

Demo lainnya:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Laporan diagnostik (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Prasyarat

Python 3.11+. Setelah clone, buat virtualenv dan pasang dependensinya; setelah itu perintah `m2mr` bisa digunakan:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Pasang dependensi dan proyek ini. chumpy (paket lama di rantai dependensi)
# meng-import pip di skrip setup-nya, sehingga gagal dengan "No module named 'pip'"
# di build terisolasi bawaan pip. Pasang paket itu dulu dengan isolasi dimatikan,
# lalu pasang proyek ini.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Bobot inferensi (GVHMR, dll.) tidak diunduh pada langkah ini. `m2mr run` pertama akan mengunduhnya ke `weights/` (~5 GB, sekali saja). `m2mr run --detect-hands` pertama juga mengunduh bobot tangan HaMeR ke `weights/hamer/` (~2,7 GB, sekali saja).

Disarankan memasang ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Pipeline tetap berjalan tanpanya, tetapi video hasilnya akan **tanpa suara** dan tidak bisa diputar di browser.

## Sebelum menjalankan: taruh file-file ini di `assets/`

Repositori ini tidak menyertakan file-file berikut; kamu harus mengambilnya sendiri. Nama file SMPL-X harus sama persis dengan tabel; nama file FBX, video, dan gambar bebas. Setiap run membutuhkan SMPL-X, satu karakter Mixamo, dan **salah satu** dari video **atau** foto. Karakter Mixamo yang diekspor ulang dari Cinema 4D juga bisa dipakai; lihat [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Apa | Di mana | Dari mana |
|---|---|---|
| Model tubuh SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Daftar di [SMPL-X](https://smpl-x.is.tue.mpg.de/) lalu unduh |
| FBX karakter Mixamo | `assets/mixamo/Y_Bot.fbx` | Dengan akun Adobe, unduh Y Bot (atau karakter lain yang sudah di-rig Mixamo) dari [Mixamo](https://www.mixamo.com) |
| Video aksi | `assets/video/<your_clip>.mp4` | Klip dengan **tepat satu** orang yang terlihat jelas, **dari kepala sampai kaki selalu berada di dalam frame** (boleh menyimpan beberapa file; setiap run memakai yang paling terakhir ditambahkan) |
| Foto pose (opsional) | `assets/image/<your_photo>.jpg` | Foto dengan **tepat satu** orang yang terlihat jelas, **dari kepala sampai kaki berada di dalam frame**. Gunakan dengan `--image` |
| Tangan kanan MANO (hanya untuk `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Daftar di [MANO](https://mano.is.tue.mpg.de/) lalu unduh **Models & Code**. Proses tubuh saja tidak membutuhkan berkas ini |

Catatan: file yang diunduh dari Mixamo bernama `Y Bot.fbx` (**dengan spasi**), berbeda satu karakter dari `Y_Bot.fbx` (**dengan garis bawah**) di tabel.
Ganti namanya ke bentuk garis bawah agar menjadi rig bawaan (`m2mr run` tanpa `--rig`). Membiarkan spasinya juga tidak masalah — jika `Y_Bot.fbx` tidak ada, `.fbx` pertama di `assets/mixamo/` yang akan dipakai.

`assets/video/` boleh berisi beberapa video. Tanpa `--video` atau `--image`, run akan memakai file yang **paling terakhir ditambahkan** ke `assets/video/`; jika folder itu kosong, run beralih ke foto terbaru di `assets/image/`.
Setiap klip atau foto hanya boleh menampilkan satu orang, **dari kepala sampai kaki berada di dalam frame** — tidak ada yang terpotong di tepi. `m2mr doctor` / `m2mr run` akan berhenti sebelum ekstraksi jika ada dua orang di dalam frame.

## Mulai Cepat

Hasil disimpan di `outputs/<run-time>_<source>/`. Run dengan video menulis ke `videos/`; run dengan foto menulis ke `images/`.

### 1. Periksa aset dan lingkungan

Semua yang belum ada akan ditampilkan beserta tempat mengunduhnya dan lokasi penempatannya.

```bash
m2mr doctor
```

`m2mr doctor` memeriksa proses tubuh. Model tangan MANO tidak diwajibkan. Untuk memeriksa juga berkas tambahan dan paket Python yang dipakai deteksi jari:

```bash
m2mr doctor --detect-hands
```

### 2. Run pertama: tampilkan hasil di layar

Tanpa flag apa pun, perintah ini memakai **file terbaru di `assets/video/`** dan `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Ini langkah yang lambat. Run pertama mengunduh ~5 GB bobot inferensi (sekali saja), lalu mengekstrak gerakan manusia dari video.
Di CPU, ekstraksi klip ~30 detik memakan waktu sekitar 8–15 menit; run berikutnya dengan durasi serupa, saat bobot sudah tersedia, sekitar 3–5 menit.
Retargeting dan rendering biasanya memakan satu atau dua menit. Memakai ulang skeleton dengan `--skeleton` di bagian berikutnya akan melewati ekstraksi sepenuhnya dan selesai dalam beberapa puluh detik.

Kaki yang menapak dikunci secara bawaan: telapak depan saat telapak depan di bawah, tumit hanya saat jari-jari terangkat. Jika kaki yang diluruskan tidak mencapai titik itu, pinggul bergeser. Lalu telapak kaki diletakkan di lantai (y = 0). `--no-foot-lock` menyimpan retarget mentah, jadi kaki bisa meluncur; telapak kaki tetap diletakkan di lantai.

### 3. Gerakan yang sama, karakter berbeda

Unduh karakter lain dari Mixamo ke `assets/mixamo/`. **Jangan menjalankan ulang hanya dengan `--rig`** — itu akan mengulang ekstraksi yang lambat.
Berikan `--skeleton` untuk memakai ulang skeleton dari run sebelumnya; hitungan menit menjadi beberapa puluh detik:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Video lain

`--video` memilih klip. Bisa dikombinasikan bebas dengan `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Foto (pose statis)

`--image` merekonstruksi **pose 3D statis** dari foto satu orang, lalu me-retarget-nya ke karakter Mixamo dengan cara yang sama seperti run video. Pratinjaunya berupa empat gambar di `images/` (tampilan yang sama dengan run video), ditambah klip orbit kiri/kanan `before_after_360_compare.mp4`. Jangan memberikan `--video` bersamaan.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` tanpa path akan memakai file yang paling terakhir ditambahkan ke `assets/image/`.

### 6. Periksa self-intersection

Setiap run juga memeriksa karakter yang sudah jadi untuk **self-intersection** — satu bagian tubuh masuk ke bagian lain, misalnya tangan di dalam kepala — dan menulis `diagnostics.json`. Terminal mencetak satu baris, misalnya `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Lantai tidak diperiksa.

Untuk memeriksa ulang sebuah run, atau melihat masalahnya:

```bash
m2mr diagnose outputs/<run>                  # tulis ulang diagnostics.json
m2mr diagnose outputs/<run> --visualize      # juga diagnostics.html: video sumber di samping karakter, timeline, daftar masalah yang bisa diklik
m2mr diagnose outputs/<run> --threshold-cm 2 # laporkan hanya tembusan yang lebih dalam dari 2 cm (default 1)
```

Setiap masalah di `diagnostics.json` adalah sepasang bagian tubuh beserta rentang frame saat keduanya saling tembus, frame terparah, dan kedalamannya. Nomor frame dihitung dari 0, sama seperti timeline Blender setelah impor glTF. Bagian yang tersambung oleh sendi (lengan atas dan lengan bawah, torso dan paha, …) tidak dibandingkan: kulitnya tumpang tindih di sekitar sendi dalam pose apa pun. `diagnostics.html` menyematkan video sumber (perlu `ffmpeg`) dan memuat three.js dari CDN, jadi tampilan 3D-nya perlu koneksi internet. Tampilan itu menggambar penanda lantai yang tetap di y = 0: silang setiap 0,5 m, yang lebih besar setiap meter, dan silang hijau di titik asal, supaya bisa dilihat apakah karakter sedang bergerak. Lajur amber di atas jalur perpotongan untuk catatan yang dilihat mata (seret sebuah rentang, atau **In** / **Out**). Daftar **Notes** di kanan menampilkannya; klik satu baris untuk meloncat ke sana. **Download notes** menyimpan catatan itu bersama daftar perpotongan. Berkas dinamai sesuai video sumber dan mencatat jalurnya.

### 7. Jari (`--detect-hands`)

`m2mr run` biasa hanya menggerakkan tubuh dan membiarkan tulang jari Mixamo pada pose istirahat. `--detect-hands` menyalakan model tangan yang menyertai ekstraktor tubuh. Dengan ekstraktor bawaan, GVHMR, model itu adalah [HaMeR](https://github.com/geopavlakos/hamer). HaMeR memotong pergelangan dari orang dan frame yang sudah dipilih GVHMR. Ia tidak mencari orang kedua di dalam klip.

**Waktunya kira-kira menjadi dua kali lipat.** Klip yang tanpa flag selesai dalam beberapa menit akan makan waktu sekitar dua kali lipat dengan `--detect-hands`, karena lintasan tangan berjalan di atas ekstraksi tubuh. Pada video yang panjang, hitung waktu tambahan ini sebelum mulai.

Letakkan `MANO_RIGHT.pkl` seperti pada tabel di atas, lalu:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Proses `--detect-hands` yang pertama mengunduh bobot HaMeR ke `weights/hamer/` (~2,7 GB, sekali). Rotasi jari ditulis ke `skeleton_motion.npz` dan menggerakkan 30 tulang jari Mixamo pada karakter yang sudah di-skin. Pergelangan yang tidak terlihat jelas pada lintasan tubuh tetap pada pose istirahat untuk tangan itu.

`--hand-smooth` adalah berapa detik penghalusan yang diterapkan pada rotasi itu. Nilai bawaannya `0.08`. `0` menyimpan estimasi mentah. Penghalusan berjalan setiap kali berkas skeleton sudah berisi gerakan tangan, termasuk proses berikutnya yang hanya memakai ulang berkas itu.

Saat memakai ulang skeleton sebelumnya:

- Berkas sudah berisi gerakan tangan: `--skeleton` menggerakkan jari dengan sendirinya. `--detect-hands` tidak diperlukan lagi.
- Belum ada, tetapi cache tubuh proses itu masih ada di sampingnya (`cache/<clip>/0_input_video.mp4`, plus `preprocess/vitpose.pt` dan `preprocess/bbx.pt`): `--skeleton ... --detect-hands` menambahkan jari tanpa mengekstrak tubuh lagi.
- Cache itu sudah hilang: jalankan lagi video atau fotonya dengan `--detect-hands`.

## Keluaran

Setiap `m2mr run` membuat direktori yang dinamai berdasarkan **waktu perintah dimulai**. File di root sama untuk video dan foto; hanya folder pratinjaunya yang berbeda.

```
outputs/20260829_193205_dance/          # atau …_pose/ untuk foto
├── run.json                            # waktu mulai, input, perintah lengkap
├── skeleton_motion.npz                 # skeleton manusia 3D (pakai ulang dengan --skeleton)
├── mixamo_rotations.npz                # rotasi Mixamo per tulang
├── mixamo_character.glb                # karakter yang sudah di-skin, impor ke Blender / Unity
├── diagnostics.json                    # laporan self-intersection (lihat Mulai Cepat langkah 6)
├── diagnostics.html                    # hanya setelah `m2mr diagnose <run> --visualize`
└── videos/   atau   images/            # pratinjau — tergantung input
```

**Input video** menulis ke `videos/` (rasio aspek sama dengan klip):

```
videos/
├── human_skeleton.mp4                  # skeleton manusia 3D hasil rekonstruksi
├── mixamo_skeleton.mp4                 # skeleton rig Mixamo
├── mixamo_character.mp4                # karakter Mixamo yang sudah di-skin
└── compare.mp4                         # 2×2: asli (kiri atas) / skeleton Mixamo (kanan atas)
                                        #      skeleton manusia (kiri bawah) / karakter (kanan bawah)
```

**Input foto** menulis ke `images/` sebagai gantinya (empat tampilan yang sama, ditambah putaran penuh):

```
images/
├── human_skeleton.png                  # skeleton manusia 3D hasil rekonstruksi
├── mixamo_skeleton.png                 # skeleton rig Mixamo
├── mixamo_character.png                # karakter Mixamo yang sudah di-skin
├── compare.png                         # 2×2: asli (kiri atas) / skeleton Mixamo (kanan atas)
│                                       #      skeleton manusia (kiri bawah) / karakter (kanan bawah)
└── before_after_360_compare.mp4        # kiri: foto asli
                                        # kanan: orbit rig per 10° (satu putaran penuh)
```

Dengan `--detect-hands`, `skeleton_motion.npz` juga menyimpan rotasi jari, dan `mixamo_rotations.npz` serta `mixamo_character.glb` memuat 30 tulang jari. Tanpa flag itu, dan tanpa gerakan tangan yang sudah tersimpan di skeleton yang dipakai ulang, tulang-tulang itu tetap dalam pose istirahat.

Buka `mixamo_character.glb` di Blender: File → Import → glTF 2.0 (.glb/.gltf). Jika kamera mengarah ke ruang kosong, pilih mesh karakter lalu gunakan View → Frame Selected. Kumpulan bola di kepala dan tangan adalah tampilan tulang, bukan mesh: di Outliner, sembunyikan **Icosphere** dan **armature**; biarkan mesh yang sudah di-skin tetap terlihat. Atur FPS scene sesuai `run.json` (`fps`) dan timeline ke frame 0 sampai `n_frames` − 1 agar pemutaran sesuai dengan sumbernya dan nomor frame cocok dengan `diagnostics.json`. Bandingkan run video dengan `videos/mixamo_character.mp4`, dan run foto dengan `images/mixamo_character.png` atau klip orbit.

## Lisensi

Kode di repositori ini berlisensi Apache-2.0. Aset yang kamu unduh sendiri memiliki ketentuannya masing-masing dan tidak boleh didistribusikan ulang bersama repo ini:

- **SMPL-X**: akses dibatasi oleh MPI; secara bawaan hanya untuk riset / pendidikan / seni non-komersial; penggunaan komersial memerlukan perjanjian terpisah
- **MANO** (hanya jika memakai `--detect-hands`): akses dibatasi oleh MPI, jenis unduhan yang sama dengan SMPL-X; simpan `MANO_RIGHT.pkl` secara lokal dan jangan distribusikan ulang
- **Mixamo FBX**: boleh dipakai dalam produk yang dirilis; jangan mendistribusikan ulang FBX mentah sebagai paket aset
- **GVHMR dan bobot inferensi lainnya**: diunduh otomatis ke `weights/` pada `m2mr run` pertama, di bawah lisensi masing-masing proyek asal
- **HaMeR**: kode inferensi di repositori ini berlisensi MIT; bobot diunduh ke `weights/hamer/` pada `m2mr run --detect-hands` pertama, mengikuti ketentuan rilis proyek asal

## Kontak

Jika kamu mengalami masalah, butuh bantuan menyelesaikan instalasi lokal, atau ingin membicarakan kerja sama, kirim email ke:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
