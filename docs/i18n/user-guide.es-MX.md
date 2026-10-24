# Motion2MixamoRig para Blender — Guía de usuario

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · Español · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

Convierte un video de una persona en un personaje de Mixamo animado, dentro de Blender.
No necesitas programar ni usar la terminal.

<!-- video: link the tutorial video here -->

> Por ahora solo se ha probado en **macOS (Apple Silicon)**. La versión para Windows está por llegar.

## Qué necesitas

- **Blender 4.2 o más reciente**
- **Conexión a internet** para la primera configuración
- **Unos 8 GB de espacio libre en disco** (entorno ~1.3 GB + modelos ~5.6 GB)
- **Una cuenta gratuita de SMPL-X** y **una cuenta gratuita de Adobe** (para Mixamo); consulta los pasos 4 y 5

## 1. Descarga el complemento

Ve al [release más reciente](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
y descarga el zip para tu computadora:

| Tu computadora | Archivo |
| --- | --- |
| Mac con Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **Próximamente** |

Por ejemplo, en `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` es la versión
del complemento y `macos-arm64` la plataforma. Si eliges el equivocado, Blender
se niega a instalarlo y te dice qué plataforma esperaba.

**No** lo descomprimas. Blender instala el zip directamente.

## 2. Instálalo en Blender

1. **Edit → Preferences → Get Extensions**
2. Haz clic en la pequeña **∨** arriba a la derecha → **Install from Disk…**
3. Elige el zip. **Motion2MixamoRig** aparece en la lista, ya activado.
4. Cierra Preferences. En el 3D Viewport presiona **N** y luego haz clic en la
   pestaña **Motion2MixamoRig** a la derecha.

<!-- screenshot: Install from Disk menu -->

## 3. Instala el entorno (una sola vez)

En el panel, haz clic en **Instalar entorno (un clic)** (Install Runtime (one click)).

El complemento descarga su propio Python y sus bibliotecas (~1.4 GB) en
`~/Motion2MixamoRig/`. No toca nada más en tu computadora. Esto tarda unos
minutos; la barra de progreso muestra el paso actual.

<!-- screenshot: Install Runtime button and progress -->

## 4. Consigue el modelo corporal SMPL-X

SMPL-X es un modelo corporal gratuito que el complemento necesita. Su licencia no
nos permite distribuirlo, así que lo descargas tú mismo, una sola vez:

1. Abre [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) y haz clic en **Register**.
   Acepta la licencia y confirma el correo.
2. Inicia sesión, abre **Download** y descarga el modelo SMPL-X (la versión
   **NPZ**).
3. Descomprímelo y busca **`SMPLX_NEUTRAL.npz`**.
4. En Blender, haz clic en **Elegir modelo SMPL-X…** (Choose SMPL-X Model…) y
   selecciona ese archivo. El panel mostrará entonces **Modelo SMPL-X: encontrado**
   (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. Consigue un personaje de Mixamo

1. Abre [mixamo.com](https://www.mixamo.com/) e inicia sesión con una cuenta de Adobe.
2. Pestaña **Characters** → elige un personaje (por ejemplo **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. Genera el movimiento

En la sección **Entrada** (Input):

1. **Tipo de origen** (Source Type): **Video** (o **Imagen** (Image) para una sola pose)
2. **Archivo de origen** (Source File): tu clip. Debe mostrar **exactamente a una
   persona, de la cabeza a los pies dentro del cuadro todo el tiempo**.
3. **FBX del rig de Mixamo** (Mixamo Rig FBX): el personaje del paso 5
4. **Detectar manos** (Detect Hands) está apagado. Enciéndelo solo si quieres que
   se muevan los dedos. Luego haz clic en **Elegir modelo de mano MANO…**
   (Choose MANO Hand Model…) y elige `MANO_RIGHT.pkl`. Consigue ese archivo igual
   que SMPL-X: regístrate en
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/), descarga **Models & Code**
   y descomprímelo. La primera pasada de las manos descarga unos **2.7 GB** más,
   una sola vez, y tarda aproximadamente el doble que una pasada solo del cuerpo. Al activarlo aparece **Finger Smoothing (seconds)**. Suaviza el movimiento de los dedos. El valor predeterminado es 0.08 segundos; 0 deja lo detectado tal cual.
5. Haz clic en **Generar movimiento** (Generate Motion)

Cuando termina, el personaje animado se importa a tu escena
automáticamente. Un pie apoyado se queda donde cayó, y la planta queda sobre el piso de Blender. En ese piso se agrega un mesh **Marcas en el piso** (Floor Markers) (una cruz cada 0.5 m). La casilla **Marcas en el piso** (Floor Markers) en Progreso / Resultado lo muestra o lo oculta.

### La primera ejecución tarda más — es normal

La primera vez, el complemento descarga unos **5.6 GB** de modelos. El panel
muestra el tamaño de la descarga, la velocidad y el tiempo restante. Los modelos
se descargan una sola vez.

Después, el video se procesa en tu computadora. En el CPU de una Mac, un clip de
10 segundos tarda unos minutos. Puedes seguir usando Blender mientras se ejecuta,
y **Cancelar** (Cancel) detiene el trabajo.

## Consejos para obtener buenos resultados

- Una sola persona, con el cuerpo completo visible y sin cortes en los bordes
- Cámara estable, buena iluminación y ropa sencilla en lugar de prendas sueltas o vaporosas
- Los clips cortos (5–20 segundos) son más rápidos para probar al principio

## Actualizar a una nueva versión

El complemento se actualiza seguido. Para actualizar:

1. Descarga el zip más nuevo del
   [release más reciente](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → quita el **Motion2MixamoRig** anterior, cierra Blender
   por completo (**Cmd+Q**), vuelve a abrirlo e instala el zip nuevo.
3. En el panel, haz clic en **Actualizar entorno** (Update Runtime).

Al actualizar se conservan los modelos descargados, así que es rápido. La versión
instalada aparece junto al complemento en **Get Extensions**.

## El panel

- **⚙ junto al título** muestra u oculta la sección **Configuración** (Setup).
- **Configuración**: idioma, entorno, SMPL-X, dispositivo (**Dispositivo** (Device);
  CPU es la opción segura) y **Revisar entorno** (Check Environment).
- **Entrada**: qué animar, el **Modelo del cuerpo** (Body Model, GVHMR) y **Detectar manos** (Detect Hands).
- **Progreso / Resultado** (Progress / Result): progreso, registro reciente y, al
  terminar un trabajo, **Importar personaje generado** (Import Generated Character), **Marcas en el piso** (Floor Markers),
  **Abrir carpeta de salida** (Open Output Folder) y **Ver registro completo** (View Full Log).
- **Diagnóstico** (Diagnostics): dónde las partes del cuerpo del personaje se
  meten unas en otras (una mano dentro de la cabeza, brazos cruzados). Las
  celdas rojas de la barra son frames con un problema; haz clic en una para ir
  ahí. El triángulo bajo la barra sigue el frame actual, y debajo aparecen las
  partes que se intersectan y qué tan profundo. **Anterior** / **Siguiente**
  (Previous / Next) saltan entre problemas. **Abrir reporte HTML** (Open HTML
  Report) abre en el navegador un reporte con el video fuente junto al
  personaje (la primera vez tarda unos 15 segundos en generarse). El video original necesita ffmpeg en la computadora (en Mac: `brew install ffmpeg`). Sin él, el personaje está ahí y el video de al lado queda en blanco. El personaje está sobre cruces de piso fijas, una cada 0.5 m, para ver si se está deslizando. El carril ámbar arriba de las pistas rojas es para notas que haces a simple vista. Aparecen a la derecha en **Notes**; haz clic en una para ir a ella. **Download notes** guarda esas notas junto con los tiempos de intersección. El archivo se llama como el video fuente.

El complemento está disponible en 19 idiomas. **Automático (Blender / Sistema)**
(Auto (Blender / System)) sigue el idioma de Blender; cámbialo en la sección
Configuración, en **Idioma de la interfaz** (UI Language).

## Si algo sale mal

| Lo que ves | Qué hacer |
| --- | --- |
| **Falló la instalación del entorno** (Runtime installation failed) | Revisa tu conexión a internet y vuelve a hacer clic en el botón. Registro: `~/Motion2MixamoRig/logs/setup.log` |
| **Modelo SMPL-X: falta** (SMPL-X model: missing) | Repite el paso 4 y selecciona `SMPLX_NEUTRAL.npz` |
| **Modelo de mano MANO: falta** (MANO hand model: missing) | Activa **Detectar manos**, luego **Elegir modelo de mano MANO…** y elige `MANO_RIGHT.pkl` |
| **El FBX de Mixamo no es válido** (Mixamo FBX invalid) | Vuelve a descargar el personaje como **FBX Binary**, **T-pose** |
| **La entrada tiene varias personas** (Input contains multiple people) | Usa un clip con una sola persona |
| **No se detectó ninguna persona en la entrada** (No person was detected in the input) | Asegúrate de que todo el cuerpo se vea y esté bien iluminado |
| **El proceso del pipeline terminó de forma inesperada** (Pipeline process exited unexpectedly) | Haz clic en **Ver registro completo** |

Cuando pidas ayuda, adjunta el registro e indica qué versión del complemento usas.

## Desinstalar

1. **Get Extensions** → quita **Motion2MixamoRig**.
2. Borra la carpeta **`~/Motion2MixamoRig`** (tu carpeta personal →
   `Motion2MixamoRig`). Quitar el complemento **no** la borra, y ocupa unos
   7 GB de entorno y modelos, además de tus resultados generados en
   `app/outputs/`.

## Licencia

Motion2MixamoRig es **solo para uso no comercial**: depende de modelos de
investigación (como GVHMR y SMPL-X) cuyas licencias no permiten el uso comercial.
Consulta [`NOTICE.md`](../../NOTICE.md).
