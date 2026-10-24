# Motion2MixamoRig

<p align="center">
  <a href="#आवश्यकताएँ"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.hi.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · हिन्दी · <a href="README.sv.md">Svenska</a>
</p>

वीडियो में किसी व्यक्ति की गति — या फ़ोटो में उसकी पोज़ — को Adobe Mixamo रिग वाले 3D कैरेक्टर पर ले जाएँ।

गेम बनाने वालों के लिए: **एक ही व्यक्ति** का एक्शन वीडियो (या एक फ़ोटो) और एक Mixamo कैरेक्टर दें; यह प्रीव्यू वीडियो और स्किनिंग वाला कैरेक्टर फ़ाइल (`.glb`) लिखता है, जिसे Blender या Unity में खींचकर डाल सकते हैं।

> Motion2MixamoRig अभी प्रयोगात्मक है। संस्करण 0.1.8 कमांड-लाइन पाइपलाइन है। इस रिपॉज़िटरी में Blender 4.2+ का एक्सटेंशन भी है, जो वही पाइपलाइन बाहरी Python वातावरण में चलाता है। सोर्स से ऐड-ऑन बनाना: [`blender_extension/README.md`](../../blender_extension/README.md)।

## इस्तेमाल के दो तरीके

### 🎨 Blender में — बिना कोड लिखे

1. अपनी प्लैटफ़ॉर्म की zip डाउनलोड करें, जैसे `motion2mixamorig-<version>-macos-arm64.zip`, [नवीनतम रिलीज़](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest) से।
2. Blender में: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, zip चुनें।
3. 3D Viewport → **N** दबाएँ → **Motion2MixamoRig** टैब → **रनटाइम इंस्टॉल करें (एक क्लिक)** (Install Runtime (one click))।
4. **SMPL-X मॉडल चुनें…** (Choose SMPL-X Model…) (मुफ़्त डाउनलोड) और एक Mixamo कैरेक्टर FBX चुनें।
5. एक व्यक्ति का वीडियो चुनें → **मोशन बनाएँ** (Generate Motion)।

क्रमवार निर्देश, सुझाव और अपडेट: **[उपयोगकर्ता गाइड](user-guide.hi.md)**। macOS (Apple Silicon) पर जाँचा गया है।

### 💻 कमांड लाइन — डेवलपरों के लिए

रिपॉज़िटरी क्लोन करें और पाइपलाइन खुद चलाएँ: [आवश्यकताएँ](#आवश्यकताएँ) से शुरू करें।

एजेंट [`AGENTS.md`](../../AGENTS.md) से शुरू करें।

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>इस रिपॉज़िटरी में <a href="../assets/demo.mp4">demo.mp4</a> खोलें।</sub>
</p>

एक और डेमो:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

डायग्नोस्टिक्स रिपोर्ट (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## आवश्यकताएँ

Python 3.11+। क्लोन करने के बाद virtualenv बनाएँ और निर्भरताएँ इंस्टॉल करें; तब `m2mr` कमांड मिल जाती है:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# निर्भरताएँ और यह प्रोजेक्ट इंस्टॉल करें। chumpy (निर्भरता शृंखला का
# पुराना पैकेज) अपने सेटअप स्क्रिप्ट में pip इंपोर्ट करता है, जो pip के
# डिफ़ॉल्ट अलग बिल्ड में "No module named 'pip'" से असफल हो जाता है। पहले
# इसे आइसोलेशन बंद करके इंस्टॉल करें, फिर यह प्रोजेक्ट इंस्टॉल करें।
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

इनफ़रेंस वेट यहाँ डाउनलोड नहीं होते। पहला `m2mr run` GVHMR के वेट `weights/` में लाता है (~5 GB, सिर्फ़ एक बार)। पहला `m2mr run --detect-hands` HaMeR के हाथ वाले वेट भी `weights/hamer/` में लाता है (~2.7 GB, सिर्फ़ एक बार)।

ffmpeg रखना अच्छा है (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`)।
पाइपलाइन इसके बिना भी चलती है, लेकिन आउटपुट वीडियो **बिना आवाज़** के होंगे और ब्राउज़र में नहीं चलेंगे।

## चलाने से पहले: ये फ़ाइलें `assets/` में रखें

यह रिपॉज़िटरी ये फ़ाइलें साथ नहीं लाती; आपको खुद लानी होंगी। SMPL-X का फ़ाइल नाम तालिका से बिल्कुल मेल खाना चाहिए; FBX, वीडियो और इमेज के नाम कुछ भी हो सकते हैं। एक रन के लिए SMPL-X, एक Mixamo कैरेक्टर, और **या तो** वीडियो **या** एक फ़ोटो चाहिए। Cinema 4D से दोबारा एक्सपोर्ट किए Mixamo कैरेक्टर भी चलते हैं; देखें [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md)।

| क्या | कहाँ | कहाँ से मिलेगा |
|---|---|---|
| SMPL-X बॉडी मॉडल | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | [SMPL-X](https://smpl-x.is.tue.mpg.de/) पर रजिस्टर करें और डाउनलोड करें |
| Mixamo कैरेक्टर FBX | `assets/mixamo/Y_Bot.fbx` | Adobe खाते से Y Bot (या कोई और Mixamo-रिग कैरेक्टर) [Mixamo](https://www.mixamo.com) से डाउनलोड करें |
| एक्शन वीडियो | `assets/video/<your_clip>.mp4` | **ठीक एक** साफ़ दिखने वाले व्यक्ति का क्लिप, **पूरे समय सिर से पैर तक फ़्रेम में** (कई फ़ाइलें रख सकते हैं; हर रन सबसे आखिर में जोड़ी गई फ़ाइल लेता है) |
| पोज़ की फ़ोटो (वैकल्पिक) | `assets/image/<your_photo>.jpg` | **ठीक एक** साफ़ दिखने वाले व्यक्ति की फ़ोटो, **सिर से पैर तक फ़्रेम में**। `--image` के साथ इस्तेमाल करें |
| MANO दायाँ हाथ (सिर्फ़ `--detect-hands` के लिए) | `assets/body_models/mano/MANO_RIGHT.pkl` | [MANO](https://mano.is.tue.mpg.de/) पर रजिस्टर करें और **Models & Code** डाउनलोड करें। सिर्फ़ शरीर वाले रन को यह फ़ाइल नहीं चाहिए |

नोट: Mixamo से डाउनलोड का नाम `Y Bot.fbx` है (**स्पेस**), तालिका के `Y_Bot.fbx` (**अंडरस्कोर**) से एक अक्षर अलग।
इसे अंडरस्कोर वाले नाम पर बदलें और यह डिफ़ॉल्ट रिग बन जाता है (`m2mr run` बिना `--rig`)। स्पेस छोड़ना भी चलता है: अगर `Y_Bot.fbx` नहीं है, तो `assets/mixamo/` की पहली `.fbx` इस्तेमाल होती है।

`assets/video/` में कई वीडियो हो सकते हैं। `--video` या `--image` के बिना रन `assets/video/` में **सबसे आखिर में जोड़ी गई** फ़ाइल लेता है; वह फ़ोल्डर खाली हो तो `assets/image/` की सबसे नई फ़ोटो लेता है।
हर क्लिप या फ़ोटो में सिर्फ़ एक व्यक्ति हो, **सिर से पैर तक फ़्रेम में**, किनारों पर कुछ कटा न हो। अगर दृश्य में दो व्यक्ति हों, तो `m2mr doctor` / `m2mr run` एक्सट्रैक्शन से पहले रुक जाते हैं।

## जल्दी शुरू करें

नतीजे `outputs/<run-time>_<source>/` में जाते हैं। वीडियो वाले रन `videos/` लिखते हैं; फ़ोटो वाले रन `images/` लिखते हैं।

### 1. एसेट और वातावरण जाँचें

जो भी गायब हो, वह कहाँ से डाउनलोड करना है और कहाँ रखना है, यह छपकर आता है।

```bash
m2mr doctor
```

`m2mr doctor` शरीर वाले रन की जाँच करता है। MANO हाथ मॉडल ज़रूरी नहीं। उँगली पहचान के अतिरिक्त फ़ाइल और Python पैकेज भी जाँचने के लिए:

```bash
m2mr doctor --detect-hands
```

### 2. पहला रन: स्क्रीन पर कुछ देखें

बिना फ़्लैग यह **`assets/video/` की सबसे नई फ़ाइल** और `assets/mixamo/Y_Bot.fbx` इस्तेमाल करता है।

```bash
m2mr run
```

यह धीमा चरण है। पहला रन ~5 GB इनफ़रेंस वेट डाउनलोड करता है (सिर्फ़ एक बार), फिर वीडियो से मानव गति निकालता है।
CPU पर ~30 सेकंड का क्लिप निकालने में करीब 8–15 मिनट लगते हैं; वेट आ जाने के बाद उतनी ही लंबाई के बाद के रन करीब 3–5 मिनट लेते हैं।
रीटार्गेट और रेंडर आमतौर पर एक-दो मिनट लेते हैं। अगले भाग में `--skeleton` से कंकाल दोबारा इस्तेमाल करने पर एक्सट्रैक्शन बिल्कुल छूट जाता है और काम दसियों सेकंड में खत्म होता है।

ज़मीन पर रखा पैर डिफ़ॉल्ट रूप से टिका रहता है: पंजे का अगला भाग जब वह नीचे हो, एड़ी सिर्फ़ जब उँगलियाँ ऊपर हों। अगर सीधी टाँग उस जगह तक न पहुँचे, तो कूल्हे हिलते हैं। फिर तलवा फ़र्श पर बैठता है (y = 0)। `--no-foot-lock` कच्चा रीटार्गेट रखता है, इसलिए पैर फिसल सकते हैं; तलवा फिर भी फ़र्श पर बैठता है।

### 3. वही गति, दूसरा कैरेक्टर

Mixamo से दूसरा कैरेक्टर `assets/mixamo/` में डाउनलोड करें। **सिर्फ़ `--rig` बदलकर दोबारा न चलाएँ** — इससे धीमा एक्सट्रैक्शन दोहराया जाएगा।
पिछले रन का कंकाल दोबारा इस्तेमाल करने के लिए `--skeleton` दें; मिनट दसियों सेकंड बन जाते हैं:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. दूसरा वीडियो

`--video` क्लिप चुनता है। यह `--rig` के साथ आज़ादी से जुड़ता है।

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. एक फ़ोटो (स्थिर पोज़)

`--image` एक व्यक्ति की फ़ोटो से **स्थिर 3D पोज़** निकालता है, फिर उसे Mixamo कैरेक्टर पर उसी तरह ले जाता है जैसे वीडियो वाला रन। प्रीव्यू `images/` में चार चित्र हैं (वीडियो रन जैसे ही दृश्य), साथ में बाएँ/दाएँ ऑर्बिट क्लिप `before_after_360_compare.mp4`। साथ में `--video` न दें।

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

बिना पथ के `--image` `assets/image/` में सबसे आखिर जोड़ी गई फ़ाइल लेता है।

### 6. सेल्फ़-इंटरसेक्शन जाँचें

हर रन तैयार कैरेक्टर में **सेल्फ़-इंटरसेक्शन** भी देखता है — शरीर का एक हिस्सा दूसरे में घुसना, जैसे सिर के अंदर हाथ — और `diagnostics.json` लिखता है। टर्मिनल एक पंक्ति छापता है, जैसे `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`। फ़र्श की जाँच नहीं होती।

किसी रन को दोबारा जाँचने या समस्याएँ देखने के लिए:

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json फिर से लिखें
m2mr diagnose outputs/<run> --visualize      # diagnostics.html भी: कैरेक्टर के बगल स्रोत वीडियो, टाइमलाइन, क्लिक करने योग्य समस्या सूची
m2mr diagnose outputs/<run> --threshold-cm 2 # सिर्फ़ 2 cm से गहरी घुसपैठ बताएँ (डिफ़ॉल्ट 1)
```

`diagnostics.json` की हर समस्या शरीर के दो हिस्सों का जोड़ा है, उन फ़्रेम सीमाओं के साथ जहाँ वे कटते हैं, सबसे खराब फ़्रेम, और उसकी गहराई। फ़्रेम संख्या 0 से गिनी जाती है, जैसे glTF इंपोर्ट के बाद Blender की टाइमलाइन। जोड़ पर जुड़े हिस्से (ऊपरी बाँह और अग्रबाहु, धड़ और जाँघ, …) तुलना में नहीं आते: किसी भी पोज़ में जोड़ के आसपास उनकी स्किन ओवरलैप करती है। `diagnostics.html` स्रोत वीडियो जोड़ता है (`ffmpeg` चाहिए) और CDN से three.js लोड करता है, इसलिए 3D दृश्य के लिए इंटरनेट चाहिए। उस दृश्य में y = 0 पर फ़र्श के स्थिर निशान रहते हैं — हर 0.5 m पर एक क्रॉस, हर मीटर पर बड़ा, और मूल बिंदु पर हरा क्रॉस — ताकि देखा जा सके कि कैरेक्टर हिल रहा है या नहीं। इंटरसेक्शन पटरियों के ऊपर की अंबर लेन आँख से लिखे नोट के लिए है (सीमा खींचें, या In / Out)। दाईं ओर की **Notes** सूची उन्हें दिखाती है; किसी पंक्ति पर क्लिक करने से वहाँ पहुँचते हैं। **Download notes** ये नोट इंटरसेक्शन सूची के साथ सहेजता है। फ़ाइल का नाम स्रोत वीडियो पर होता है और उस वीडियो का पथ दर्ज रहता है।

### 7. उँगलियाँ (`--detect-hands`)

सादा `m2mr run` शरीर हिलाता है और Mixamo की उँगली की हड्डियों को आराम की स्थिति में छोड़ता है। `--detect-hands` वह हाथ मॉडल चालू करता है जो शरीर निकालने वाले के साथ चलता है। डिफ़ॉल्ट एक्सट्रैक्टर GVHMR के साथ वह मॉडल [HaMeR](https://github.com/geopavlakos/hamer) है। HaMeR व्यक्ति और उन फ़्रेम से कलाइयाँ काटता है जिन्हें GVHMR पहले ही चुन चुका है। वह क्लिप में दूसरे व्यक्ति को नहीं खोजता।

**समय लगभग दोगुना हो जाता है।** जो क्लिप बिना फ़्लैग कुछ मिनट में खत्म होता, `--detect-hands` के साथ लगभग दुगुना लेता है, क्योंकि हाथ वाला पास शरीर निकालने के ऊपर चलता है। लंबे वीडियो पर शुरू करने से पहले यह अतिरिक्त समय रखें।

`MANO_RIGHT.pkl` ऊपर की तालिका की तरह रखें, फिर:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

`--detect-hands` वाला पहला रन HaMeR के वेट `weights/hamer/` में डाउनलोड करता है (~2.7 GB, एक बार)। उँगली के घुमाव `skeleton_motion.npz` में लिखे जाते हैं और स्किन वाले कैरेक्टर की 30 Mixamo उँगली हड्डियों को चलाते हैं। जिस कलाई को शरीर वाला पास साफ़ न देख पाया हो, वह हाथ आराम पर रहता है।

`--hand-smooth` बताता है कि उन घुमावों पर कितने सेकंड की स्मूथिंग लगे। डिफ़ॉल्ट `0.08` है। `0` कच्चा अनुमान रखता है। स्मूथिंग तब चलती है जब कंकाल फ़ाइल में हाथ की गति पहले से हो, बाद वाले उस रन में भी जो सिर्फ़ वही फ़ाइल दोबारा इस्तेमाल करता है।

पिछला कंकाल दोबारा इस्तेमाल करते समय:

- फ़ाइल में हाथ की गति पहले से है: `--skeleton` उँगलियाँ खुद चलाता है। `--detect-hands` फिर ज़रूरी नहीं।
- नहीं है, पर उस रन का बॉडी कैश अभी बगल में है (`cache/<clip>/0_input_video.mp4`, साथ में `preprocess/vitpose.pt` और `preprocess/bbx.pt`): `--skeleton ... --detect-hands` शरीर दोबारा निकाले बिना उँगलियाँ जोड़ता है।
- वह कैश नहीं रहा: वीडियो या फ़ोटो `--detect-hands` के साथ फिर चलाएँ।

## आउटपुट

हर `m2mr run` एक डायरेक्टरी बनाता है, जिसका नाम **कमांड शुरू होने का समय** होता है। रूट की फ़ाइलें वीडियो और फ़ोटो दोनों में एक जैसी होती हैं; सिर्फ़ प्रीव्यू फ़ोल्डर बदलता है।

```
outputs/20260829_193205_dance/          # फ़ोटो के लिए …_pose/
├── run.json                            # शुरू का समय, इनपुट, पूरा कमांड
├── skeleton_motion.npz                 # 3D मानव कंकाल (--skeleton से दोबारा इस्तेमाल)
├── mixamo_rotations.npz                # हर हड्डी पर Mixamo घुमाव
├── mixamo_character.glb                # स्किन वाला कैरेक्टर, Blender / Unity में इंपोर्ट
├── diagnostics.json                    # सेल्फ़-इंटरसेक्शन रिपोर्ट (जल्दी शुरू करें का चरण 6)
├── diagnostics.html                    # सिर्फ़ `m2mr diagnose <run> --visualize` के बाद
└── videos/   या   images/              # प्रीव्यू — इनपुट पर निर्भर
```

**वीडियो इनपुट** `videos/` लिखता है (क्लिप जैसा ही आस्पेक्ट रेशियो):

```
videos/
├── human_skeleton.mp4                  # निकाला गया 3D मानव कंकाल
├── mixamo_skeleton.mp4                 # Mixamo रिग का कंकाल
├── mixamo_character.mp4                # स्किन वाला Mixamo कैरेक्टर
└── compare.mp4                         # 2×2: मूल (ऊपर बाएँ) / Mixamo कंकाल (ऊपर दाएँ)
                                        #      मानव कंकाल (नीचे बाएँ) / कैरेक्टर (नीचे दाएँ)
```

**फ़ोटो इनपुट** इसकी जगह `images/` लिखता है (वही चार दृश्य, साथ में एक घुमाव):

```
images/
├── human_skeleton.png                  # निकाला गया 3D मानव कंकाल
├── mixamo_skeleton.png                 # Mixamo रिग का कंकाल
├── mixamo_character.png                # स्किन वाला Mixamo कैरेक्टर
├── compare.png                         # 2×2: मूल (ऊपर बाएँ) / Mixamo कंकाल (ऊपर दाएँ)
│                                       #      मानव कंकाल (नीचे बाएँ) / कैरेक्टर (नीचे दाएँ)
└── before_after_360_compare.mp4        # बाएँ: मूल फ़ोटो
                                        # दाएँ: रिग की 10° ऑर्बिट (एक पूरा चक्कर)
```

`--detect-hands` के साथ `skeleton_motion.npz` उँगली के घुमाव भी रखता है, और `mixamo_rotations.npz` / `mixamo_character.glb` में 30 उँगली हड्डियाँ आती हैं। उस फ़्लैग के बिना, और दोबारा इस्तेमाल किए कंकाल में पहले से सहेजी हाथ गति के बिना, वे हड्डियाँ आराम पर रहती हैं।

`mixamo_character.glb` Blender में खोलें: File → Import → glTF 2.0 (.glb/.gltf)। अगर कैमरा खाली जगह पर हो, तो कैरेक्टर मेश चुनें और View → Frame Selected इस्तेमाल करें। सिर और हाथों पर गोलों का गुच्छा हड्डी का दिखावा है, मेश नहीं: Outliner में **Icosphere** और **armature** छिपाएँ; स्किन वाली मेश दिखती रहने दें। `run.json` से सीन का FPS (`fps`) सेट करें और टाइमलाइन फ़्रेम 0 से `n_frames` − 1 तक रखें, ताकि प्लेबैक स्रोत से मिले और फ़्रेम संख्या `diagnostics.json` से मिले। वीडियो वाले रन की तुलना `videos/mixamo_character.mp4` से करें, फ़ोटो वाले रन की `images/mixamo_character.png` या ऑर्बिट क्लिप से।

## लाइसेंस

इस रिपॉज़िटरी का कोड Apache-2.0 है। जो एसेट आप डाउनलोड करते हैं, उनकी अपनी शर्तें हैं, और उन्हें इस रिपॉज़िटरी के साथ नहीं बाँटना चाहिए:

- **SMPL-X**: MPI से गेटेड; डिफ़ॉल्ट रूप से गैर-व्यावसायिक शोध / शिक्षा / कला; व्यावसायिक उपयोग के लिए अलग समझौता चाहिए
- **MANO** (सिर्फ़ जब `--detect-hands` इस्तेमाल करें): MPI से गेटेड, SMPL-X जैसा ही डाउनलोड; `MANO_RIGHT.pkl` स्थानीय रखें और बाँटें नहीं
- **Mixamo FBX**: भेजे गए उत्पाद में चल सकता है; कच्ची FBX को एसेट पैक की तरह न बाँटें
- **GVHMR वेट**: पहले `m2mr run` पर `weights/` में अपने-आप डाउनलोड, मूल लाइसेंस के तहत
- **HaMeR**: इस रिपॉज़िटरी का इनफ़रेंस कोड MIT है; वेट पहले `m2mr run --detect-hands` पर `weights/hamer/` में डाउनलोड होते हैं, मूल रिलीज़ की शर्तों पर

## संपर्क

कोई समस्या हो, स्थानीय सेटअप पूरा करने में मदद चाहिए, या साथ काम करने की बात करनी हो, तो लिखें:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
