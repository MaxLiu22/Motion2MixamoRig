# Motion2MixamoRig

<p align="center">
  <a href="#gereksinimler"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.tr.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · Türkçe · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Bir videodaki kişinin hareketini — ya da bir fotoğraftaki pozu — Adobe Mixamo ile rig'lenmiş bir 3D karaktere aktarın.

Oyun geliştiricileri için: **tek kişilik** bir aksiyon videosu (ya da bir fotoğraf) ve bir Mixamo karakteri verin; araç önizleme videoları ile Blender veya Unity'ye doğrudan aktarabileceğiniz skin'lenmiş bir karakter dosyası (`.glb`) üretir.

> Motion2MixamoRig şu anda deneysel aşamadadır. 0.1.8 sürümü komut satırı pipeline'ıdır. Bu depo ayrıca aynı pipeline'ı harici bir Python ortamında çalıştıran bir Blender 4.2+ Extension da içerir. Eklentiyi kaynak koddan derlemek için: [`blender_extension/README.md`](../../blender_extension/README.md).

## İki kullanım yolu

### 🎨 Blender'da — kod yazmadan

1. Platformunuza uygun zip dosyasını, örneğin `motion2mixamorig-<version>-macos-arm64.zip`, [en son sürüm](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest) sayfasından indirin.
2. Blender'da: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…** ile zip dosyasını seçin.
3. 3D Viewport → **N** tuşuna basın → **Motion2MixamoRig** sekmesi → **Çalışma Ortamını Kur (tek tık)** (Install Runtime (one click)).
4. **SMPL-X Modeli Seç…** (Choose SMPL-X Model…) (ücretsiz indirme) ve bir Mixamo karakter FBX dosyası seçin.
5. Tek kişilik bir video seçin → **Hareket Üret** (Generate Motion).

Adım adım talimatlar, ipuçları ve güncelleme: **[Kullanım Kılavuzu](user-guide.tr.md)**. macOS (Apple Silicon) üzerinde test edilmiştir.

### 💻 Komut satırı — geliştiriciler için

Depoyu klonlayın ve pipeline'ı kendiniz çalıştırın: [Gereksinimler](#gereksinimler) bölümünden başlayın.

Agent'lar işe [`AGENTS.md`](../../AGENTS.md) ile başlamalıdır.

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Bu depodaki <a href="../assets/demo.mp4">demo.mp4</a> dosyasını açın.</sub>
</p>

Başka bir demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Tanılama raporu (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Gereksinimler

Python 3.11+. Klonladıktan sonra bir virtualenv oluşturun ve bağımlılıkları kurun; ardından `m2mr` komutu kullanılabilir olur:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Bağımlılıkları ve bu projeyi kurun. chumpy (bağımlılık zincirindeki eski bir
# paket) setup betiğinde pip'i import ettiği için pip'in varsayılan izole
# build ortamında "No module named 'pip'" hatası verir. Önce izolasyon
# kapalıyken onu kurun, ardından bu projeyi kurun.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Çıkarım ağırlıkları (GVHMR vb.) bu adımda indirilmez. İlk `m2mr run` bunları `weights/` klasörüne indirir (~5 GB, yalnızca bir kez). İlk `m2mr run --detect-hands` HaMeR el ağırlıklarını da `weights/hamer/` içine indirir (~2,7 GB, yalnızca bir kez).

ffmpeg kurmanız önerilir (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Pipeline onsuz da çalışır, ancak çıktı videoları **sessiz** olur ve tarayıcıda oynatılamaz.

## Çalıştırmadan önce: bunları `assets/` içine koyun

Bu depo bu dosyaları içermez; kendiniz edinmeniz gerekir. SMPL-X dosya adı tabloyla birebir aynı olmalıdır; FBX, video ve görsel adları serbesttir. Her çalıştırma için SMPL-X, bir Mixamo karakteri ve **ya** bir video **ya da** bir fotoğraf gerekir. Cinema 4D'den yeniden dışa aktarılan Mixamo karakterleri de desteklenir; ayrıntılar için [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md) dosyasına bakın.

| Ne | Nereye | Nereden |
|---|---|---|
| SMPL-X vücut modeli | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | [SMPL-X](https://smpl-x.is.tue.mpg.de/) sitesine kaydolup indirin |
| Mixamo karakter FBX'i | `assets/mixamo/Y_Bot.fbx` | Bir Adobe hesabıyla [Mixamo](https://www.mixamo.com)'dan Y Bot'u (ya da Mixamo ile rig'lenmiş başka bir karakteri) indirin |
| Aksiyon videosu | `assets/video/<your_clip>.mp4` | **Tam olarak bir** kişinin net göründüğü ve **baştan ayağa sürekli kadrajda** olduğu bir klip (birden fazla dosya tutabilirsiniz; her çalıştırma en son ekleneni kullanır) |
| Poz fotoğrafı (isteğe bağlı) | `assets/image/<your_photo>.jpg` | **Tam olarak bir** kişinin net göründüğü ve **baştan ayağa kadrajda** olduğu bir fotoğraf. `--image` ile kullanın |
| MANO sağ el (yalnızca `--detect-hands` için) | `assets/body_models/mano/MANO_RIGHT.pkl` | [MANO](https://mano.is.tue.mpg.de/) adresine kaydolup **Models & Code** indirin. Yalnızca gövde çalıştırması bu dosyaya ihtiyaç duymaz |

Not: Mixamo'dan inen dosyanın adı `Y Bot.fbx`'tir (**boşluklu**); tablodaki `Y_Bot.fbx`'ten (**alt çizgili**) tek bir karakter farklıdır.
Adını alt çizgili biçime çevirirseniz varsayılan rig olur (`--rig` olmadan `m2mr run`). Boşluğu bırakmak da sorun değildir — `Y_Bot.fbx` yoksa `assets/mixamo/` içindeki ilk `.fbx` kullanılır.

`assets/video/` birden fazla video içerebilir. `--video` ya da `--image` verilmezse çalıştırma `assets/video/` içine **en son eklenen** dosyayı kullanır; bu klasör boşsa `assets/image/` içindeki en yeni fotoğrafa geçer.
Her klip ya da fotoğrafta yalnızca bir kişi olmalı ve **baştan ayağa kadrajda** görünmelidir — kenarlarda kesik olmamalıdır. Kadrajda iki kişi varsa `m2mr doctor` / `m2mr run` çıkarım adımından önce durur.

## Hızlı Başlangıç

Sonuçlar `outputs/<run-time>_<source>/` altına yazılır. Video çalıştırmaları `videos/`, fotoğraf çalıştırmaları `images/` klasörüne yazar.

### 1. Varlıkları ve ortamı kontrol edin

Eksik olan her şey, nereden indirileceği ve nereye konacağıyla birlikte yazdırılır.

```bash
m2mr doctor
```

`m2mr doctor` gövde çalıştırmasını denetler. MANO el modelini istemez. Parmak algılamanın kullandığı ek dosyayı ve Python paketlerini de denetlemek için:

```bash
m2mr doctor --detect-hands
```

### 2. İlk çalıştırma: ekranda bir sonuç görün

Hiçbir parametre verilmezse **`assets/video/` içindeki en yeni dosya** ve `assets/mixamo/Y_Bot.fbx` kullanılır.

```bash
m2mr run
```

Yavaş adım budur. İlk çalıştırma ~5 GB çıkarım ağırlığını indirir (yalnızca bir kez), ardından videodan insan hareketini çıkarır.
CPU'da ~30 saniyelik bir klibin çıkarımı yaklaşık 8–15 dakika sürer; ağırlıklar hazırken benzer uzunluktaki sonraki çalıştırmalar yaklaşık 3–5 dakika sürer.
Retargeting ve render genellikle bir iki dakika sürer. Sonraki bölümdeki `--skeleton` ile bir iskeleti yeniden kullanmak çıkarımı tamamen atlar ve birkaç on saniyede biter.

Yere basan ayak varsayılan olarak sabitlenir: tarak yere değiyorsa tarak, parmaklar kalkıksa yalnızca topuk. Düz bacak o noktaya yetişemezse kalça kayar. Ardından taban zemine (y = 0) oturtulur. `--no-foot-lock` ham retarget'i korur, bu yüzden ayaklar kayabilir; taban yine de zemine oturtulur.

### 3. Aynı hareket, farklı karakter

Mixamo'dan başka bir karakteri `assets/mixamo/` içine indirin. **Yalnızca `--rig` ile yeniden çalıştırmayın** — bu, yavaş çıkarımı tekrarlar.
Önceki bir çalıştırmanın iskeletini yeniden kullanmak için `--skeleton` verin; dakikalar birkaç on saniyeye iner:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Farklı bir video

`--video` klibi seçer. `--rig` ile serbestçe birleştirilebilir.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Bir fotoğraf (sabit poz)

`--image`, tek bir kişinin fotoğrafından **sabit bir 3D poz** çıkarır ve onu bir video çalıştırmasıyla aynı şekilde Mixamo karakterine retarget eder. Önizlemeler `images/` içindeki dört görseldir (video çalıştırmasıyla aynı görünümler), ayrıca sola/sağa dönen bir yörünge klibi `before_after_360_compare.mp4` vardır. Aynı anda `--video` vermeyin.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

Yol verilmeden kullanılan `--image`, `assets/image/` içine en son eklenen dosyayı kullanır.

### 6. Kendi içine geçmeyi kontrol edin

Her çalıştırma, bitmiş karakterde **kendi içine geçme** olup olmadığını da kontrol eder — bir vücut parçasının diğerinin içine girmesi, örneğin elin başın içine girmesi — ve `diagnostics.json` yazar. Terminal tek bir satır yazdırır, örn. `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Zemin kontrol edilmez.

Bir çalıştırmayı yeniden kontrol etmek veya sorunları görmek için:

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json'u yeniden yazar
m2mr diagnose outputs/<run> --visualize      # ayrıca diagnostics.html: karakterin yanında kaynak video, timeline, tıklanabilir sorun listesi
m2mr diagnose outputs/<run> --threshold-cm 2 # yalnızca 2 cm'den derin geçmeleri raporlar (varsayılan 1)
```

`diagnostics.json` içindeki her sorun bir vücut parçası çiftidir; iç içe geçtikleri kare aralıklarını, en kötü kareyi ve onun derinliğini içerir. Kare numaraları, glTF içe aktarımından sonraki Blender timeline'ı gibi 0'dan başlar. Bir eklemle bağlı parçalar (üst kol ve ön kol, gövde ve uyluk, …) karşılaştırılmaz: derileri her pozda eklem çevresinde üst üste biner. `diagnostics.html` kaynak videoyu gömer (`ffmpeg` gerekir) ve three.js'i bir CDN'den yükler; bu yüzden 3D görünümü internet bağlantısı ister. Bu görünüm y = 0 üzerine sabit zemin işaretleri çizer: her 0,5 m'de bir çarpı, her metrede daha büyüğü ve başlangıçta yeşil bir çarpı, böylece karakterin hareket edip etmediği anlaşılır. Kesişim izlerinin üstündeki amber şerit, gözle görülen notlar içindir (bir aralık sürükleyin veya **In** / **Out**). Sağdaki **Notes** listesi bunları gösterir; bir satıra tıklamak oraya gider. **Download notes** bu notları kesişim listesiyle birlikte kaydeder. Dosya kaynak videonun adını taşır ve onun yolunu içerir.

### 7. Parmaklar (`--detect-hands`)

Düz bir `m2mr run` gövdeyi hareket ettirir ve Mixamo parmak kemiklerini dinlenmede bırakır. `--detect-hands`, gövde çıkarıcısıyla birlikte gelen el modelini açar. Varsayılan çıkarıcı GVHMR ile bu model [HaMeR](https://github.com/geopavlakos/hamer) olur. HaMeR, GVHMR'nin çoktan seçtiği kişiden ve karelerden bilekleri keser. Klipte ikinci bir kişiyi aramaz.

**Süre yaklaşık iki katına çıkar.** Bayrak olmadan birkaç dakikada biten bir klip, `--detect-hands` ile yaklaşık iki kat sürer; el geçişi gövde çıkarımının üstüne biner. Uzun bir videoda başlamadan önce bu süreyi hesaba katın.

`MANO_RIGHT.pkl` dosyasını yukarıdaki tabloya göre koyun, sonra:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

`--detect-hands` ile ilk çalıştırma HaMeR ağırlıklarını `weights/hamer/` içine indirir (~2,7 GB, bir kez). Parmak dönüşleri `skeleton_motion.npz` içine yazılır ve derili karakterdeki 30 Mixamo parmak kemiğini sürer. Gövde geçişinin net görmediği bilek, o el için dinlenmede kalır.

`--hand-smooth`, bu dönüşlere kaç saniyelik yumuşatma uygulanacağını söyler. Varsayılan `0.08` değeridir. `0` ham tahmini korur. İskelet dosyasında zaten el hareketi varsa yumuşatma çalışır; buna yalnızca bu dosyayı yeniden kullanan sonraki bir çalıştırma da dahildir.

Önceki bir iskeleti yeniden kullanırken:

- Dosyada zaten el hareketi vardır: `--skeleton` parmakları kendisi sürer. `--detect-hands` bir daha gerekmez.
- El hareketi yoktur ama o çalıştırmanın gövde önbelleği hâlâ yanındadır (`cache/<clip>/0_input_video.mp4` ile `preprocess/vitpose.pt` ve `preprocess/bbx.pt`): `--skeleton ... --detect-hands` gövdeyi yeniden çıkarmadan parmakları ekler.
- O önbellek yoksa: videoyu veya fotoğrafı `--detect-hands` ile yeniden çalıştırın.

## Çıktılar

Her `m2mr run`, **komutun başladığı zamana** göre adlandırılmış bir dizin oluşturur. Kök dizindeki dosyalar video ve fotoğraf için aynıdır; yalnızca önizleme klasörü değişir.

```
outputs/20260829_193205_dance/          # fotoğraf için …_pose/
├── run.json                            # başlangıç zamanı, girdiler, tam komut
├── skeleton_motion.npz                 # 3D insan iskeleti (--skeleton ile yeniden kullanın)
├── mixamo_rotations.npz                # kemik başına Mixamo rotasyonları
├── mixamo_character.glb                # skin'lenmiş karakter, Blender / Unity'ye aktarın
├── diagnostics.json                    # kendi içine geçme raporu (Hızlı Başlangıç adım 6'ya bakın)
├── diagnostics.html                    # yalnızca `m2mr diagnose <run> --visualize` sonrasında
└── videos/   veya   images/            # önizlemeler — girdiye göre
```

**Video girdisi** `videos/` klasörüne yazar (klibin en-boy oranıyla aynı):

```
videos/
├── human_skeleton.mp4                  # yeniden oluşturulan 3D insan iskeleti
├── mixamo_skeleton.mp4                 # Mixamo rig iskeleti
├── mixamo_character.mp4                # skin'lenmiş Mixamo karakteri
└── compare.mp4                         # 2×2: orijinal (sol üst) / Mixamo iskeleti (sağ üst)
                                        #      insan iskeleti (sol alt) / karakter (sağ alt)
```

**Fotoğraf girdisi** bunun yerine `images/` klasörüne yazar (aynı dört görünüm ve bir tam tur dönüş):

```
images/
├── human_skeleton.png                  # yeniden oluşturulan 3D insan iskeleti
├── mixamo_skeleton.png                 # Mixamo rig iskeleti
├── mixamo_character.png                # skin'lenmiş Mixamo karakteri
├── compare.png                         # 2×2: orijinal (sol üst) / Mixamo iskeleti (sağ üst)
│                                       #      insan iskeleti (sol alt) / karakter (sağ alt)
└── before_after_360_compare.mp4        # sol: orijinal fotoğraf
                                        # sağ: rig etrafında 10°'lik adımlarla yörünge (tam bir tur)
```

`--detect-hands` ile `skeleton_motion.npz` parmak dönüşlerini de saklar; `mixamo_rotations.npz` ve `mixamo_character.glb` 30 parmak kemiğini içerir. Bu bayrak yoksa ve yeniden kullanılan iskelette de el hareketi yoksa bu kemikler dinlenmede kalır.

`mixamo_character.glb` dosyasını Blender'da açın: File → Import → glTF 2.0 (.glb/.gltf). Kamera boş bir alana bakıyorsa karakter mesh'ini seçip View → Frame Selected kullanın. Baş ve ellerdeki küre kümesi kemik gösterimidir, mesh değildir: Outliner'da **Icosphere** ve **armature**'ü gizleyin; skin'lenmiş mesh'i görünür bırakın. Oynatmanın kaynakla, kare numaralarının da `diagnostics.json` ile eşleşmesi için sahnenin FPS'ini `run.json` (`fps`) değerine, timeline'ı da 0 ile `n_frames` − 1 arasındaki karelere ayarlayın. Bir video çalıştırmasını `videos/mixamo_character.mp4` ile, bir fotoğraf çalıştırmasını `images/mixamo_character.png` ya da yörünge klibiyle karşılaştırın.

## Lisans

Bu deponun kodu Apache-2.0 lisanslıdır. Kendi indirdiğiniz varlıkların kendi koşulları vardır ve bu depoyla birlikte yeniden dağıtılmamalıdır:

- **SMPL-X**: MPI erişim kontrollü; varsayılan olarak ticari olmayan araştırma / eğitim / sanat; ticari kullanım için ayrı bir anlaşma gerekir
- **MANO** (yalnızca `--detect-hands` ile): MPI erişim kontrollü, SMPL-X ile aynı tür indirme; `MANO_RIGHT.pkl` dosyasını yerelde tutun ve yeniden dağıtmayın
- **Mixamo FBX**: yayınlanan bir üründe kullanılabilir; ham FBX'i bir varlık paketi olarak yeniden dağıtmayın
- **GVHMR ve diğer çıkarım ağırlıkları**: ilk `m2mr run` sırasında `weights/` içine otomatik indirilir, her birinin kaynak projesinin lisansı altındadır
- **HaMeR**: bu depodaki çıkarım kodu MIT'tir; ağırlıklar ilk `m2mr run --detect-hands` sırasında `weights/hamer/` içine iner, kaynak yayının koşulları altında

## İletişim

Bir sorunla karşılaşırsanız, yerel kurulumu tamamlamak için yardıma ihtiyacınız olursa ya da iş birliği hakkında konuşmak isterseniz şu adrese e-posta gönderin:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
