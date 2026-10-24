# Motion2MixamoRig

<p align="center">
  <a href="#prérequis"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.fr.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · Français · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Transférez le mouvement d’une personne filmée — ou la pose d’une photo — sur un personnage 3D riggé avec Adobe Mixamo.

Pour les développeurs de jeux : fournissez une vidéo d’action avec **une seule personne** (ou une photo) et un personnage Mixamo ; l’outil produit des vidéos d’aperçu ainsi qu’un fichier de personnage skinné (`.glb`) à importer directement dans Blender ou Unity.

> Motion2MixamoRig est encore expérimental. La version 0.1.8 correspond au pipeline en ligne de commande. Ce dépôt contient aussi une extension Blender 4.2+ qui exécute ce même pipeline dans un environnement Python externe. Compiler le module à partir des sources : [`blender_extension/README.md`](../../blender_extension/README.md).

## Deux façons de l’utiliser

### 🎨 Dans Blender — sans programmation

1. Téléchargez le zip correspondant à votre plateforme, par ex. `motion2mixamorig-<version>-macos-arm64.zip`, depuis la [dernière version](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. Dans Blender : **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, puis choisissez le zip.
3. 3D Viewport → appuyez sur **N** → onglet **Motion2MixamoRig** → **Installer l’environnement (en un clic)** (Install Runtime (one click)).
4. **Choisir le modèle SMPL-X…** (Choose SMPL-X Model… ; téléchargement gratuit), puis choisissez le FBX d’un personnage Mixamo.
5. Choisissez une vidéo d’une seule personne → **Générer le mouvement** (Generate Motion).

Instructions pas à pas, conseils et mises à jour : **[Guide d’utilisation](user-guide.fr.md)**. Testé sur macOS (Apple Silicon).

### 💻 Ligne de commande — pour les développeurs

Clonez le dépôt et exécutez le pipeline vous-même : commencez par les [Prérequis](#prérequis).

Les agents doivent commencer par [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Ouvrez <a href="../assets/demo.mp4">demo.mp4</a> dans ce dépôt.</sub>
</p>

Une autre démo :

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Rapport de diagnostic (`diagnostics.html`) :

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Prérequis

Python 3.11+. Après le clonage, créez un virtualenv et installez les dépendances ; la commande `m2mr` est alors disponible :

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Installer les dépendances et ce projet. chumpy (un ancien paquet de la chaîne
# de dépendances) importe pip dans son script setup, ce qui échoue avec
# « No module named 'pip' » dans le build isolé par défaut de pip. Installez-le
# d’abord avec l’isolation désactivée, puis installez ce projet.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Les poids d’inférence (GVHMR, etc.) ne sont pas téléchargés à cette étape. Le premier `m2mr run` les récupère dans `weights/` (~5 Go, une seule fois). Le premier `m2mr run --detect-hands` récupère aussi les poids de main HaMeR dans `weights/hamer/` (~2,7 Go, une seule fois).

ffmpeg est recommandé (macOS : `brew install ffmpeg`, Ubuntu : `apt install ffmpeg`).
Le pipeline fonctionne sans lui, mais les vidéos produites seront **muettes** et ne pourront pas être lues dans un navigateur.

## Avant de lancer : placez ces fichiers dans `assets/`

Ce dépôt ne fournit pas ces fichiers ; vous devez les récupérer vous-même. Le nom du fichier SMPL-X doit correspondre exactement au tableau ; les noms des fichiers FBX, vidéo et image sont libres. Chaque exécution nécessite SMPL-X, un personnage Mixamo et **soit** une vidéo, **soit** une photo. Les personnages Mixamo réexportés depuis Cinema 4D fonctionnent aussi ; voir [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Quoi | Où | Où l’obtenir |
|---|---|---|
| Modèle corporel SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Inscrivez-vous sur [SMPL-X](https://smpl-x.is.tue.mpg.de/) puis téléchargez-le |
| FBX du personnage Mixamo | `assets/mixamo/Y_Bot.fbx` | Avec un compte Adobe, téléchargez Y Bot (ou tout autre personnage riggé par Mixamo) depuis [Mixamo](https://www.mixamo.com) |
| Vidéo d’action | `assets/video/<your_clip>.mp4` | Un clip avec **exactement une** personne bien visible, **de la tête aux pieds dans le cadre en permanence** (vous pouvez garder plusieurs fichiers ; chaque exécution utilise le plus récemment ajouté) |
| Photo de pose (facultative) | `assets/image/<your_photo>.jpg` | Une photo avec **exactement une** personne bien visible, **de la tête aux pieds dans le cadre**. À utiliser avec `--image` |
| Main droite MANO (uniquement pour `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Inscrivez-vous sur [MANO](https://mano.is.tue.mpg.de/) et téléchargez **Models & Code**. Une exécution du corps seul n’a pas besoin de ce fichier |

Remarque : le fichier téléchargé depuis Mixamo s’appelle `Y Bot.fbx` (**espace**), soit un caractère de différence avec `Y_Bot.fbx` (**tiret bas**) dans le tableau.
Renommez-le avec le tiret bas et il devient le rig par défaut (`m2mr run` sans `--rig`). Garder l’espace fonctionne aussi — si `Y_Bot.fbx` est absent, le premier `.fbx` de `assets/mixamo/` est utilisé.

`assets/video/` peut contenir plusieurs vidéos. Sans `--video` ni `--image`, l’exécution utilise le fichier **le plus récemment ajouté** à `assets/video/` ; si ce dossier est vide, elle se rabat sur la photo la plus récente de `assets/image/`.
Chaque clip ou photo ne doit montrer qu’une seule personne, **de la tête aux pieds dans le cadre** — rien de coupé sur les bords. `m2mr doctor` / `m2mr run` s’arrêtent avant l’extraction si deux personnes sont visibles.

## Démarrage rapide

Les résultats sont écrits dans `outputs/<run-time>_<source>/`. Les exécutions vidéo écrivent `videos/` ; les exécutions photo écrivent `images/`.

### 1. Vérifier les ressources et l’environnement

Tout élément manquant est affiché avec l’endroit où le télécharger et où le placer.

```bash
m2mr doctor
```

`m2mr doctor` vérifie l’exécution du corps. Il n’exige pas le modèle de main MANO. Pour vérifier aussi le fichier supplémentaire et les paquets Python utilisés par la détection des doigts :

```bash
m2mr doctor --detect-hands
```

### 2. Première exécution : obtenir un résultat à l’écran

Sans option, cette commande utilise **le fichier le plus récent de `assets/video/`** et `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

C’est l’étape lente. La première exécution télécharge ~5 Go de poids d’inférence (une seule fois), puis extrait le mouvement humain de la vidéo.
Sur CPU, l’extraction d’un clip d’environ 30 secondes prend environ 8 à 15 minutes ; les exécutions suivantes de durée similaire, une fois les poids présents, prennent environ 3 à 5 minutes.
Le retargeting et le rendu prennent généralement une ou deux minutes. Réutiliser un squelette avec `--skeleton` dans la section suivante saute complètement l’extraction et se termine en quelques dizaines de secondes.

Un pied posé est fixé par défaut : la plante quand la plante est au sol, le talon seulement quand les orteils sont levés. Si une jambe tendue n’atteint pas ce point, les hanches bougent. La plante est ensuite posée sur le sol (y = 0). `--no-foot-lock` conserve le retargeting brut, les pieds peuvent donc glisser ; la plante est quand même posée sur le sol.

### 3. Même mouvement, autre personnage

Téléchargez un autre personnage depuis Mixamo dans `assets/mixamo/`. **Ne relancez pas avec seulement `--rig`** — cela refait l’extraction lente.
Passez `--skeleton` pour réutiliser le squelette d’une exécution précédente ; quelques minutes deviennent quelques dizaines de secondes :

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Une autre vidéo

`--video` choisit le clip. Il se combine librement avec `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Une photo (pose statique)

`--image` reconstruit une **pose 3D statique** à partir de la photo d’une personne, puis la retargete sur le personnage Mixamo de la même manière qu’une exécution vidéo. Les aperçus sont quatre images fixes dans `images/` (mêmes vues que l’exécution vidéo), plus un clip en orbite gauche/droite `before_after_360_compare.mp4`. Ne passez pas `--video` en même temps.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` sans chemin utilise le fichier le plus récemment ajouté à `assets/image/`.

### 6. Vérifier les auto-intersections

Chaque exécution vérifie aussi le personnage final à la recherche d’**auto-intersections** — une partie du corps qui entre dans une autre, comme une main dans la tête — et écrit `diagnostics.json`. Le terminal affiche une ligne, par exemple `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Le sol n’est pas vérifié.

Pour revérifier une exécution, ou pour voir les problèmes :

```bash
m2mr diagnose outputs/<run>                  # réécrit diagnostics.json
m2mr diagnose outputs/<run> --visualize      # écrit aussi diagnostics.html : vidéo source à côté du personnage, timeline, liste cliquable des problèmes
m2mr diagnose outputs/<run> --threshold-cm 2 # ne signale que les pénétrations de plus de 2 cm (1 par défaut)
```

Chaque problème dans `diagnostics.json` est une paire de parties du corps, avec les plages d’images où elles s’intersectent, la pire image et sa profondeur. Les numéros d’image commencent à 0, comme la timeline de Blender après un import glTF. Les parties reliées par une articulation (bras et avant-bras, torse et cuisse, …) ne sont pas comparées : leur peau se chevauche autour de l’articulation dans toutes les poses. `diagnostics.html` intègre la vidéo source (nécessite `ffmpeg`) et charge three.js depuis un CDN ; sa vue 3D a donc besoin d’une connexion internet. Cette vue dessine des repères de sol fixes sur y = 0 : une croix tous les 0,5 m, une plus grande à chaque mètre, et une croix verte à l’origine, pour juger si le personnage bouge. La bande ambre au-dessus des pistes d’intersection sert aux remarques faites à l’œil (glisser une plage, ou **In** / **Out**). La liste **Notes** à droite les affiche ; un clic sur une ligne y saute. **Download notes** enregistre ces remarques avec la liste des intersections. Le fichier porte le nom de la vidéo source et contient son chemin.

### 7. Doigts (`--detect-hands`)

Un simple `m2mr run` déplace le corps et laisse les os des doigts Mixamo au repos. `--detect-hands` active le modèle de main qui accompagne l’extracteur de corps. Avec l’extracteur par défaut, GVHMR, ce modèle est [HaMeR](https://github.com/geopavlakos/hamer). HaMeR découpe les poignets à partir de la personne et des images déjà choisies par GVHMR. Il ne cherche pas une seconde personne dans le clip.

**Cela double à peu près la durée.** Un clip qui se termine en quelques minutes sans le drapeau prend environ deux fois plus de temps avec `--detect-hands`, parce que la passe des mains s’ajoute à l’extraction du corps. Sur une longue vidéo, prévoyez ce temps avant de lancer.

Placez `MANO_RIGHT.pkl` comme dans le tableau ci-dessus, puis :

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

La première exécution avec `--detect-hands` télécharge les poids HaMeR dans `weights/hamer/` (~2,7 Go, une fois). Les rotations des doigts sont écrites dans `skeleton_motion.npz` et animent les 30 os des doigts Mixamo du personnage skinné. Un poignet que la passe du corps n’a pas vu clairement reste au repos pour cette main.

`--hand-smooth` indique combien de secondes de lissage appliquer à ces rotations. La valeur par défaut est `0.08`. `0` conserve l’estimation brute. Le lissage s’applique dès que le fichier de squelette contient déjà un mouvement de main, y compris lors d’une exécution ultérieure qui ne réutilise que ce fichier.

Réutiliser un squelette précédent :

- Le fichier contient déjà un mouvement de main : `--skeleton` anime les doigts tout seul. `--detect-hands` n’est plus nécessaire.
- Il n’en contient pas, mais le cache du corps de cette exécution est encore à côté (`cache/<clip>/0_input_video.mp4`, plus `preprocess/vitpose.pt` et `preprocess/bbx.pt`) : `--skeleton ... --detect-hands` ajoute les doigts sans extraire à nouveau le corps.
- Ce cache a disparu : relancez la vidéo ou la photo avec `--detect-hands`.

## Sorties

Chaque `m2mr run` crée un répertoire nommé d’après **l’heure de démarrage de la commande**. Les fichiers à la racine sont identiques pour la vidéo et la photo ; seul le dossier d’aperçu change.

```
outputs/20260829_193205_dance/          # ou …_pose/ pour une photo
├── run.json                            # heure de début, entrées, commande complète
├── skeleton_motion.npz                 # squelette humain 3D (réutilisable avec --skeleton)
├── mixamo_rotations.npz                # rotations Mixamo par os
├── mixamo_character.glb                # personnage skinné, à importer dans Blender / Unity
├── diagnostics.json                    # rapport d’auto-intersection (voir l’étape 6 du Démarrage rapide)
├── diagnostics.html                    # seulement après `m2mr diagnose <run> --visualize`
└── videos/   ou   images/              # aperçus — selon l’entrée
```

Une **entrée vidéo** écrit `videos/` (même format d’image que le clip) :

```
videos/
├── human_skeleton.mp4                  # squelette humain 3D reconstruit
├── mixamo_skeleton.mp4                 # squelette du rig Mixamo
├── mixamo_character.mp4                # personnage Mixamo skinné
└── compare.mp4                         # 2×2 : original (haut gauche) / squelette Mixamo (haut droite)
                                        #       squelette humain (bas gauche) / personnage (bas droite)
```

Une **entrée photo** écrit plutôt `images/` (les mêmes quatre vues, plus une rotation complète) :

```
images/
├── human_skeleton.png                  # squelette humain 3D reconstruit
├── mixamo_skeleton.png                 # squelette du rig Mixamo
├── mixamo_character.png                # personnage Mixamo skinné
├── compare.png                         # 2×2 : original (haut gauche) / squelette Mixamo (haut droite)
│                                       #       squelette humain (bas gauche) / personnage (bas droite)
└── before_after_360_compare.mp4        # gauche : photo d’origine
                                        # droite : orbite du rig par pas de 10° (un tour complet)
```

Avec `--detect-hands`, `skeleton_motion.npz` contient aussi les rotations des doigts, et `mixamo_rotations.npz` ainsi que `mixamo_character.glb` incluent les 30 os des doigts. Sans ce drapeau, et sans mouvement de main déjà stocké dans un squelette réutilisé, ces os restent au repos.

Ouvrez `mixamo_character.glb` dans Blender : File → Import → glTF 2.0 (.glb/.gltf). Si la caméra vise un espace vide, sélectionnez le mesh du personnage puis utilisez View → Frame Selected. L’amas de sphères sur la tête et les mains correspond à l’affichage des os, pas au mesh : dans l’Outliner, masquez **Icosphere** et l’**armature** ; laissez le mesh skinné visible. Réglez le FPS de la scène d’après `run.json` (`fps`) et la timeline sur les images 0 à `n_frames` − 1 pour que la lecture corresponde à la source et que les numéros d’image correspondent à `diagnostics.json`. Comparez une exécution vidéo à `videos/mixamo_character.mp4`, une exécution photo à `images/mixamo_character.png` ou au clip en orbite.

## Licence

Le code de ce dépôt est sous licence Apache-2.0. Les ressources que vous téléchargez ont leurs propres conditions et ne doivent pas être redistribuées avec ce dépôt :

- **SMPL-X** : accès contrôlé par le MPI ; par défaut recherche / enseignement / art non commerciaux ; un usage commercial nécessite un accord séparé
- **MANO** (seulement avec `--detect-hands`) : accès contrôlé par le MPI, le même type de téléchargement que SMPL-X ; placez `MANO_RIGHT.pkl` en local et ne le redistribuez pas
- **Mixamo FBX** : autorisé dans un produit publié ; ne redistribuez pas le FBX brut sous forme de pack de ressources
- **GVHMR et autres poids d’inférence** : téléchargés automatiquement dans `weights/` au premier `m2mr run`, sous la licence de chaque projet d’origine
- **HaMeR** : le code d’inférence de ce dépôt est sous MIT ; les poids sont téléchargés dans `weights/hamer/` au premier `m2mr run --detect-hands`, selon les conditions de publication en amont

## Contact

Si vous rencontrez un problème, avez besoin d’aide pour terminer une installation locale ou souhaitez discuter d’une collaboration, écrivez à :
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
