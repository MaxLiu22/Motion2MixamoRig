# Motion2MixamoRig لـ Blender — دليل المستخدم

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · <a href="user-guide.ko.md">한국어</a> · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · العربية · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

حوّل فيديو لشخص واحد إلى شخصية Mixamo متحركة، داخل Blender.
لا حاجة إلى برمجة أو طرفية.

<!-- video: link the tutorial video here -->

> جُرّب حتى الآن على **macOS (Apple Silicon)** فقط. إصدار Windows قريب.

## ما تحتاج إليه

- **Blender 4.2 أو أحدث**
- **اتصال بالإنترنت** للإعداد الأول
- **نحو 8 غيغابايت من المساحة الحرة** (بيئة التشغيل ~1.3 غيغابايت + النماذج ~5.6 غيغابايت)
- **حساب SMPL-X مجاني** و**حساب Adobe مجاني** (لـ Mixamo)؛ انظر الخطوتين 4 و5

## 1. نزّل الإضافة

افتح [أحدث إصدار](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
ونزّل ملف zip المناسب لجهازك:

| جهازك | الملف |
| --- | --- |
| Mac بمعالج Apple Silicon (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **قريبًا** |

مثلًا `motion2mixamorig-0.1.8-macos-arm64.zip`: `0.1.8` هو إصدار الإضافة،
و`macos-arm64` هو المنصة. إن اخترت الملف الخطأ، يرفض Blender تثبيته ويذكر
المنصة التي كان يتوقعها.

**لا** تفك ضغطه. Blender يثبّت ملف zip بنفسه.

## 2. ثبّتها في Blender

1. **Edit → Preferences → Get Extensions**
2. انقر السهم الصغير **∨** أعلى اليمين → **Install from Disk…**
3. اختر ملف zip. تظهر **Motion2MixamoRig** في القائمة مفعّلة.
4. أغلق Preferences. في 3D Viewport اضغط **N**، ثم انقر تبويب
   **Motion2MixamoRig** على اليمين.

<!-- screenshot: Install from Disk menu -->

## 3. ثبّت بيئة التشغيل (مرة واحدة)

في اللوحة، انقر **تثبيت بيئة التشغيل (بنقرة واحدة)** (Install Runtime (one click)).

تنزّل الإضافة Python ومكتباتها الخاصة (~1.4 غيغابايت) إلى
`~/Motion2MixamoRig/`. لا تلمس أي شيء آخر على جهازك. يستغرق هذا بضع دقائق،
ويعرض شريط التقدم الخطوة الحالية.

<!-- screenshot: Install Runtime button and progress -->

## 4. احصل على نموذج الجسم SMPL-X

SMPL-X نموذج جسم مجاني تحتاج إليه الإضافة. رخصته لا تسمح لنا بتوزيعه، لذا
تنزّله بنفسك، مرة واحدة:

1. افتح [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/) وانقر **Register**.
   وافق على الرخصة وأكّد بريدك الإلكتروني.
2. سجّل الدخول، وافتح **Download**، ونزّل نموذج SMPL-X (نسخة **NPZ**).
3. فك ضغطه وابحث عن **`SMPLX_NEUTRAL.npz`**.
4. في Blender، انقر **اختر نموذج SMPL-X…** (Choose SMPL-X Model…) واختر ذلك الملف.
   تعرض اللوحة بعدها **نموذج SMPL-X: موجود** (SMPL-X model: found).

<!-- screenshot: SMPL-X download page -->

## 5. احصل على شخصية Mixamo

1. افتح [mixamo.com](https://www.mixamo.com/) وسجّل الدخول بحساب Adobe.
2. تبويب **Characters** → اختر شخصية (مثلًا **Y Bot**).
3. **Download** → Format **FBX Binary (.fbx)**، Pose **T-pose** → Download.

<!-- screenshot: Mixamo download dialog -->

## 6. ولّد الحركة

في مربع **إدخال** (Input):

1. **نوع المصدر** (Source Type): فيديو (Video) (أو صورة (Image) لوضعية واحدة)
2. **ملف المصدر** (Source File): مقطعك. يجب أن يظهر فيه **شخص واحد بالضبط، من
   الرأس إلى القدمين داخل الإطار طوال الوقت**.
3. **هيكل Mixamo FBX** (Mixamo Rig FBX): الشخصية من الخطوة 5
4. **اكتشاف اليدين** (Detect Hands) مطفأ. شغّله فقط إذا أردت أن تتحرك الأصابع.
   ثم انقر **اختر نموذج يد MANO…** (Choose MANO Hand Model…) واختر `MANO_RIGHT.pkl`.
   تحصل على هذا الملف كما تحصل على SMPL-X: سجّل في
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/) ونزّل **Models & Code** وفك ضغطه.
   أول تشغيل لليدين ينزّل نحو **2.7 غيغابايت** إضافية مرة واحدة، ويستغرق حوالي ضعف تشغيل الجسم وحده. عند تشغيله يظهر **Finger Smoothing (seconds)**. ينعّم حركة الأصابع. القيمة الافتراضية 0.08 ثانية، و0 يُبقي ما تم اكتشافه كما هو.
5. انقر **توليد الحركة** (Generate Motion)

عند الانتهاء، تُستورد الشخصية المتحركة إلى مشهدك تلقائيًا. تبقى القدم المرتكزة حيث هبطت، وتُوضع الأخمص على أرضية Blender. تُضاف إلى تلك الأرضية شبكة **علامات الأرضية** (Floor Markers) (صليب كل 0.5 م). مربع **علامات الأرضية** (Floor Markers) ضمن التقدم / النتيجة يُظهرها أو يخفيها.

### التشغيل الأول يستغرق وقتًا أطول — هذا طبيعي

في المرة الأولى، تنزّل الإضافة نحو **5.6 غيغابايت** من النماذج. تعرض اللوحة حجم
التنزيل والسرعة والوقت المتبقي. تُنزَّل النماذج مرة واحدة فقط.

بعد ذلك يُعالَج الفيديو على جهازك. على معالج Mac المركزي (CPU)، يستغرق مقطع
مدته 10 ثوانٍ بضع دقائق. يبقى Blender قابلًا للاستخدام أثناء ذلك، و**إلغاء**
(Cancel) يوقف المهمة.

## نصائح لنتائج جيدة

- شخص واحد فقط، الجسم كله ظاهر، غير مقطوع عند الحواف
- كاميرا ثابتة، إضاءة جيدة، ملابس عادية بدلًا من الفضفاضة أو المنسدلة
- المقاطع القصيرة (5–20 ثانية) أسرع للتجربة أولًا

## التحديث إلى إصدار جديد

تُحدَّث الإضافة كثيرًا. للتحديث:

1. نزّل أحدث ملف zip من
   [أحدث إصدار](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest).
2. **Get Extensions** → أزل **Motion2MixamoRig** القديمة، وأغلق Blender
   كليًا (**Cmd+Q**)، ثم أعد فتحه وثبّت ملف zip الجديد.
3. في اللوحة، انقر **تحديث بيئة التشغيل** (Update Runtime).

يحتفظ التحديث بالنماذج المنزّلة، لذا فهو سريع. يظهر إصدارك المثبّت بجوار
الإضافة في **Get Extensions**.

## اللوحة

- **⚙ بجوار العنوان** يُظهر مربع **إعداد** (Setup) أو يخفيه.
- **إعداد**: اللغة، وبيئة التشغيل، وSMPL-X، و**الجهاز** (Device) (المعالج المركزي CPU هو
  الخيار الآمن)، و**فحص البيئة** (Check Environment).
- **إدخال**: ما تريد تحريكه، و**نموذج الجسم** (Body Model، GVHMR)، و**اكتشاف اليدين** (Detect Hands).
- **التقدم / النتيجة** (Progress / Result): التقدم، وأحدث سطور السجل، وبعد انتهاء المهمة
  **استيراد الشخصية المولَّدة** (Import Generated Character)، **علامات الأرضية** (Floor Markers)، و**فتح مجلد الناتج** (Open Output Folder)،
  و**عرض السجل الكامل** (View Full Log).
- **التشخيص** (Diagnostics): المواضع التي تدخل فيها أجزاء جسم الشخصية بعضها في
  بعض (يد داخل الرأس، ذراعان متشابكتان). الخلايا الحمراء في الشريط إطارات فيها
  مشكلة؛ انقر إحداها للانتقال إليها. يتبع المثلث أسفل الشريط الإطار الحالي،
  وتحته الأجزاء المتداخلة ومدى عمقها. ينتقل **السابق** / **التالي** (Previous
  / Next) بين المشكلات. يفتح **فتح تقرير HTML** (Open HTML Report) تقريرًا في
  متصفح الويب يعرض الفيديو المصدر بجانب الشخصية (يستغرق إنشاؤه في المرة الأولى
  نحو 15 ثانية). يحتاج الفيديو الأصلي إلى ffmpeg على الكمبيوتر (على Mac: `brew install ffmpeg`). بدونه تبقى الشخصية، ويبقى الفيديو بجانبها فارغًا. تقف الشخصية على صلبان أرضية ثابتة، واحد كل 0.5 م، لترى إن كانت تنزلق. المسار الكهرماني فوق المسارات الحمراء لملاحظات تراها بعينك. تظهر في قائمة **Notes** على اليمين؛ انقر صفًا للانتقال إليه. يحفظ **Download notes** هذه الملاحظات مع أوقات التداخل. اسم الملف هو اسم الفيديو المصدر.

تتحدث الإضافة 19 لغة. **تلقائي** (Auto) يتبع لغة Blender؛ غيّره في مربع
**إعداد** ضمن **لغة الواجهة** (UI Language).

## إذا حدث خطأ ما

| ما تراه | ما تفعله |
| --- | --- |
| **فشل تثبيت بيئة التشغيل** (Runtime installation failed) | تحقق من اتصالك بالإنترنت وانقر الزر مرة أخرى. السجل: `~/Motion2MixamoRig/logs/setup.log` |
| **نموذج SMPL-X: مفقود** (SMPL-X model: missing) | كرر الخطوة 4 واختر `SMPLX_NEUTRAL.npz` |
| **نموذج يد MANO: مفقود** (MANO hand model: missing) | شغّل **اكتشاف اليدين**، ثم **اختر نموذج يد MANO…** واختر `MANO_RIGHT.pkl` |
| **ملف Mixamo FBX غير صالح** (Mixamo FBX invalid) | نزّل الشخصية مرة أخرى بصيغة **FBX Binary**، **T-pose** |
| **المصدر يحتوي على أكثر من شخص** (Input contains multiple people) | استخدم مقطعًا فيه شخص واحد فقط |
| **لم يُكتشف أي شخص في المصدر** (No person was detected in the input) | تأكد من أن الجسم كله ظاهر ومضاء جيدًا |
| **توقفت عملية المعالجة بشكل غير متوقع** (Pipeline process exited unexpectedly) | انقر **عرض السجل الكامل** |

عند طلب المساعدة، أرفق السجل واذكر إصدار الإضافة الذي تستخدمه.

## إلغاء التثبيت

1. **Get Extensions** → أزل **Motion2MixamoRig**.
2. احذف المجلد **`~/Motion2MixamoRig`** (مجلدك الرئيسي →
   `Motion2MixamoRig`). إزالة الإضافة **لا** تحذفه، وهو يضم نحو 7 غيغابايت من
   بيئة التشغيل والنماذج، إضافة إلى نتائجك المولَّدة في `app/outputs/`.

## الرخصة

Motion2MixamoRig مخصّص **للاستخدام غير التجاري فقط**: فهو يعتمد على نماذج
بحثية (مثل GVHMR وSMPL-X) لا تسمح رخصها بالاستخدام التجاري.
انظر [`NOTICE.md`](../../NOTICE.md).
