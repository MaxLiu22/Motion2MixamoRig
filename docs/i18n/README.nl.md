# Motion2MixamoRig

<p align="center">
  <a href="#vereisten"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.nl.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · Nederlands · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Zet de beweging van een persoon in een video — of de pose op een foto — over op een 3D-personage dat met Adobe Mixamo is gerigd.

Voor gameontwikkelaars: geef een actievideo met **één persoon** (of een foto) en een Mixamo-personage op; het levert previewvideo's en een geskind personagebestand (`.glb`) dat je direct in Blender of Unity kunt laden.

> Motion2MixamoRig is momenteel experimenteel. Versie 0.1.8 is de command-line-pipeline. Deze repository bevat ook een Blender 4.2+ Extension die dezelfde pipeline in een externe Python-omgeving uitvoert. De add-on vanuit de broncode bouwen: [`blender_extension/README.md`](../../blender_extension/README.md).

## Twee manieren om het te gebruiken

### 🎨 In Blender — zonder programmeren

1. Download de zip voor je platform, bijv. `motion2mixamorig-<version>-macos-arm64.zip`, van de [nieuwste release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. In Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…** en kies de zip.
3. 3D Viewport → druk op **N** → tabblad **Motion2MixamoRig** → **Runtime installeren (één klik)** (Install Runtime (one click)).
4. **SMPL-X-model kiezen…** (Choose SMPL-X Model…; gratis te downloaden) en kies een FBX van een Mixamo-personage.
5. Kies een video van één persoon → **Beweging genereren** (Generate Motion).

Stapsgewijze instructies, tips en bijwerken: **[Gebruikershandleiding](user-guide.nl.md)**. Getest op macOS (Apple Silicon).

### 💻 Command line — voor ontwikkelaars

Clone de repository en voer de pipeline zelf uit: begin bij [Vereisten](#vereisten).

Agents moeten beginnen bij [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Open <a href="../assets/demo.mp4">demo.mp4</a> in deze repository.</sub>
</p>

Nog een demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Diagnoserapport (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Vereisten

Python 3.11+. Maak na het clonen een virtualenv aan en installeer de afhankelijkheden; daarna is het commando `m2mr` beschikbaar:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Installeer de afhankelijkheden en dit project. chumpy (een oud pakket in de
# afhankelijkheidsketen) importeert pip in zijn setup-script en faalt daardoor met
# "No module named 'pip'" in de standaard geïsoleerde build van pip. Installeer het
# eerst met isolatie uitgeschakeld en installeer daarna dit project.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

De inferentiegewichten (GVHMR enz.) worden in deze stap niet gedownload. De eerste `m2mr run` haalt ze op naar `weights/` (~5 GB, maar één keer). De eerste `m2mr run --detect-hands` haalt ook de HaMeR-handgewichten op naar `weights/hamer/` (~2,7 GB, maar één keer).

ffmpeg wordt aanbevolen (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
De pipeline werkt ook zonder, maar de uitvoervideo's zijn dan **zonder geluid** en spelen niet af in een browser.

## Voordat je start: zet deze bestanden in `assets/`

Deze repository levert deze bestanden niet mee; je moet ze zelf ophalen. De bestandsnaam van SMPL-X moet exact overeenkomen met de tabel; de namen van FBX-, video- en afbeeldingsbestanden zijn vrij. Elke run heeft SMPL-X, een Mixamo-personage en **ofwel** een video **ofwel** een foto nodig. Mixamo-personages die opnieuw uit Cinema 4D zijn geëxporteerd werken ook; zie [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Wat | Waar | Waar te krijgen |
|---|---|---|
| SMPL-X-lichaamsmodel | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Registreer je op [SMPL-X](https://smpl-x.is.tue.mpg.de/) en download het |
| FBX van een Mixamo-personage | `assets/mixamo/Y_Bot.fbx` | Download met een Adobe-account Y Bot (of een ander met Mixamo gerigd personage) van [Mixamo](https://www.mixamo.com) |
| Actievideo | `assets/video/<your_clip>.mp4` | Een clip met **precies één** duidelijk zichtbare persoon, **de hele tijd van top tot teen in beeld** (je kunt meerdere bestanden bewaren; elke run gebruikt het laatst toegevoegde) |
| Posefoto (optioneel) | `assets/image/<your_photo>.jpg` | Een foto met **precies één** duidelijk zichtbare persoon, **van top tot teen in beeld**. Te gebruiken met `--image` |
| MANO-rechterhand (alleen voor `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Registreer bij [MANO](https://mano.is.tue.mpg.de/) en download **Models & Code**. Een run met alleen het lichaam heeft dit bestand niet nodig |

Let op: het bestand dat je van Mixamo downloadt heet `Y Bot.fbx` (**met spatie**), één teken anders dan `Y_Bot.fbx` (**met underscore**) in de tabel.
Hernoem het naar de vorm met underscore en het wordt de standaard-rig (`m2mr run` zonder `--rig`). De spatie laten staan werkt ook — als `Y_Bot.fbx` ontbreekt, wordt het eerste `.fbx`-bestand in `assets/mixamo/` gebruikt.

`assets/video/` kan meerdere video's bevatten. Zonder `--video` of `--image` gebruikt de run het bestand dat **het laatst is toegevoegd** aan `assets/video/`; als die map leeg is, valt hij terug op de nieuwste foto in `assets/image/`.
Elke clip of foto mag maar één persoon tonen, **van top tot teen in beeld** — niets afgesneden aan de randen. `m2mr doctor` / `m2mr run` stoppen vóór de extractie als er twee personen in beeld zijn.

## Snel aan de slag

Resultaten komen in `outputs/<run-time>_<source>/`. Runs met een video schrijven naar `videos/`; runs met een foto schrijven naar `images/`.

### 1. Controleer de assets en de omgeving

Alles wat ontbreekt wordt getoond, samen met waar je het kunt downloaden en waar je het moet neerzetten.

```bash
m2mr doctor
```

`m2mr doctor` controleert de lichaamsrun. Het MANO-handmodel is niet verplicht. Om ook het extra bestand en de Python-pakketten voor vingerdetectie te controleren:

```bash
m2mr doctor --detect-hands
```

### 2. Eerste run: krijg iets op je scherm

Zonder opties gebruikt dit **het nieuwste bestand in `assets/video/`** en `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Dit is de langzame stap. De eerste run downloadt ~5 GB aan inferentiegewichten (maar één keer) en haalt daarna de menselijke beweging uit de video.
Op een CPU duurt de extractie van een clip van ~30 seconden ongeveer 8–15 minuten; latere runs van vergelijkbare lengte, met de gewichten al aanwezig, duren ongeveer 3–5 minuten.
Retargeting en rendering duren meestal een minuut of twee. Een skelet hergebruiken met `--skeleton` in de volgende sectie slaat de extractie volledig over en is binnen enkele tientallen seconden klaar.

Een neergezette voet wordt standaard vastgezet: de bal als de bal op de grond staat, de hiel alleen als de tenen omhoog zijn. Als een gestrekt been dat punt niet haalt, schuiven de heupen. Daarna staat de zool op de vloer (y = 0). `--no-foot-lock` houdt de ruwe retarget, dus de voeten kunnen schuiven; de zool wordt toch op de vloer gezet.

### 3. Dezelfde beweging, een ander personage

Download een ander personage van Mixamo naar `assets/mixamo/`. **Draai niet opnieuw met alleen `--rig`** — dan wordt de langzame extractie herhaald.
Geef `--skeleton` mee om het skelet van een eerdere run te hergebruiken; minuten worden enkele tientallen seconden:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Een andere video

`--video` kiest de clip. Het is vrij te combineren met `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Een foto (statische pose)

`--image` reconstrueert een **statische 3D-pose** uit een foto van één persoon en zet die vervolgens op dezelfde manier als bij een videorun over op het Mixamo-personage. De previews zijn vier stilstaande beelden in `images/` (dezelfde weergaven als bij een videorun), plus een links/rechts draaiende orbitclip `before_after_360_compare.mp4`. Geef niet tegelijk `--video` mee.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` zonder pad gebruikt het bestand dat het laatst is toegevoegd aan `assets/image/`.

### 6. Controleren op zelfdoorsnijding

Elke run controleert het afgewerkte personage ook op **zelfdoorsnijding** — een lichaamsdeel dat in een ander gaat, zoals een hand in het hoofd — en schrijft `diagnostics.json`. De terminal toont één regel, bijv. `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. De vloer wordt niet gecontroleerd.

Om een run opnieuw te controleren, of om de problemen te bekijken:

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json opnieuw schrijven
m2mr diagnose outputs/<run> --visualize      # ook diagnostics.html: bronvideo naast het personage, tijdlijn, klikbare lijst met problemen
m2mr diagnose outputs/<run> --threshold-cm 2 # alleen doordringingen dieper dan 2 cm melden (standaard 1)
```

Elk probleem in `diagnostics.json` is een paar lichaamsdelen met de framebereiken waarin ze elkaar doorsnijden, het ergste frame en de diepte daarvan. Framenummers tellen vanaf 0, zoals de tijdlijn van Blender na een glTF-import. Delen die via een gewricht verbonden zijn (bovenarm en onderarm, romp en dij, …) worden niet vergeleken: hun huid overlapt rond het gewricht in elke pose. `diagnostics.html` bevat de bronvideo (vereist `ffmpeg`) en laadt three.js van een CDN, dus de 3D-weergave heeft een internetverbinding nodig. Die weergave tekent vaste vloermarkeringen op y = 0: een kruis elke 0,5 m, een groter kruis per meter en een groen kruis in de oorsprong, zodat je kunt zien of het personage beweegt. De amberkleurige baan boven de snijsporen is voor notities die je met het oog ziet (sleep een bereik, of **In** / **Out**). De lijst **Notes** rechts toont ze; een klik op een rij springt ernaartoe. **Download notes** bewaart die notities samen met de snijlijst. Het bestand heet naar de bronvideo en bevat het pad daarvan.

### 7. Vingers (`--detect-hands`)

Een gewone `m2mr run` beweegt het lichaam en laat de Mixamo-vingerbotten in rust. `--detect-hands` zet het handmodel aan dat met de lichaamsextractor meegaat. Bij de standaardextractor, GVHMR, is dat [HaMeR](https://github.com/geopavlakos/hamer). HaMeR snijdt de polsen uit de persoon en de frames die GVHMR al koos. Er wordt niet opnieuw naar een tweede persoon in de clip gezocht.

**Dit verdubbelt de tijd ongeveer.** Een clip die zonder de vlag in een paar minuten klaar is, doet er met `--detect-hands` ongeveer twee keer zo lang over, omdat de handgang bovenop de lichaamsextractie loopt. Reken bij een lange video op die extra tijd voordat je start.

Zet `MANO_RIGHT.pkl` neer zoals in de tabel hierboven, en dan:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

De eerste run met `--detect-hands` downloadt de HaMeR-gewichten naar `weights/hamer/` (~2,7 GB, één keer). Vingerrotaties worden in `skeleton_motion.npz` geschreven en sturen de 30 Mixamo-vingerbotten van het geskinde personage aan. Een pols die de lichaamsgang niet duidelijk zag, blijft voor die hand in rust.

`--hand-smooth` is hoeveel seconden afvlakking op die rotaties wordt toegepast. De standaard is `0.08`. `0` houdt de ruwe schatting. Afvlakking gebeurt zodra het skeletbestand al handbeweging bevat, ook bij een latere run die alleen dat bestand hergebruikt.

Een eerder skelet hergebruiken:

- Het bestand bevat al handbeweging: `--skeleton` stuurt de vingers vanzelf aan. `--detect-hands` is niet opnieuw nodig.
- Dat doet het niet, maar de lichaamscache van die run ligt er nog naast (`cache/<clip>/0_input_video.mp4`, plus `preprocess/vitpose.pt` en `preprocess/bbx.pt`): `--skeleton ... --detect-hands` voegt de vingers toe zonder het lichaam opnieuw te extraheren.
- Die cache is weg: draai de video of de foto opnieuw met `--detect-hands`.

## Uitvoer

Elke `m2mr run` maakt een map aan die is genoemd naar **het tijdstip waarop het commando startte**. De bestanden in de hoofdmap zijn hetzelfde voor video en foto; alleen de previewmap verschilt.

```
outputs/20260829_193205_dance/          # of …_pose/ voor een foto
├── run.json                            # starttijd, invoer, volledig commando
├── skeleton_motion.npz                 # 3D-skelet van de persoon (hergebruik met --skeleton)
├── mixamo_rotations.npz                # Mixamo-rotaties per bot
├── mixamo_character.glb                # geskind personage, te importeren in Blender / Unity
├── diagnostics.json                    # rapport over zelfdoorsnijding (zie Snel aan de slag, stap 6)
├── diagnostics.html                    # alleen na `m2mr diagnose <run> --visualize`
└── videos/   of   images/              # previews — afhankelijk van de invoer
```

**Video-invoer** schrijft naar `videos/` (dezelfde beeldverhouding als de clip):

```
videos/
├── human_skeleton.mp4                  # gereconstrueerd 3D-skelet van de persoon
├── mixamo_skeleton.mp4                 # skelet van de Mixamo-rig
├── mixamo_character.mp4                # geskind Mixamo-personage
└── compare.mp4                         # 2×2: origineel (linksboven) / Mixamo-skelet (rechtsboven)
                                        #      menselijk skelet (linksonder) / personage (rechtsonder)
```

**Foto-invoer** schrijft in plaats daarvan naar `images/` (dezelfde vier weergaven, plus een volledige rondgang):

```
images/
├── human_skeleton.png                  # gereconstrueerd 3D-skelet van de persoon
├── mixamo_skeleton.png                 # skelet van de Mixamo-rig
├── mixamo_character.png                # geskind Mixamo-personage
├── compare.png                         # 2×2: origineel (linksboven) / Mixamo-skelet (rechtsboven)
│                                       #      menselijk skelet (linksonder) / personage (rechtsonder)
└── before_after_360_compare.mp4        # links: originele foto
                                        # rechts: orbit rond de rig in stappen van 10° (één volledige rondgang)
```

Met `--detect-hands` bevat `skeleton_motion.npz` ook de vingerrotaties, en `mixamo_rotations.npz` en `mixamo_character.glb` bevatten de 30 vingerbotten. Zonder die vlag, en zonder al opgeslagen handbeweging in een hergebruikt skelet, blijven die botten in rust.

Open `mixamo_character.glb` in Blender: File → Import → glTF 2.0 (.glb/.gltf). Als de camera op een lege ruimte gericht is, selecteer dan de mesh van het personage en gebruik View → Frame Selected. Het cluster bollen op het hoofd en de handen is de weergave van de botten, niet de mesh: verberg in de Outliner **Icosphere** en de **armature**; laat de geskinde mesh zichtbaar. Stel de FPS van de scène in op basis van `run.json` (`fps`) en de tijdlijn op frames 0 tot en met `n_frames` − 1, zodat het afspelen overeenkomt met de bron en de framenummers met `diagnostics.json`. Vergelijk een videorun met `videos/mixamo_character.mp4`, een fotorun met `images/mixamo_character.png` of de orbitclip.

## Licentie

De code van deze repository valt onder Apache-2.0. De assets die je zelf downloadt hebben hun eigen voorwaarden en mogen niet samen met deze repo worden herverspreid:

- **SMPL-X**: toegang via MPI; standaard niet-commercieel onderzoek / onderwijs / kunst; commercieel gebruik vereist een aparte overeenkomst
- **MANO** (alleen met `--detect-hands`): toegang via MPI, hetzelfde soort download als SMPL-X; zet `MANO_RIGHT.pkl` lokaal en verspreid het niet opnieuw
- **Mixamo FBX**: mag in een uitgebracht product worden gebruikt; verspreid de ruwe FBX niet als assetpakket
- **GVHMR en andere inferentiegewichten**: worden bij de eerste `m2mr run` automatisch gedownload naar `weights/`, onder de licentie van elk afzonderlijk bronproject
- **HaMeR**: de inferentiecode in deze repository is MIT; de gewichten komen bij de eerste `m2mr run --detect-hands` in `weights/hamer/`, onder de publicatievoorwaarden van upstream

## Contact

Loop je tegen een probleem aan, heb je hulp nodig bij een lokale installatie of wil je praten over samenwerking, stuur dan een e-mail naar:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
