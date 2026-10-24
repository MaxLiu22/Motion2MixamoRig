# Motion2MixamoRig voor Blender — Gebruikershandleiding

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · Nederlands · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Maak van een video van één persoon een geanimeerd Mixamo-personage, gewoon in Blender.
Geen programmeren of terminal nodig.

<!-- video: link the tutorial video here -->

> Tot nu toe alleen getest op **macOS (Apple Silicon)**. Een Windows-build komt eraan.

## Wat je nodig hebt

- **Blender 4.2 of nieuwer**
- **Een internetverbinding** voor de eerste installatie
- **Ongeveer 8 GB vrije schijfruimte** (runtime ~1,3 GB + modellen ~5,6 GB)
- **Een gratis SMPL-X-account** en **een gratis Adobe-account** (voor Mixamo); zie stap 4 en 5

## 1. Download de add-on

Ga naar de [nieuwste release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
en download de zip voor je computer:

| Je computer | Bestand |
| --- | --- |
| Mac met Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Binnenkort** |

Bijvoorbeeld `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` is de versie van
de add-on, `macos-arm64` het platform. Kies je de verkeerde, dan weigert Blender
de installatie en noemt het platform dat verwacht werd.

Pak de zip **niet** uit. Blender installeert de zip zelf.

## 2. Installeer de add-on in Blender

1. **Edit → Preferences → Get Extensions**
2. Klik rechtsboven op het kleine **∨** → **Install from Disk…**
3. Kies de zip. **Motion2MixamoRig** verschijnt ingeschakeld in de lijst.
4. Sluit Preferences. Druk in de 3D Viewport op **N** en klik rechts op het
   tabblad **Motion2MixamoRig**.

<!-- screenshot: Install from Disk menu -->

## 3. Installeer de runtime (eenmalig)

Klik in het paneel op **Runtime installeren (één klik)** (Install Runtime (one click)).

De add-on downloadt zijn eigen Python en bibliotheken (~1,4 GB) naar
`~/Motion2MixamoRig/`. Verder wordt er niets op je computer aangeraakt. Dit
duurt een paar minuten; de voortgangsbalk toont de huidige stap.

<!-- screenshot: Install Runtime button and progress -->

## 4. Haal het SMPL-X-lichaamsmodel op

SMPL-X is een gratis lichaamsmodel dat de add-on nodig heeft. De licentie staat
niet toe dat wij het meeleveren, dus je downloadt het eenmalig zelf:

1. Open [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) en klik op **Register**.
   Accepteer de licentie en bevestig de e-mail.
2. Log in, open **Download** en download het SMPL-X-model (de **NPZ**-versie).
3. Pak het uit en zoek **`SMPLX_NEUTRAL.npz`**.
4. Klik in Blender op **SMPL-X-model kiezen…** (Choose SMPL-X Model…) en kies dat
   bestand. Het paneel toont dan **SMPL-X-model: gevonden** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Haal een Mixamo-personage op

1. Open [mixamo.com](https://www.mixamo.com/) en log in met een Adobe-account.
2. Tabblad **Characters** → kies een personage (bijvoorbeeld **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Genereer beweging

In het vak **Invoer** (Input):

1. **Brontype** (Source Type): Video (of Afbeelding voor één pose)
2. **Bronbestand** (Source File): je clip. Daarin moet **precies één persoon te
   zien zijn, de hele tijd van top tot teen in beeld**.
3. **Mixamo-rig FBX** (Mixamo Rig FBX): het personage uit stap 5
4. **Handen detecteren** (Detect Hands) staat uit. Zet het alleen aan als de vingers
   moeten bewegen. Klik daarna op **MANO-handmodel kiezen…** (Choose MANO Hand Model…)
   en kies `MANO_RIGHT.pkl`. Dat bestand haal je op zoals SMPL-X: registreer op
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), download **Models & Code** en pak
   het uit. De eerste handgang downloadt eenmalig ongeveer **2,7 GB** extra en duurt
   ongeveer twee keer zo lang als een run met alleen het lichaam. Staat het aan, dan verschijnt **Finger Smoothing (seconds)**. Het maakt de vingerbeweging zachter. De standaard is 0,08 seconden; 0 houdt wat er is gedetecteerd.
5. Klik op **Beweging genereren** (Generate Motion)

Als het klaar is, wordt het geanimeerde personage automatisch in je scène
geïmporteerd. Een neergezette voet blijft waar hij neerkwam, en de zool staat op de vloer van Blender. Op die vloer komt een mesh **Vloermarkeringen** (Floor Markers) (een kruis elke 0,5 m). Het vakje **Vloermarkeringen** (Floor Markers) onder Voortgang / Resultaat toont of verbergt het.

### De eerste run duurt langer — dat is normaal

De eerste keer downloadt de add-on ongeveer **5,6 GB** aan modellen. Het paneel
toont de downloadgrootte, snelheid en resterende tijd. Modellen worden maar één
keer gedownload.

Daarna wordt de video op je eigen computer verwerkt. Op een Mac-CPU duurt een
clip van 10 seconden een paar minuten. Blender blijft bruikbaar terwijl het
loopt, en **Annuleren** (Cancel) stopt de taak.

## Tips voor goede resultaten

- Slechts één persoon, het hele lichaam zichtbaar, niet afgesneden aan de randen
- Stabiele camera, goed licht, eenvoudige kleding in plaats van wijde of loshangende
- Korte clips (5–20 seconden) zijn sneller om eerst mee te proberen

## Bijwerken naar een nieuwe versie

De add-on wordt vaak bijgewerkt. Zo werk je hem bij:

1. Download de nieuwste zip van de
   [nieuwste release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → verwijder de oude **Motion2MixamoRig**, sluit Blender
   volledig af (**Cmd+Q**), open het opnieuw en installeer de nieuwe zip.
3. Klik in het paneel op **Runtime bijwerken** (Update Runtime).

Bij het bijwerken blijven de gedownloade modellen behouden, dus het gaat snel.
Je geïnstalleerde versie staat naast de add-on in **Get Extensions**.

## Het paneel

- **⚙ naast de titel** toont of verbergt het vak **Instellen** (Setup).
- **Instellen**: taal, runtime, SMPL-X, **Apparaat** (Device; CPU is de veilige
  keuze) en **Omgeving controleren** (Check Environment).
- **Invoer**: wat er geanimeerd moet worden, het **Lichaamsmodel** (Body Model, GVHMR) en **Handen detecteren** (Detect Hands).
- **Voortgang / Resultaat** (Progress / Result): voortgang, recent log en na een taak
  **Gegenereerd personage importeren** (Import Generated Character), **Vloermarkeringen** (Floor Markers), **Uitvoermap openen** (Open Output Folder),
  **Volledig log bekijken** (View Full Log).
- **Diagnose** (Diagnostics): plekken waar lichaamsdelen van het personage in
  elkaar zitten (een hand in het hoofd, gekruiste armen). Rode cellen in de
  balk zijn frames met een probleem; klik erop om erheen te gaan. Het
  driehoekje onder de balk volgt het huidige frame, en daaronder staat welke
  delen elkaar doorsnijden en hoe diep. **Vorige** / **Volgende** (Previous /
  Next) springen tussen problemen. **HTML-rapport openen** (Open HTML Report)
  opent in de webbrowser een rapport met de bronvideo naast het personage (de
  eerste keer duurt het maken ongeveer 15 seconden). De originele video heeft ffmpeg op de computer nodig (op een Mac: `brew install ffmpeg`). Zonder blijft het personage zichtbaar en is de video ernaast leeg. Het personage staat op vaste vloerkruisen, elke 0,5 m één, zodat te zien is of het schuift. De amberkleurige baan boven de rode sporen is voor notities die je met het oog maakt. Ze staan rechts onder **Notes**; een klik op een rij springt ernaartoe. **Download notes** bewaart die notities samen met de snijtijden. Het bestand heet naar de bronvideo.

De add-on spreekt 19 talen. **Automatisch (Blender / Systeem)** (Auto) volgt de taal van Blender;
je wijzigt dit in het vak Instellen onder **Interfacetaal** (UI Language).

## Als er iets misgaat

| Wat je ziet | Wat je doet |
| --- | --- |
| **Installatie van runtime mislukt** (Runtime installation failed) | Controleer je internetverbinding en klik opnieuw op de knop. Log: `~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X-model: ontbreekt** (SMPL-X model: missing) | Doe stap 4 opnieuw en kies `SMPLX_NEUTRAL.npz` |
| **MANO-handmodel: ontbreekt** (MANO hand model: missing) | Zet **Handen detecteren** aan, dan **MANO-handmodel kiezen…** en kies `MANO_RIGHT.pkl` |
| **Mixamo-FBX ongeldig** (Mixamo FBX invalid) | Download het personage opnieuw als **FBX Binary**, **T-pose** |
| **Invoer bevat meerdere personen** (Input contains multiple people) | Gebruik een clip met maar één persoon |
| **Geen persoon gevonden in de invoer** (No person was detected in the input) | Zorg dat het hele lichaam zichtbaar en goed belicht is |
| **Pipelineproces onverwacht gestopt** (Pipeline process exited unexpectedly) | Klik op **Volledig log bekijken** |

Als je om hulp vraagt, voeg dan het log toe en vermeld welke versie van de add-on je gebruikt.

## Verwijderen

1. **Get Extensions** → verwijder **Motion2MixamoRig**.
2. Verwijder de map **`~/Motion2MixamoRig`** (je thuismap →
   `Motion2MixamoRig`). Het verwijderen van de add-on verwijdert deze map
   **niet**; hij bevat ongeveer 7 GB aan runtime en modellen, plus je
   gegenereerde resultaten in `app/outputs/`.

## Licentie

Motion2MixamoRig is **alleen voor niet-commercieel gebruik**: het steunt op
onderzoeksmodellen (zoals GVHMR en SMPL-X) waarvan de licenties geen commercieel
gebruik toestaan. Zie [`NOTICE.md`](../../NOTICE.md).
