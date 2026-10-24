# Motion2MixamoRig för Blender — Användarhandbok

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · Svenska
</p>

Gör en video av en person till en animerad Mixamo-karaktär, inne i Blender.
Ingen programmering och ingen terminal behövs.

<!-- video: link the tutorial video here -->

> Hittills testat bara på **macOS (Apple Silicon)**. En Windows-version är på väg.

## Det här behöver du

- **Blender 4.2 eller nyare**
- **En internetanslutning** för den första installationen
- **Ungefär 8 GB ledigt diskutrymme** (körningsmiljö ~1,3 GB + modeller ~5,6 GB)
- **Ett gratis SMPL-X-konto** och **ett gratis Adobe-konto** (för Mixamo); se steg 4 och 5

## 1. Ladda ner tillägget

Gå till [senaste utgåvan](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
och ladda ner zip-filen för din dator:

| Din dator | Fil |
| --- | --- |
| Mac med Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Kommer snart** |

Till exempel `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` är tilläggets
version, `macos-arm64` plattformen. Om du väljer fel vägrar Blender att
installera den och talar om vilken plattform den väntade sig.

Packa **inte** upp den. Blender installerar zip-filen själv.

## 2. Installera den i Blender

1. **Edit → Preferences → Get Extensions**
2. Klicka på det lilla **∨** uppe till höger → **Install from Disk…**
3. Välj zip-filen. **Motion2MixamoRig** syns i listan, redan påslagen.
4. Stäng Preferences. I 3D Viewport trycker du **N** och klickar på fliken
   **Motion2MixamoRig** till höger.

<!-- screenshot: Install from Disk menu -->

## 3. Installera körningsmiljön (en gång)

I panelen klickar du på **Installera körningsmiljön (ett klick)** (Install Runtime (one click)).

Tillägget laddar ner sin egen Python och bibliotek (~1,4 GB) till
`~/Motion2MixamoRig/`. Det rör inget annat på datorn. Det tar några minuter;
förloppsindikatorn visar det aktuella steget.

<!-- screenshot: Install Runtime button and progress -->

## 4. Hämta SMPL-X-kroppsmodellen

SMPL-X är en gratis kroppsmodell som tillägget behöver. Licensen tillåter inte
att vi skickar med den, så du laddar ner den själv, en gång:

1. Öppna [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) och klicka på
   **Register**. Godkänn licensen och bekräfta mejlet.
2. Logga in, öppna **Download** och ladda ner SMPL-X-modellen (**NPZ**-versionen).
3. Packa upp den och hitta **`SMPLX_NEUTRAL.npz`**.
4. I Blender klickar du på **Välj SMPL-X-modell…** (Choose SMPL-X Model…)
   och väljer den filen. Panelen visar då **SMPL-X-modell: hittad**
   (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Hämta en Mixamo-karaktär

1. Öppna [mixamo.com](https://www.mixamo.com/) och logga in med ett Adobe-konto.
2. Fliken **Characters** → välj en karaktär (till exempel **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Generera rörelse

I rutan **Input**:

1. **Källtyp** (Source Type): Video (eller Image för en enda pose)
2. **Källfil** (Source File): ditt klipp. Det ska visa **exakt en person, från
   huvud till tå i bild hela tiden**.
3. **Mixamo-riggens FBX** (Mixamo Rig FBX): karaktären från steg 5
4. **Identifiera händer** (Detect Hands) är av. Slå på det bara när fingrarna
   ska röra sig. Klicka sedan på **Välj MANO-handmodell…** (Choose MANO Hand
   Model…) och välj `MANO_RIGHT.pkl`. Den filen hämtas på samma sätt som
   SMPL-X: registrera dig på [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/),
   ladda ner **Models & Code** och packa upp. Första handpasset laddar ner
   ungefär **2,7 GB** till, en gång, och tar ungefär dubbelt så lång tid som
   ett pass med bara kroppen. När händerna är på syns **Utjämning av fingrar
   (sekunder)** (Finger Smoothing (seconds)). Det mjukar upp fingerrörelsen.
   Standard är 0,08 sekunder; 0 behåller det som hittades.
5. Klicka på **Generera rörelse** (Generate Motion)

När det är klart importeras den animerade karaktären till scenen automatiskt.
En fot som står i marken stannar där den landade, och sulan läggs på Blenders
golv. Ett **Golvmarkörer**-mesh (Floor Markers) läggs till på det golvet (ett
kryss var 0,5 m). Kryssrutan **Golvmarkörer** (Floor Markers) under Förlopp /
Resultat visar eller döljer det.

### Första körningen tar längre tid — det är normalt

Första gången laddar tillägget ner ungefär **5,6 GB** modeller. Panelen visar
nedladdningens storlek, hastighet och tid som är kvar. Modellerna laddas ner
bara en gång.

Sedan bearbetas videon på din dator. På en Mac-CPU tar ett 10-sekundersklipp
några minuter. Blender går att använda medan det kör, och **Avbryt** (Cancel)
stoppar jobbet.

## Tips för ett bra resultat

- Bara en person, hela kroppen synlig, inte avskuren i kanterna
- Stillastående kamera, bra ljus, enkla kläder hellre än vida eller fladdrande
- Korta klipp (5–20 sekunder) går snabbare att prova först

## Uppdatera till en ny version

Tillägget uppdateras ofta. Så här uppdaterar du:

1. Ladda ner den nyaste zip-filen från
   [senaste utgåvan](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → ta bort den gamla **Motion2MixamoRig**, avsluta Blender
   helt (**Cmd+Q**), öppna igen och installera den nya zip-filen.
3. I panelen klickar du på **Uppdatera körningsmiljön** (Update Runtime).

Uppdateringen behåller de nedladdade modellerna, så den går snabbt. Den
installerade versionen visas bredvid tillägget i **Get Extensions**.

## Panelen

- **⚙ bredvid titeln** visar eller döljer rutan **Inställningar** (Setup).
- **Inställningar**: språk, körningsmiljö, SMPL-X, enhet (CPU är det säkra
  valet) och **Kontrollera miljön** (Check Environment).
- **Input**: vad som ska animeras, **Kroppsmodell** (Body Model, GVHMR) och
  **Identifiera händer** (Detect Hands).
- **Förlopp / Resultat** (Progress / Result): förlopp, senaste loggen och efter
  ett jobb **Importera den genererade karaktären** (Import Generated
  Character), kryssrutan **Golvmarkörer** (Floor Markers), **Öppna
  utdatamappen** (Open Output Folder), **Visa hela loggen** (View Full Log).
- **Diagnostik** (Diagnostics): var karaktärens kroppsdelar går in i varandra
  (en hand inuti huvudet, korsade armar). Röda celler i raden är bildrutor med
  ett problem; klicka på en för att gå dit. Triangeln under raden följer den
  aktuella bildrutan, och under den står delarna som korsas och hur djupt.
  **Föregående** / **Nästa** (Previous / Next) hoppar mellan problemen.
  **Öppna HTML-rapport** (Open HTML Report) öppnar en rapport i webbläsaren
  med källvideon bredvid karaktären (första gången tar det ungefär 15 sekunder
  att bygga). Den videon behöver ffmpeg installerat på datorn (på en Mac,
  `brew install ffmpeg`); utan det förblir rutan tom. Karaktären står på fasta
  golvkryss, ett var 0,5 m, så att du ser om den glider. Den bärnstensfärgade
  banan ovanför de röda spåren är till för anteckningar du gör med ögat. De
  listas under **Notes** till höger; klicka på en för att hoppa dit.
  **Download notes** sparar de anteckningarna tillsammans med korsningstiderna.
  Filen döps efter källvideon.

Tilläggets panel finns på 19 språk. **Auto** följer Blenders språk när det
språket är ett av dem; annars stannar panelen på engelska. Byt i rutan
Inställningar under **Gränssnittsspråk** (UI Language). Den här handboken är
på svenska; det valet finns inte i panelen ännu, och de engelska namnen inom
parentes är texten på knapparna.

## Om något går fel

| Det du ser | Det du gör |
| --- | --- |
| Installationen av körningsmiljön misslyckades (Runtime installation failed) | Kontrollera internet och klicka på knappen igen. Logg: `~/Motion2MixamoRig/logs/setup.log` |
| SMPL-X-modell: saknas (SMPL-X model: missing) | Gör steg 4 igen och välj `SMPLX_NEUTRAL.npz` |
| MANO-handmodell: saknas (MANO hand model: missing) | Slå på **Identifiera händer**, sedan **Välj MANO-handmodell…** och välj `MANO_RIGHT.pkl` |
| Mixamo-FBX ogiltig (Mixamo FBX invalid) | Ladda ner karaktären igen som **FBX Binary**, **T-pose** |
| Indata innehåller flera personer (Input contains multiple people) | Använd ett klipp med bara en person |
| Ingen person hittades (No person was detected) | Se till att hela kroppen syns och är bra belyst |
| Pipeline-processen avslutades oväntat (Pipeline process exited unexpectedly) | Klicka på **Visa hela loggen** (View Full Log) |

När du ber om hjälp, bifoga loggen och säg vilken version av tillägget du använder.

## Avinstallera

1. **Get Extensions** → ta bort **Motion2MixamoRig**.
2. Ta bort mappen **`~/Motion2MixamoRig`** (din hemmapp →
   `Motion2MixamoRig`). Att ta bort tillägget tar **inte** bort mappen, och den
   rymmer ungefär 7 GB körningsmiljö och modeller, plus dina genererade
   resultat i `app/outputs/`.

## Licens

Motion2MixamoRig är **bara för icke-kommersiell användning**: det bygger på
forskningsmodeller (som GVHMR och SMPL-X) vars licenser inte tillåter
kommersiell användning. Se [`NOTICE.md`](../../NOTICE.md).
