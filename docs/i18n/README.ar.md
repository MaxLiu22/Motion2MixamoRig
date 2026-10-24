# Motion2MixamoRig

<p align="center">
  <a href="#المتطلبات"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.ar.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · العربية · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

ينقل حركة شخص في مقطع فيديو — أو الوضعية في صورة ثابتة — إلى شخصية ثلاثية الأبعاد بهيكل تحريك Adobe Mixamo.

للمطوّرين في مجال الألعاب: قدّم فيديو حركة لـ**شخص واحد** (أو صورة) وشخصية Mixamo؛ يكتب معاينات وملف شخصية مكسوّة (`.glb`) يمكن وضعه في Blender أو Unity.

> Motion2MixamoRig لا يزال تجريبيًا. الإصدار 0.1.8 هو مسار سطر الأوامر. يضم هذا المستودع أيضًا امتداد Blender 4.2+ يشغّل المسار نفسه في Python خارجي. بناء الإضافة من المصدر: [`blender_extension/README.md`](../../blender_extension/README.md).

## طريقتان للاستخدام

### 🎨 داخل Blender — دون برمجة

1. نزّل ملف zip الخاص بمنصتك، مثل `motion2mixamorig-<version>-macos-arm64.zip`، من [أحدث إصدار](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. في Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**، واختر ملف zip.
3. 3D Viewport → اضغط **N** → تبويب **Motion2MixamoRig** → **تثبيت بيئة التشغيل (بنقرة واحدة)** (Install Runtime (one click)).
4. **اختر نموذج SMPL-X…** (Choose SMPL-X Model…) (تنزيل مجاني)، واختر ملف FBX لشخصية Mixamo.
5. اختر فيديو لشخص واحد → **توليد الحركة** (Generate Motion).

التعليمات خطوة بخطوة والنصائح والتحديث: **[دليل المستخدم](user-guide.ar.md)**. جُرّب على macOS (Apple Silicon).

### 💻 سطر الأوامر — للمطوّرين

استنسخ المستودع وشغّل المسار بنفسك: ابدأ من [المتطلبات](#المتطلبات).

ينبغي للوكلاء البرمجيين (Agents) البدء من [`AGENTS.md`](../../AGENTS.md).

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>افتح <a href="../assets/demo.mp4">demo.mp4</a> في هذا المستودع.</sub>
</p>

عرض توضيحي آخر:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

تقرير التشخيص (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## المتطلبات

يلزم توفر Python 3.11+. بعد الاستنساخ، أنشئ بيئة افتراضية وثبّت الاعتماديات؛ يصبح أمر `m2mr` متاحًا بعد ذلك:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# ثبّت الاعتماديات وهذا المشروع. حزمة chumpy (قديمة في سلسلة الاعتماديات)
# تستورد pip في سكربت الإعداد، فيفشل البناء المعزول الافتراضي لـ pip
# برسالة "No module named 'pip'". ثبّتها أولًا مع إيقاف العزل
# (--no-build-isolation)، ثم ثبّت هذا المشروع.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

أوزان الاستدلال (GVHMR وغيرها) لا تُنزَّل في هذه الخطوة. أول `m2mr run` يسحبها إلى `weights/` (حوالي 5 غيغابايت، مرة واحدة فقط). أول `m2mr run --detect-hands` يسحب أيضًا أوزان يد HaMeR إلى `weights/hamer/` (حوالي 2.7 غيغابايت، مرة واحدة فقط).

يُفضَّل تثبيت ffmpeg (macOS: `brew install ffmpeg`، Ubuntu: `apt install ffmpeg`).
يعمل مسار المعالجة بدونه، لكن مقاطع الإخراج ستكون **صامتة** ولن تُشغَّل في المتصفح.

## قبل التشغيل: ضع هذه في `assets/`

هذا المستودع لا يتضمّن هذه الملفات؛ ينبغي جلبها بنفسك. يجب أن يطابق اسم ملف SMPL-X الجدول حرفيًا؛ أما أسماء FBX والفيديو والصورة فحرة. يحتاج التشغيل إلى SMPL-X وشخصية Mixamo و**إما** فيديو **أو** صورة. شخصيات Mixamo المُعاد تصديرها من Cinema 4D مدعومة أيضًا؛ راجع [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md).

| ماذا | أين | من أين |
|---|---|---|
| نموذج جسم SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | سجّل في [SMPL-X](https://smpl-x.is.tue.mpg.de/) ثم نزّله |
| ملف FBX لشخصية Mixamo | `assets/mixamo/Y_Bot.fbx` | بحساب Adobe نزّل Y Bot (أو أي شخصية بهيكل Mixamo) من [Mixamo](https://www.mixamo.com) |
| فيديو الحركة | `assets/video/<your_clip>.mp4` | مقطع فيه **شخص واحد بالضبط** ظاهر بوضوح، **من الرأس إلى القدمين داخل الإطار طوال المقطع** (يمكن وضع عدة ملفات؛ كل تشغيل يستخدم آخر ملف أُضيف) |
| صورة وضعية (اختياري) | `assets/image/<your_photo>.jpg` | صورة فيها **شخص واحد بالضبط** ظاهر بوضوح، **من الرأس إلى القدمين داخل الإطار**. مع `--image` |
| اليد اليمنى MANO (فقط مع `--detect-hands`) | `assets/body_models/mano/MANO_RIGHT.pkl` | سجّل في [MANO](https://mano.is.tue.mpg.de/) ونزّل **Models & Code**. تشغيل الجسم وحده لا يحتاج هذا الملف |

ملاحظة: ملف التنزيل من Mixamo اسمه `Y Bot.fbx` (**مسافة**)، ويختلف بحرف واحد عن `Y_Bot.fbx` (**شرطة سفلية**) في الجدول.
أعد تسميته بالشرطة السفلية فيصبح الهيكل الافتراضي (`m2mr run` دون `--rig`). الإبقاء على المسافة جائز أيضًا — إن غاب `Y_Bot.fbx` يُستخدم أول `.fbx` في `assets/mixamo/`.

يمكن وضع عدة فيديوهات في `assets/video/`. دون `--video` أو `--image` يستخدم التشغيل **آخر ملف أُضيف إلى `assets/video/`**؛ إن كان المجلد فارغًا يعود إلى أحدث صورة في `assets/image/`.
يجب أن يظهر في كل مقطع أو صورة شخص واحد فقط، **من الرأس إلى القدمين داخل الإطار** — دون قص عند الحواف. يتوقف `m2mr doctor` / `m2mr run` قبل الاستخراج إن ظهر شخصان.

## البدء السريع

النتائج في `outputs/<وقت-التشغيل>_<المصدر>/`. تشغيل الفيديو يكتب `videos/`؛ تشغيل الصورة يكتب `images/`.

### 1. تحقق من الأصول والبيئة

يُطبع الناقص مع مصدر التنزيل ومكان الوضع.

```bash
m2mr doctor
```

يفحص `m2mr doctor` تشغيل الجسم. لا يطلب نموذج يد MANO. للتحقق أيضًا من الملف الإضافي وحزم بايثون التي يستخدمها اكتشاف الأصابع:

```bash
m2mr doctor --detect-hands
```

### 2. أول تشغيل: إظهار نتيجة على الشاشة

دون خيارات، يُستخدم **أحدث ملف في `assets/video/`** و`assets/mixamo/Y_Bot.fbx`.

```bash
m2mr run
```

هذه الخطوة الأبطأ. أول تشغيل ينزّل حوالي 5 غيغابايت من أوزان الاستدلال (مرة واحدة)، ثم يستخرج حركة الإنسان من الفيديو.
على المعالج المركزي (CPU)، يستغرق استخراج مقطع مدته نحو 30 ثانية حوالي 8–15 دقيقة؛ التشغيلات اللاحقة بطول مشابه مع وجود الأوزان تستغرق حوالي 3–5 دقائق.
إعادة توجيه الحركة والتصيير عادة دقيقة أو دقيقتان. إعادة استخدام الهيكل بـ `--skeleton` في القسم التالي تتخطى الاستخراج بالكامل وتنتهي خلال عشرات الثواني.

القدم المرتكزة تُثبَّت افتراضيًا: مشط القدم حين يكون المشط على الأرض، والكعب فقط حين تكون الأصابع مرفوعة. إذا لم تبلغ الساق الممدودة تلك النقطة، يتحرك الحوض. ثم تُوضع أخمص القدم على الأرض (y = 0). يُبقي `--no-foot-lock` إعادة التوجيه الخام، فقد تنزلق القدمان؛ وتُوضع الأخمص على الأرض رغم ذلك.

### 3. الحركة نفسها، شخصية مختلفة

نزّل شخصية أخرى من Mixamo إلى `assets/mixamo/`. **لا تُعِد التشغيل باستخدام `--rig` فقط** — ذلك يكرر الاستخراج البطيء.
استخدم `--skeleton` لإعادة استخدام هيكل تشغيل سابق؛ الدقائق تصبح عشرات الثواني:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. فيديو مختلف

`--video` يختار المقطع. ويمكن جمعه مع `--rig` بحرية.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. صورة ثابتة (وضعية ساكنة)

`--image` يستعيد **وضعية ثلاثية الأبعاد ساكنة** من صورة لشخص واحد، ثم ينقلها إلى شخصية Mixamo كما يفعل تشغيل الفيديو. المعاينات أربع صور في `images/` (نفس المناظر كتشغيل الفيديو) إضافة إلى مقطع المدار يمين/يسار `before_after_360_compare.mp4`. لا تُجمع مع `--video`.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

`--image` دون مسار يستخدم آخر ملف أُضيف إلى `assets/image/`.

### 6. فحص التداخل الذاتي

كل تشغيل يفحص أيضًا الشخصية الناتجة بحثًا عن **التداخل الذاتي** — دخول جزء من الجسم في جزء آخر، مثل يد داخل الرأس — ويكتب `diagnostics.json`. تطبع الطرفية سطرًا واحدًا، مثل `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`. لا يُفحص التداخل مع الأرضية.

لإعادة فحص تشغيل ما، أو لرؤية المشكلات:

```bash
m2mr diagnose outputs/<run>                  # يعيد كتابة diagnostics.json
m2mr diagnose outputs/<run> --visualize      # وأيضًا diagnostics.html: الفيديو المصدر بجانب الشخصية، خط زمني، قائمة مشكلات قابلة للنقر
m2mr diagnose outputs/<run> --threshold-cm 2 # يبلّغ فقط عن التداخلات الأعمق من 2 cm (الافتراضي 1)
```

كل مشكلة في `diagnostics.json` هي زوج من أجزاء الجسم مع نطاقات الإطارات التي يتداخلان فيها، وأسوأ إطار، وعمقه. تبدأ أرقام الإطارات من 0، كما في الخط الزمني لـ Blender بعد استيراد glTF. لا تُقارَن الأجزاء المتصلة بمفصل (العضد والساعد، الجذع والفخذ، …): جلدها يتداخل حول المفصل في أي وضعية. يضمّن `diagnostics.html` الفيديو المصدر (يتطلب `ffmpeg`) ويحمّل three.js من CDN، لذا يحتاج العرض ثلاثي الأبعاد إلى اتصال بالإنترنت. يرسم هذا العرض علامات أرضية ثابتة على y = 0: صليب كل 0.5 م، وآخر أكبر كل متر، وصليب أخضر عند الأصل، لمعرفة ما إذا كانت الشخصية تتحرك. المسار الكهرماني فوق مسارات التداخل مخصّص لملاحظات تراها العين (اسحب مدى، أو **In** / **Out**). قائمة **Notes** على اليمين تعرضها؛ انقر صفًا للانتقال إليه. يحفظ **Download notes** هذه الملاحظات مع قائمة التداخل. اسم الملف هو اسم الفيديو المصدر، ويحوي مساره.

### 7. الأصابع (`--detect-hands`)

تشغيل `m2mr run` العادي يحرّك الجسم ويترك عظام أصابع Mixamo في وضع الراحة. يفتح `--detect-hands` نموذج اليد الذي يرافق مستخرج الجسم. مع المستخرج الافتراضي GVHMR، هذا النموذج هو [HaMeR](https://github.com/geopavlakos/hamer). يقتطع HaMeR المعصمين من الشخص والإطارات التي اختارها GVHMR مسبقًا. لا يبحث في المقطع عن شخص ثانٍ.

**يتضاعف الوقت تقريبًا.** المقطع الذي ينتهي في بضع دقائق من دون الخيار يستغرق مع `--detect-hands` نحو ضعف ذلك، لأن مرور اليد يجري فوق استخراج الجسم. في فيديو طويل، احسب هذا الوقت قبل أن تبدأ.

ضع `MANO_RIGHT.pkl` كما في الجدول أعلاه، ثم:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

أول تشغيل بـ `--detect-hands` ينزّل أوزان HaMeR إلى `weights/hamer/` (حوالي 2.7 غيغابايت، مرة واحدة). تُكتب دورانات الأصابع في `skeleton_motion.npz` وتقود عظام أصابع Mixamo الثلاثين على الشخصية ذات الجلد. المعصم الذي لم يره مرور الجسم بوضوح يبقى في وضع الراحة لتلك اليد.

`--hand-smooth` هو عدد ثواني التنعيم المطبَّق على هذه الدورانات. القيمة الافتراضية `0.08`. يُبقي `0` التقدير الخام. يعمل التنعيم كلما احتوى ملف الهيكل على حركة يد مسبقًا، بما في ذلك تشغيل لاحق يعيد استخدام هذا الملف فقط.

عند إعادة استخدام هيكل سابق:

- الملف يحتوي مسبقًا على حركة اليد: `--skeleton` يقود الأصابع بنفسه. لا حاجة إلى `--detect-hands` مرة أخرى.
- لا يحتويها، لكن ذاكرة الجسم المؤقتة لذلك التشغيل ما زالت بجانبه (`cache/<clip>/0_input_video.mp4` مع `preprocess/vitpose.pt` و`preprocess/bbx.pt`): يضيف `--skeleton ... --detect-hands` الأصابع من دون استخراج الجسم من جديد.
- ذهبت تلك الذاكرة المؤقتة: شغّل الفيديو أو الصورة مرة أخرى مع `--detect-hands`.

## المخرجات

كل `m2mr run` ينشئ مجلدًا باسم **وقت بدء الأمر**. الملفات في الجذر واحدة للفيديو والصورة؛ يتغيّر مجلد المعاينة فقط.

```
outputs/20260829_193205_dance/          # تشغيل الصورة: …_pose/
├── run.json                            # وقت البدء، المدخلات، الأمر الكامل
├── skeleton_motion.npz                 # هيكل إنسان ثلاثي الأبعاد (إعادة استخدام بـ --skeleton)
├── mixamo_rotations.npz                # دورانات عظام Mixamo لكل عظم
├── mixamo_character.glb                # شخصية مكسوّة، استيراد إلى Blender / Unity
├── diagnostics.json                    # تقرير التداخل الذاتي (انظر الخطوة 6 في البدء السريع)
├── diagnostics.html                    # فقط بعد `m2mr diagnose <run> --visualize`
└── videos/   أو   images/              # المعاينات — حسب المدخل
```

**إدخال الفيديو** يكتب `videos/` (نسبة العرض إلى الارتفاع نفسها كالمقطع):

```
videos/
├── human_skeleton.mp4                  # هيكل الإنسان الثلاثي المستعاد
├── mixamo_skeleton.mp4                 # هيكل Mixamo
├── mixamo_character.mp4                # شخصية Mixamo المكسوّة
└── compare.mp4                         # 2×2: الأصل (أعلى اليسار) / هيكل Mixamo (أعلى اليمين)
                                        #      هيكل الإنسان (أسفل اليسار) / الشخصية (أسفل اليمين)
```

**إدخال الصورة** يكتب `images/` بدلًا من ذلك (نفس المناظر الأربعة مع مدار):

```
images/
├── human_skeleton.png                  # هيكل الإنسان الثلاثي المستعاد
├── mixamo_skeleton.png                 # هيكل Mixamo
├── mixamo_character.png                # شخصية Mixamo المكسوّة
├── compare.png                         # 2×2: الأصل (أعلى اليسار) / هيكل Mixamo (أعلى اليمين)
│                                       #      هيكل الإنسان (أسفل اليسار) / الشخصية (أسفل اليمين)
└── before_after_360_compare.mp4        # اليسار: الصورة الأصلية
                                        # اليمين: مدار 10° حول الهيكل (دورة كاملة)
```

مع `--detect-hands` يخزّن `skeleton_motion.npz` دورانات الأصابع أيضًا، ويضم `mixamo_rotations.npz` و`mixamo_character.glb` عظام الأصابع الثلاثين. من دون هذا الخيار، ومن دون حركة يد مخزّنة مسبقًا في هيكل يُعاد استخدامه، تبقى هذه العظام في وضع الراحة.

افتح `mixamo_character.glb` في Blender: File → Import → glTF 2.0 (.glb/.gltf). إن وُجّهت الكاميرا إلى فراغ، حدّد شبكة الشخصية ثم View → Frame Selected. مجموعة الكرات على الرأس واليدين هي عرض للعظام وليست الشبكة: في Outliner أخفِ **Icosphere** و**armature** واترك الشبكة المكسوّة ظاهرة. اضبط FPS المشهد من `run.json` (`fps`) والخط الزمني على الإطارات من 0 إلى `n_frames` − 1 حتى يطابق التشغيل المصدر وتطابق أرقام الإطارات `diagnostics.json`. في تشغيل الفيديو قارن مع `videos/mixamo_character.mp4`، وفي تشغيل الصورة مع `images/mixamo_character.png` أو مقطع المدار.

## الرخصة

شيفرة هذا المستودع Apache-2.0. للأصول التي تنزّلها شروطها الخاصة، ويجب ألا تُعاد توزيعها مع هذا المستودع:

- **SMPL-X**: يخضع لقيود MPI؛ الاستخدام الافتراضي بحث / تعليم / فن غير تجاري؛ الاستخدام التجاري يحتاج اتفاقًا منفصلًا
- **MANO** (فقط مع `--detect-hands`): يخضع لقيود MPI، والتنزيل من نوع تنزيل SMPL-X نفسه؛ ضع `MANO_RIGHT.pkl` محليًا ولا تعِد توزيعه
- **Mixamo FBX**: جائز في منتج نهائي؛ يُحظر إعادة توزيع ملف FBX الخام كحزمة أصول
- **GVHMR وأوزان الاستدلال الأخرى**: تُنزَّل تلقائيًا إلى `weights/` عند أول `m2mr run`، وفق رخصة كل مصدر
- **HaMeR**: شيفرة الاستدلال في هذا المستودع برخصة MIT؛ تُنزَّل الأوزان إلى `weights/hamer/` عند أول `m2mr run --detect-hands`، وفق شروط إصدار المصدر

## التواصل

إن واجهت مشكلة، أو احتجت إلى مساعدة لإكمال الإعداد المحلي، أو رغبت في الحديث عن التعاون، يُرجى المراسلة على:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
