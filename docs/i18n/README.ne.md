# Motion2MixamoRig

<p align="center">
  <a href="#आवश्यकताहरू"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.ne.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · नेपाली · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

भिडियोमा भएको व्यक्तिको चाल — वा स्थिर फोटोमा भएको पोज — Adobe Mixamo ले rig गरिएको 3D क्यारेक्टरमा सार्नुहोस्।

गेम डेभलपरहरूका लागि: **एक जना मात्र** व्यक्ति भएको एक्सन भिडियो (वा एउटा फोटो) र एउटा Mixamo क्यारेक्टर दिनुहोस्; यसले प्रिभ्यु भिडियोहरू र skin गरिएको क्यारेक्टर फाइल (`.glb`) बनाउँछ, जुन तपाईं सिधै Blender वा Unity मा राख्न सक्नुहुन्छ।

> Motion2MixamoRig अहिले प्रयोगात्मक चरणमा छ। संस्करण 0.1.8 कमान्ड-लाइन pipeline हो। यो रिपोजिटरीमा उही pipeline लाई बाहिरी Python वातावरणमा चलाउने Blender 4.2+ Extension पनि समावेश छ। सोर्सबाट एड-अन build गर्ने: [`blender_extension/README.md`](../../blender_extension/README.md)।

## प्रयोग गर्ने दुई तरिका

### 🎨 Blender मा — कोडिङ बिना

1. आफ्नो प्लेटफर्मको zip, जस्तै `motion2mixamorig-<version>-macos-arm64.zip`, [पछिल्लो release](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest) बाट डाउनलोड गर्नुहोस्।
2. Blender मा: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…**, अनि zip छान्नुहोस्।
3. 3D Viewport → **N** थिच्नुहोस् → **Motion2MixamoRig** ट्याब → **रनटाइम इन्स्टल गर्नुहोस् (एक क्लिक)** (Install Runtime (one click))।
4. **SMPL-X मोडेल छान्नुहोस्…** (Choose SMPL-X Model…) (निःशुल्क डाउनलोड), र Mixamo क्यारेक्टरको FBX छान्नुहोस्।
5. एक जना व्यक्ति भएको भिडियो छान्नुहोस् → **चाल बनाउनुहोस्** (Generate Motion)।

चरण-दर-चरण निर्देशन, सुझाव र अपडेट: **[प्रयोगकर्ता गाइड](user-guide.ne.md)**। macOS (Apple Silicon) मा परीक्षण गरिएको।

### 💻 कमान्ड लाइन — डेभलपरहरूका लागि

रिपोजिटरी clone गरेर pipeline आफैँ चलाउनुहोस्: [आवश्यकताहरू](#आवश्यकताहरू) बाट सुरु गर्नुहोस्।

Agent हरूले [`AGENTS.md`](../../AGENTS.md) बाट सुरु गर्नुपर्छ।

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>यो रिपोजिटरीमा <a href="../assets/demo.mp4">demo.mp4</a> खोल्नुहोस्।</sub>
</p>

अर्को डेमो:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

निदान प्रतिवेदन (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## आवश्यकताहरू

Python 3.11+। clone गरेपछि virtualenv बनाउनुहोस् र dependency हरू इन्स्टल गर्नुहोस्; त्यसपछि `m2mr` कमान्ड प्रयोग गर्न मिल्छ:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# dependency हरू र यो प्रोजेक्ट इन्स्टल गर्नुहोस्। chumpy (dependency chain को एउटा
# पुरानो प्याकेज) ले आफ्नो setup स्क्रिप्टमा pip import गर्छ, त्यसैले pip को
# पूर्वनिर्धारित isolated build मा "No module named 'pip'" भनेर असफल हुन्छ।
# पहिले isolation बन्द गरेर यसलाई इन्स्टल गर्नुहोस्, अनि यो प्रोजेक्ट इन्स्टल गर्नुहोस्।
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

Inference weight हरू (GVHMR आदि) यो चरणमा डाउनलोड हुँदैनन्। पहिलो `m2mr run` ले तिनलाई `weights/` मा तान्छ (~5 GB, एक पटक मात्र)। पहिलो `m2mr run --detect-hands` ले HaMeR का हातका weight हरू पनि `weights/hamer/` मा तान्छ (~2.7 GB, एक पटक मात्र)।

ffmpeg इन्स्टल गर्न सिफारिस गरिन्छ (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`)।
यो बिना पनि pipeline चल्छ, तर आउटपुट भिडियोहरू **आवाजविहीन** हुन्छन् र ब्राउजरमा चल्दैनन्।

## चलाउनु अघि: यी फाइलहरू `assets/` मा राख्नुहोस्

यो रिपोजिटरीमा यी फाइलहरू समावेश छैनन्; तपाईं आफैंले ल्याउनुपर्छ। SMPL-X को फाइल नाम तालिकासँग ठ्याक्कै मिल्नुपर्छ; FBX, भिडियो र फोटोको नाम जुनसुकै हुन सक्छ। प्रत्येक run लाई SMPL-X, एउटा Mixamo क्यारेक्टर, र **कि त** एउटा भिडियो **कि त** एउटा फोटो चाहिन्छ। Cinema 4D बाट फेरि export गरिएका Mixamo पात्रहरू पनि चल्छन्; थप जानकारीका लागि [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md) हेर्नुहोस्।

| के | कहाँ | कहाँबाट पाउने |
|---|---|---|
| SMPL-X शरीर मोडेल | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | [SMPL-X](https://smpl-x.is.tue.mpg.de/) मा दर्ता गरेर डाउनलोड गर्नुहोस् |
| Mixamo क्यारेक्टर FBX | `assets/mixamo/Y_Bot.fbx` | Adobe खाता प्रयोग गरेर [Mixamo](https://www.mixamo.com) बाट Y Bot (वा Mixamo ले rig गरेको अरू कुनै क्यारेक्टर) डाउनलोड गर्नुहोस् |
| एक्सन भिडियो | `assets/video/<your_clip>.mp4` | **ठ्याक्कै एक जना** स्पष्ट देखिने व्यक्ति भएको, **टाउकोदेखि खुट्टासम्म सधैं फ्रेमभित्र** रहेको क्लिप (धेरै फाइल राख्न सकिन्छ; हरेक run ले सबैभन्दा पछि थपिएको फाइल प्रयोग गर्छ) |
| पोज फोटो (ऐच्छिक) | `assets/image/<your_photo>.jpg` | **ठ्याक्कै एक जना** स्पष्ट देखिने व्यक्ति भएको, **टाउकोदेखि खुट्टासम्म फ्रेमभित्र** रहेको फोटो। `--image` सँग प्रयोग गर्नुहोस् |
| MANO दायाँ हात (`--detect-hands` का लागि मात्र) | `assets/body_models/mano/MANO_RIGHT.pkl` | [MANO](https://mano.is.tue.mpg.de/) मा दर्ता भएर **Models & Code** डाउनलोड गर्नुहोस्। शरीर मात्रको रनलाई यो फाइल चाहिँदैन |

ध्यान दिनुहोस्: Mixamo बाट डाउनलोड हुने फाइलको नाम `Y Bot.fbx` (**खाली ठाउँ सहित**) हुन्छ, जुन तालिकाको `Y_Bot.fbx` (**underscore सहित**) भन्दा एउटा अक्षरले मात्र फरक छ।
यसलाई underscore भएको नाममा बदल्नुभयो भने यो पूर्वनिर्धारित rig बन्छ (`--rig` बिना `m2mr run`)। खाली ठाउँ नै राख्दा पनि हुन्छ — `Y_Bot.fbx` नभए `assets/mixamo/` को पहिलो `.fbx` प्रयोग हुन्छ।

`assets/video/` मा धेरै भिडियो राख्न सकिन्छ। `--video` वा `--image` नदिँदा run ले `assets/video/` मा **सबैभन्दा पछि थपिएको** फाइल प्रयोग गर्छ; त्यो फोल्डर खाली भए `assets/image/` को सबैभन्दा नयाँ फोटो प्रयोग गर्छ।
हरेक क्लिप वा फोटोमा एक जना मात्र व्यक्ति, **टाउकोदेखि खुट्टासम्म फ्रेमभित्र** हुनुपर्छ — किनारमा केही काटिएको हुनु हुँदैन। फ्रेममा दुई जना देखिए `m2mr doctor` / `m2mr run` extraction अघि नै रोकिन्छ।

## छिटो सुरुवात

नतिजाहरू `outputs/<run-time>_<source>/` मा राखिन्छन्। भिडियो run ले `videos/` मा लेख्छ; फोटो run ले `images/` मा लेख्छ।

### 1. assets र वातावरण जाँच गर्नुहोस्

नपुगेका सबै कुरा कहाँबाट डाउनलोड गर्ने र कहाँ राख्ने भन्ने जानकारीसहित देखाइन्छ।

```bash
m2mr doctor
```

`m2mr doctor` ले शरीरको रन जाँच्छ। MANO हात मोडेल अनिवार्य गर्दैन। औँला पत्ता लगाउन प्रयोग हुने थप फाइल र Python प्याकेजहरू पनि जाँच्न:

```bash
m2mr doctor --detect-hands
```

### 2. पहिलो run: स्क्रिनमा नतिजा हेर्नुहोस्

कुनै flag नदिँदा यसले **`assets/video/` को सबैभन्दा नयाँ फाइल** र `assets/mixamo/Y_Bot.fbx` प्रयोग गर्छ।

```bash
m2mr run
```

यो ढिलो चरण हो। पहिलो run ले ~5 GB inference weight डाउनलोड गर्छ (एक पटक मात्र), अनि भिडियोबाट मानिसको चाल निकाल्छ।
CPU मा ~30 सेकेन्डको क्लिपको extraction मा करिब 8–15 मिनेट लाग्छ; weight हरू भइसकेपछि उस्तै लम्बाइका पछिल्ला run हरूमा करिब 3–5 मिनेट लाग्छ।
Retargeting र render मा सामान्यतया एक-दुई मिनेट लाग्छ। अर्को खण्डमा `--skeleton` प्रयोग गरेर skeleton पुनः प्रयोग गर्दा extraction पूरै छोडिन्छ र केही दशक सेकेन्डमै सकिन्छ।

टेकेको खुट्टा पूर्वनिर्धारित रूपमा अडिन्छ: पञ्जा तल छ भने पञ्जा, औँला उठेका बेला मात्र कुर्कुच्चा। सीधा खुट्टाले त्यो बिन्दु पुग्दैन भने कम्मर सर्छ। अनि तलुवा भुइँमा (y = 0) राखिन्छ। `--no-foot-lock` ले कच्चा retarget राख्छ, त्यसैले खुट्टा चिप्लिन सक्छ; तलुवा चाहिँ भुइँमै राखिन्छ।

### 3. उही चाल, अर्को क्यारेक्टर

Mixamo बाट अर्को क्यारेक्टर `assets/mixamo/` मा डाउनलोड गर्नुहोस्। **केवल `--rig` दिएर फेरि नचलाउनुहोस्** — त्यसले ढिलो extraction दोहोर्याउँछ।
अघिल्लो run को skeleton पुनः प्रयोग गर्न `--skeleton` दिनुहोस्; मिनेटहरू केही दशक सेकेन्डमा झर्छन्:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. अर्को भिडियो

`--video` ले क्लिप छान्छ। यसलाई `--rig` सँग स्वतन्त्र रूपमा जोड्न सकिन्छ।

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. स्थिर फोटो (स्थिर पोज)

`--image` ले एक जना व्यक्तिको फोटोबाट **स्थिर 3D पोज** निकाल्छ, अनि भिडियो run जस्तै गरी Mixamo क्यारेक्टरमा retarget गर्छ। प्रिभ्युमा `images/` भित्र चारवटा स्थिर तस्बिर (भिडियो run कै दृश्यहरू) र बायाँ/दायाँ घुम्ने orbit क्लिप `before_after_360_compare.mp4` हुन्छन्। एकै साथ `--video` नदिनुहोस्।

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

path बिनाको `--image` ले `assets/image/` मा सबैभन्दा पछि थपिएको फाइल प्रयोग गर्छ।

### 6. self-intersection जाँच गर्नुहोस्

हरेक run ले तयार भएको क्यारेक्टरमा **self-intersection** पनि जाँच्छ — शरीरको एउटा भाग अर्को भागभित्र पस्नु, जस्तै हात टाउकोभित्र — र `diagnostics.json` लेख्छ। टर्मिनलले एउटा लाइन देखाउँछ, जस्तै `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm`। भुइँ जाँच गरिँदैन।

कुनै run फेरि जाँच्न, वा समस्याहरू हेर्न:

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json फेरि लेख्छ
m2mr diagnose outputs/<run> --visualize      # diagnostics.html पनि: क्यारेक्टरसँगै स्रोत भिडियो, timeline, क्लिक गर्न मिल्ने समस्या सूची
m2mr diagnose outputs/<run> --threshold-cm 2 # 2 cm भन्दा गहिरो पसाइ मात्र रिपोर्ट गर्छ (पूर्वनिर्धारित 1)
```

`diagnostics.json` मा हरेक समस्या शरीरका दुई भागको जोडी हो, साथमा ती भाग एकअर्कामा पसेका frame दायरा, सबैभन्दा खराब frame र त्यसको गहिराइ हुन्छ। frame नम्बर 0 बाट गनिन्छ, glTF import पछि Blender को timeline जस्तै। जोर्नीले जोडिएका भागहरू (पाखुराको माथिल्लो र तल्लो भाग, धड र तिघ्रा, …) तुलना गरिँदैनन्: जुनसुकै पोजमा पनि जोर्नी वरिपरि तिनको छाला खप्टिन्छ। `diagnostics.html` ले स्रोत भिडियो embed गर्छ (`ffmpeg` चाहिन्छ) र three.js CDN बाट लोड गर्छ, त्यसैले यसको 3D दृश्यलाई इन्टरनेट जडान चाहिन्छ। त्यो दृश्यले y = 0 मा स्थिर भुइँ चिन्ह कोर्छ: हरेक 0.5 मिटरमा क्रस, हरेक मिटरमा ठूलो, र मूलबिन्दुमा हरियो क्रस, ताकि क्यारेक्टर चलिरहेको छ कि छैन भनेर देखियोस्। प्रतिच्छेदन ट्र्याकमाथिको एम्बर लेन आँखाले देखेका टिप्पणीका लागि हो (एउटा दायरा तान्नुहोस्, वा **In** / **Out**)। दायाँको **Notes** सूचीले ती देखाउँछ; एउटा पङ्क्तिमा क्लिक गर्दा त्यहाँ पुगिन्छ। **Download notes** ले यी टिप्पणी र प्रतिच्छेदन सूची सँगै बचत गर्छ। फाइलको नाम स्रोत भिडियोको नाम हो, र त्यसको पथ पनि लेखिएको हुन्छ।

### 7. औँला (`--detect-hands`)

साधारण `m2mr run` ले शरीर मात्र चलाउँछ र Mixamo का औँलाका हड्डी विश्राममा छोड्छ। `--detect-hands` ले शरीर निकाल्नेसँगै आउने हात मोडेल खोल्छ। पूर्वनिर्धारित निकाल्ने GVHMR मा त्यो मोडेल [HaMeR](https://github.com/geopavlakos/hamer) हो। HaMeR ले GVHMR ले पहिले नै रोजेका व्यक्ति र frame बाट नाडी काट्छ। क्लिपभित्र अर्को व्यक्ति खोज्दैन।

**समय लगभग दोब्बर हुन्छ।** फ्ल्याग बिना केही मिनेटमा सकिने क्लिप `--detect-hands` सँग लगभग दोब्बर लाग्छ, किनभने हातको पास शरीर निकाल्ने काममाथि चल्छ। लामो भिडियोमा सुरु गर्नुअघि यो समय जोड्नुहोस्।

माथिको तालिकाअनुसार `MANO_RIGHT.pkl` राख्नुहोस्, अनि:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

पहिलो `--detect-hands` रनले HaMeR का weight `weights/hamer/` मा डाउनलोड गर्छ (~2.7 GB, एक पटक)। औँलाका परिक्रमा `skeleton_motion.npz` मा लेखिन्छन् र skin भएको क्यारेक्टरका 30 वटा Mixamo औँलाका हड्डी चलाउँछन्। शरीरको पासले स्पष्ट नदेखेको नाडी त्यो हातका लागि विश्राममा रहन्छ।

`--hand-smooth` ले ती परिक्रमामा कति सेकेन्डको समतल लगाउने बताउँछ। पूर्वनिर्धारित `0.08` हो। `0` ले कच्चा अनुमान राख्छ। skeleton फाइलमा पहिले नै हातको चाल छ भने समतल चल्छ, त्यो फाइल मात्र पुनः प्रयोग गर्ने पछिको रनमा पनि।

अघिल्लो skeleton पुनः प्रयोग गर्दा:

- फाइलमा पहिले नै हातको चाल छ: `--skeleton` ले औँला आफैँ चलाउँछ। `--detect-hands` फेरि चाहिँदैन।
- चाल छैन, तर त्यो रनको शरीरको cache अझै छेउमै छ (`cache/<clip>/0_input_video.mp4`, साथमा `preprocess/vitpose.pt` र `preprocess/bbx.pt`): `--skeleton ... --detect-hands` ले शरीर फेरि ननिकाली औँला थप्छ।
- त्यो cache छैन: भिडियो वा फोटो `--detect-hands` सँग फेरि चलाउनुहोस्।

## आउटपुट

हरेक `m2mr run` ले **कमान्ड सुरु भएको समय** अनुसार नाम दिइएको डाइरेक्टरी बनाउँछ। root मा रहेका फाइलहरू भिडियो र फोटो दुवैका लागि उस्तै हुन्छन्; प्रिभ्यु फोल्डर मात्र फरक हुन्छ।

```
outputs/20260829_193205_dance/          # फोटोका लागि …_pose/
├── run.json                            # सुरु समय, इनपुट, पूरा कमान्ड
├── skeleton_motion.npz                 # मानिसको 3D skeleton (--skeleton सँग पुनः प्रयोग गर्नुहोस्)
├── mixamo_rotations.npz                # हड्डी अनुसार Mixamo rotation
├── mixamo_character.glb                # skin गरिएको क्यारेक्टर, Blender / Unity मा import गर्नुहोस्
├── diagnostics.json                    # self-intersection रिपोर्ट (छिटो सुरुवातको चरण 6 हेर्नुहोस्)
├── diagnostics.html                    # `m2mr diagnose <run> --visualize` पछि मात्र
└── videos/   वा   images/              # प्रिभ्यु — इनपुटमा भर पर्छ
```

**भिडियो इनपुट** ले `videos/` मा लेख्छ (क्लिपकै aspect ratio मा):

```
videos/
├── human_skeleton.mp4                  # पुनर्निर्माण गरिएको मानिसको 3D skeleton
├── mixamo_skeleton.mp4                 # Mixamo rig को skeleton
├── mixamo_character.mp4                # skin गरिएको Mixamo क्यारेक्टर
└── compare.mp4                         # 2×2: मूल (माथि बायाँ) / Mixamo skeleton (माथि दायाँ)
                                        #      मानिसको skeleton (तल बायाँ) / क्यारेक्टर (तल दायाँ)
```

**फोटो इनपुट** ले यसको सट्टा `images/` मा लेख्छ (उही चारवटा दृश्य, साथै एक पूरा घुमाइ):

```
images/
├── human_skeleton.png                  # पुनर्निर्माण गरिएको मानिसको 3D skeleton
├── mixamo_skeleton.png                 # Mixamo rig को skeleton
├── mixamo_character.png                # skin गरिएको Mixamo क्यारेक्टर
├── compare.png                         # 2×2: मूल (माथि बायाँ) / Mixamo skeleton (माथि दायाँ)
│                                       #      मानिसको skeleton (तल बायाँ) / क्यारेक्टर (तल दायाँ)
└── before_after_360_compare.mp4        # बायाँ: मूल फोटो
                                        # दायाँ: rig वरिपरि 10° का दरले orbit (एक पूरा फन्को)
```

`--detect-hands` हुँदा `skeleton_motion.npz` मा औँलाका परिक्रमा पनि रहन्छन्, र `mixamo_rotations.npz` तथा `mixamo_character.glb` मा 30 वटा औँलाका हड्डी हुन्छन्। त्यो फ्ल्याग नभएमा, र पुनः प्रयोग गरिएको skeleton मा पनि हातको चाल नभएमा, ती हड्डी विश्राममा रहन्छन्।

`mixamo_character.glb` लाई Blender मा खोल्नुहोस्: File → Import → glTF 2.0 (.glb/.gltf)। क्यामेरा खाली ठाउँतिर फर्केको छ भने क्यारेक्टरको mesh छानेर View → Frame Selected प्रयोग गर्नुहोस्। टाउको र हातमा देखिने गोलाहरूको झुप्पा हड्डीको display हो, mesh होइन: Outliner मा **Icosphere** र **armature** लुकाउनुहोस्; skin गरिएको mesh देखिने नै राख्नुहोस्। playback स्रोतसँग र frame नम्बर `diagnostics.json` सँग मिलोस् भनेर scene को FPS `run.json` (`fps`) अनुसार र timeline लाई frame 0 देखि `n_frames` − 1 सम्म सेट गर्नुहोस्। भिडियो run लाई `videos/mixamo_character.mp4` सँग, र फोटो run लाई `images/mixamo_character.png` वा orbit क्लिपसँग तुलना गर्नुहोस्।

## लाइसेन्स

यो रिपोजिटरीको कोड Apache-2.0 अन्तर्गत छ। तपाईं आफैंले डाउनलोड गर्ने assets का आफ्नै सर्तहरू छन्, र तिनलाई यो repo सँगै पुनः वितरण गर्नु हुँदैन:

- **SMPL-X**: MPI मार्फत पहुँच; पूर्वनिर्धारित रूपमा गैर-व्यावसायिक अनुसन्धान / शिक्षा / कला मात्र; व्यावसायिक प्रयोगका लागि छुट्टै सम्झौता चाहिन्छ
- **MANO** (`--detect-hands` प्रयोग गर्दा मात्र): MPI मार्फत पहुँच, SMPL-X जस्तै डाउनलोड; `MANO_RIGHT.pkl` स्थानीय राख्नुहोस् र पुनः वितरण नगर्नुहोस्
- **Mixamo FBX**: प्रकाशित उत्पादनमा प्रयोग गर्न मिल्छ; कच्चा FBX लाई asset pack को रूपमा पुनः वितरण नगर्नुहोस्
- **GVHMR र अन्य inference weight हरू**: पहिलो `m2mr run` मा `weights/` मा स्वतः डाउनलोड हुन्छन्, प्रत्येकको मूल प्रोजेक्टको लाइसेन्स अन्तर्गत
- **HaMeR**: यो रिपोजिटरीको inference कोड MIT हो; weight हरू पहिलो `m2mr run --detect-hands` मा `weights/hamer/` मा आउँछन्, मूल प्रकाशनका सर्तअन्तर्गत

## सम्पर्क

कुनै समस्या आएमा, स्थानीय सेटअप पूरा गर्न सहयोग चाहिएमा, वा सहकार्यबारे कुरा गर्न चाहनुहुन्छ भने यो ठेगानामा इमेल गर्नुहोस्:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
