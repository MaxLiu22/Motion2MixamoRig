# Motion2MixamoRig

<p align="center">
  <a href="#mga-kailangan"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.fil.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · Filipino · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Ilipat ang galaw ng isang tao sa video — o ang pose sa isang still na larawan — sa isang 3D character na naka-rig gamit ang Adobe Mixamo.

Para sa mga game developer: bigyan ito ng action video na may **iisang tao** (o isang still) at isang Mixamo character; gagawa ito ng mga preview video at isang skinned na character file (`.glb`) na puwede mong ilagay agad sa Blender o Unity.

> Eksperimental pa ang Motion2MixamoRig sa ngayon. Ang bersyon 0.1.8 ay ang command-line pipeline. May kasama ring Blender 4.2+ Extension ang repository na ito na nagpapatakbo ng parehong pipeline sa isang hiwalay na Python environment. Pag-build ng add-on mula sa source: [`blender_extension/README.md`](../../blender_extension/README.md).

## Dalawang paraan para gamitin ito

### 🎨 Sa Blender — walang coding

1. I-download ang zip para sa platform mo, hal. `motion2mixamorig-<version>-macos-arm64.zip`, mula sa [latest release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. Sa Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, piliin ang zip.
3. 3D Viewport → pindutin ang **N** → **Motion2MixamoRig** tab → **I-install ang Runtime (isang click)** (Install Runtime (one click)).
4. **Pumili ng SMPL-X Model…** (Choose SMPL-X Model…) (libreng download) at pumili ng Mixamo character FBX.
5. Pumili ng video ng iisang tao → **Gumawa ng Galaw** (Generate Motion).

Step-by-step na instructions, mga tip, at pag-update: **[User Guide](user-guide.fil.md)**. Na-test sa macOS (Apple Silicon).

### 💻 Command line — para sa mga developer

I-clone ang repository at ikaw mismo ang magpatakbo ng pipeline: magsimula sa [Mga Kailangan](#mga-kailangan).

Dapat magsimula ang mga agent sa [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Buksan ang <a href="../assets/demo.mp4">demo.mp4</a> sa repository na ito.</sub>
</p>

Isa pang demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Ulat ng diagnostics (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Mga Kailangan

Python 3.11+. Pagkatapos i-clone, gumawa ng virtualenv at i-install ang mga dependency; magagamit na pagkatapos ang command na `m2mr`:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# I-install ang mga dependency at ang proyektong ito. Ang chumpy (isang lumang
# package sa dependency chain) ay nag-i-import ng pip sa setup script nito, kaya
# pumapalya ito ng "No module named 'pip'" sa default na isolated build ng pip.
# I-install muna ito nang naka-off ang isolation, saka i-install ang proyekto.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Hindi dina-download dito ang mga inference weight (GVHMR at iba pa). Ang unang `m2mr run` ang magda-download ng mga ito sa `weights/` (~5 GB, isang beses lang). Ang unang `m2mr run --detect-hands` ay magda-download din ng mga HaMeR hand weight sa `weights/hamer/` (~2.7 GB, isang beses lang).

Inirerekomenda ang ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Tatakbo ang pipeline kahit wala ito, pero **walang tunog** ang mga output video at hindi ito mapapatugtog sa browser.

## Bago tumakbo: ilagay ang mga ito sa `assets/`

Hindi kasama sa repository na ito ang mga file na ito; kailangan mo silang kunin. Dapat eksaktong tugma sa table ang filename ng SMPL-X; puwedeng kahit ano ang pangalan ng FBX, video, at larawan. Kailangan ng bawat run ang SMPL-X, isang Mixamo character, at **alinman sa** isang video **o** isang still. Gumagana rin ang mga Mixamo character na ni-re-export mula sa Cinema 4D; tingnan ang [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Ano | Saan ilalagay | Saan kukunin |
|---|---|---|
| SMPL-X body model | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Mag-register sa [SMPL-X](https://smpl-x.is.tue.mpg.de/) at i-download ito |
| Mixamo character FBX | `assets/mixamo/Y_Bot.fbx` | Gamit ang Adobe account, i-download ang Y Bot (o ibang character na naka-rig sa Mixamo) mula sa [Mixamo](https://www.mixamo.com) |
| Action video | `assets/video/<your_clip>.mp4` | Isang clip na may **eksaktong isang** taong malinaw na nakikita, **mula ulo hanggang paa na nasa frame sa buong video** (puwedeng maglagay ng ilang file; ang pinakahuling idinagdag ang gagamitin sa bawat run) |
| Still ng pose (opsyonal) | `assets/image/<your_photo>.jpg` | Isang larawan na may **eksaktong isang** taong malinaw na nakikita, **mula ulo hanggang paa na nasa frame**. Gamitin kasama ng `--image` |
| Kanang kamay ng MANO (para lang sa `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Magrehistro sa [MANO](https://mano.is.tue.mpg.de/) at i-download ang **Models & Code**. Hindi kailangan ang file na ito sa body-only na run |

Paalala: `Y Bot.fbx` (**may space**) ang pangalan ng file na dina-download mula sa Mixamo, isang character lang ang pagkakaiba sa `Y_Bot.fbx` (**may underscore**) sa table.
Palitan ito ng pangalang may underscore para ito ang maging default na rig (`m2mr run` nang walang `--rig`). Ayos lang din kung iiwan ang space — kapag walang `Y_Bot.fbx`, ang unang `.fbx` sa `assets/mixamo/` ang gagamitin.

Puwedeng maglaman ng ilang video ang `assets/video/`. Kapag walang `--video` o `--image`, ang file na **pinakahuling idinagdag** sa `assets/video/` ang gagamitin; kapag walang laman ang folder na iyon, ang pinakabagong still sa `assets/image/` ang gagamitin.
Dapat iisang tao lang ang nasa bawat clip o larawan, **mula ulo hanggang paa na nasa frame** — walang naputol sa gilid. Hihinto ang `m2mr doctor` / `m2mr run` bago ang extraction kapag may dalawang tao sa frame.

## Mabilis na Pagsisimula

Mapupunta ang mga resulta sa `outputs/<run-time>_<source>/`. Sa `videos/` sumusulat ang mga video run; sa `images/` naman ang mga still run.

### 1. Suriin ang mga asset at ang environment

Ipi-print ang anumang kulang, kasama kung saan ito ida-download at kung saan ilalagay.

```bash
m2mr doctor
```

Tinitingnan ng `m2mr doctor` ang body run. Hindi nito hinihingi ang MANO hand model. Para tingnan din ang dagdag na file at ang mga Python package na ginagamit ng pag-detect ng mga daliri:

```bash
m2mr doctor --detect-hands
```

### 2. Unang run: magpakita ng resulta sa screen

Kapag walang flag, gagamitin nito ang **pinakabagong file sa `assets/video/`** at ang `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Ito ang mabagal na hakbang. Sa unang run, magda-download ito ng ~5 GB na inference weight (isang beses lang), saka kukunin ang galaw ng tao mula sa video.
Sa CPU, mga 8–15 minuto ang extraction ng ~30 segundong clip; ang mga susunod na run na kapareho ang haba, kapag nandiyan na ang mga weight, ay mga 3–5 minuto.
Karaniwang isa o dalawang minuto ang retargeting at rendering. Kapag ginamit muli ang skeleton gamit ang `--skeleton` sa susunod na seksyon, nilalaktawan nang buo ang extraction at matatapos ito sa loob ng ilang sampung segundo.

Naka-pin nang default ang nakalapag na paa: ang bola ng paa kapag nasa baba ito, ang sakong lang kapag nakataas ang mga daliri. Kapag hindi umabot ang nakaunat na binti, gumagalaw ang balakang. Pagkatapos, inilalagay ang talampakan sa sahig (y = 0). Pinapanatili ng `--no-foot-lock` ang hilaw na retarget, kaya maaaring dumulas ang mga paa; inilalagay pa rin ang talampakan sa sahig.

### 3. Parehong galaw, ibang character

Mag-download ng isa pang character mula sa Mixamo papunta sa `assets/mixamo/`. **Huwag patakbuhin muli gamit lang ang `--rig`** — uulitin nito ang mabagal na extraction.
Ipasa ang `--skeleton` para magamit muli ang skeleton mula sa nakaraang run; mula ilang minuto, magiging ilang sampung segundo na lang:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Ibang video

Ang `--video` ang pumipili ng clip. Malaya itong maisasama sa `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Isang still na larawan (static na pose)

Kinukuha ng `--image` ang isang **static na 3D pose** mula sa larawan ng isang tao, saka ito ire-retarget sa Mixamo character sa parehong paraan ng video run. Ang mga preview ay apat na still sa `images/` (parehong mga view ng video run), kasama ang isang left/right na orbit clip na `before_after_360_compare.mp4`. Huwag ipasa ang `--video` nang sabay.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

Kapag walang path ang `--image`, ang file na pinakahuling idinagdag sa `assets/image/` ang gagamitin.

### 6. Suriin ang self-intersection

Sinusuri rin ng bawat run ang natapos na character para sa **self-intersection** — isang bahagi ng katawan na pumapasok sa isa pa, gaya ng kamay sa loob ng ulo — at isinusulat ang `diagnostics.json`. Nagpi-print ang terminal ng isang linya, hal. `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Hindi sinusuri ang sahig.

Para suriin muli ang isang run, o para makita ang mga problema:

```bash
m2mr diagnose outputs/<run>                  # isulat muli ang diagnostics.json
m2mr diagnose outputs/<run> --visualize      # pati diagnostics.html: source video katabi ng character, timeline, listahan ng problema na puwedeng i-click
m2mr diagnose outputs/<run> --threshold-cm 2 # iulat lang ang pagpasok na mas malalim sa 2 cm (default 1)
```

Ang bawat problema sa `diagnostics.json` ay isang pares ng bahagi ng katawan, kasama ang mga frame range kung saan sila nagsasalubong, ang pinakamalalang frame, at ang lalim nito. Nagsisimula sa 0 ang bilang ng frame, gaya ng timeline ng Blender pagkatapos mag-import ng glTF. Hindi pinaghahambing ang mga bahaging pinagdugtong ng kasukasuan (upper arm at forearm, torso at hita, …): nagpapatong ang balat nila sa paligid ng kasukasuan sa anumang pose. Ini-embed ng `diagnostics.html` ang source video (kailangan ng `ffmpeg`) at nilo-load ang three.js mula sa CDN, kaya kailangan ng internet ang 3D view nito. Gumuguhit ang view na iyon ng mga nakapirming marka sa sahig sa y = 0: isang krus kada 0.5 m, mas malaki kada metro, at berdeng krus sa origin, para makita kung gumagalaw ang character. Ang amber na lane sa ibabaw ng mga intersection track ay para sa mga tala na nakikita ng mata (i-drag ang isang range, o **In** / **Out**). Ipinapakita ng listahang **Notes** sa kanan ang mga ito; i-click ang isang row para lumipat doon. Sine-save ng **Download notes** ang mga talang ito kasama ang listahan ng intersection. Ipinangalan ang file sa source video at nakatala roon ang path nito.

### 7. Mga daliri (`--detect-hands`)

Ang ordinaryong `m2mr run` ay ginagalaw ang katawan at iniiwan sa rest ang mga buto ng daliri ng Mixamo. Binubuksan ng `--detect-hands` ang hand model na kasama ng body extractor. Sa default na extractor, ang GVHMR, ang model na iyon ay [HaMeR](https://github.com/geopavlakos/hamer). Kinukuha ng HaMeR ang mga pulso mula sa tao at sa mga frame na pinili na ng GVHMR. Hindi ito naghahanap ng pangalawang tao sa clip.

**Halos dumodoble ang oras.** Ang clip na matatapos sa loob ng ilang minuto kung walang flag ay aabot nang halos doble kapag may `--detect-hands`, dahil tumatakbo ang hand pass sa ibabaw ng body extraction. Sa mahabang video, isama ang oras na iyon bago magsimula.

Ilagay ang `MANO_RIGHT.pkl` gaya ng nasa talahanayan sa itaas, tapos:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Ang unang run na may `--detect-hands` ay nagda-download ng mga HaMeR weight sa `weights/hamer/` (~2.7 GB, isang beses). Isinusulat ang mga rotation ng daliri sa `skeleton_motion.npz` at minamaneho nito ang 30 buto ng daliri ng Mixamo sa skinned na character. Ang pulsong hindi malinaw na nakita ng body pass ay nananatili sa rest para sa kamay na iyon.

Sinasabi ng `--hand-smooth` kung ilang segundo ng smoothing ang ilalapat sa mga rotation na iyon. `0.08` ang default. Pinapanatili ng `0` ang hilaw na estimate. Tumatakbo ang smoothing kapag may galaw na ng kamay ang skeleton file, kasama ang susunod na run na ang file lang na iyon ang gagamitin muli.

Kapag ginamit muli ang isang dating skeleton:

- May galaw na ng kamay ang file: minamaneho ng `--skeleton` ang mga daliri nang mag-isa. Hindi na kailangan ulit ang `--detect-hands`.
- Wala, pero naroon pa ang body cache ng run na iyon (`cache/<clip>/0_input_video.mp4`, at `preprocess/vitpose.pt` at `preprocess/bbx.pt`): nagdaragdag ng mga daliri ang `--skeleton ... --detect-hands` nang hindi kinukuha muli ang katawan.
- Wala na ang cache na iyon: patakbuhin muli ang video o ang still gamit ang `--detect-hands`.

## Mga Output

Bawat `m2mr run` ay gumagawa ng directory na pinangalanan ayon sa **oras ng pagsisimula ng command**. Pareho para sa video at still ang mga file sa root; ang preview folder lang ang nagbabago.

```
outputs/20260829_193205_dance/          # o …_pose/ para sa still
├── run.json                            # oras ng simula, mga input, buong command
├── skeleton_motion.npz                 # 3D skeleton ng tao (gamitin muli sa --skeleton)
├── mixamo_rotations.npz                # Mixamo rotation ng bawat buto
├── mixamo_character.glb                # skinned na character, i-import sa Blender / Unity
├── diagnostics.json                    # ulat ng self-intersection (tingnan ang hakbang 6 ng Mabilis na Pagsisimula)
├── diagnostics.html                    # pagkatapos lang ng `m2mr diagnose <run> --visualize`
└── videos/   o   images/               # mga preview — depende sa input
```

Ang **video input** ay sumusulat sa `videos/` (parehong aspect ratio ng clip):

```
videos/
├── human_skeleton.mp4                  # na-recover na 3D skeleton ng tao
├── mixamo_skeleton.mp4                 # skeleton ng Mixamo rig
├── mixamo_character.mp4                # skinned na Mixamo character
└── compare.mp4                         # 2×2: orihinal (kaliwa-itaas) / Mixamo skeleton (kanan-itaas)
                                        #      skeleton ng tao (kaliwa-ibaba) / character (kanan-ibaba)
```

Ang **still input** naman ay sumusulat sa `images/` (parehong apat na view, dagdag ang isang turntable):

```
images/
├── human_skeleton.png                  # na-recover na 3D skeleton ng tao
├── mixamo_skeleton.png                 # skeleton ng Mixamo rig
├── mixamo_character.png                # skinned na Mixamo character
├── compare.png                         # 2×2: orihinal (kaliwa-itaas) / Mixamo skeleton (kanan-itaas)
│                                       #      skeleton ng tao (kaliwa-ibaba) / character (kanan-ibaba)
└── before_after_360_compare.mp4        # kaliwa: orihinal na larawan
                                        # kanan: 10° na orbit ng rig (isang buong ikot)
```

Kapag may `--detect-hands`, may mga rotation din ng daliri sa `skeleton_motion.npz`, at kasama sa `mixamo_rotations.npz` at `mixamo_character.glb` ang 30 buto ng daliri. Kung wala ang flag na iyon, at wala ring galaw ng kamay na naka-store na sa muling ginamit na skeleton, nananatili sa rest ang mga butong iyon.

Buksan ang `mixamo_character.glb` sa Blender: File → Import → glTF 2.0 (.glb/.gltf). Kung nakatutok ang camera sa bakanteng espasyo, piliin ang character mesh at gamitin ang View → Frame Selected. Ang kumpol ng mga sphere sa ulo at mga kamay ay display ng buto, hindi ang mesh: sa Outliner, itago ang **Icosphere** at ang **armature**; hayaang nakikita ang skinned na mesh. Itakda ang FPS ng scene mula sa `run.json` (`fps`) at ang timeline sa mga frame 0 hanggang `n_frames` − 1 para tumugma ang playback sa source at ang mga numero ng frame sa `diagnostics.json`. Ikumpara ang video run sa `videos/mixamo_character.mp4`, at ang still run sa `images/mixamo_character.png` o sa orbit clip.

## Lisensya

Apache-2.0 ang code ng repository na ito. May sariling mga tuntunin ang mga asset na ikaw mismo ang nagda-download, at hindi dapat ipamahagi muli kasama ng repo na ito:

- **SMPL-X**: may gate ng MPI; default ay hindi pangkomersyal na pananaliksik / edukasyon / sining; kailangan ng hiwalay na kasunduan para sa komersyal na paggamit
- **MANO** (kapag ginamit lang ang `--detect-hands`): may gate ng MPI, kapareho ng uri ng download ng SMPL-X; ilagay ang `MANO_RIGHT.pkl` sa lokal at huwag itong ipamahagi muli
- **Mixamo FBX**: puwede sa isang inilabas na produkto; huwag ipamahagi muli ang raw na FBX bilang asset pack
- **GVHMR at iba pang inference weight**: awtomatikong dina-download sa `weights/` sa unang `m2mr run`, sa ilalim ng lisensya ng bawat upstream
- **HaMeR**: MIT ang inference code sa repository na ito; dina-download ang mga weight sa `weights/hamer/` sa unang `m2mr run --detect-hands`, sa ilalim ng mga tuntunin ng upstream na release

## Contact

Kung may problema ka, kailangan mo ng tulong para matapos ang local setup, o gusto mong pag-usapan ang pakikipagtulungan, mag-email sa:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
