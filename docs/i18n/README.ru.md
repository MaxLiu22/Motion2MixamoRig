# Motion2MixamoRig

<p align="center">
  <a href="#требования"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.ru.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · Русский · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Переносит движение человека из видео — или позу с фото — на 3D-персонажа с ригом Adobe Mixamo.

Для разработчиков игр: видео с **одним человеком** (или фото) и персонаж Mixamo; на выходе превью и файл персонажа со скином (`.glb`) для Blender или Unity.

> Motion2MixamoRig пока экспериментален. Версия 0.1.8 — конвейер командной строки. В этом репозитории также есть расширение Blender 4.2+, которое запускает тот же конвейер во внешнем Python. Сборка аддона из исходников: [`blender_extension/README.md`](../../blender_extension/README.md).

## Два способа использования

### 🎨 В Blender — без программирования

1. Скачайте zip для своей платформы, например `motion2mixamorig-<version>-macos-arm64.zip`, из [последнего релиза](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. В Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, выберите zip.
3. 3D Viewport → нажмите **N** → вкладка **Motion2MixamoRig** → **Установить среду (в один клик)** (Install Runtime (one click)).
4. **Выбрать модель SMPL-X…** (Choose SMPL-X Model…) (бесплатная загрузка) и выберите FBX персонажа Mixamo.
5. Выберите видео с одним человеком → **Сгенерировать движение** (Generate Motion).

Пошаговые инструкции, советы и обновление: **[Руководство пользователя](user-guide.ru.md)**. Проверено на macOS (Apple Silicon).

### 💻 Командная строка — для разработчиков

Клонируйте репозиторий и запускайте конвейер сами: начните с раздела [Требования](#требования).

Агентам следует начать с [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Откройте <a href="../assets/demo.mp4">demo.mp4</a> в этом репозитории.</sub>
</p>

Ещё одно демо:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Отчёт диагностики (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Требования

Python 3.11+. После клонирования создайте виртуальное окружение и установите зависимости; команда `m2mr` станет доступна:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Установка зависимостей и этого проекта. chumpy (старый пакет в цепочке
# зависимостей) импортирует pip в setup-скрипте; в изолированной сборке pip
# это падает с "No module named 'pip'". Сначала поставьте его с
# --no-build-isolation, затем этот проект.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Веса инференса (GVHMR и т.д.) здесь не скачиваются. Первый `m2mr run` тянет их в `weights/` (~5 ГБ, один раз). Первый `m2mr run --detect-hands` также тянет веса кистей HaMeR в `weights/hamer/` (~2,7 ГБ, один раз).

Рекомендуется ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Без него пайплайн работает, но выходные видео будут **без звука** и не откроются в браузере.

## Перед запуском: положите это в `assets/`

Репозиторий эти файлы не содержит — их нужно получить самостоятельно. Имя файла SMPL-X должно совпадать с таблицей буква в букву; имена FBX, видео и фото любые. Для запуска нужны SMPL-X, персонаж Mixamo и **либо** видео, **либо** фото. Персонажи Mixamo, повторно экспортированные из Cinema 4D, тоже поддерживаются; подробнее: [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Что | Куда | Откуда |
|---|---|---|
| Модель тела SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Зарегистрироваться на [SMPL-X](https://smpl-x.is.tue.mpg.de/) и скачать |
| FBX-персонаж Mixamo | `assets/mixamo/Y_Bot.fbx` | С Adobe-аккаунтом скачать Y Bot (или другого персонажа с ригом Mixamo) с [Mixamo](https://www.mixamo.com) |
| Видео с действием | `assets/video/<your_clip>.mp4` | Ролик с **ровно одним** хорошо видимым человеком, **с головы до ног весь ролик в кадре** (можно несколько файлов; каждый запуск берёт последний добавленный) |
| Фото позы (необязательно) | `assets/image/<your_photo>.jpg` | Фото с **ровно одним** хорошо видимым человеком, **с головы до ног в кадре**. Вместе с `--image` |
| Правая кисть MANO (только для `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Зарегистрируйтесь на [MANO](https://mano.is.tue.mpg.de/) и скачайте **Models & Code**. Для прогона только тела этот файл не нужен |

Замечание: скачанный файл Mixamo называется `Y Bot.fbx` (**пробел**), на один символ отличается от `Y_Bot.fbx` (**подчёркивание**) в таблице.
Переименуйте с подчёркиванием — это станет ригом по умолчанию (`m2mr run` без `--rig`). Можно не переименовывать: если `Y_Bot.fbx` нет, берётся первый `.fbx` в `assets/mixamo/`.

В `assets/video/` можно класть несколько видео. Без `--video` или `--image` запуск берёт файл, **последним положенный в `assets/video/`**; если папка пуста — последнее фото в `assets/image/`.
В каждом ролике или фото должен быть один человек, **с головы до ног в кадре** — ничего не обрезано по краям. `m2mr doctor` / `m2mr run` останавливаются до извлечения, если в кадре двое.

## Быстрый старт

Результаты в `outputs/<время-запуска>_<источник>/`. Видео-запуск пишет в `videos/`; фото-запуск — в `images/`.

### 1. Проверить ассеты и окружение

Чего не хватает — печатается вместе с тем, откуда скачать и куда положить.

```bash
m2mr doctor
```

`m2mr doctor` проверяет прогон тела. Модель кисти MANO он не требует. Чтобы проверить ещё файл и пакеты Python для распознавания пальцев:

```bash
m2mr doctor --detect-hands
```

### 2. Первый запуск: чтобы что-то появилось на экране

Без флагов: **последний файл в `assets/video/`** и `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Это медленный шаг. Первый запуск скачивает ~5 ГБ весов инференса (один раз), затем извлекает движение человека из видео.
На CPU клип ~30 секунд извлекается примерно 8–15 минут; повторные прогоны той же длины с уже скачанными весами — около 3–5 минут.
Ретаргетинг и рендеринг обычно минута–две. Повторное использование скелета через `--skeleton` в следующем разделе полностью пропускает извлечение и заканчивается за десятки секунд.

Опирающаяся стопа по умолчанию фиксируется: подушечка, когда подушечка на земле, пятка только когда пальцы подняты. Если выпрямленная нога не достаёт, таз сдвигается. Затем подошва ставится на пол (y = 0). `--no-foot-lock` оставляет сырой ретаргет, поэтому стопы могут скользить; подошва всё равно ставится на пол.

### 3. То же движение, другой персонаж

Скачайте другого персонажа с Mixamo в `assets/mixamo/`. **Не перезапускайте только с `--rig`** — медленное извлечение повторится.
`--skeleton` берёт скелет предыдущего запуска; минуты превращаются в десятки секунд:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Другое видео

`--video` выбирает клип. Свободно сочетается с `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Фото (статическая поза)

`--image` восстанавливает **статическую 3D-позу** с фото одного человека и переносит её на персонажа Mixamo так же, как видео-запуск. Превью — четыре кадра в `images/` (те же виды, что у видео) плюс клип орбиты слева/справа `before_after_360_compare.mp4`. Не сочетать с `--video`.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` без пути берёт файл, последним положенный в `assets/image/`.

### 6. Проверка самопересечений

Каждый запуск также проверяет готового персонажа на **самопересечения** — когда одна часть тела входит в другую, например рука в голову, — и записывает `diagnostics.json`. В терминал выводится одна строка, например `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Пол не проверяется.

Чтобы перепроверить запуск или посмотреть на проблемы:

```bash
m2mr diagnose outputs/<run>                  # перезаписать diagnostics.json
m2mr diagnose outputs/<run> --visualize      # плюс diagnostics.html: исходное видео рядом с персонажем, таймлайн, кликабельный список проблем
m2mr diagnose outputs/<run> --threshold-cm 2 # сообщать только о проникновениях глубже 2 см (по умолчанию 1)
```

Каждая проблема в `diagnostics.json` — это пара частей тела с диапазонами кадров, где они пересекаются, худшим кадром и его глубиной. Кадры нумеруются с 0, как на таймлайне Blender после импорта glTF. Части, соединённые суставом (плечо и предплечье, торс и бедро, …), не сравниваются: их кожа у сустава перекрывается в любой позе. `diagnostics.html` встраивает исходное видео (нужен `ffmpeg`) и загружает three.js с CDN, поэтому для 3D-вида нужен интернет. Этот вид рисует неподвижные метки на полу на y = 0: крест каждые 0,5 м, более крупный каждый метр и зелёный крест в начале координат, чтобы было видно, движется ли персонаж. Янтарная дорожка над дорожками пересечений — для заметок, которые видны только глазом (протяните диапазон или **In** / **Out**). Список **Notes** справа их показывает; щелчок по строке переходит к ней. **Download notes** сохраняет эти заметки вместе со списком пересечений. Файл называется как исходное видео и содержит его путь.

### 7. Пальцы (`--detect-hands`)

Обычный `m2mr run` двигает тело и оставляет кости пальцев Mixamo в покое. `--detect-hands` включает модель кисти, которая идёт вместе с экстрактором тела. У экстрактора по умолчанию, GVHMR, это [HaMeR](https://github.com/geopavlakos/hamer). HaMeR вырезает запястья у человека и кадров, которые GVHMR уже выбрал. Второй человек в клипе не ищется.

**Время увеличивается примерно вдвое.** Клип, который без флага заканчивается за несколько минут, с `--detect-hands` занимает примерно вдвое больше: проход кистей идёт поверх извлечения тела. На длинном видео заложите это время до запуска.

Положите `MANO_RIGHT.pkl`, как в таблице выше, затем:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Первый запуск с `--detect-hands` скачивает веса HaMeR в `weights/hamer/` (~2,7 ГБ, один раз). Вращения пальцев пишутся в `skeleton_motion.npz` и двигают 30 костей пальцев Mixamo на скиненном персонаже. Запястье, которое проход тела видел неясно, остаётся в покое для этой кисти.

`--hand-smooth` — сколько секунд сглаживания применить к этим вращениям. По умолчанию `0.08`. `0` оставляет сырую оценку. Сглаживание выполняется, когда в файле скелета уже есть движение кистей, в том числе при позднем запуске, который только переиспользует этот файл.

Повторное использование прежнего скелета:

- В файле уже есть движение кистей: `--skeleton` сам двигает пальцы. `--detect-hands` снова не нужен.
- Движения нет, но кэш тела этого прогона ещё рядом (`cache/<clip>/0_input_video.mp4`, плюс `preprocess/vitpose.pt` и `preprocess/bbx.pt`): `--skeleton ... --detect-hands` добавляет пальцы без повторного извлечения тела.
- Этого кэша нет: запустите видео или фото ещё раз с `--detect-hands`.

## Результаты

Каждый `m2mr run` создаёт каталог по **времени старта команды**. Файлы в корне одинаковы для видео и фото; меняется только папка превью.

```
outputs/20260829_193205_dance/          # для фото: …_pose/
├── run.json                            # время старта, входы, полная команда
├── skeleton_motion.npz                 # 3D-скелет человека (повторно с --skeleton)
├── mixamo_rotations.npz                # вращения костей Mixamo
├── mixamo_character.glb                # персонаж со скином, импорт в Blender / Unity
├── diagnostics.json                    # отчёт о самопересечениях (см. шаг 6 «Быстрого старта»)
├── diagnostics.html                    # только после `m2mr diagnose <run> --visualize`
└── videos/   или   images/             # превью — зависит от входа
```

**Видео-вход** пишет в `videos/` (то же соотношение сторон, что у клипа):

```
videos/
├── human_skeleton.mp4                  # восстановленный 3D-скелет человека
├── mixamo_skeleton.mp4                 # скелет рига Mixamo
├── mixamo_character.mp4                # персонаж Mixamo со скином
└── compare.mp4                         # 2×2: оригинал (верхний левый) / скелет Mixamo (верхний правый)
                                        #      скелет человека (нижний левый) / персонаж (нижний правый)
```

**Фото-вход** пишет в `images/` (те же четыре вида плюс орбита):

```
images/
├── human_skeleton.png                  # восстановленный 3D-скелет человека
├── mixamo_skeleton.png                 # скелет рига Mixamo
├── mixamo_character.png                # персонаж Mixamo со скином
├── compare.png                         # 2×2: оригинал (верхний левый) / скелет Mixamo (верхний правый)
│                                       #      скелет человека (нижний левый) / персонаж (нижний правый)
└── before_after_360_compare.mp4        # слева: исходное фото
                                        # справа: орбита 10° вокруг рига (полный оборот)
```

С `--detect-hands` в `skeleton_motion.npz` также записываются вращения пальцев, а `mixamo_rotations.npz` и `mixamo_character.glb` включают 30 костей пальцев. Без этого флага и без уже сохранённого движения кистей в повторно используемом скелете эти кости остаются в покое.

`mixamo_character.glb` в Blender: File → Import → glTF 2.0 (.glb/.gltf). Если камера смотрит в пустоту, выберите меш персонажа и View → Frame Selected. Скопление сфер на голове и руках — отображение костей, не меш: в Outliner спрячьте **Icosphere** и **armature**, оставьте видимым меш со скином. FPS сцены возьмите из `run.json` (`fps`), а таймлайн задайте с кадра 0 по `n_frames` − 1, чтобы длительность совпала с исходником, а номера кадров — с `diagnostics.json`. Видео-запуск сверяйте с `videos/mixamo_character.mp4`, фото-запуск — с `images/mixamo_character.png` или клипом орбиты.

## Лицензия

Код репозитория — Apache-2.0. Скачанные вами ассеты имеют свои условия и не должны распространяться вместе с этим репо:

- **SMPL-X**: доступ через MPI; по умолчанию некоммерческие исследования / образование / искусство; коммерческое использование — отдельный договор
- **MANO** (только с `--detect-hands`): доступ через MPI, тот же способ загрузки, что у SMPL-X; положите `MANO_RIGHT.pkl` локально и не распространяйте его
- **Mixamo FBX**: можно в готовом продукте; сырой FBX нельзя раздавать как пак ассетов
- **GVHMR и другие веса инференса**: при первом `m2mr run` автоматически в `weights/`, по лицензии каждого апстрима
- **HaMeR**: код инференса в этом репозитории — MIT; веса скачиваются в `weights/hamer/` при первом `m2mr run --detect-hands`, на условиях публикации апстрима

## Контакты

Если возникла проблема, нужна помощь с локальной установкой или вы хотите обсудить сотрудничество, напишите на:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
