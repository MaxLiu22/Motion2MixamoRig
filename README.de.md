# Motion2MixamoRig

![Motion2MixamoRig](repo_poster.png)

<p align="center">
  <a href="README.zh-CN.md">中文</a> · <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · Deutsch · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a>
</p>

Überträgt die Bewegung einer Person aus einem Video — oder die Pose aus einem Foto — auf einen Adobe-Mixamo-geriggten 3D-Charakter.

Für Spieleentwickler: ein Video mit **genau einer Person** (oder ein Still) und ein Mixamo-Charakter; Ausgabe sind Vorschauen plus eine Charakterdatei mit Skinning (`.glb`) für Blender oder Unity.

Agents beginnen mit [`AGENTS.md`](AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub><a href="demo.mp4">demo.mp4</a> in diesem Repository öffnen.</sub>
</p>

Weiteres Demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

## Voraussetzungen

Python 3.10+. Nach dem Klonen eine virtuelle Umgebung anlegen und Abhängigkeiten installieren; danach steht `m2mr` bereit:

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

Inferenzgewichte (GVHMR usw.) werden hier nicht geladen. Der erste `m2mr run` zieht sie nach `weights/` (~5 GB, nur einmal).

ffmpeg wird empfohlen (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Ohne ffmpeg läuft die Pipeline, aber die Ausgabevideos sind **stumm** und spielen im Browser nicht.

## Vor dem Lauf: dies nach `assets/` legen

Dieses Repository enthält diese Dateien nicht; sie müssen selbst besorgt werden. Der SMPL-X-Dateiname muss exakt zur Tabelle passen; FBX-, Video- und Bildnamen sind frei. Ein Lauf braucht SMPL-X, einen Mixamo-Charakter und **entweder** ein Video **oder** ein Still.

| Was | Wohin | Woher |
|---|---|---|
| SMPL-X-Körpermodell | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Bei [SMPL-X](https://smpl-x.is.tue.mpg.de/) registrieren und herunterladen |
| Mixamo-Charakter-FBX | `assets/mixamo/Y_Bot.fbx` | Mit Adobe-Konto Y Bot (oder einen anderen Mixamo-geriggten Charakter) von [Mixamo](https://www.mixamo.com) laden |
| Bewegungsvideo | `assets/video/<your_clip>.mp4` | Clip mit **genau einer** klar sichtbaren Person, **Kopf bis Fuß die ganze Zeit im Bild** (mehrere Dateien möglich; jeder Lauf nimmt die zuletzt hinzugefügte) |
| Pose-Foto (optional) | `assets/image/<your_photo>.jpg` | Foto mit **genau einer** klar sichtbaren Person, **Kopf bis Fuß im Bild**. Mit `--image` |

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

### 2. Erster Lauf: etwas auf dem Bildschirm

Ohne Flags: die **neueste Datei in `assets/video/`** und `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Das ist der langsame Schritt. Der erste Lauf lädt ~5 GB Inferenzgewichte (nur einmal), dann extrahiert er die menschliche Bewegung.
Auf CPU dauert ein ~30-Sekunden-Clip etwa 8–15 Minuten; spätere Läufe ähnlicher Länge mit vorhandenen Gewichten etwa 3–5 Minuten.
Retargeting und Rendering dauern meist ein bis zwei Minuten. Mit `--skeleton` im nächsten Abschnitt entfällt die Extraktion komplett, fertig in wenigen zehn Sekunden.

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

## Ausgaben

Jeder `m2mr run` legt ein Verzeichnis an, benannt nach **Startzeit des Befehls**. Die vier Dateien im Wurzelverzeichnis sind für Video und Foto gleich; nur der Vorschauordner ändert sich.

```
outputs/20260829_193205_dance/          # Foto-Lauf: …_pose/
├── run.json                            # Startzeit, Eingaben, vollständiger Befehl
├── skeleton_motion.npz                 # 3D-Körperskelett (mit --skeleton wiederverwenden)
├── mixamo_rotations.npz                # Mixamo-Rotationen pro Bone
├── mixamo_character.glb                # Charakter mit Skinning, Import in Blender / Unity
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

`mixamo_character.glb` in Blender öffnen: File → Import → glTF 2.0 (.glb/.gltf). Zeigt die Kamera ins Leere, den Charakter wählen und View → Frame Selected. Die Kugeln an Kopf und Händen sind die Knochenanzeige, nicht das Mesh: Armature wählen und unter Armature → Viewport Display die Shapes ausschalten. Beim Videolauf das letzte Timeline-Frame auf die Cliplänge setzen und mit `videos/mixamo_character.mp4` vergleichen. Beim Fotolauf mit `images/mixamo_character.png` oder dem Orbit-Clip vergleichen.

## Lizenz

Der Code dieses Repositories ist Apache-2.0. Die selbst beschafften Assets haben eigene Bedingungen und dürfen nicht mit diesem Repo weitergegeben werden:

- **SMPL-X**: MPI-Zugang; Standard nichtkommerziell Forschung / Bildung / Kunst; kommerzielle Nutzung braucht eine eigene Vereinbarung
- **Mixamo FBX**: in einem Produkt erlaubt; das rohe FBX nicht als Asset-Pack weitergeben
- **GVHMR und andere Inferenzgewichte**: beim ersten `m2mr run` automatisch nach `weights/`, jeweils unter der Upstream-Lizenz

## Kontakt

Bei Problemen, wenn Hilfe beim lokalen Setup nötig ist oder Sie über eine Zusammenarbeit sprechen möchten, schreiben Sie an:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)
