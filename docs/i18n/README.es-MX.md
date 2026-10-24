# Motion2MixamoRig

<p align="center">
  <a href="#requisitos"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.es-MX.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · Español · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Transfiere el movimiento de una persona en un video — o la pose de una foto fija — a un personaje 3D riggeado con Adobe Mixamo.

Para desarrolladores de videojuegos: dale un video de acción con **una sola persona** (o una foto) y un personaje de Mixamo; genera videos de vista previa y un archivo de personaje con skinning (`.glb`) que puedes llevar directo a Blender o Unity.

> Motion2MixamoRig todavía es experimental. La versión 0.1.8 es el pipeline de línea de comandos. Este repositorio también incluye una extensión para Blender 4.2+ que ejecuta ese mismo pipeline en un entorno de Python externo. Cómo compilar el complemento desde el código fuente: [`blender_extension/README.md`](../../blender_extension/README.md).

## Dos formas de usarlo

### 🎨 En Blender — sin programar

1. Descarga el zip para tu plataforma, p. ej. `motion2mixamorig-<version>-macos-arm64.zip`, desde el [release más reciente](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. En Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…** y elige el zip.
3. 3D Viewport → presiona **N** → pestaña **Motion2MixamoRig** → **Instalar entorno (un clic)** (Install Runtime (one click)).
4. **Elegir modelo SMPL-X…** (Choose SMPL-X Model…) (una descarga gratuita) y elige un FBX de personaje de Mixamo.
5. Elige un video de una persona → **Generar movimiento** (Generate Motion).

Instrucciones paso a paso, consejos y cómo actualizar: **[Guía de usuario](user-guide.es-MX.md)**. Probado en macOS (Apple Silicon).

### 💻 Línea de comandos — para desarrolladores

Clona el repositorio y ejecuta el pipeline tú mismo: empieza por [Requisitos](#requisitos).

Los agentes deben empezar por [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Abre <a href="../assets/demo.mp4">demo.mp4</a> en este repositorio.</sub>
</p>

Otra demo:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Informe de diagnóstico (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Requisitos

Python 3.11+. Después de clonar, crea un virtualenv e instala las dependencias; con eso ya tendrás disponible el comando `m2mr`:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Instala las dependencias y este proyecto. chumpy (un paquete antiguo en la
# cadena de dependencias) importa pip en su script de setup, así que falla con
# "No module named 'pip'" en el build aislado que pip usa por defecto. Instálalo
# primero con el aislamiento desactivado y después instala este proyecto.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Los pesos de inferencia (GVHMR, etc.) no se descargan aquí. El primer `m2mr run` los descarga en `weights/` (~5 GB, solo una vez). El primer `m2mr run --detect-hands` también descarga los pesos de mano de HaMeR en `weights/hamer/` (~2.7 GB, solo una vez).

Se recomienda instalar ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
El pipeline funciona sin él, pero los videos de salida quedarán **sin audio** y no se podrán reproducir en el navegador.

## Antes de ejecutar: coloca estos archivos en `assets/`

Este repositorio no incluye estos archivos; tienes que conseguirlos tú. El nombre del archivo de SMPL-X debe coincidir exactamente con la tabla; los nombres del FBX, el video y la imagen pueden ser cualquiera. Cada ejecución necesita SMPL-X, un personaje de Mixamo y **o bien** un video **o bien** una foto. También funcionan los personajes de Mixamo reexportados desde Cinema 4D; consulta [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Qué | Dónde | Dónde conseguirlo |
|---|---|---|
| Modelo corporal SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Regístrate en [SMPL-X](https://smpl-x.is.tue.mpg.de/) y descárgalo |
| FBX del personaje de Mixamo | `assets/mixamo/Y_Bot.fbx` | Con una cuenta de Adobe, descarga Y Bot (o cualquier otro personaje riggeado con Mixamo) desde [Mixamo](https://www.mixamo.com) |
| Video de acción | `assets/video/<your_clip>.mp4` | Un clip con **exactamente una** persona bien visible, **de pies a cabeza dentro del cuadro todo el tiempo** (puedes guardar varios archivos; cada ejecución usa el que se agregó más recientemente) |
| Foto de pose (opcional) | `assets/image/<your_photo>.jpg` | Una foto con **exactamente una** persona bien visible, **de pies a cabeza dentro del cuadro**. Úsala con `--image` |
| Mano derecha MANO (solo para `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Regístrate en [MANO](https://mano.is.tue.mpg.de/) y descarga **Models & Code**. Una ejecución solo del cuerpo no necesita este archivo |

Nota: el archivo que descargas de Mixamo se llama `Y Bot.fbx` (**con espacio**), un carácter distinto de `Y_Bot.fbx` (**con guion bajo**) en la tabla.
Cámbiale el nombre a la forma con guion bajo y se convertirá en el rig predeterminado (`m2mr run` sin `--rig`). Dejar el espacio también funciona — si no existe `Y_Bot.fbx`, se usa el primer `.fbx` de `assets/mixamo/`.

`assets/video/` puede contener varios videos. Sin `--video` ni `--image`, la ejecución usa el archivo **agregado más recientemente** a `assets/video/`; si esa carpeta está vacía, usa la foto más reciente de `assets/image/`.
Cada clip o foto debe mostrar a una sola persona, **de pies a cabeza dentro del cuadro** — nada recortado en los bordes. `m2mr doctor` / `m2mr run` se detienen antes de la extracción si hay dos personas a la vista.

## Inicio rápido

Los resultados se guardan en `outputs/<run-time>_<source>/`. Las ejecuciones con video escriben `videos/`; las ejecuciones con foto escriben `images/`.

### 1. Revisa los recursos y el entorno

Todo lo que falte se muestra junto con dónde descargarlo y dónde colocarlo.

```bash
m2mr doctor
```

`m2mr doctor` revisa la ejecución del cuerpo. No exige el modelo de mano MANO. Para revisar también el archivo extra y los paquetes de Python que usa la detección de dedos:

```bash
m2mr doctor --detect-hands
```

### 2. Primera ejecución: ver algo en pantalla

Sin opciones, usa **el archivo más reciente de `assets/video/`** y `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Este es el paso lento. La primera ejecución descarga ~5 GB de pesos de inferencia (solo una vez) y luego extrae el movimiento humano del video.
En CPU, la extracción de un clip de ~30 segundos tarda unos 8–15 minutos; las ejecuciones posteriores de duración similar, con los pesos ya descargados, tardan unos 3–5 minutos.
El retargeting y el render suelen tardar uno o dos minutos. Reutilizar un esqueleto con `--skeleton` en la siguiente sección se salta por completo la extracción y termina en unas decenas de segundos.

Un pie apoyado se fija de forma predeterminada: el metatarso cuando el metatarso está abajo, el talón solo cuando los dedos están arriba. Si una pierna estirada no alcanza ese punto, la cadera se mueve. Después la planta queda sobre el piso (y = 0). `--no-foot-lock` conserva el retarget en bruto, así que los pies pueden deslizarse; la planta igual se coloca sobre el piso.

### 3. El mismo movimiento, otro personaje

Descarga otro personaje de Mixamo en `assets/mixamo/`. **No vuelvas a ejecutar solo con `--rig`** — eso repite la extracción lenta.
Pasa `--skeleton` para reutilizar el esqueleto de una ejecución anterior; los minutos se vuelven decenas de segundos:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Otro video

`--video` elige el clip. Se puede combinar libremente con `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Una foto fija (pose estática)

`--image` reconstruye una **pose 3D estática** a partir de la foto de una persona y luego la retargetea al personaje de Mixamo igual que una ejecución con video. Las vistas previas son cuatro imágenes fijas en `images/` (las mismas vistas que en la ejecución con video), además de un clip orbital izquierda/derecha `before_after_360_compare.mp4`. No pases `--video` al mismo tiempo.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` sin ruta usa el archivo agregado más recientemente a `assets/image/`.

### 6. Revisar autointersecciones

Cada ejecución también revisa el personaje terminado en busca de **autointersecciones** — una parte del cuerpo que entra en otra, como una mano dentro de la cabeza — y escribe `diagnostics.json`. La terminal imprime una línea, por ejemplo `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. No se revisa el piso.

Para volver a revisar una ejecución, o para ver los problemas:

```bash
m2mr diagnose outputs/<run>                  # reescribe diagnostics.json
m2mr diagnose outputs/<run> --visualize      # además diagnostics.html: video fuente junto al personaje, timeline, lista de problemas en la que puedes hacer clic
m2mr diagnose outputs/<run> --threshold-cm 2 # reporta solo penetraciones de más de 2 cm (por defecto 1)
```

Cada problema en `diagnostics.json` es un par de partes del cuerpo con los rangos de frames en que se intersectan, el peor frame y su profundidad. Los números de frame empiezan en 0, como la timeline de Blender después de importar un glTF. Las partes unidas por una articulación (brazo y antebrazo, torso y muslo, …) no se comparan: su piel se traslapa alrededor de la articulación en cualquier pose. `diagnostics.html` incrusta el video fuente (requiere `ffmpeg`) y carga three.js desde un CDN, así que su vista 3D necesita conexión a internet. Esa vista dibuja marcas de piso fijas en y = 0: una cruz cada 0.5 m, una más grande cada metro y una cruz verde en el origen, para ver si el personaje se está moviendo. El carril ámbar arriba de las pistas de intersección es para notas hechas a simple vista (arrastra un rango, o **In** / **Out**). La lista **Notes** de la derecha las muestra; haz clic en una fila para ir a ella. **Download notes** guarda esas notas junto con la lista de intersecciones. El archivo se llama como el video fuente y guarda su ruta.

### 7. Dedos (`--detect-hands`)

Un `m2mr run` normal mueve el cuerpo y deja los huesos de los dedos de Mixamo en reposo. `--detect-hands` enciende el modelo de mano que acompaña al extractor del cuerpo. Con el extractor predeterminado, GVHMR, ese modelo es [HaMeR](https://github.com/geopavlakos/hamer). HaMeR recorta las muñecas a partir de la persona y los frames que GVHMR ya eligió. No busca a otra persona en el clip.

**Esto casi duplica el tiempo.** Un clip que termina en unos minutos sin la opción tarda aproximadamente el doble con `--detect-hands`, porque el pase de las manos corre encima de la extracción del cuerpo. En un video largo, toma en cuenta ese tiempo antes de empezar.

Coloca `MANO_RIGHT.pkl` como en la tabla de arriba y luego:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

La primera ejecución con `--detect-hands` descarga los pesos de HaMeR en `weights/hamer/` (~2.7 GB, una vez). Las rotaciones de los dedos se escriben en `skeleton_motion.npz` y mueven los 30 huesos de los dedos de Mixamo del personaje con skin. Una muñeca que el pase del cuerpo no vio con claridad se queda en reposo en esa mano.

`--hand-smooth` es cuántos segundos de suavizado se aplican a esas rotaciones. El valor predeterminado es `0.08`. `0` conserva la estimación en bruto. El suavizado corre siempre que el archivo del esqueleto ya contiene movimiento de manos, incluso en una ejecución posterior que solo reutiliza ese archivo.

Al reutilizar un esqueleto anterior:

- El archivo ya contiene movimiento de manos: `--skeleton` mueve los dedos por sí solo. `--detect-hands` no hace falta otra vez.
- No lo contiene, pero el caché del cuerpo de esa ejecución sigue al lado (`cache/<clip>/0_input_video.mp4`, más `preprocess/vitpose.pt` y `preprocess/bbx.pt`): `--skeleton ... --detect-hands` agrega los dedos sin extraer el cuerpo de nuevo.
- Ese caché ya no está: vuelve a correr el video o la foto con `--detect-hands`.

## Salidas

Cada `m2mr run` crea un directorio con el nombre de **la hora en que inició el comando**. Los archivos de la raíz son iguales para video y foto; solo cambia la carpeta de vistas previas.

```
outputs/20260829_193205_dance/          # o …_pose/ para una foto
├── run.json                            # hora de inicio, entradas, comando completo
├── skeleton_motion.npz                 # esqueleto humano 3D (reutilízalo con --skeleton)
├── mixamo_rotations.npz                # rotaciones de Mixamo por hueso
├── mixamo_character.glb                # personaje con skinning, impórtalo en Blender / Unity
├── diagnostics.json                    # reporte de autointersecciones (ver el paso 6 de Inicio rápido)
├── diagnostics.html                    # solo después de `m2mr diagnose <run> --visualize`
└── videos/   o   images/               # vistas previas — según la entrada
```

Una **entrada de video** escribe `videos/` (con la misma relación de aspecto que el clip):

```
videos/
├── human_skeleton.mp4                  # esqueleto humano 3D reconstruido
├── mixamo_skeleton.mp4                 # esqueleto del rig de Mixamo
├── mixamo_character.mp4                # personaje de Mixamo con skinning
└── compare.mp4                         # 2×2: original (arriba izq.) / esqueleto Mixamo (arriba der.)
                                        #      esqueleto humano (abajo izq.) / personaje (abajo der.)
```

Una **entrada de foto** escribe `images/` en su lugar (las mismas cuatro vistas, más un giro completo):

```
images/
├── human_skeleton.png                  # esqueleto humano 3D reconstruido
├── mixamo_skeleton.png                 # esqueleto del rig de Mixamo
├── mixamo_character.png                # personaje de Mixamo con skinning
├── compare.png                         # 2×2: original (arriba izq.) / esqueleto Mixamo (arriba der.)
│                                       #      esqueleto humano (abajo izq.) / personaje (abajo der.)
└── before_after_360_compare.mp4        # izquierda: foto original
                                        # derecha: órbita del rig en pasos de 10° (una vuelta completa)
```

Con `--detect-hands`, `skeleton_motion.npz` también guarda las rotaciones de los dedos, y `mixamo_rotations.npz` y `mixamo_character.glb` incluyen los 30 huesos de los dedos. Sin esa opción, y sin movimiento de manos ya guardado en un esqueleto reutilizado, esos huesos se quedan en reposo.

Abre `mixamo_character.glb` en Blender: File → Import → glTF 2.0 (.glb/.gltf). Si la cámara apunta a un espacio vacío, selecciona el mesh del personaje y usa View → Frame Selected. El grupo de esferas en la cabeza y las manos es la visualización de los huesos, no el mesh: en el Outliner, oculta **Icosphere** y la **armature**; deja visible el mesh con skinning. Ajusta los FPS de la escena según `run.json` (`fps`) y la timeline a los frames 0 a `n_frames` − 1 para que la reproducción coincida con la fuente y los números de frame con `diagnostics.json`. Compara una ejecución con video contra `videos/mixamo_character.mp4`, y una con foto contra `images/mixamo_character.png` o el clip orbital.

## Licencia

El código de este repositorio es Apache-2.0. Los recursos que descargues tienen sus propios términos y no deben redistribuirse junto con este repositorio:

- **SMPL-X**: acceso controlado por el MPI; por defecto, investigación / educación / arte sin fines comerciales; el uso comercial requiere un acuerdo aparte
- **MANO** (solo si usas `--detect-hands`): acceso controlado por el MPI, el mismo tipo de descarga que SMPL-X; deja `MANO_RIGHT.pkl` en local y no lo redistribuyas
- **Mixamo FBX**: se puede usar en un producto publicado; no redistribuyas el FBX original como paquete de recursos
- **GVHMR y otros pesos de inferencia**: se descargan automáticamente en `weights/` en el primer `m2mr run`, bajo la licencia de cada proyecto original
- **HaMeR**: el código de inferencia de este repositorio es MIT; los pesos se descargan en `weights/hamer/` en el primer `m2mr run --detect-hands`, bajo las condiciones de publicación del proyecto original

## Contacto

Si tienes algún problema, necesitas ayuda para terminar una instalación local o quieres platicar sobre una colaboración, escribe a:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
