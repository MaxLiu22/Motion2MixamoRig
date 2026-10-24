# Motion2MixamoRig para sa Blender — User Guide

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · Filipino · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Gawing animated na Mixamo character ang video ng isang tao, sa loob mismo ng Blender.
Walang coding o terminal na kailangan.

<!-- video: link the tutorial video here -->

> Sa ngayon, sa **macOS (Apple Silicon)** pa lang ito na-test. Paparating na ang build para sa Windows.

## Mga kailangan mo

- **Blender 4.2 o mas bago**
- **Internet connection** para sa unang setup
- **Mga 8 GB na libreng disk space** (runtime ~1.3 GB + mga model ~5.6 GB)
- **Libreng SMPL-X account** at **libreng Adobe account** (para sa Mixamo); tingnan ang steps 4 at 5

## 1. I-download ang add-on

Pumunta sa [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
at i-download ang zip para sa computer mo:

| Computer mo | File |
| --- | --- |
| Mac na may Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Malapit na** |

Halimbawa, `motion2mixamorig-0.1.8-macos-arm64.zip`: ang `0.1.8` ay ang
bersyon ng add-on, at ang `macos-arm64` ay ang platform. Kapag mali ang napili
mo, tatanggihan ito ng Blender at sasabihin kung anong platform ang inaasahan.

**Huwag** itong i-unzip. Ang Blender mismo ang mag-i-install ng zip.

## 2. I-install ito sa Blender

1. **Edit → Preferences → Get Extensions**
2. I-click ang maliit na **∨** sa kanang itaas → **Install from Disk…**
3. Piliin ang zip. Lalabas ang **Motion2MixamoRig** sa listahan, naka-enable na.
4. Isara ang Preferences. Sa 3D Viewport, pindutin ang **N**, tapos i-click ang
   **Motion2MixamoRig** tab sa kanan.

<!-- screenshot: Install from Disk menu -->

## 3. I-install ang runtime (isang beses lang)

Sa panel, i-click ang **I-install ang Runtime (isang click)** (Install Runtime (one click)).

Magda-download ang add-on ng sarili nitong Python at mga library (~1.4 GB) sa
`~/Motion2MixamoRig/`. Wala itong ginagalaw na iba pa sa computer mo. Ilang
minuto ito; ipinapakita ng progress bar ang kasalukuyang step.

<!-- screenshot: Install Runtime button and progress -->

## 4. Kunin ang SMPL-X body model

Ang SMPL-X ay isang libreng body model na kailangan ng add-on. Hindi kami
pinapayagan ng lisensya nito na isama ito, kaya ikaw mismo ang magda-download,
isang beses lang:

1. Buksan ang [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) at mag-**Register**.
   Tanggapin ang lisensya at i-confirm ang email.
2. Mag-log in, buksan ang **Download**, at i-download ang SMPL-X model (ang
   **NPZ** na bersyon).
3. I-unzip ito at hanapin ang **`SMPLX_NEUTRAL.npz`**.
4. Sa Blender, i-click ang **Pumili ng SMPL-X Model…** (Choose SMPL-X Model…) at
   piliin ang file na iyon. Ipapakita ng panel ang **SMPL-X model: nakita** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Kumuha ng Mixamo character

1. Buksan ang [mixamo.com](https://www.mixamo.com/) at mag-sign in gamit ang Adobe account.
2. **Characters** tab → pumili ng character (halimbawa **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Gumawa ng galaw

Sa **Input** box:

1. **Uri ng Source** (Source Type): Video (o **Larawan** (Image) para sa iisang pose)
2. **Source File**: ang clip mo. Dapat **eksaktong isang tao lang ang nasa
   clip, kita mula ulo hanggang paa sa frame sa buong oras**.
3. **Mixamo Rig FBX**: ang character mula sa step 5
4. Naka-off ang **I-detect ang mga kamay** (Detect Hands). I-on lang ito kapag
   dapat gumalaw ang mga daliri. Pagkatapos, i-click ang **Piliin ang MANO Hand Model…**
   (Choose MANO Hand Model…) at piliin ang `MANO_RIGHT.pkl`. Kunin ang file na iyon
   gaya ng SMPL-X: magrehistro sa
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), i-download ang **Models & Code**,
   at i-unzip. Ang unang hand run ay magda-download pa ng mga **2.7 GB**, isang beses,
   at aabot nang halos doble ng body-only na run. Kapag naka-on, lumalabas ang **Finger Smoothing (seconds)**. Pinapalambot nito ang galaw ng mga daliri. Ang default ay 0.08 segundo; ang 0 ay iniiwan ang nadetect.
5. I-click ang **Gumawa ng Galaw** (Generate Motion)

Pagkatapos nito, awtomatikong ii-import sa scene mo ang animated na character. Nanatili ang nakalapag na paa kung saan ito dumapo, at inilalagay ang talampakan sa sahig ng Blender. May idinaragdag na mesh na **Mga marka sa sahig** (Floor Markers) sa sahig na iyon (isang krus kada 0.5 m). Ipinapakita o itinatago ito ng checkbox na **Mga marka sa sahig** (Floor Markers) sa ilalim ng Progreso / Resulta.

### Mas matagal ang unang run — normal lang ito

Sa unang beses, magda-download ang add-on ng mga **5.6 GB** na model. Ipinapakita
ng panel ang laki ng download, bilis, at natitirang oras. Isang beses lang
dina-download ang mga model.

Pagkatapos noon, sa computer mo na pinoproseso ang video. Sa Mac CPU, ilang
minuto ang 10-segundong clip. Magagamit mo pa rin ang Blender habang tumatakbo
ito, at pinapahinto ng **Kanselahin** (Cancel) ang job.

## Mga tip para sa magandang resulta

- Iisang tao lang, kita ang buong katawan, hindi naputol sa mga gilid
- Steady na camera, maayos na ilaw, simpleng damit sa halip na maluwag o nililipad
- Mas mabilis subukan muna ang maiikling clip (5–20 segundo)

## Mag-update sa bagong bersyon

Madalas ma-update ang add-on. Para mag-update:

1. I-download ang pinakabagong zip mula sa
   [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → alisin ang lumang **Motion2MixamoRig**, isara nang
   tuluyan ang Blender (**Cmd+Q**), buksan ulit, at i-install ang bagong zip.
3. Sa panel, i-click ang **I-update ang Runtime** (Update Runtime).

Hindi nabubura ang mga na-download na model sa pag-update, kaya mabilis ito.
Makikita ang naka-install mong bersyon sa tabi ng add-on sa **Get Extensions**.

## Ang panel

- Ang **⚙ sa tabi ng title** ay nagpapakita o nagtatago ng **Setup** box.
- **Setup**: wika, runtime, SMPL-X, **Device** (CPU ang ligtas na piliin), at
  **Suriin ang Environment** (Check Environment).
- **Input**: kung ano ang ia-animate, ang **Model ng katawan** (Body Model, GVHMR), at **I-detect ang mga kamay** (Detect Hands).
- **Progreso / Resulta** (Progress / Result): progress, recent log, at pagkatapos ng job,
  **I-import ang Nagawang Character** (Import Generated Character), **Mga marka sa sahig** (Floor Markers), **Buksan ang
  Output Folder** (Open Output Folder), **Tingnan ang Buong Log** (View Full Log).
- **Diagnostics**: kung saan pumapasok sa isa't isa ang mga bahagi ng katawan
  ng character (kamay sa loob ng ulo, nakakrus na braso). Ang mga pulang cell
  sa bar ay mga frame na may problema; i-click ang isa para pumunta roon.
  Sinusundan ng tatsulok sa ilalim ng bar ang kasalukuyang frame, at sa ibaba
  nito ang mga bahaging nagsasalubong at kung gaano kalalim. Lumilipat sa
  pagitan ng mga problema ang **Nauna** / **Susunod** (Previous / Next).
  Binubuksan ng **Buksan ang HTML Report** (Open HTML Report) ang isang report
  sa web browser na katabi ng character ang source video (sa unang beses, mga
  15 segundo bago ito mabuo). Kailangan ng orihinal na video ang ffmpeg sa computer (sa Mac: `brew install ffmpeg`). Kung wala, nandoon ang character at blangko ang video sa tabi nito. Nakatayo ang character sa mga nakapirming krus sa sahig, isa kada 0.5 m, para makita kung dumudulas ito. Ang amber na lane sa ibabaw ng mga pulang track ay para sa mga talang nakikita ng mata. Nasa listahang **Notes** sa kanan ang mga ito; i-click ang isang row para lumipat doon. Sine-save ng **Download notes** ang mga talang ito kasama ang oras ng intersection. Ipinangalan ang file sa source video.

Available ang add-on sa 19 wika. Sinusunod ng **Auto (sundan ang Blender / system)**
ang wika ng Blender; palitan ito sa Setup box sa **Wika ng UI** (UI Language).

## Kapag may nagkaproblema

| Ang nakikita mo | Ang dapat gawin |
| --- | --- |
| **Pumalya ang pag-install ng runtime** (Runtime installation failed) | I-check ang internet connection mo at i-click ulit ang button. Log: `~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X model: wala** (SMPL-X model: missing) | Ulitin ang step 4 at piliin ang `SMPLX_NEUTRAL.npz` |
| **MANO hand model: wala** (MANO hand model: missing) | I-on ang **I-detect ang mga kamay**, tapos **Piliin ang MANO Hand Model…** at piliin ang `MANO_RIGHT.pkl` |
| **Hindi valid ang Mixamo FBX** (Mixamo FBX invalid) | I-download ulit ang character bilang **FBX Binary**, **T-pose** |
| **Higit sa isang tao ang nasa input** (Input contains multiple people) | Gumamit ng clip na iisang tao lang ang nasa loob |
| **Walang taong na-detect sa input** (No person was detected in the input) | Siguraduhing kita ang buong katawan at maliwanag ang ilaw |
| **Biglang huminto ang pipeline process** (Pipeline process exited unexpectedly) | I-click ang **Tingnan ang Buong Log** |

Kapag hihingi ka ng tulong, i-attach ang log at sabihin kung anong bersyon ng add-on ang gamit mo.

## Pag-uninstall

1. **Get Extensions** → alisin ang **Motion2MixamoRig**.
2. Burahin ang folder na **`~/Motion2MixamoRig`** (ang home folder mo →
   `Motion2MixamoRig`). **Hindi** ito nabubura kapag inalis ang add-on, at
   naglalaman ito ng mga 7 GB na runtime at model, pati ang mga nagawa mong
   resulta sa `app/outputs/`.

## Lisensya

Ang Motion2MixamoRig ay **para lang sa non-commercial na paggamit**: umaasa ito
sa mga research model (gaya ng GVHMR at SMPL-X) na hindi pinapayagan ng lisensya
ang commercial na paggamit. Tingnan ang [`NOTICE.md`](../../NOTICE.md).
