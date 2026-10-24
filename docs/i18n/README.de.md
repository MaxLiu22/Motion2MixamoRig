# Motion2MixamoRig

<p align="center">
  <a href="#voraussetzungen"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.de.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · Deutsch · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Überträgt die Bewegung einer Person aus einem Video — oder die Pose aus einem Foto — auf einen Adobe-Mixamo-geriggten 3D-Charakter.

Für Spieleentwickler: ein Video mit **genau einer Person** (oder ein Still) und ein Mixamo-Charakter; Ausgabe sind Vorschauen plus eine Charakterdatei mit Skinning (`.glb`) für Blender oder Unity.

> Motion2MixamoRig ist noch experimentell. Version 0.1.8 ist die Kommandozeilen-Pipeline. In diesem Repository liegt außerdem eine Blender-4.2+-Extension, die dieselbe Pipeline in einem externen Python ausführt. Add-on aus dem Quellcode bauen: [`blender_extension/README.md`](../../blender_extension/README.md).

## Zwei Wege zur Nutzung

### 🎨 In Blender — ohne Programmieren

1. Lade die Zip-Datei für deine Plattform, z. B. `motion2mixamorig-<version>-macos-arm64.zip`, aus dem [neuesten Release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest) herunter.
2. In Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, dann die Zip-Datei wählen.
3. 3D Viewport → **N** drücken → Tab **Motion2MixamoRig** → **Laufzeitumgebung installieren (ein Klick)** (Install Runtime (one click)).
4. **SMPL-X-Modell wählen…** (Choose SMPL-X Model…; kostenloser Download) und eine Mixamo-Charakter-FBX wählen.
5. Ein Video mit einer Person wählen → **Motion erzeugen** (Generate Motion).

Schritt-für-Schritt-Anleitung, Tipps und Aktualisieren: **[Benutzerhandbuch](user-guide.de.md)**. Getestet unter macOS (Apple Silicon).

### 💻 Kommandozeile — für Entwickler

Repository klonen und die Pipeline selbst ausführen: Beginne bei den [Voraussetzungen](#voraussetzungen).

Agents beginnen mit [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub><a href="../assets/demo.mp4">demo.mp4</a> in diesem Repository öffnen.</sub>
</p>

Weiteres Demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Diagnosebericht (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Voraussetzungen

Python 3.11+. Nach dem Klonen eine virtuelle Umgebung anlegen und Abhängigkeiten installieren; danach steht `m2mr` bereit:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Abhängigkeiten und dieses Projekt installieren. chumpy (ein altes Paket in der
# Abhängigkeitskette) importiert pip im Setup-Skript; das schlägt in pips
# isoliertem Build mit "No module named 'pip'" fehl. Zuerst ohne Isolation
# installieren (--no-build-isolation), dann dieses Projekt.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Inferenzgewichte (GVHMR usw.) werden hier nicht geladen. Der erste `m2mr run` zieht sie nach `weights/` (~5 GB, nur einmal). Der erste `m2mr run --detect-hands` holt zusätzlich die HaMeR-Handgewichte nach `weights/hamer/` (~2,7 GB, nur einmal).

ffmpeg wird empfohlen (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Ohne ffmpeg läuft die Pipeline, aber die Ausgabevideos sind **stumm** und spielen im Browser nicht.

## Vor dem Lauf: dies nach `assets/` legen

Dieses Repository enthält diese Dateien nicht; sie müssen selbst besorgt werden. Der SMPL-X-Dateiname muss exakt zur Tabelle passen; FBX-, Video- und Bildnamen sind frei. Ein Lauf braucht SMPL-X, einen Mixamo-Charakter und **entweder** ein Video **oder** ein Still. Aus Cinema 4D neu exportierte Mixamo-Charakter-FBX funktionieren ebenfalls; siehe [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Was | Wohin | Woher |
|---|---|---|
| SMPL-X-Körpermodell | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Bei [SMPL-X](https://smpl-x.is.tue.mpg.de/) registrieren und herunterladen |
| Mixamo-Charakter-FBX | `assets/mixamo/Y_Bot.fbx` | Mit Adobe-Konto Y Bot (oder einen anderen Mixamo-geriggten Charakter) von [Mixamo](https://www.mixamo.com) laden |
| Bewegungsvideo | `assets/video/<your_clip>.mp4` | Clip mit **genau einer** klar sichtbaren Person, **Kopf bis Fuß die ganze Zeit im Bild** (mehrere Dateien möglich; jeder Lauf nimmt die zuletzt hinzugefügte) |
| Pose-Foto (optional) | `assets/image/<your_photo>.jpg` | Foto mit **genau einer** klar sichtbaren Person, **Kopf bis Fuß im Bild**. Mit `--image` |
| MANO-rechte Hand (nur für `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Bei [MANO](https://mano.is.tue.mpg.de/) registrieren und **Models & Code** laden. Ein reiner Körperlauf braucht diese Datei nicht |

Hinweis: Der Download von Mixamo heißt `Y Bot.fbx` (**Leerzeichen**) und weicht um ein Zeichen von `Y_Bot.fbx` (**Unterstrich**) in der Tabelle ab.
Umbenennen zum Unterstrich macht es zum Standard-Rig (`m2mr run` ohne `--rig`). Der Name mit Leerzeichen ist ebenfalls in Ordnung — fehlt `Y_Bot.fbx`, wird die erste `.fbx` in `assets/mixamo/` verwendet.

In `assets/video/` können mehrere Videos liegen. Ohne `--video` oder `--image` nimmt der Lauf die **zuletzt in `assets/video/` gelegte** Datei; ist der Ordner leer, das neueste Still in `assets/image/`.
Jeder Clip oder jedes Foto darf nur eine Person zeigen, **Kopf bis Fuß im Bild** — nichts am Rand abgeschnitten. `m2mr doctor` / `m2mr run` stoppen vor der Extraktion, wenn zwei Personen zu sehen sind.

## Schnellstart

Ergebnisse liegen in `outputs/<Laufzeit>_<Quelle>/`. Videoläufe schreiben `videos/`; Fotoläufe schreiben `images/`.

### 1. Assets und Umgebung prüfen

Fehlendes wird mit Download-Ort und Zielpfad ausgegeben.

```bash
m2mr doctor
```

`m2mr doctor` prüft den Körperlauf. Das MANO-Handmodell verlangt es nicht. So prüfst du die zusätzliche Datei und die Python-Pakete für die Fingererkennung:

```bash
m2mr doctor --detect-hands
```

### 2. Erster Lauf: etwas auf dem Bildschirm

Ohne Flags: die **neueste Datei in `assets/video/`** und `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Das ist der langsame Schritt. Der erste Lauf lädt ~5 GB Inferenzgewichte (nur einmal), dann extrahiert er die menschliche Bewegung.
Auf CPU dauert ein ~30-Sekunden-Clip etwa 8–15 Minuten; spätere Läufe ähnlicher Länge mit vorhandenen Gewichten etwa 3–5 Minuten.
Retargeting und Rendering dauern meist ein bis zwei Minuten. Mit `--skeleton` im nächsten Abschnitt entfällt die Extraktion komplett, fertig in wenigen zehn Sekunden.

Ein aufgesetzter Fuß wird standardmäßig festgehalten: der Ballen, wenn der Ballen unten ist, die Ferse nur, wenn die Zehen oben sind. Reicht ein gestrecktes Bein nicht, verschiebt sich die Hüfte. Danach liegt die Sohle auf dem Boden (y = 0). `--no-foot-lock` behält das rohe Retargeting, die Füße können also rutschen; die Sohle wird trotzdem auf den Boden gesetzt.

### 3. Gleiche Bewegung, anderer Charakter

Einen weiteren Charakter von Mixamo nach `assets/mixamo/` legen. **Nicht nur mit `--rig` neu starten** — das wiederholt die langsame Extraktion.
`--skeleton` verwendet das Skelett eines früheren Laufs; Minuten werden zu wenigen zehn Sekunden:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Ein anderes Video

`--video` wählt den Clip. Kombinierbar mit `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Ein Still (statische Pose)

`--image` rekonstruiert eine **statische 3D-Pose** aus einem Foto mit einer Person und überträgt sie wie ein Videolauf auf den Mixamo-Charakter. Vorschauen sind vier Stills in `images/` (gleiche Ansichten wie der Videolauf) plus der Links/Rechts-Orbit-Clip `before_after_360_compare.mp4`. Nicht zusammen mit `--video` verwenden.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` ohne Pfad nimmt die zuletzt nach `assets/image/` gelegte Datei.

### 6. Auf Selbstdurchdringung prüfen

Jeder Lauf prüft den fertigen Charakter außerdem auf **Selbstdurchdringung** — ein Körperteil dringt in ein anderes ein, etwa eine Hand in den Kopf — und schreibt `diagnostics.json`. Das Terminal gibt eine Zeile aus, z. B. `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Der Boden wird nicht geprüft.

Um einen Lauf erneut zu prüfen oder die Probleme anzusehen:

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json neu schreiben
m2mr diagnose outputs/<run> --visualize      # zusätzlich diagnostics.html: Quellvideo neben dem Charakter, Timeline, anklickbare Problemliste
m2mr diagnose outputs/<run> --threshold-cm 2 # nur Durchdringungen tiefer als 2 cm melden (Standard 1)
```

Jedes Problem in `diagnostics.json` ist ein Paar von Körperteilen mit den Frame-Bereichen, in denen sie sich durchdringen, dem schlimmsten Frame und dessen Tiefe. Frame-Nummern zählen ab 0, wie die Blender-Timeline nach einem glTF-Import. Durch ein Gelenk verbundene Teile (Ober- und Unterarm, Rumpf und Oberschenkel, …) werden nicht verglichen: Ihre Haut überlappt am Gelenk in jeder Pose. `diagnostics.html` bettet das Quellvideo ein (braucht `ffmpeg`) und lädt three.js von einem CDN, daher braucht die 3D-Ansicht eine Internetverbindung. Diese Ansicht zeichnet feste Bodenmarkierungen auf y = 0: ein Kreuz alle 0,5 m, ein größeres jeden Meter, am Ursprung ein grünes, damit du sehen kannst, ob sich der Charakter bewegt. Die bernsteinfarbene Spur über den Schnittspuren ist für Notizen, die man mit dem Auge sieht (einen Bereich ziehen oder **In** / **Out**). Die Liste **Notes** rechts zeigt sie; ein Klick auf eine Zeile springt dorthin. **Download notes** speichert diese Notizen zusammen mit der Schnittliste. Die Datei trägt den Namen des Quellvideos und enthält dessen Pfad.

### 7. Finger (`--detect-hands`)

Ein schlichtes `m2mr run` bewegt den Körper und lässt die Mixamo-Fingerknochen in Ruhepose. `--detect-hands` schaltet das Handmodell ein, das zum Körper-Extraktor gehört. Beim Standard-Extraktor GVHMR ist das [HaMeR](https://github.com/geopavlakos/hamer). HaMeR schneidet die Handgelenke aus der Person und den Frames, die GVHMR schon gewählt hat. Es sucht im Clip nicht nach einer zweiten Person.

**Das verdoppelt die Laufzeit ungefähr.** Ein Clip, der ohne das Flag in wenigen Minuten fertig ist, braucht mit `--detect-hands` etwa doppelt so lang, weil der Handdurchlauf auf der Körperextraktion sitzt. Bei einem langen Video plane diese Zeit ein, bevor du startest.

Lege `MANO_RIGHT.pkl` wie in der Tabelle oben ab, dann:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Der erste Lauf mit `--detect-hands` lädt die HaMeR-Gewichte nach `weights/hamer/` (~2,7 GB, einmal). Die Fingerrotationen landen in `skeleton_motion.npz` und treiben die 30 Mixamo-Fingerknochen am geskinnten Charakter. Ein Handgelenk, das der Körperdurchlauf nicht klar gesehen hat, bleibt für diese Hand in Ruhepose.

`--hand-smooth` ist, wie viele Sekunden Glättung auf diese Rotationen kommen. Der Standard ist `0.08`. `0` behält die rohe Schätzung. Die Glättung läuft, sobald die Skelettdatei schon Handbewegung enthält, auch bei einem späteren Lauf, der nur diese Datei wiederverwendet.

Ein früheres Skelett wiederverwenden:

- Die Datei enthält schon Handbewegung: `--skeleton` treibt die Finger von selbst. `--detect-hands` ist nicht noch einmal nötig.
- Sie enthält keine, aber der Körper-Cache dieses Laufs liegt noch daneben (`cache/<clip>/0_input_video.mp4` plus `preprocess/vitpose.pt` und `preprocess/bbx.pt`): `--skeleton ... --detect-hands` ergänzt die Finger, ohne den Körper neu zu extrahieren.
- Dieser Cache ist weg: Video oder Foto noch einmal mit `--detect-hands` laufen lassen.

## Ausgaben

Jeder `m2mr run` legt ein Verzeichnis an, benannt nach **Startzeit des Befehls**. Die Dateien im Wurzelverzeichnis sind für Video und Foto gleich; nur der Vorschauordner ändert sich.

```
outputs/20260829_193205_dance/          # Foto-Lauf: …_pose/
├── run.json                            # Startzeit, Eingaben, vollständiger Befehl
├── skeleton_motion.npz                 # 3D-Körperskelett (mit --skeleton wiederverwenden)
├── mixamo_rotations.npz                # Mixamo-Rotationen pro Bone
├── mixamo_character.glb                # Charakter mit Skinning, Import in Blender / Unity
├── diagnostics.json                    # Bericht zur Selbstdurchdringung (siehe Schnellstart, Schritt 6)
├── diagnostics.html                    # nur nach `m2mr diagnose <run> --visualize`
└── videos/   oder   images/            # Vorschauen — je nach Eingabe
```

**Videoeingabe** schreibt `videos/` (gleiches Seitenverhältnis wie der Clip):

```
videos/
├── human_skeleton.mp4                  # rekonstruiertes 3D-Körperskelett
├── mixamo_skeleton.mp4                 # Mixamo-Rig-Skelett
├── mixamo_character.mp4                # Mixamo-Charakter mit Skinning
└── compare.mp4                         # 2×2: Original (oben links) / Mixamo-Skelett (oben rechts)
                                        #      Körperskelett (unten links) / Charakter (unten rechts)
```

**Fotoeingabe** schreibt stattdessen `images/` (dieselben vier Ansichten plus Turntable):

```
images/
├── human_skeleton.png                  # rekonstruiertes 3D-Körperskelett
├── mixamo_skeleton.png                 # Mixamo-Rig-Skelett
├── mixamo_character.png                # Mixamo-Charakter mit Skinning
├── compare.png                         # 2×2: Original (oben links) / Mixamo-Skelett (oben rechts)
│                                       #      Körperskelett (unten links) / Charakter (unten rechts)
└── before_after_360_compare.mp4        # links: Originalfoto
                                        # rechts: 10°-Orbit um den Rig (eine volle Umdrehung)
```

Mit `--detect-hands` stehen in `skeleton_motion.npz` auch die Fingerrotationen, und `mixamo_rotations.npz` sowie `mixamo_character.glb` enthalten die 30 Fingerknochen. Ohne dieses Flag, und ohne schon gespeicherte Handbewegung in einem wiederverwendeten Skelett, bleiben diese Knochen in Ruhepose.

`mixamo_character.glb` in Blender öffnen: File → Import → glTF 2.0 (.glb/.gltf). Zeigt die Kamera ins Leere, das Charakter-Mesh wählen und View → Frame Selected. Die Kugeln an Kopf und Händen sind die Knochenanzeige, nicht das Mesh: im Outliner **Icosphere** und die **Armature** ausblenden, das Mesh mit Skinning sichtbar lassen. Szene-FPS aus `run.json` (`fps`) und die Timeline auf die Frames 0 bis `n_frames` − 1 setzen, damit die Wiedergabe zur Quelle passt und die Frame-Nummern zu `diagnostics.json`. Videolauf mit `videos/mixamo_character.mp4` vergleichen, Fotolauf mit `images/mixamo_character.png` oder dem Orbit-Clip.

## Lizenz

Der Code dieses Repositories ist Apache-2.0. Die selbst beschafften Assets haben eigene Bedingungen und dürfen nicht mit diesem Repo weitergegeben werden:

- **SMPL-X**: MPI-Zugang; Standard nichtkommerziell Forschung / Bildung / Kunst; kommerzielle Nutzung braucht eine eigene Vereinbarung
- **MANO** (nur mit `--detect-hands`): MPI-Zugang, dieselbe Art Download wie SMPL-X; `MANO_RIGHT.pkl` lokal ablegen und nicht weitergeben
- **Mixamo FBX**: in einem Produkt erlaubt; das rohe FBX nicht als Asset-Pack weitergeben
- **GVHMR und andere Inferenzgewichte**: beim ersten `m2mr run` automatisch nach `weights/`, jeweils unter der Upstream-Lizenz
- **HaMeR**: der Inferenzcode in diesem Repository ist MIT; die Gewichte landen beim ersten `m2mr run --detect-hands` in `weights/hamer/`, unter den Bedingungen der Upstream-Veröffentlichung

## Kontakt

Bei Problemen, wenn Hilfe beim lokalen Setup nötig ist oder Sie über eine Zusammenarbeit sprechen möchten, schreiben Sie an:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
