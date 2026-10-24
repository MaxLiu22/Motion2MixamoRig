# Blender için Motion2MixamoRig — Kullanım Kılavuzu

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · Türkçe · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Tek kişilik bir videoyu Blender içinde animasyonlu bir Mixamo karakterine dönüştürün.
Kod yazmanız veya terminal kullanmanız gerekmez.

<!-- video: link the tutorial video here -->

> Şimdiye kadar yalnızca **macOS (Apple Silicon)** üzerinde test edilmiştir.
> Windows sürümü yakında geliyor.

## Gerekenler

- **Blender 4.2 veya daha yeni bir sürüm**
- İlk kurulum için **internet bağlantısı**
- **Yaklaşık 8 GB boş disk alanı** (çalışma ortamı ~1,3 GB + modeller ~5,6 GB)
- **Ücretsiz bir SMPL-X hesabı** ve **ücretsiz bir Adobe hesabı** (Mixamo için); 4. ve 5. adımlara bakın

## 1. Eklentiyi indirin

[En son sürüm](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
sayfasına gidin ve bilgisayarınıza uygun zip dosyasını indirin:

| Bilgisayarınız | Dosya |
| --- | --- |
| Apple Silicon'lu Mac (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Çok yakında** |

Örneğin `motion2mixamorig-0.1.8-macos-arm64.zip` dosyasında `0.1.8` eklenti
sürümü, `macos-arm64` ise platformdur. Yanlış dosyayı seçerseniz Blender
kurulumu reddeder ve beklediği platformu belirtir.

Dosyayı **açmayın** (zip'ten çıkarmayın). Blender zip dosyasını kendisi kurar.

## 2. Blender'a kurun

1. **Edit → Preferences → Get Extensions**
2. Sağ üstteki küçük **∨** simgesine tıklayın → **Install from Disk…**
3. Zip dosyasını seçin. **Motion2MixamoRig** listede etkin olarak görünür.
4. Preferences penceresini kapatın. 3D Viewport içinde **N** tuşuna basın, ardından
   sağdaki **Motion2MixamoRig** sekmesine tıklayın.

<!-- screenshot: Install from Disk menu -->

## 3. Çalışma ortamını kurun (bir kez)

Panelde **Çalışma Ortamını Kur (tek tık)** (Install Runtime (one click)) düğmesine tıklayın.

Eklenti kendi Python'ını ve kütüphanelerini (~1,4 GB) `~/Motion2MixamoRig/`
klasörüne indirir. Bilgisayarınızdaki başka hiçbir şeye dokunmaz. Bu işlem
birkaç dakika sürer; ilerleme çubuğu o anki adımı gösterir.

<!-- screenshot: Install Runtime button and progress -->

## 4. SMPL-X vücut modelini edinin

SMPL-X, eklentinin ihtiyaç duyduğu ücretsiz bir vücut modelidir. Lisansı onu
eklentiyle birlikte dağıtmamıza izin vermez; bu yüzden bir kereliğine kendiniz
indirmeniz gerekir:

1. [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) adresini açın ve **Register** ile kaydolun.
   Lisansı kabul edin ve e-postanızı onaylayın.
2. Giriş yapın, **Download** sayfasını açın ve SMPL-X modelini (**NPZ**
   sürümü) indirin.
3. Arşivi açın ve **`SMPLX_NEUTRAL.npz`** dosyasını bulun.
4. Blender'da **SMPL-X Modeli Seç…** (Choose SMPL-X Model…) düğmesine tıklayın ve
   bu dosyayı seçin. Panelde ardından **SMPL-X modeli: bulundu** (SMPL-X model: found)
   görünür.

<!-- screenshot: SMPL-X download page -->

## 5. Bir Mixamo karakteri edinin

1. [mixamo.com](https://www.mixamo.com/) adresini açın ve bir Adobe hesabıyla giriş yapın.
2. **Characters** sekmesi → bir karakter seçin (örneğin **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Hareket üretin

**Girdi** (Input) kutusunda:

1. **Kaynak Türü** (Source Type): **Video** (tek bir poz için **Görsel** (Image))
2. **Kaynak Dosya** (Source File): klibiniz. Klipte **tam olarak bir kişi
   bulunmalı ve kişi baştan ayağa, sürekli kadrede olmalıdır**.
3. **Mixamo Karakter FBX** (Mixamo Rig FBX): 5. adımdaki karakter
4. **Elleri algıla** (Detect Hands) kapalıdır. Yalnızca parmaklar hareket etsin
   istiyorsanız açın. Ardından **MANO el modelini seç…** (Choose MANO Hand Model…)
   düğmesine tıklayıp `MANO_RIGHT.pkl` dosyasını seçin. Bu dosyayı SMPL-X gibi alırsınız:
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/) adresine kaydolun, **Models & Code**
   indirin ve açın. İlk el geçişi bir kez yaklaşık **2,7 GB** daha indirir ve yalnızca
   gövde çalıştırmasının yaklaşık iki katı sürer. Açıkken **Finger Smoothing (seconds)** da görünür. Parmak hareketini yumuşatır. Varsayılan 0,08 saniyedir; 0, algılananı olduğu gibi bırakır.
5. **Hareket Üret** (Generate Motion) düğmesine tıklayın

İşlem bittiğinde animasyonlu karakter sahnenize otomatik olarak içe
aktarılır. Yere basan ayak indiği yerde kalır ve taban Blender'ın zeminine oturtulur. O zemine bir **Zemin işaretleri** (Floor Markers) mesh'i eklenir (her 0,5 m'de bir çarpı). İlerleme / Sonuç altındaki **Zemin işaretleri** (Floor Markers) kutusu onu gösterir ya da gizler.

### İlk çalıştırma daha uzun sürer — bu normaldir

İlk seferde eklenti yaklaşık **5,6 GB** model indirir. Panel indirme boyutunu,
hızını ve kalan süreyi gösterir. Modeller yalnızca bir kez indirilir.

Bundan sonra video bilgisayarınızda işlenir. Bir Mac'in CPU'sunda 10 saniyelik
bir klip birkaç dakika sürer. İşlem sürerken Blender'ı kullanmaya devam
edebilirsiniz; **İptal** (Cancel) işi durdurur.

## İyi sonuçlar için ipuçları

- Yalnızca bir kişi, tüm vücut görünür ve kenarlardan kesilmemiş
- Sabit kamera, iyi ışık; bol veya dalgalanan kıyafetler yerine sade kıyafetler
- İlk denemeler için kısa klipler (5–20 saniye) daha hızlıdır

## Yeni bir sürüme güncelleme

Eklenti sık sık güncellenir. Güncellemek için:

1. En yeni zip dosyasını
   [en son sürüm](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest) sayfasından indirin.
2. **Get Extensions** → eski **Motion2MixamoRig**'i kaldırın, Blender'dan
   tamamen çıkın (**Cmd+Q**), yeniden açın ve yeni zip dosyasını kurun.
3. Panelde **Çalışma Ortamını Güncelle** (Update Runtime) düğmesine tıklayın.

Güncelleme, indirilmiş modelleri korur; bu yüzden hızlıdır. Kurulu sürümünüz
**Get Extensions** içinde eklentinin yanında gösterilir.

## Panel

- **Başlığın yanındaki ⚙** simgesi **Kurulum** (Setup) kutusunu gösterir veya gizler.
- **Kurulum**: dil, çalışma ortamı, SMPL-X, cihaz (**Cihaz** (Device); güvenli
  seçim CPU'dur) ve **Ortamı Denetle** (Check Environment).
- **Girdi**: neyin canlandırılacağı, **Vücut modeli** (Body Model, GVHMR) ve **Elleri algıla** (Detect Hands).
- **İlerleme / Sonuç** (Progress / Result): ilerleme, son günlük kayıtları ve bir iş
  bittikten sonra **Üretilen Karakteri İçe Aktar** (Import Generated Character), **Zemin işaretleri** (Floor Markers),
  **Çıktı Klasörünü Aç** (Open Output Folder), **Tüm Günlüğü Göster** (View Full Log).
- **Tanılama** (Diagnostics): karakterin vücut parçalarının birbirinin içine
  girdiği yerler (başın içindeki el, kavuşturulmuş kollar). Çubuktaki kırmızı
  hücreler sorunlu karelerdir; birine tıklayınca oraya gidilir. Çubuğun
  altındaki üçgen geçerli kareyi izler; altında da hangi parçaların iç içe
  geçtiği ve ne kadar derin olduğu görünür. **Önceki** / **Sonraki** (Previous
  / Next) sorunlar arasında geçiş yapar. **HTML Raporunu Aç** (Open HTML
  Report), kaynak videonun karakterin yanında gösterildiği bir raporu web
  tarayıcısında açar (ilk seferde oluşturulması yaklaşık 15 saniye sürer). Özgün videonun görünmesi için bilgisayarda ffmpeg olmalıdır (Mac’te `brew install ffmpeg`). Yoksa karakter durur, yanındaki video boş kalır. Karakter, kayıp kaymadığı görülsün diye her 0,5 m'de bir sabit zemin çarpısının üzerinde durur. Kırmızı izlerin üstündeki amber şerit, gözünüzle gördüğünüz notlar içindir. Sağdaki **Notes** listesinde dururlar; bir satıra tıklamak oraya gider. **Download notes** bu notları kesişim zamanlarıyla birlikte kaydeder. Dosya kaynak videonun adını taşır.

Eklenti 19 dili destekler. **Otomatik (Blender / Sistem)** (Auto (Blender / System))
Blender'ın dilini izler; bunu Kurulum kutusundaki **Arayüz Dili** (UI Language)
ayarından değiştirebilirsiniz.

## Bir sorun çıkarsa

| Gördüğünüz | Yapmanız gereken |
| --- | --- |
| **Çalışma ortamı kurulumu başarısız** (Runtime installation failed) | İnternet bağlantınızı kontrol edin ve düğmeye yeniden tıklayın. Günlük: `~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X modeli: eksik** (SMPL-X model: missing) | 4. adımı tekrarlayın ve `SMPLX_NEUTRAL.npz` dosyasını seçin |
| **MANO el modeli: eksik** (MANO hand model: missing) | **Elleri algıla** seçeneğini açın, sonra **MANO el modelini seç…** ile `MANO_RIGHT.pkl` dosyasını seçin |
| **Mixamo FBX geçersiz** (Mixamo FBX invalid) | Karakteri **FBX Binary**, **T-pose** olarak yeniden indirin |
| **Girdide birden fazla kişi var** (Input contains multiple people) | Yalnızca bir kişinin olduğu bir klip kullanın |
| **Girdide kişi algılanmadı** (No person was detected in the input) | Tüm vücudun görünür ve iyi aydınlatılmış olduğundan emin olun |
| **Pipeline işlemi beklenmedik şekilde sonlandı** (Pipeline process exited unexpectedly) | **Tüm Günlüğü Göster** düğmesine tıklayın |

Yardım isterken günlük dosyasını ekleyin ve hangi eklenti sürümünü kullandığınızı belirtin.

## Kaldırma

1. **Get Extensions** → **Motion2MixamoRig**'i kaldırın.
2. **`~/Motion2MixamoRig`** klasörünü silin (ana klasörünüz →
   `Motion2MixamoRig`). Eklentiyi kaldırmak bu klasörü **silmez**; klasör
   yaklaşık 7 GB çalışma ortamı ve model ile `app/outputs/` içindeki
   ürettiğiniz sonuçları barındırır.

## Lisans

Motion2MixamoRig **yalnızca ticari olmayan kullanım** içindir: lisansları ticari
kullanıma izin vermeyen araştırma modellerine (GVHMR ve SMPL-X gibi) dayanır.
[`NOTICE.md`](../../NOTICE.md) dosyasına bakın.
