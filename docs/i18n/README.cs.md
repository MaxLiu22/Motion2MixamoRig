# Motion2MixamoRig

<p align="center">
  <a href="#požadavky"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.cs.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · Čeština · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Přeneste pohyb člověka ve videu — nebo pózu na fotografii — na 3D postavu s rigem Adobe Mixamo.

Pro vývojáře her: dejte mu akční video s **jednou osobou** (nebo fotografii) a postavu Mixamo; zapíše náhledová videa a soubor postavy se skinningem (`.glb`), který můžete přetáhnout do Blenderu nebo Unity.

> Motion2MixamoRig je zatím experimentální. Verze 0.1.8 je pipeline pro příkazový řádek. Tento repozitář obsahuje také rozšíření pro Blender 4.2+, které spouští stejný pipeline v externím prostředí Pythonu. Sestavení doplňku ze zdrojů: [`blender_extension/README.md`](../../blender_extension/README.md).

## Dva způsoby použití

### 🎨 V Blenderu — bez programování

1. Stáhněte zip pro svou platformu, například `motion2mixamorig-<version>-macos-arm64.zip`, z [nejnovějšího vydání](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. V Blenderu: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, vyberte zip.
3. 3D Viewport → stiskněte **N** → karta **Motion2MixamoRig** → **Nainstalovat prostředí (jedním kliknutím)** (Install Runtime (one click)).
4. **Vybrat model SMPL-X…** (Choose SMPL-X Model…) (stažení zdarma) a vyberte FBX postavy Mixamo.
5. Vyberte video s jednou osobou → **Vygenerovat pohyb** (Generate Motion).

Postup krok za krokem, tipy a aktualizace: **[Uživatelská příručka](user-guide.cs.md)**. Vyzkoušeno na macOS (Apple Silicon).

### 💻 Příkazový řádek — pro vývojáře

Naklonujte repozitář a spusťte pipeline sami: začněte u [Požadavků](#požadavky).

Agenti by měli začít u [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Otevřete <a href="../assets/demo.mp4">demo.mp4</a> v tomto repozitáři.</sub>
</p>

Další ukázka:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Diagnostická zpráva (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Požadavky

Python 3.11+. Po naklonování vytvořte virtualenv a nainstalujte závislosti; příkaz `m2mr` je pak k dispozici:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Nainstalujte závislosti a tento projekt. chumpy (zastaralý balíček v
# řetězci závislostí) importuje pip ve svém instalačním skriptu, což selže s
# "No module named 'pip'" při výchozím izolovaném sestavení pipu. Nejdřív ho
# nainstalujte s vypnutou izolací a teprve potom tento projekt.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Váhy pro inferenci se tady nestahují. První `m2mr run` stáhne váhy GVHMR do `weights/` (~5 GB, jen jednou). První `m2mr run --detect-hands` stáhne také váhy ruky HaMeR do `weights/hamer/` (~2,7 GB, jen jednou).

Doporučuje se ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Pipeline běží i bez něj, ale výstupní videa budou **bez zvuku** a v prohlížeči se nepřehrají.

## Než spustíte: vložte tyto soubory do `assets/`

Tento repozitář je neobsahuje; musíte si je opatřit. Název souboru SMPL-X se musí přesně shodovat s tabulkou; názvy FBX, videa a obrázku mohou být libovolné. Spuštění potřebuje SMPL-X, postavu Mixamo a **buď** video, **nebo** fotografii. Fungují i postavy Mixamo znovu exportované z Cinema 4D; viz [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Co | Kam | Kde to získat |
|---|---|---|
| Model těla SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Zaregistrujte se na [SMPL-X](https://smpl-x.is.tue.mpg.de/) a stáhněte ho |
| FBX postavy Mixamo | `assets/mixamo/Y_Bot.fbx` | S účtem Adobe stáhněte Y Bot (nebo jinou postavu s rigem Mixamo) z [Mixamo](https://www.mixamo.com) |
| Akční video | `assets/video/<your_clip>.mp4` | Klip s **přesně jednou** zřetelně viditelnou osobou, **od hlavy k patě v záběru po celou dobu** (souborů může být víc; každé spuštění vezme naposledy přidaný) |
| Fotografie pózy (volitelně) | `assets/image/<your_photo>.jpg` | Fotografie s **přesně jednou** zřetelně viditelnou osobou, **od hlavy k patě v záběru**. Použijte s `--image` |
| Pravá ruka MANO (jen pro `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Zaregistrujte se na [MANO](https://mano.is.tue.mpg.de/) a stáhněte **Models & Code**. Spuštění jen těla tento soubor nepotřebuje |

Poznámka: soubor stažený z Mixama se jmenuje `Y Bot.fbx` (**mezera**), o jeden znak jinak než `Y_Bot.fbx` (**podtržítko**) v tabulce.
Přejmenujte ho na tvar s podtržítkem a stane se výchozím rigem (`m2mr run` bez `--rig`). Nechat mezeru je také v pořádku: když `Y_Bot.fbx` chybí, použije se první `.fbx` v `assets/mixamo/`.

`assets/video/` může obsahovat víc videí. Bez `--video` a bez `--image` spuštění použije soubor **naposledy přidaný** do `assets/video/`; když je složka prázdná, vezme nejnovější fotografii v `assets/image/`.
Každý klip nebo fotografie musí ukazovat jen jednu osobu, **od hlavy k patě v záběru**, bez oříznutí na okrajích. `m2mr doctor` / `m2mr run` se zastaví před extrakcí, když jsou v záběru dva lidé.

## Rychlý start

Výsledky skončí v `outputs/<run-time>_<source>/`. Spuštění s videem zapisují `videos/`; spuštění s fotografií zapisují `images/`.

### 1. Zkontrolujte assety a prostředí

Všechno, co chybí, se vypíše i s tím, odkud to stáhnout a kam to dát.

```bash
m2mr doctor
```

`m2mr doctor` kontroluje spuštění těla. Model ruky MANO nevyžaduje. Další soubor a balíčky Pythonu pro detekci prstů zkontrolujete takto:

```bash
m2mr doctor --detect-hands
```

### 2. První spuštění: něco na obrazovce

Bez přepínačů se použije **nejnovější soubor v `assets/video/`** a `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Tohle je pomalý krok. První spuštění stáhne ~5 GB vah pro inferenci (jen jednou) a pak z videa vytáhne lidský pohyb.
Na CPU trvá extrakce klipu o délce ~30 sekund asi 8–15 minut; pozdější spuštění podobné délky, když už váhy jsou na místě, trvají asi 3–5 minut.
Retarget a vykreslení obvykle zaberou minutu nebo dvě. Opětovné použití kostry s `--skeleton` v další části extrakci úplně přeskočí a skončí za několik desítek sekund.

Došlápnutá noha se ve výchozím stavu přichytí: špička, když je špička dole, pata jen když jsou prsty nahoře. Když natažená noha na to místo nedosáhne, posunou se boky. Chodidlo se pak položí na podlahu (y = 0). `--no-foot-lock` nechá syrový retarget, takže nohy mohou klouzat; chodidlo se na podlahu položí i tak.

### 3. Stejný pohyb, jiná postava

Stáhněte z Mixama další postavu do `assets/mixamo/`. **Nespouštějte znovu jen se změnou `--rig`**: zopakovala by se pomalá extrakce.
Předejte `--skeleton`, abyste znovu použili kostru z předchozího spuštění; minuty se změní na desítky sekund:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Jiné video

`--video` vybere klip. Volně se kombinuje s `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Fotografie (statická póza)

`--image` obnoví **statickou 3D pózu** z fotografie jedné osoby a přenese ji na postavu Mixamo stejně jako spuštění s videem. Náhledy jsou čtyři obrázky v `images/` (stejné pohledy jako u videa) plus klip orbity vlevo/vpravo `before_after_360_compare.mp4`. Nepředávejte zároveň `--video`.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` bez cesty použije soubor naposledy přidaný do `assets/image/`.

### 6. Zkontrolujte samoprůniky

Každé spuštění také kontroluje hotovou postavu na **samoprůnik** — jedna část těla vniká do druhé, třeba ruka uvnitř hlavy — a zapíše `diagnostics.json`. Terminál vypíše jeden řádek, například `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Podlaha se nekontroluje.

Opětovná kontrola spuštění, nebo zobrazení problémů:

```bash
m2mr diagnose outputs/<run>                  # přepíše diagnostics.json
m2mr diagnose outputs/<run> --visualize      # také diagnostics.html: zdrojové video vedle postavy, časová osa, klikatelný seznam problémů
m2mr diagnose outputs/<run> --threshold-cm 2 # hlásí jen průniky hlubší než 2 cm (výchozí 1)
```

Každý problém v `diagnostics.json` je dvojice částí těla s rozsahy snímků, kde se protínají, nejhorším snímkem a jeho hloubkou. Čísla snímků se počítají od 0, stejně jako časová osa Blenderu po importu glTF. Části spojené kloubem (paže a předloktí, trup a stehno, …) se neporovnávají: jejich kůže se kolem kloubu překrývá v každé póze. `diagnostics.html` vloží zdrojové video (potřebuje `ffmpeg`) a načte three.js z CDN, takže 3D pohled potřebuje internet. Ten pohled drží pevné značky podlahy na y = 0 — kříž každých 0,5 m, větší každý metr a zelený kříž v počátku — abyste poznali, jestli se postava hýbe. Jantarový pruh nad stopami průniků je na poznámky od oka (přetáhněte rozsah, nebo In / Out). Seznam **Notes** vpravo je ukazuje; klik na řádek na něj skočí. **Download notes** uloží tyto poznámky spolu se seznamem průniků. Soubor se jmenuje podle zdrojového videa a zaznamená jeho cestu.

### 7. Prsty (`--detect-hands`)

Obyčejné `m2mr run` hýbe tělem a nechává kosti prstů Mixamo v klidu. `--detect-hands` zapne model ruky, který jde s extraktorem těla. U výchozího extraktoru, GVHMR, je tím modelem [HaMeR](https://github.com/geopavlakos/hamer). HaMeR vyřízne zápěstí z osoby a ze snímků, které GVHMR už vybral. Druhou osobu v klipu nehledá.

**Čas se zhruba zdvojnásobí.** Klip, který bez přepínače skončí za pár minut, trvá s `--detect-hands` asi dvakrát tak dlouho, protože průchod rukou běží nad extrakcí těla. U dlouhého videa s tím počítejte před startem.

Položte `MANO_RIGHT.pkl` podle tabulky výše a pak:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

První spuštění s `--detect-hands` stáhne váhy HaMeR do `weights/hamer/` (~2,7 GB, jednou). Rotace prstů se zapíšou do `skeleton_motion.npz` a řídí 30 kostí prstů Mixamo na postavě se skinem. Zápěstí, které průchod těla neviděl zřetelně, zůstane u té ruky v klidu.

`--hand-smooth` je, kolik sekund vyhlazení se na ty rotace použije. Výchozí hodnota je `0.08`. `0` nechá syrový odhad. Vyhlazení běží pokaždé, když soubor kostry už obsahuje pohyb rukou, včetně pozdějšího spuštění, které ten soubor jen znovu použije.

Opětovné použití předchozí kostry:

- Soubor už obsahuje pohyb rukou: `--skeleton` řídí prsty sám. `--detect-hands` už není potřeba.
- Neobsahuje, ale cache těla toho spuštění je pořád vedle (`cache/<clip>/0_input_video.mp4` plus `preprocess/vitpose.pt` a `preprocess/bbx.pt`): `--skeleton ... --detect-hands` přidá prsty bez nové extrakce těla.
- Ta cache už není: spusťte video nebo fotografii znovu s `--detect-hands`.

## Výstupy

Každé `m2mr run` vytvoří složku pojmenovanou **časem, kdy příkaz začal**. Soubory v kořeni jsou stejné pro video i fotografii; mění se jen složka náhledů.

```
outputs/20260829_193205_dance/          # nebo …_pose/ pro fotografii
├── run.json                            # čas startu, vstupy, celý příkaz
├── skeleton_motion.npz                 # 3D kostra člověka (znovu s --skeleton)
├── mixamo_rotations.npz                # rotace Mixamo po kostech
├── mixamo_character.glb                # postava se skinem, import do Blenderu / Unity
├── diagnostics.json                    # zpráva o samoprůnicích (viz krok 6 rychlého startu)
├── diagnostics.html                    # až po `m2mr diagnose <run> --visualize`
└── videos/   nebo   images/            # náhledy — podle vstupu
```

**Vstupní video** zapíše `videos/` (stejný poměr stran jako klip):

```
videos/
├── human_skeleton.mp4                  # obnovená 3D kostra člověka
├── mixamo_skeleton.mp4                 # kostra rigu Mixamo
├── mixamo_character.mp4                # postava Mixamo se skinem
└── compare.mp4                         # 2×2: originál (vlevo nahoře) / kostra Mixamo (vpravo nahoře)
                                        #      kostra člověka (vlevo dole) / postava (vpravo dole)
```

**Vstupní fotografie** místo toho zapíše `images/` (stejné čtyři pohledy plus otočka):

```
images/
├── human_skeleton.png                  # obnovená 3D kostra člověka
├── mixamo_skeleton.png                 # kostra rigu Mixamo
├── mixamo_character.png                # postava Mixamo se skinem
├── compare.png                         # 2×2: originál (vlevo nahoře) / kostra Mixamo (vpravo nahoře)
│                                       #      kostra člověka (vlevo dole) / postava (vpravo dole)
└── before_after_360_compare.mp4        # vlevo: původní fotografie
                                        # vpravo: orbita rigu po 10° (jedno celé otočení)
```

S `--detect-hands` ukládá `skeleton_motion.npz` také rotace prstů a `mixamo_rotations.npz` / `mixamo_character.glb` obsahují 30 kostí prstů. Bez tohoto přepínače a bez pohybu rukou už uloženého v znovu použité kostře ty kosti zůstanou v klidu.

Otevřete `mixamo_character.glb` v Blenderu: File → Import → glTF 2.0 (.glb/.gltf). Když kamera míří do prázdna, vyberte síť postavy a použijte View → Frame Selected. Shluk koulí na hlavě a rukou je zobrazení kostí, ne síť: v Outlineru skryjte **Icosphere** a **armature**; nechte viditelnou síť se skinem. Nastavte FPS scény z `run.json` (`fps`) a časovou osu na snímky 0 až `n_frames` − 1, aby přehrávání sedělo se zdrojem a čísla snímků s `diagnostics.json`. Spuštění s videem porovnejte s `videos/mixamo_character.mp4`, spuštění s fotografií s `images/mixamo_character.png` nebo s klipem orbity.

## Licence

Kód tohoto repozitáře je Apache-2.0. Assety, které stahujete, mají vlastní podmínky a nesmějí se šířit spolu s tímto repozitářem:

- **SMPL-X**: přístup přes MPI; ve výchozím stavu jen nekomerční výzkum / výuka / umění; komerční použití potřebuje samostatnou dohodu
- **MANO** (jen když používáte `--detect-hands`): přístup přes MPI, stejný druh stažení jako SMPL-X; položte `MANO_RIGHT.pkl` lokálně a nešiřte ho
- **FBX Mixamo**: v dodaném produktu být může; surový FBX nešiřte jako balíček assetů
- **Váhy GVHMR**: při prvním `m2mr run` se automaticky stáhnou do `weights/`, pod licencí původního projektu
- **HaMeR**: inferenční kód v tomto repozitáři je MIT; váhy se stáhnou do `weights/hamer/` při prvním `m2mr run --detect-hands`, podle podmínek původního vydání

## Kontakt

Když narazíte na problém, potřebujete pomoct s místní instalací nebo chcete mluvit o spolupráci, napište na:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
