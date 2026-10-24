# Motion2MixamoRig

<p align="center">
  <a href="#передумови"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.uk.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · Українська · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

Перенесіть рух людини з відео — або позу зі світлини — на 3D-персонажа з ригом Adobe Mixamo.

Для розробників ігор: дайте відео дії з **однією людиною** (або світлину) і персонажа Mixamo; програма запише відео попереднього перегляду і файл персонажа зі скінінгом (`.glb`), який можна перетягнути в Blender або Unity.

> Motion2MixamoRig наразі експериментальний. Версія 0.1.8 — це конвеєр командного рядка. У цьому репозиторії також є розширення для Blender 4.2+, яке запускає той самий конвеєр у зовнішньому середовищі Python. Збирання додатка з джерельного коду: [`blender_extension/README.md`](../../blender_extension/README.md).

## Два способи користування

### 🎨 У Blender — без програмування

1. Завантажте zip для своєї платформи, наприклад `motion2mixamorig-<version>-macos-arm64.zip`, з [останнього випуску](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. У Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, виберіть zip.
3. 3D Viewport → натисніть **N** → вкладка **Motion2MixamoRig** → **Встановити середовище (один клік)** (Install Runtime (one click)).
4. **Вибрати модель SMPL-X…** (Choose SMPL-X Model…) (безкоштовне завантаження) і виберіть FBX персонажа Mixamo.
5. Виберіть відео з однією людиною → **Згенерувати рух** (Generate Motion).

Покрокові інструкції, поради й оновлення: **[Посібник користувача](user-guide.uk.md)**. Перевірено на macOS (Apple Silicon).

### 💻 Командний рядок — для розробників

Клонуйте репозиторій і запустіть конвеєр самостійно: почніть із [Передумов](#передумови).

Агентам слід почати з [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>Відкрийте <a href="../assets/demo.mp4">demo.mp4</a> у цьому репозиторії.</sub>
</p>

Ще одна демонстрація:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

Звіт діагностики (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## Передумови

Python 3.11+. Після клонування створіть virtualenv і встановіть залежності; після цього доступна команда `m2mr`:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# Встановіть залежності і цей проєкт. chumpy (застарілий пакунок у
# ланцюжку залежностей) імпортує pip у скрипті встановлення, і це падає з
# "No module named 'pip'" за типового ізольованого збирання pip. Спершу
# встановіть його без ізоляції, а потім цей проєкт.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Ваги для інференсу тут не завантажуються. Перший `m2mr run` завантажує ваги GVHMR у `weights/` (~5 ГБ, один раз). Перший `m2mr run --detect-hands` також завантажує ваги руки HaMeR у `weights/hamer/` (~2,7 ГБ, один раз).

Рекомендовано ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
Конвеєр працює і без нього, але вихідні відео будуть **без звуку** і не відтворяться в браузері.

## Перед запуском: покладіть ці файли в `assets/`

Цей репозиторій їх не містить; їх треба отримати самостійно. Ім’я файлу SMPL-X має точно збігатися з таблицею; імена FBX, відео та зображень можуть бути будь-якими. Для запуску потрібні SMPL-X, персонаж Mixamo і **або** відео, **або** світлина. Персонажі Mixamo, повторно експортовані з Cinema 4D, теж підходять; див. [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| Що | Куди | Де взяти |
|---|---|---|
| Модель тіла SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | Зареєструйтеся на [SMPL-X](https://smpl-x.is.tue.mpg.de/) і завантажте |
| FBX персонажа Mixamo | `assets/mixamo/Y_Bot.fbx` | З обліковим записом Adobe завантажте Y Bot (або іншого персонажа з ригом Mixamo) з [Mixamo](https://www.mixamo.com) |
| Відео дії | `assets/video/<your_clip>.mp4` | Кліп з **рівно однією** добре видимою людиною, **від голови до п’ят у кадрі весь час** (файлів може бути кілька; кожен запуск бере останній доданий) |
| Світлина пози (необов’язково) | `assets/image/<your_photo>.jpg` | Світлина з **рівно однією** добре видимою людиною, **від голови до п’ят у кадрі**. Використовуйте з `--image` |
| Права рука MANO (лише для `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | Зареєструйтеся на [MANO](https://mano.is.tue.mpg.de/) і завантажте **Models & Code**. Запуск лише тіла цей файл не потребує |

Примітка: файл із Mixamo називається `Y Bot.fbx` (**пробіл**), на один символ інакше, ніж `Y_Bot.fbx` (**підкреслення**) у таблиці.
Перейменуйте його з підкресленням — і це стане типовим ригом (`m2mr run` без `--rig`). Пробіл теж можна лишити: якщо `Y_Bot.fbx` немає, береться перший `.fbx` у `assets/mixamo/`.

У `assets/video/` може бути кілька відео. Без `--video` і без `--image` запуск бере файл, **доданий останнім** до `assets/video/`; якщо тека порожня, береться остання світлина в `assets/image/`.
Кожен кліп або світлина має показувати лише одну людину, **від голови до п’ят у кадрі**, без обрізання по краях. `m2mr doctor` / `m2mr run` зупиняються до видобування, якщо в кадрі двоє людей.

## Швидкий старт

Результати потрапляють у `outputs/<run-time>_<source>/`. Запуски з відео пишуть `videos/`; запуски зі світлини пишуть `images/`.

### 1. Перевірте ресурси й середовище

Усе, чого бракує, друкується разом із тим, звідки завантажити і куди покласти.

```bash
m2mr doctor
```

`m2mr doctor` перевіряє запуск тіла. Модель руки MANO не потрібна. Щоб перевірити також додатковий файл і пакунки Python для виявлення пальців:

```bash
m2mr doctor --detect-hands
```

### 2. Перший запуск: побачити результат на екрані

Без параметрів використовується **останній файл у `assets/video/`** і `assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

Це повільний крок. Перший запуск завантажує ~5 ГБ ваг для інференсу (один раз), потім видобуває рух людини з відео.
На CPU кліп близько 30 секунд видобувається приблизно 8–15 хвилин; наступні запуски подібної тривалості, коли ваги вже є, тривають близько 3–5 хвилин.
Ретаргет і рендер зазвичай займають хвилину-дві. Повторне використання скелета з `--skeleton` у наступному розділі повністю пропускає видобування і завершується за кілька десятків секунд.

Поставлена стопа фіксується типово: подушечка, коли подушечка на підлозі, п’ята лише коли пальці підняті. Якщо випрямлена нога не дістає до цієї точки, стегна зсуваються. Потім підошва ставиться на підлогу (y = 0). `--no-foot-lock` лишає сирий ретаргет, тож стопи можуть ковзати; підошва все одно ставиться на підлогу.

### 3. Той самий рух, інший персонаж

Завантажте іншого персонажа з Mixamo в `assets/mixamo/`. **Не запускайте знову, змінивши лише `--rig`**: це повторить повільне видобування.
Передайте `--skeleton`, щоб використати скелет попереднього запуску; хвилини стають десятками секунд:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. Інше відео

`--video` вибирає кліп. Вільно поєднується з `--rig`.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. Світлина (статична поза)

`--image` відновлює **статичну 3D-позу** зі світлини однієї людини, а потім переносить її на персонажа Mixamo так само, як запуск із відео. Попередні перегляди — чотири зображення в `images/` (ті самі ракурси, що й для відео), плюс кліп орбіти ліворуч/праворуч `before_after_360_compare.mp4`. Не передавайте `--video` одночасно.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` без шляху бере файл, доданий останнім до `assets/image/`.

### 6. Перевірте самоперетини

Кожен запуск також перевіряє готового персонажа на **самоперетин** — одна частина тіла входить в іншу, наприклад рука всередині голови — і записує `diagnostics.json`. Термінал друкує один рядок, наприклад `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. Підлога не перевіряється.

Щоб перевірити запуск знову або побачити проблеми:

```bash
m2mr diagnose outputs/<run>                  # перезаписати diagnostics.json
m2mr diagnose outputs/<run> --visualize      # також diagnostics.html: вихідне відео поруч із персонажем, шкала часу, список проблем, на який можна натиснути
m2mr diagnose outputs/<run> --threshold-cm 2 # повідомляти лише проникнення глибші за 2 см (типово 1)
```

Кожна проблема в `diagnostics.json` — це пара частин тіла з діапазонами кадрів, де вони перетинаються, найгіршим кадром і його глибиною. Номери кадрів рахуються від 0, як шкала часу Blender після імпорту glTF. Частини, з’єднані суглобом (плече і передпліччя, тулуб і стегно, …), не порівнюються: їхня шкіра перекривається навколо суглоба в будь-якій позі. `diagnostics.html` вбудовує вихідне відео (потрібен `ffmpeg`) і завантажує three.js з CDN, тож 3D-вигляд потребує інтернету. У цьому вигляді на y = 0 лишаються фіксовані позначки підлоги — хрест кожні 0,5 м, більший щометра й зелений хрест у початку координат — щоб оцінити, чи персонаж рухається. Бурштинова смуга над доріжками перетинів призначена для нотаток на око (протягніть діапазон або In / Out). Список **Notes** праворуч їх показує; клік по рядку переходить до нього. **Download notes** зберігає ці нотатки разом зі списком перетинів. Файл називається за вихідним відео і записує шлях до нього.

### 7. Пальці (`--detect-hands`)

Звичайний `m2mr run` рухає тіло і лишає кістки пальців Mixamo в спокої. `--detect-hands` вмикає модель руки, яка йде разом із видобувачем тіла. Для типового видобувача, GVHMR, ця модель — [HaMeR](https://github.com/geopavlakos/hamer). HaMeR вирізає зап’ястя з людини і з кадрів, які GVHMR уже обрав. Другу людину в кліпі він не шукає.

**Час приблизно подвоюється.** Кліп, який без прапорця завершується за кілька хвилин, з `--detect-hands` триває приблизно вдвічі довше, бо прохід рук додається до видобування тіла. На довгому відео закладіть цей додатковий час до старту.

Покладіть `MANO_RIGHT.pkl`, як у таблиці вище, а потім:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

Перший запуск із `--detect-hands` завантажує ваги HaMeR у `weights/hamer/` (~2,7 ГБ, один раз). Обертання пальців записуються в `skeleton_motion.npz` і керують 30 кістками пальців Mixamo на персонажі зі скіном. Зап’ястя, яке прохід тіла побачив нечітко, лишається в спокої для тієї руки.

`--hand-smooth` — це скільки секунд згладжування застосувати до цих обертань. Типове значення — `0.08`. `0` лишає сиру оцінку. Згладжування виконується щоразу, коли файл скелета вже містить рух рук, зокрема під час пізнішого запуску, який лише повторно використовує цей файл.

Повторне використання попереднього скелета:

- Файл уже містить рух рук: `--skeleton` сам керує пальцями. `--detect-hands` знову не потрібен.
- Не містить, але кеш тіла того запуску ще лежить поруч (`cache/<clip>/0_input_video.mp4`, а також `preprocess/vitpose.pt` і `preprocess/bbx.pt`): `--skeleton ... --detect-hands` додає пальці без повторного видобування тіла.
- Того кешу вже немає: запустіть відео або світлину знову з `--detect-hands`.

## Результати

Кожен `m2mr run` створює теку, названу **часом початку команди**. Файли в корені однакові для відео і світлини; змінюється лише тека попереднього перегляду.

```
outputs/20260829_193205_dance/          # або …_pose/ для світлини
├── run.json                            # час початку, вхідні дані, повна команда
├── skeleton_motion.npz                 # 3D-скелет людини (повторне використання з --skeleton)
├── mixamo_rotations.npz                # обертання Mixamo для кожної кістки
├── mixamo_character.glb                # персонаж зі скіном, імпорт у Blender / Unity
├── diagnostics.json                    # звіт про самоперетини (див. крок 6 швидкого старту)
├── diagnostics.html                    # лише після `m2mr diagnose <run> --visualize`
└── videos/   або   images/             # попередній перегляд — залежить від вхідних даних
```

**Вхідне відео** записує `videos/` (те саме співвідношення сторін, що й у кліпу):

```
videos/
├── human_skeleton.mp4                  # відновлений 3D-скелет людини
├── mixamo_skeleton.mp4                 # скелет рига Mixamo
├── mixamo_character.mp4                # персонаж Mixamo зі скіном
└── compare.mp4                         # 2×2: оригінал (верх ліворуч) / скелет Mixamo (верх праворуч)
                                        #      скелет людини (низ ліворуч) / персонаж (низ праворуч)
```

**Вхідна світлина** натомість записує `images/` (ті самі чотири ракурси плюс обертання):

```
images/
├── human_skeleton.png                  # відновлений 3D-скелет людини
├── mixamo_skeleton.png                 # скелет рига Mixamo
├── mixamo_character.png                # персонаж Mixamo зі скіном
├── compare.png                         # 2×2: оригінал (верх ліворуч) / скелет Mixamo (верх праворуч)
│                                       #      скелет людини (низ ліворуч) / персонаж (низ праворуч)
└── before_after_360_compare.mp4        # ліворуч: вихідна світлина
                                        # праворуч: орбіта рига по 10° (повний оберт)
```

З `--detect-hands` файл `skeleton_motion.npz` також зберігає обертання пальців, а `mixamo_rotations.npz` / `mixamo_character.glb` містять 30 кісток пальців. Без цього прапорця і без уже збереженого руху рук у повторно використаному скелеті ці кістки лишаються в спокої.

Відкрийте `mixamo_character.glb` у Blender: File → Import → glTF 2.0 (.glb/.gltf). Якщо камера дивиться в порожнечу, виберіть сітку персонажа і скористайтеся View → Frame Selected. Скупчення сфер на голові й руках — це показ кісток, а не сітка: в Outliner сховайте **Icosphere** і **armature**; лишіть видимою сітку зі скіном. Задайте FPS сцени з `run.json` (`fps`), а шкалу часу — на кадри від 0 до `n_frames` − 1, щоб відтворення збігалося з джерелом, а номери кадрів — із `diagnostics.json`. Запуск із відео порівняйте з `videos/mixamo_character.mp4`, запуск зі світлини — з `images/mixamo_character.png` або з кліпом орбіти.

## Ліцензія

Код цього репозиторію — Apache-2.0. Ресурси, які ви завантажуєте, мають власні умови і не мають поширюватися разом із цим репозиторієм:

- **SMPL-X**: доступ через MPI; типово лише некомерційні дослідження / освіта / мистецтво; комерційне використання потребує окремої угоди
- **MANO** (лише якщо ви користуєтеся `--detect-hands`): доступ через MPI, той самий тип завантаження, що й SMPL-X; покладіть `MANO_RIGHT.pkl` локально і не поширюйте його
- **FBX Mixamo**: можна включати в готовий продукт; не поширюйте сирий FBX як пакунок ресурсів
- **Ваги GVHMR**: автоматично завантажуються в `weights/` під час першого `m2mr run`, за ліцензією першоджерела
- **HaMeR**: код інференсу в цьому репозиторії — MIT; ваги завантажуються в `weights/hamer/` під час першого `m2mr run --detect-hands`, за умовами випуску першоджерела

## Контакт

Якщо виникла проблема, потрібна допомога з локальним налаштуванням або хочете поговорити про співпрацю, напишіть:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
