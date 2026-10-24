# Motion2MixamoRig pour Blender — Guide d’utilisation

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · Français · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Transformez la vidéo d’une personne en personnage Mixamo animé, directement dans Blender.
Aucune programmation ni aucun terminal nécessaires.

<!-- video: link the tutorial video here -->

> Testé pour l’instant uniquement sur **macOS (Apple Silicon)**. Une version Windows arrive bientôt.

## Ce qu’il vous faut

- **Blender 4.2 ou plus récent**
- **Une connexion Internet** pour la première configuration
- **Environ 8 Go d’espace disque libre** (environnement ~1,3 Go + modèles ~5,6 Go)
- **Un compte SMPL-X gratuit** et **un compte Adobe gratuit** (pour Mixamo) ; voir les étapes 4 et 5

## 1. Télécharger le module

Rendez-vous sur la [dernière version](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
et téléchargez le zip correspondant à votre ordinateur :

| Votre ordinateur | Fichier |
| --- | --- |
| Mac avec Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Bientôt disponible** |

Par exemple `motion2mixamorig-0.1.8-macos-arm64.zip` : `0.1.8` est la version du
module, `macos-arm64` la plateforme. Si vous choisissez le mauvais fichier,
Blender refuse de l’installer et indique la plateforme attendue.

Ne le **décompressez pas**. Blender installe le zip lui-même.

## 2. L’installer dans Blender

1. **Edit → Preferences → Get Extensions**
2. Cliquez sur le petit **∨** en haut à droite → **Install from Disk…**
3. Choisissez le zip. **Motion2MixamoRig** apparaît dans la liste, activé.
4. Fermez les Preferences. Dans le 3D Viewport, appuyez sur **N**, puis cliquez
   sur l’onglet **Motion2MixamoRig** à droite.

<!-- screenshot: Install from Disk menu -->

## 3. Installer l’environnement (une seule fois)

Dans le panneau, cliquez sur **Installer l’environnement (en un clic)** (Install Runtime (one click)).

Le module télécharge son propre Python et ses bibliothèques (~1,4 Go) dans
`~/Motion2MixamoRig/`. Il ne modifie rien d’autre sur votre ordinateur. Cela
prend quelques minutes ; la barre de progression indique l’étape en cours.

<!-- screenshot: Install Runtime button and progress -->

## 4. Obtenir le modèle corporel SMPL-X

SMPL-X est un modèle corporel gratuit dont le module a besoin. Sa licence ne
nous permet pas de le distribuer : vous le téléchargez donc vous-même, une seule fois :

1. Ouvrez [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) et cliquez sur **Register**.
   Acceptez la licence et confirmez l’e-mail.
2. Connectez-vous, ouvrez **Download** et téléchargez le modèle SMPL-X (la
   version **NPZ**).
3. Décompressez-le et repérez **`SMPLX_NEUTRAL.npz`**.
4. Dans Blender, cliquez sur **Choisir le modèle SMPL-X…** (Choose SMPL-X Model…)
   et sélectionnez ce fichier. Le panneau affiche alors **Modèle SMPL-X : trouvé** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Obtenir un personnage Mixamo

1. Ouvrez [mixamo.com](https://www.mixamo.com/) et connectez-vous avec un compte Adobe.
2. Onglet **Characters** → choisissez un personnage (par exemple **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Générer le mouvement

Dans la zone **Entrée** (Input) :

1. **Type de source** (Source Type) : Vidéo (ou Image pour une pose unique)
2. **Fichier source** (Source File) : votre clip. Il doit montrer **exactement une
   personne, entièrement cadrée de la tête aux pieds pendant toute la durée**.
3. **FBX du rig Mixamo** (Mixamo Rig FBX) : le personnage de l’étape 5
4. **Détecter les mains** (Detect Hands) est désactivé. Activez-le seulement si les
   doigts doivent bouger. Cliquez ensuite sur **Choisir le modèle de main MANO…**
   (Choose MANO Hand Model…) et sélectionnez `MANO_RIGHT.pkl`. Récupérez ce fichier
   comme SMPL-X : inscrivez-vous sur
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), téléchargez **Models & Code**
   et décompressez-le. Le premier passage des mains télécharge environ **2,7 Go** de
   plus, une seule fois, et dure environ deux fois plus longtemps qu’un passage du corps seul. Lorsqu’il est activé, **Finger Smoothing (seconds)** apparaît. Il adoucit le mouvement des doigts. La valeur par défaut est 0,08 seconde ; 0 garde ce qui a été détecté.
5. Cliquez sur **Générer le mouvement** (Generate Motion)

Une fois le traitement terminé, le personnage animé est automatiquement importé
dans votre scène. Un pied posé reste là où il s’est posé, et la plante est placée sur le sol de Blender. Un mesh **Repères au sol** (Floor Markers) est ajouté sur ce sol (une croix tous les 0,5 m). La case **Repères au sol** (Floor Markers) sous Progression / Résultat l’affiche ou le masque.

### Le premier lancement est plus long — c’est normal

La première fois, le module télécharge environ **5,6 Go** de modèles. Le panneau
affiche la taille du téléchargement, la vitesse et le temps restant. Les modèles
ne sont téléchargés qu’une seule fois.

Ensuite, la vidéo est traitée sur votre ordinateur. Sur le CPU d’un Mac, un clip
de 10 secondes prend quelques minutes. Blender reste utilisable pendant le
traitement, et **Annuler** (Cancel) arrête la tâche.

## Conseils pour de bons résultats

- Une seule personne, corps entier visible, sans être coupé sur les bords
- Caméra stable, bon éclairage, vêtements simples plutôt qu’amples ou flottants
- Les clips courts (5 à 20 secondes) sont plus rapides pour un premier essai

## Passer à une nouvelle version

Le module est mis à jour fréquemment. Pour le mettre à jour :

1. Téléchargez le zip le plus récent depuis la
   [dernière version](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → supprimez l’ancien **Motion2MixamoRig**, quittez
   complètement Blender (**Cmd+Q**), relancez-le et installez le nouveau zip.
3. Dans le panneau, cliquez sur **Mettre à jour l’environnement** (Update Runtime).

La mise à jour conserve les modèles déjà téléchargés : elle est donc rapide. La
version installée est indiquée à côté du module dans **Get Extensions**.

## Le panneau

- **⚙ à côté du titre** affiche ou masque la zone **Configuration** (Setup).
- **Configuration** : langue, environnement, SMPL-X, **Appareil** (Device ; le CPU
  est le choix le plus sûr) et **Vérifier l’environnement** (Check Environment).
- **Entrée** : ce qu’il faut animer, le **Modèle du corps** (Body Model, GVHMR) et **Détecter les mains** (Detect Hands).
- **Progression / Résultat** (Progress / Result) : progression, journal récent et, après une tâche,
  **Importer le personnage généré** (Import Generated Character), **Repères au sol** (Floor Markers), **Ouvrir le dossier de sortie** (Open Output Folder),
  **Voir le journal complet** (View Full Log).
- **Diagnostic** (Diagnostics) : les endroits où des parties du corps du
  personnage entrent l’une dans l’autre (une main dans la tête, des bras
  croisés). Les cases rouges de la barre sont des images avec un problème ;
  cliquez sur l’une d’elles pour y aller. Le triangle sous la barre suit
  l’image courante, et en dessous s’affichent les parties qui se chevauchent
  et leur profondeur. **Précédent** / **Suivant** (Previous / Next) passent
  d’un problème à l’autre. **Ouvrir le rapport HTML** (Open HTML Report) ouvre
  dans le navigateur un rapport avec la vidéo source à côté du personnage (la
  première fois, sa création prend environ 15 secondes). La vidéo d’origine a besoin de ffmpeg sur l’ordinateur (sur Mac : `brew install ffmpeg`). Sans lui, le personnage est là et la vidéo à côté reste vide. Le personnage se tient sur des croix de sol fixes, une tous les 0,5 m, pour voir s’il glisse. La bande ambre au-dessus des pistes rouges sert aux remarques que vous faites à l’œil. Elles sont listées à droite sous **Notes** ; un clic sur une ligne y saute. **Download notes** enregistre ces remarques avec les instants d’intersection. Le fichier porte le nom de la vidéo source.

Le module parle 19 langues. **Automatique (Blender / Système)** (Auto) suit la langue de Blender ;
vous pouvez la changer dans la zone Configuration, sous **Langue de l’interface** (UI Language).

## En cas de problème

| Ce que vous voyez | Que faire |
| --- | --- |
| **Échec de l’installation de l’environnement** (Runtime installation failed) | Vérifiez votre connexion Internet et cliquez à nouveau sur le bouton. Journal : `~/Motion2MixamoRig/logs/setup.log` |
| **Modèle SMPL-X : manquant** (SMPL-X model: missing) | Refaites l’étape 4 et sélectionnez `SMPLX_NEUTRAL.npz` |
| **Modèle de main MANO : manquant** (MANO hand model: missing) | Activez **Détecter les mains**, puis **Choisir le modèle de main MANO…** et sélectionnez `MANO_RIGHT.pkl` |
| **FBX Mixamo non valide** (Mixamo FBX invalid) | Téléchargez à nouveau le personnage en **FBX Binary**, **T-pose** |
| **L’entrée contient plusieurs personnes** (Input contains multiple people) | Utilisez un clip avec une seule personne |
| **Aucune personne détectée dans l’entrée** (No person was detected in the input) | Vérifiez que le corps entier est visible et bien éclairé |
| **Le processus du pipeline s’est arrêté de façon inattendue** (Pipeline process exited unexpectedly) | Cliquez sur **Voir le journal complet** |

Lorsque vous demandez de l’aide, joignez le journal et précisez la version du module que vous utilisez.

## Désinstallation

1. **Get Extensions** → supprimez **Motion2MixamoRig**.
2. Supprimez le dossier **`~/Motion2MixamoRig`** (votre dossier personnel →
   `Motion2MixamoRig`). Supprimer le module ne le supprime **pas** ; il contient
   environ 7 Go d’environnement et de modèles, ainsi que vos résultats générés
   dans `app/outputs/`.

## Licence

Motion2MixamoRig est réservé à un **usage non commercial** : il s’appuie sur des
modèles de recherche (comme GVHMR et SMPL-X) dont les licences n’autorisent pas
l’usage commercial. Voir [`NOTICE.md`](../../NOTICE.md).
