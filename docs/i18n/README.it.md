# Motion2MixamoRig

<p align="center">
  <a href="#prerequisiti"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.it.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · Italiano · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Trasferisci il movimento di una persona in un video — o la posa in una foto — su un personaggio 3D con rig Adobe Mixamo.

Per sviluppatori di videogiochi: dagli un video d’azione con **una sola persona** (o una foto) e un personaggio Mixamo; genera video di anteprima e un file di personaggio con skinning (`.glb`) da trascinare in Blender o Unity.

> Motion2MixamoRig è al momento sperimentale. La versione 0.1.8 è la pipeline da riga di comando. Questo repository include anche un’estensione per Blender 4.2+ che esegue la stessa pipeline in un ambiente Python esterno. Compilare il componente aggiuntivo dai sorgenti: [`blender_extension/README.md`](../../blender_extension/README.md).

## Due modi per usarlo

### 🎨 In Blender — senza programmare

1. Scarica lo zip per la tua piattaforma, per esempio `motion2mixamorig-<version>-macos-arm64.zip`, dall’[ultima release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. In Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, scegli lo zip.
3. 3D Viewport → premi **N** → scheda **Motion2MixamoRig** → **Installa l’ambiente (un clic)** (Install Runtime (one click)).
4. **Scegli il modello SMPL-X…** (Choose SMPL-X Model…) (download gratuito) e scegli un FBX di un personaggio Mixamo.
5. Scegli un video con una sola persona → **Genera movimento** (Generate Motion).

Istruzioni passo passo, consigli e aggiornamenti: **[Guida utente](user-guide.it.md)**. Testato su macOS (Apple Silicon).

### 💻 Riga di comando — per sviluppatori

Clona il repository ed esegui la pipeline da solo: inizia da [Prerequisiti](#prerequisiti).

Gli agent dovrebbero iniziare da [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Apri <a href="../assets/demo.mp4">demo.mp4</a> in questo repository.</sub>
</p>

Un’altra demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Report di diagnostica (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Prerequisiti

Python 3.11+. Dopo il clone, crea un virtualenv e installa le dipendenze; a quel punto il comando `m2mr` è disponibile:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Installa le dipendenze e questo progetto. chumpy (un pacchetto datato nella
# catena di dipendenze) importa pip nello script di setup, che fallisce con
# "No module named 'pip'" nella build isolata predefinita di pip. Installalo
# prima con l'isolamento disattivato, poi installa questo progetto.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

I pesi di inferenza (GVHMR e altri) non vengono scaricati qui. Il primo `m2mr run` li scarica in `weights/` (~5 GB, una sola volta). Il primo `m2mr run --detect-hands` scarica anche i pesi della mano HaMeR in `weights/hamer/` (~2,7 GB, una sola volta).

Si consiglia ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
La pipeline funziona anche senza, ma i video in uscita saranno **senza audio** e non si potranno riprodurre in un browser.

## Prima di eseguire: metti questi file in `assets/`

Questo repository non include questi file; devi procurarteli. Il nome del file SMPL-X deve corrispondere esattamente alla tabella; i nomi di FBX, video e immagini possono essere qualsiasi. Un’esecuzione richiede SMPL-X, un personaggio Mixamo e **un video oppure** una foto. Funzionano anche i personaggi Mixamo riesportati da Cinema 4D; vedi [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Cosa | Dove | Dove trovarlo |
|---|---|---|
| Modello del corpo SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Registrati su [SMPL-X](https://smpl-x.is.tue.mpg.de/) e scaricalo |
| FBX del personaggio Mixamo | `assets/mixamo/Y_Bot.fbx` | Con un account Adobe, scarica Y Bot (o un altro personaggio con rig Mixamo) da [Mixamo](https://www.mixamo.com) |
| Video d’azione | `assets/video/<your_clip>.mp4` | Una clip con **una sola** persona ben visibile, **dalla testa ai piedi nell’inquadratura per tutto il tempo** (puoi tenere più file; ogni esecuzione usa quello aggiunto per ultimo) |
| Foto della posa (facoltativa) | `assets/image/<your_photo>.jpg` | Una foto con **una sola** persona ben visibile, **dalla testa ai piedi nell’inquadratura**. Da usare con `--image` |
| Mano destra MANO (solo per `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Registrati su [MANO](https://mano.is.tue.mpg.de/) e scarica **Models & Code**. Un’esecuzione solo del corpo non ha bisogno di questo file |

Nota: il file scaricato da Mixamo si chiama `Y Bot.fbx` (con uno **spazio**), un carattere diverso da `Y_Bot.fbx` (con il **trattino basso**) della tabella.
Rinominalo con il trattino basso e diventa il rig predefinito (`m2mr run` senza `--rig`). Va bene anche lasciare lo spazio: se `Y_Bot.fbx` manca, viene usato il primo `.fbx` in `assets/mixamo/`.

`assets/video/` può contenere più video. Senza `--video` o `--image`, l’esecuzione usa il file **aggiunto per ultimo** in `assets/video/`; se la cartella è vuota, passa all’ultima foto in `assets/image/`.
Ogni clip o foto deve mostrare una sola persona, **dalla testa ai piedi nell’inquadratura**, senza nulla tagliato ai bordi. `m2mr doctor` / `m2mr run` si fermano prima dell’estrazione se nell’inquadratura ci sono due persone.

## Avvio rapido

I risultati finiscono in `outputs/<run-time>_<source>/`. Le esecuzioni con video scrivono `videos/`; quelle con foto scrivono `images/`.

### 1. Controlla gli asset e l’ambiente

Per tutto ciò che manca viene indicato dove scaricarlo e dove metterlo.

```bash
m2mr doctor
```

`m2mr doctor` controlla l’esecuzione del corpo. Non richiede il modello della mano MANO. Per controllare anche il file aggiuntivo e i pacchetti Python usati dal rilevamento delle dita:

```bash
m2mr doctor --detect-hands
```

### 2. Prima esecuzione: ottieni subito un risultato

Senza opzioni usa il **file più recente in `assets/video/`** e `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Questo è il passaggio lento. La prima esecuzione scarica ~5 GB di pesi di inferenza (una sola volta), poi estrae il movimento umano dal video.
Su CPU, l’estrazione di una clip di ~30 secondi richiede circa 8–15 minuti; le esecuzioni successive di durata simile, con i pesi già presenti, circa 3–5 minuti.
Retargeting e rendering richiedono di solito un minuto o due. Riutilizzando uno scheletro con `--skeleton` (sezione successiva) l’estrazione viene saltata del tutto e si finisce in poche decine di secondi.

Un piede appoggiato viene bloccato per impostazione predefinita: l’avampiede quando l’avampiede è a terra, il tallone solo quando le dita sono alzate. Se una gamba tesa non arriva a quel punto, le anche si spostano. Poi la pianta viene appoggiata sul pavimento (y = 0). `--no-foot-lock` tiene il retarget grezzo, quindi i piedi possono scivolare; la pianta viene comunque appoggiata sul pavimento.

### 3. Stesso movimento, altro personaggio

Scarica un altro personaggio da Mixamo in `assets/mixamo/`. **Non rieseguire cambiando solo `--rig`**: ripeteresti la lenta estrazione.
Passa `--skeleton` per riutilizzare lo scheletro di un’esecuzione precedente; i minuti diventano decine di secondi:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Un altro video

`--video` sceglie la clip. Si combina liberamente con `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Una foto (posa statica)

`--image` ricostruisce una **posa 3D statica** dalla foto di una persona, poi la trasferisce sul personaggio Mixamo come fa un’esecuzione con video. Le anteprime sono quattro immagini in `images/` (le stesse viste dell’esecuzione con video), più una clip orbitale sinistra/destra `before_after_360_compare.mp4`. Non usare `--video` insieme.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` senza percorso usa il file aggiunto per ultimo in `assets/image/`.

### 6. Controlla le autointersezioni

Ogni esecuzione controlla anche il personaggio finito alla ricerca di **autointersezioni** — una parte del corpo che entra in un’altra, come una mano dentro la testa — e scrive `diagnostics.json`. Il terminale stampa una riga, per esempio `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Il pavimento non viene controllato.

Per ricontrollare un’esecuzione, o per vedere i problemi:

```bash
m2mr diagnose outputs/<run>                  # riscrive diagnostics.json
m2mr diagnose outputs/<run> --visualize      # anche diagnostics.html: video sorgente accanto al personaggio, timeline, elenco di problemi cliccabile
m2mr diagnose outputs/<run> --threshold-cm 2 # segnala solo le penetrazioni più profonde di 2 cm (predefinito 1)
```

Ogni problema in `diagnostics.json` è una coppia di parti del corpo, con gli intervalli di frame in cui si intersecano, il frame peggiore e la sua profondità. I numeri dei frame partono da 0, come la timeline di Blender dopo l’importazione di un glTF. Le parti unite da un’articolazione (braccio e avambraccio, busto e coscia, …) non vengono confrontate: la loro pelle si sovrappone attorno all’articolazione in qualsiasi posa. `diagnostics.html` incorpora il video sorgente (richiede `ffmpeg`) e carica three.js da una CDN, quindi la vista 3D richiede una connessione a internet. Quella vista disegna dei segni fissi sul pavimento a y = 0: una croce ogni 0,5 m, una più grande ogni metro e una croce verde all’origine, così si vede se il personaggio si sta muovendo. La corsia ambra sopra le tracce di intersezione serve per le note fatte a occhio (trascina un intervallo, oppure **In** / **Out**). L’elenco **Notes** a destra le mostra; un clic su una riga ci salta. **Download notes** salva queste note insieme all’elenco delle intersezioni. Il file prende il nome del video sorgente e ne registra il percorso.

### 7. Dita (`--detect-hands`)

Un semplice `m2mr run` muove il corpo e lascia le ossa delle dita Mixamo a riposo. `--detect-hands` attiva il modello della mano che accompagna l’estrattore del corpo. Con l’estrattore predefinito, GVHMR, quel modello è [HaMeR](https://github.com/geopavlakos/hamer). HaMeR ritaglia i polsi dalla persona e dai frame che GVHMR ha già scelto. Non cerca una seconda persona nel clip.

**Il tempo circa raddoppia.** Un clip che senza il flag finisce in pochi minuti ne impiega circa il doppio con `--detect-hands`, perché il passaggio delle mani si aggiunge all’estrazione del corpo. Su un video lungo, conta questo tempo prima di partire.

Metti `MANO_RIGHT.pkl` come nella tabella sopra, poi:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

La prima esecuzione con `--detect-hands` scarica i pesi HaMeR in `weights/hamer/` (~2,7 GB, una volta). Le rotazioni delle dita vengono scritte in `skeleton_motion.npz` e muovono le 30 ossa delle dita Mixamo del personaggio con skin. Un polso che il passaggio del corpo non ha visto bene resta a riposo per quella mano.

`--hand-smooth` indica quanti secondi di smussatura applicare a quelle rotazioni. Il valore predefinito è `0.08`. `0` tiene la stima grezza. La smussatura avviene ogni volta che il file dello scheletro contiene già il movimento delle mani, anche in un’esecuzione successiva che riusa solo quel file.

Quando riusi uno scheletro precedente:

- Il file contiene già il movimento delle mani: `--skeleton` muove le dita da solo. `--detect-hands` non serve di nuovo.
- Non lo contiene, ma la cache del corpo di quell’esecuzione è ancora accanto (`cache/<clip>/0_input_video.mp4`, più `preprocess/vitpose.pt` e `preprocess/bbx.pt`): `--skeleton ... --detect-hands` aggiunge le dita senza estrarre di nuovo il corpo.
- Quella cache non c’è più: esegui di nuovo il video o la foto con `--detect-hands`.

## Output

Ogni `m2mr run` crea una cartella che prende il nome dall’**ora di avvio del comando**. I file nella radice sono gli stessi per video e foto; cambia solo la cartella delle anteprime.

```
outputs/20260829_193205_dance/          # oppure …_pose/ per una foto
├── run.json                            # ora di avvio, input, comando completo
├── skeleton_motion.npz                 # scheletro umano 3D (riutilizzabile con --skeleton)
├── mixamo_rotations.npz                # rotazioni Mixamo per osso
├── mixamo_character.glb                # personaggio con skinning, da importare in Blender / Unity
├── diagnostics.json                    # report delle autointersezioni (vedi il passo 6 dell’Avvio rapido)
├── diagnostics.html                    # solo dopo `m2mr diagnose <run> --visualize`
└── videos/   oppure   images/          # anteprime — dipende dall’input
```

L’**input video** scrive `videos/` (stesse proporzioni della clip):

```
videos/
├── human_skeleton.mp4                  # scheletro umano 3D ricostruito
├── mixamo_skeleton.mp4                 # scheletro del rig Mixamo
├── mixamo_character.mp4                # personaggio Mixamo con skinning
└── compare.mp4                         # 2×2: originale (in alto a sx) / scheletro Mixamo (in alto a dx)
                                        #      scheletro umano (in basso a sx) / personaggio (in basso a dx)
```

L’**input foto** scrive invece `images/` (le stesse quattro viste, più una rotazione completa):

```
images/
├── human_skeleton.png                  # scheletro umano 3D ricostruito
├── mixamo_skeleton.png                 # scheletro del rig Mixamo
├── mixamo_character.png                # personaggio Mixamo con skinning
├── compare.png                         # 2×2: originale (in alto a sx) / scheletro Mixamo (in alto a dx)
│                                       #      scheletro umano (in basso a sx) / personaggio (in basso a dx)
└── before_after_360_compare.mp4        # sinistra: foto originale
                                        # destra: orbita del rig a 10° (un giro completo)
```

Con `--detect-hands`, `skeleton_motion.npz` contiene anche le rotazioni delle dita, e `mixamo_rotations.npz` e `mixamo_character.glb` includono le 30 ossa delle dita. Senza quel flag, e senza un movimento delle mani già salvato in uno scheletro riutilizzato, quelle ossa restano a riposo.

Apri `mixamo_character.glb` in Blender: File → Import → glTF 2.0 (.glb/.gltf). Se la camera inquadra uno spazio vuoto, seleziona la mesh del personaggio e usa View → Frame Selected. Il gruppo di sfere su testa e mani è la visualizzazione delle ossa, non la mesh: nell’Outliner nascondi **Icosphere** e l’**armature**; lascia visibile la mesh con skinning. Imposta gli FPS della scena da `run.json` (`fps`) e la timeline sui frame da 0 a `n_frames` − 1, così la riproduzione corrisponde alla sorgente e i numeri dei frame corrispondono a `diagnostics.json`. Confronta un’esecuzione con video con `videos/mixamo_character.mp4`, una con foto con `images/mixamo_character.png` o con la clip orbitale.

## Licenza

Il codice di questo repository è Apache-2.0. Gli asset che scarichi hanno condizioni proprie e non devono essere ridistribuiti con questo repository:

- **SMPL-X**: accesso controllato dal MPI; per impostazione predefinita solo ricerca / istruzione / arte non commerciali; l’uso commerciale richiede un accordo separato
- **MANO** (solo con `--detect-hands`): accesso controllato dal MPI, lo stesso tipo di download di SMPL-X; metti `MANO_RIGHT.pkl` in locale e non ridistribuirlo
- **FBX Mixamo**: utilizzabili in un prodotto distribuito; non ridistribuire gli FBX originali come pacchetto di asset
- **GVHMR e gli altri pesi di inferenza**: scaricati automaticamente in `weights/` al primo `m2mr run`, ciascuno con la propria licenza originale
- **HaMeR**: il codice di inferenza in questo repository è MIT; i pesi vengono scaricati in `weights/hamer/` al primo `m2mr run --detect-hands`, secondo i termini di pubblicazione a monte

## Contatti

Se incontri un problema, hai bisogno di aiuto per completare un’installazione locale o vuoi parlare di una collaborazione, scrivi a:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
