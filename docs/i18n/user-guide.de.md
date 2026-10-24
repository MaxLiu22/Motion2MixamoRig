# Motion2MixamoRig für Blender — Benutzerhandbuch

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · Deutsch · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Mach aus dem Video einer Person einen animierten Mixamo-Charakter — direkt in Blender.
Ohne Programmieren und ohne Terminal.

<!-- video: link the tutorial video here -->

> Bisher nur unter **macOS (Apple Silicon)** getestet. Eine Windows-Version kommt bald.

## Was du brauchst

- **Blender 4.2 oder neuer**
- **Eine Internetverbindung** für die erste Einrichtung
- **Etwa 8 GB freien Speicherplatz** (Laufzeitumgebung ~1,3 GB + Modelle ~5,6 GB)
- **Ein kostenloses SMPL-X-Konto** und **ein kostenloses Adobe-Konto** (für Mixamo); siehe Schritt 4 und 5

## 1. Add-on herunterladen

Öffne das [neueste Release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
und lade die Zip-Datei für deinen Computer herunter:

| Dein Computer | Datei |
| --- | --- |
| Mac mit Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Kommt bald** |

Zum Beispiel `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` ist die
Add-on-Version, `macos-arm64` die Plattform. Erwischst du die falsche Datei,
verweigert Blender die Installation und nennt die erwartete Plattform.

Entpacke die Datei **nicht**. Blender installiert die Zip-Datei selbst.

## 2. In Blender installieren

1. **Edit → Preferences → Get Extensions**
2. Klicke oben rechts auf das kleine **∨** → **Install from Disk…**
3. Wähle die Zip-Datei. **Motion2MixamoRig** erscheint aktiviert in der Liste.
4. Schließe die Preferences. Drück im 3D Viewport **N** und klicke dann rechts
   auf den Tab **Motion2MixamoRig**.

<!-- screenshot: Install from Disk menu -->

## 3. Laufzeitumgebung installieren (einmalig)

Klicke im Panel auf **Laufzeitumgebung installieren (ein Klick)** (Install Runtime (one click)).

Das Add-on lädt sein eigenes Python samt Bibliotheken (~1,4 GB) nach
`~/Motion2MixamoRig/`. Sonst wird auf deinem Computer nichts verändert. Das
dauert ein paar Minuten; der Fortschrittsbalken zeigt den aktuellen Schritt.

<!-- screenshot: Install Runtime button and progress -->

## 4. SMPL-X-Körpermodell besorgen

SMPL-X ist ein kostenloses Körpermodell, das das Add-on braucht. Seine Lizenz
erlaubt uns nicht, es mitzuliefern, also lädst du es einmalig selbst herunter:

1. Öffne [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) und klicke auf **Register**.
   Akzeptiere die Lizenz und bestätige die E-Mail.
2. Melde dich an, öffne **Download** und lade das SMPL-X-Modell herunter (die
   **NPZ**-Version).
3. Entpacke es und suche **`SMPLX_NEUTRAL.npz`**.
4. Klicke in Blender auf **SMPL-X-Modell wählen…** (Choose SMPL-X Model…) und
   wähle diese Datei. Das Panel zeigt dann **SMPL-X-Modell: gefunden** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Mixamo-Charakter besorgen

1. Öffne [mixamo.com](https://www.mixamo.com/) und melde dich mit einem Adobe-Konto an.
2. Tab **Characters** → wähle einen Charakter (zum Beispiel **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Motion erzeugen

Im Bereich **Eingabe** (Input):

1. **Quelltyp** (Source Type): Video (oder Bild für eine einzelne Pose)
2. **Quelldatei** (Source File): dein Clip. Er muss **genau eine Person zeigen,
   die die ganze Zeit von Kopf bis Fuß im Bild ist**.
3. **Mixamo-Rig FBX** (Mixamo Rig FBX): der Charakter aus Schritt 5
4. **Hände erkennen** (Detect Hands) ist aus. Schalte es nur ein, wenn sich die
   Finger bewegen sollen. Klicke dann auf **MANO-Handmodell wählen…** (Choose MANO
   Hand Model…) und wähle `MANO_RIGHT.pkl`. Die Datei holst du wie SMPL-X: registriere
   dich auf [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), lade **Models & Code**
   und entpacke es. Der erste Handlauf lädt einmalig etwa **2,7 GB** zusätzlich und
   dauert ungefähr doppelt so lang wie ein reiner Körperlauf. Ist es an, erscheint **Finger Smoothing (seconds)**. Es glättet die Fingerbewegung. Der Standard ist 0,08 Sekunden; 0 lässt die erkannte Bewegung unverändert.
5. Klicke auf **Motion erzeugen** (Generate Motion)

Wenn der Vorgang fertig ist, wird der animierte Charakter automatisch in deine
Szene importiert. Ein aufgesetzter Fuß bleibt, wo er gelandet ist, und die Sohle liegt auf dem Boden von Blender. Auf diesem Boden kommt ein Mesh **Bodenmarkierungen** (Floor Markers) dazu (ein Kreuz alle 0,5 m). Das Kontrollkästchen **Bodenmarkierungen** (Floor Markers) unter Fortschritt / Ergebnis blendet es ein oder aus.

### Der erste Lauf dauert länger — das ist normal

Beim ersten Mal lädt das Add-on etwa **5,6 GB** an Modellen herunter. Das Panel
zeigt Downloadgröße, Geschwindigkeit und Restzeit. Die Modelle werden nur
einmal heruntergeladen.

Danach wird das Video auf deinem Computer verarbeitet. Auf einer Mac-CPU
braucht ein 10-Sekunden-Clip ein paar Minuten. Blender bleibt währenddessen
benutzbar, und **Abbrechen** (Cancel) stoppt den Auftrag.

## Tipps für gute Ergebnisse

- Nur eine Person, ganzer Körper sichtbar, nicht an den Rändern abgeschnitten
- Ruhige Kamera, gutes Licht, eher anliegende als weite oder wehende Kleidung
- Kurze Clips (5–20 Sekunden) sind für erste Versuche schneller

## Auf eine neue Version aktualisieren

Das Add-on wird häufig aktualisiert. So aktualisierst du:

1. Lade die neueste Zip-Datei aus dem
   [neuesten Release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest) herunter.
2. **Get Extensions** → entferne das alte **Motion2MixamoRig**, beende Blender
   vollständig (**Cmd+Q**), öffne es wieder und installiere die neue Zip-Datei.
3. Klicke im Panel auf **Laufzeitumgebung aktualisieren** (Update Runtime).

Beim Aktualisieren bleiben die heruntergeladenen Modelle erhalten, daher geht
es schnell. Deine installierte Version steht neben dem Add-on in **Get Extensions**.

## Das Panel

- **⚙ neben dem Titel** blendet den Bereich **Einrichtung** (Setup) ein oder aus.
- **Einrichtung**: Sprache, Laufzeitumgebung, SMPL-X, **Gerät** (Device; CPU ist
  die sichere Wahl) und **Umgebung prüfen** (Check Environment).
- **Eingabe**: was animiert werden soll, **Körpermodell** (Body Model, GVHMR) und **Hände erkennen** (Detect Hands).
- **Fortschritt / Ergebnis** (Progress / Result): Fortschritt, aktuelles Log und nach einem Auftrag
  **Erzeugten Charakter importieren** (Import Generated Character), **Bodenmarkierungen** (Floor Markers), **Ausgabeordner öffnen** (Open Output Folder),
  **Vollständiges Protokoll** (View Full Log).
- **Diagnose** (Diagnostics): Stellen, an denen Körperteile des Charakters
  ineinander stecken (eine Hand im Kopf, verschränkte Arme). Rote Zellen im
  Balken sind Frames mit einem Problem; ein Klick springt dorthin. Das Dreieck
  unter dem Balken folgt dem aktuellen Frame, darunter stehen die betroffenen
  Teile und wie tief sie ineinander stecken. **Zurück** / **Weiter** (Previous
  / Next) springen zwischen den Problemen. **HTML-Bericht öffnen** (Open HTML
  Report) öffnet im Webbrowser einen Bericht mit dem Quellvideo neben dem
  Charakter (beim ersten Mal dauert das Erstellen etwa 15 Sekunden). Das Originalvideo braucht ffmpeg auf dem Computer (auf dem Mac: `brew install ffmpeg`). Ohne ffmpeg ist der Charakter da, und das Video daneben bleibt leer. Der Charakter steht auf festen Bodenkreuzen, alle 0,5 m eines, damit zu sehen ist, ob er rutscht. Die bernsteinfarbene Spur über den roten Spuren ist für Notizen, die du mit dem Auge machst. Sie stehen rechts unter **Notes**; ein Klick auf eine Zeile springt dorthin. **Download notes** speichert diese Notizen zusammen mit den Schnittzeiten. Die Datei heißt wie das Quellvideo.

Das Add-on spricht 19 Sprachen. **Automatisch (Blender / System)** (Auto) folgt der Sprache von Blender;
ändern kannst du das im Bereich Einrichtung unter **UI-Sprache** (UI Language).

## Wenn etwas schiefgeht

| Was du siehst | Was du tun kannst |
| --- | --- |
| **Installation der Laufzeitumgebung fehlgeschlagen** (Runtime installation failed) | Prüfe deine Internetverbindung und klicke erneut auf den Button. Log: `~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X-Modell: fehlt** (SMPL-X model: missing) | Wiederhole Schritt 4 und wähle `SMPLX_NEUTRAL.npz` |
| **MANO-Handmodell: fehlt** (MANO hand model: missing) | Schalte **Hände erkennen** ein, dann **MANO-Handmodell wählen…** und `MANO_RIGHT.pkl` wählen |
| **Mixamo-FBX ungültig** (Mixamo FBX invalid) | Lade den Charakter erneut als **FBX Binary**, **T-pose** herunter |
| **Die Quelle enthält mehrere Personen** (Input contains multiple people) | Verwende einen Clip mit nur einer Person |
| **Keine Person in der Quelle erkannt** (No person was detected in the input) | Achte darauf, dass der ganze Körper sichtbar und gut beleuchtet ist |
| **Pipeline-Prozess unerwartet beendet** (Pipeline process exited unexpectedly) | Klicke auf **Vollständiges Protokoll** |

Wenn du um Hilfe bittest, häng das Log an und nenne deine Add-on-Version.

## Deinstallieren

1. **Get Extensions** → entferne **Motion2MixamoRig**.
2. Lösche den Ordner **`~/Motion2MixamoRig`** (dein Benutzerordner →
   `Motion2MixamoRig`). Beim Entfernen des Add-ons wird er **nicht** gelöscht;
   er enthält etwa 7 GB Laufzeitumgebung und Modelle sowie deine erzeugten
   Ergebnisse in `app/outputs/`.

## Lizenz

Motion2MixamoRig ist **nur für die nicht-kommerzielle Nutzung** bestimmt: Es
basiert auf Forschungsmodellen (etwa GVHMR und SMPL-X), deren Lizenzen keine
kommerzielle Nutzung erlauben. Siehe [`NOTICE.md`](../../NOTICE.md).
