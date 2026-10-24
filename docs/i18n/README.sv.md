# Motion2MixamoRig

<p align="center">
  <a href="#förutsättningar"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.sv.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · Svenska
</p>

För över rörelsen hos en person i en video — eller posen i ett stillbildsfoto — till en 3D-karaktär med Adobe Mixamo-rigg.

För spelutvecklare: ge den en actionvideo med **en enda person** (eller ett foto) och en Mixamo-karaktär. Den skriver förhandsvisningsvideor och en karaktärsfil med skinning (`.glb`) som du kan släppa in i Blender eller Unity.

> Motion2MixamoRig är tills vidare experimentellt. Version 0.1.8 är kommandoradspipelinen. Det här arkivet innehåller också ett tillägg för Blender 4.2+ som kör samma pipeline i en extern Python-miljö. Bygg tillägget från källkoden: [`blender_extension/README.md`](../../blender_extension/README.md).

## Två sätt att använda det

### 🎨 I Blender — utan att programmera

1. Ladda ner zip-filen för din plattform, till exempel `motion2mixamorig-<version>-macos-arm64.zip`, från [senaste utgåvan](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. I Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, välj zip-filen.
3. 3D Viewport → tryck **N** → fliken **Motion2MixamoRig** → **Installera körningsmiljön (ett klick)** (Install Runtime (one click)).
4. **Välj SMPL-X-modell…** (Choose SMPL-X Model…) (gratis nedladdning) och välj en FBX med en Mixamo-karaktär.
5. Välj en video med en person → **Generera rörelse** (Generate Motion).

Steg för steg, tips och uppdatering: **[Användarhandbok](user-guide.sv.md)**. Testat på macOS (Apple Silicon).

### 💻 Kommandoraden — för utvecklare

Klona arkivet och kör pipelinen själv: börja vid [Förutsättningar](#förutsättningar).

Agenter ska börja med [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Öppna <a href="../assets/demo.mp4">demo.mp4</a> i det här arkivet.</sub>
</p>

En till demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Diagnostikrapport (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Förutsättningar

Python 3.11+. Efter klonen skapar du en virtualenv och installerar beroendena. Då finns kommandot `m2mr`:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Installera beroenden och det här projektet. chumpy (ett äldre paket i
# beroendekedjan) importerar pip i sitt installationsskript, vilket misslyckas
# med "No module named 'pip'" i pips isolerade standardbygge. Installera det
# först med isoleringen avstängd, och installera sedan det här projektet.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Inferensvikterna laddas inte ner här. Första `m2mr run` hämtar GVHMR-vikterna till `weights/` (~5 GB, bara en gång). Första `m2mr run --detect-hands` hämtar också HaMeR-handvikterna till `weights/hamer/` (~2,7 GB, bara en gång).

ffmpeg rekommenderas (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Pipelinen körs utan det, men videorna som skrivs ut blir **tysta** och spelas inte upp i en webbläsare.

## Innan du kör: lägg de här filerna i `assets/`

Arkivet innehåller inte de här filerna; du måste hämta dem. SMPL-X-filnamnet måste stämma exakt med tabellen. FBX-, video- och bildnamn kan vara vad som helst. En körning behöver SMPL-X, en Mixamo-karaktär och **antingen** en video **eller** ett foto. Mixamo-karaktärer som exporterats om från Cinema 4D fungerar också; se [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Vad | Var | Var du får tag i det |
|---|---|---|
| SMPL-X-kroppsmodell | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Registrera dig på [SMPL-X](https://smpl-x.is.tue.mpg.de/) och ladda ner den |
| Mixamo-karaktärens FBX | `assets/mixamo/Y_Bot.fbx` | Med ett Adobe-konto, ladda ner Y Bot (eller en annan karaktär med Mixamo-rigg) från [Mixamo](https://www.mixamo.com) |
| Actionvideo | `assets/video/<your_clip>.mp4` | Ett klipp med **exakt en** tydligt synlig person, **från huvud till tå i bild hela tiden** (du kan ha flera filer; varje körning tar den som lades till senast) |
| Posfoto (valfritt) | `assets/image/<your_photo>.jpg` | Ett foto med **exakt en** tydligt synlig person, **från huvud till tå i bild**. Använd med `--image` |
| MANO högerhand (bara för `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Registrera dig på [MANO](https://mano.is.tue.mpg.de/) och ladda ner **Models & Code**. En körning med bara kroppen behöver inte den här filen |

Obs: filen från Mixamo heter `Y Bot.fbx` (**mellanslag**), ett tecken ifrån `Y_Bot.fbx` (**understreck**) i tabellen.
Döp om den till formen med understreck så blir den standardriggen (`m2mr run` utan `--rig`). Det går också bra att lämna mellanslaget: om `Y_Bot.fbx` saknas används den första `.fbx`-filen i `assets/mixamo/`.

`assets/video/` kan innehålla flera videor. Utan `--video` eller `--image` använder körningen filen som **lades till senast** i `assets/video/`. Om mappen är tom tas det senaste fotot i `assets/image/`.
Varje klipp eller foto ska visa bara en person, **från huvud till tå i bild**, utan att något är avskuret i kanterna. `m2mr doctor` / `m2mr run` stannar före extraktionen om två personer syns.

## Snabbstart

Resultaten hamnar i `outputs/<run-time>_<source>/`. Videokörningar skriver `videos/`; fotokörningar skriver `images/`.

### 1. Kontrollera tillgångar och miljön

Allt som saknas skrivs ut tillsammans med var det laddas ner och var det ska ligga.

```bash
m2mr doctor
```

`m2mr doctor` kontrollerar kroppskörningen. Den kräver inte MANO-handmodellen. Så här kontrollerar du också den extra filen och Python-paketen för fingerigenkänning:

```bash
m2mr doctor --detect-hands
```

### 2. Första körningen: få något på skärmen

Utan flaggor används **den senaste filen i `assets/video/`** och `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Det här är det långsamma steget. Första körningen laddar ner ~5 GB inferensvikter (bara en gång) och extraherar sedan människans rörelse ur videon.
På CPU tar ett klipp på ~30 sekunder ungefär 8–15 minuter att extrahera. Senare körningar av liknande längd, när vikterna redan finns, tar ungefär 3–5 minuter.
Retarget och rendering tar oftast en minut eller två. Att återanvända ett skelett med `--skeleton` i nästa avsnitt hoppar över extraktionen helt och blir klar på några tiotal sekunder.

En fot som står i marken fästs som standard: trampdynan när trampdynan är nere, hälen bara när tårna är uppe. Om ett rakt ben inte når den punkten flyttas höfterna. Sulan läggs sedan på golvet (y = 0). `--no-foot-lock` behåller den råa retargeten, så fötterna kan glida. Sulan läggs ändå på golvet.

### 3. Samma rörelse, annan karaktär

Ladda ner en annan karaktär från Mixamo till `assets/mixamo/`. **Kör inte om med bara `--rig` ändrad** — då görs den långsamma extraktionen igen.
Skicka `--skeleton` för att återanvända skelettet från en tidigare körning. Minuter blir tiotals sekunder:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. En annan video

`--video` väljer klippet. Det kombineras fritt med `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Ett foto (statisk pose)

`--image` återskapar en **statisk 3D-pose** från ett foto av en person och för över den till Mixamo-karaktären på samma sätt som en videokörning. Förhandsvisningarna är fyra bilder i `images/` (samma vyer som videokörningen) plus ett omloppsklipp vänster/höger, `before_after_360_compare.mp4`. Skicka inte `--video` samtidigt.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` utan sökväg använder filen som lades till senast i `assets/image/`.

### 6. Leta efter självkorsningar

Varje körning kontrollerar också den färdiga karaktären efter **självkorsning** — en kroppsdel som går in i en annan, till exempel en hand inuti huvudet — och skriver `diagnostics.json`. Terminalen skriver en rad, till exempel `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Golvet kontrolleras inte.

För att kontrollera en körning igen, eller för att se problemen:

```bash
m2mr diagnose outputs/<run>                  # skriv om diagnostics.json
m2mr diagnose outputs/<run> --visualize      # också diagnostics.html: källvideon bredvid karaktären, tidslinje, klickbar problemlista
m2mr diagnose outputs/<run> --threshold-cm 2 # rapportera bara intrång djupare än 2 cm (standard 1)
```

Varje problem i `diagnostics.json` är ett par kroppsdelar med de bildruteintervall där de korsas, den värsta bildrutan och dess djup. Bildrutenumren räknas från 0, som Blenders tidslinje efter en glTF-import. Delar som sitter ihop i en led (överarm och underarm, bål och lår, …) jämförs inte: deras skinn överlappar runt leden i vilken pose som helst. `diagnostics.html` bäddar in källvideon (behöver `ffmpeg`) och laddar three.js från ett CDN, så 3D-vyn behöver internet. Den vyn har fasta golvmarkörer på y = 0 — ett kryss var 0,5 m, ett större varje meter och ett grönt kryss i origo — så att du kan bedöma om karaktären rör sig. Den bärnstensfärgade banan ovanför korsningsspåren är till för anteckningar gjorda med ögat (dra ett intervall, eller In / Out). Listan **Notes** till höger visar dem; ett klick på en rad hoppar dit. **Download notes** sparar de anteckningarna tillsammans med korsningslistan. Filen döps efter källvideon och sparar videons sökväg.

### 7. Fingrar (`--detect-hands`)

Ett vanligt `m2mr run` rör kroppen och lämnar Mixamos fingerben i vila. `--detect-hands` slår på handmodellen som följer med kroppsextraktorn. Med standardextraktorn, GVHMR, är den modellen [HaMeR](https://github.com/geopavlakos/hamer). HaMeR beskär handlederna från personen och från de bildrutor GVHMR redan valt. Den letar inte efter en andra person i klippet.

**Tiden ungefär fördubblas.** Ett klipp som utan flaggan blir klart på några minuter tar ungefär dubbelt så lång tid med `--detect-hands`, eftersom handpasset körs ovanpå kroppsextraktionen. På en lång video, räkna med den extra tiden innan du startar.

Lägg `MANO_RIGHT.pkl` som i tabellen ovan och kör sedan:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Första körningen med `--detect-hands` laddar ner HaMeR-vikterna till `weights/hamer/` (~2,7 GB, en gång). Fingerrotationerna skrivs till `skeleton_motion.npz` och driver de 30 Mixamo-fingerbenen på den skinnade karaktären. En handled som kroppspasset inte såg tydligt stannar i vila för den handen.

`--hand-smooth` är hur många sekunders utjämning som ska läggas på de rotationerna. Standard är `0.08`. `0` behåller den råa skattningen. Utjämningen körs när skelettfilen redan innehåller handrörelse, också vid en senare körning som bara återanvänder den filen.

När du återanvänder ett tidigare skelett:

- Filen innehåller redan handrörelse: `--skeleton` driver fingrarna av sig själv. `--detect-hands` behövs inte igen.
- Den gör det inte, men den körningens kroppscache ligger kvar bredvid (`cache/<clip>/0_input_video.mp4`, plus `preprocess/vitpose.pt` och `preprocess/bbx.pt`): `--skeleton ... --detect-hands` lägger till fingrarna utan att extrahera kroppen igen.
- Den cachen är borta: kör videon eller fotot igen med `--detect-hands`.

## Utdata

Varje `m2mr run` skapar en mapp döpt efter **tiden då kommandot startade**. Filerna i roten är desamma för video och foto; bara förhandsvisningsmappen ändras.

```
outputs/20260829_193205_dance/          # eller …_pose/ för ett foto
├── run.json                            # starttid, indata, hela kommandot
├── skeleton_motion.npz                 # 3D-skelett av människan (återanvänd med --skeleton)
├── mixamo_rotations.npz                # Mixamo-rotationer per ben
├── mixamo_character.glb                # skinnad karaktär, importera i Blender / Unity
├── diagnostics.json                    # självkorsningsrapport (se snabbstart steg 6)
├── diagnostics.html                    # bara efter `m2mr diagnose <run> --visualize`
└── videos/   eller   images/           # förhandsvisningar — beror på indata
```

**Video som indata** skriver `videos/` (samma bildförhållande som klippet):

```
videos/
├── human_skeleton.mp4                  # återskapat 3D-skelett av människan
├── mixamo_skeleton.mp4                 # Mixamo-riggens skelett
├── mixamo_character.mp4                # skinnad Mixamo-karaktär
└── compare.mp4                         # 2×2: original (uppe vänster) / Mixamo-skelett (uppe höger)
                                        #      människoskelett (nere vänster) / karaktär (nere höger)
```

**Foto som indata** skriver i stället `images/` (samma fyra vyer, plus en vridning):

```
images/
├── human_skeleton.png                  # återskapat 3D-skelett av människan
├── mixamo_skeleton.png                 # Mixamo-riggens skelett
├── mixamo_character.png                # skinnad Mixamo-karaktär
├── compare.png                         # 2×2: original (uppe vänster) / Mixamo-skelett (uppe höger)
│                                       #      människoskelett (nere vänster) / karaktär (nere höger)
└── before_after_360_compare.mp4        # vänster: originalfotot
                                        # höger: riggens omlopp i 10° (ett helt varv)
```

Med `--detect-hands` lagrar `skeleton_motion.npz` också fingerrotationerna, och `mixamo_rotations.npz` / `mixamo_character.glb` innehåller de 30 fingerbenen. Utan den flaggan, och utan handrörelse som redan ligger i ett återanvänt skelett, stannar de benen i vila.

Öppna `mixamo_character.glb` i Blender: File → Import → glTF 2.0 (.glb/.gltf). Om kameran är riktad mot tomrum, markera karaktärens mesh och använd View → Frame Selected. Klustret av sfärer på huvudet och händerna är benvisning, inte meshen: dölj **Icosphere** och **armature** i Outliner och lämna den skinnade meshen synlig. Sätt scenens FPS från `run.json` (`fps`) och tidslinjen till bildrutorna 0 till `n_frames` − 1, så att uppspelningen stämmer med källan och bildrutenumren med `diagnostics.json`. Jämför en videokörning med `videos/mixamo_character.mp4`, en fotokörning med `images/mixamo_character.png` eller omloppsklippet.

## Licens

Koden i det här arkivet är Apache-2.0. Tillgångarna du laddar ner har egna villkor och får inte spridas tillsammans med det här arkivet:

- **SMPL-X**: MPI-styrt; som standard bara icke-kommersiell forskning / utbildning / konst; kommersiell användning kräver ett separat avtal
- **MANO** (bara om du använder `--detect-hands`): MPI-styrt, samma sorts nedladdning som SMPL-X; lägg `MANO_RIGHT.pkl` lokalt och sprid den inte
- **Mixamo-FBX**: går bra i en färdig produkt; sprid inte den råa FBX-filen som ett tillgångspaket
- **GVHMR-vikter**: laddas ner automatiskt till `weights/` vid första `m2mr run`, under uppströmslicensen
- **HaMeR**: inferenskoden i det här arkivet är MIT; vikterna laddas ner till `weights/hamer/` vid första `m2mr run --detect-hands`, under uppströmsutgåvans villkor

## Kontakt

Om du stöter på ett problem, behöver hjälp att bli klar med en lokal installation eller vill prata om ett samarbete, mejla:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
