# Motion2MixamoRig

<p align="center">
  <a href="#สิ่งที่ต้องมี"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.th.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · ไทย · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.uk.md">Українська</a> · <a href="README.cs.md">Čeština</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.sv.md">Svenska</a>
</p>

ถ่ายทอดการเคลื่อนไหวของคนในวิดีโอ — หรือท่าทางในภาพนิ่ง — ไปยังตัวละคร 3D ที่ริกด้วย Adobe Mixamo

สำหรับนักพัฒนาเกม: ใส่วิดีโอแอ็กชันที่มี **คนเพียงคนเดียว** (หรือภาพนิ่ง) กับตัวละคร Mixamo หนึ่งตัว เครื่องมือจะสร้างวิดีโอพรีวิวและไฟล์ตัวละครที่ skin แล้ว (`.glb`) ซึ่งนำไปใช้ใน Blender หรือ Unity ได้ทันที

> ขณะนี้ Motion2MixamoRig ยังอยู่ในขั้นทดลอง เวอร์ชัน 0.1.8 คือ pipeline แบบบรรทัดคำสั่ง รีโพนี้ยังมี Blender 4.2+ Extension ที่รัน pipeline เดียวกันใน Python environment ภายนอกด้วย การ build add-on จากซอร์สโค้ด: [`blender_extension/README.md`](../../blender_extension/README.md)

## สองวิธีในการใช้งาน

### 🎨 ใน Blender — ไม่ต้องเขียนโค้ด

1. ดาวน์โหลดไฟล์ zip สำหรับแพลตฟอร์มของคุณ เช่น `motion2mixamorig-<version>-macos-arm64.zip` จาก [รีลีสล่าสุด](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)
2. ใน Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…** แล้วเลือกไฟล์ zip
3. 3D Viewport → กด **N** → แท็บ **Motion2MixamoRig** → **ติดตั้งรันไทม์ (คลิกเดียว)** (Install Runtime (one click))
4. **เลือกโมเดล SMPL-X…** (Choose SMPL-X Model…) (ดาวน์โหลดได้ฟรี) แล้วเลือกไฟล์ FBX ตัวละคร Mixamo
5. เลือกวิดีโอที่มีคนเพียงคนเดียว → **สร้างการเคลื่อนไหว** (Generate Motion)

คำแนะนำทีละขั้นตอน เคล็ดลับ และการอัปเดต: **[คู่มือการใช้งาน](user-guide.th.md)** ทดสอบแล้วบน macOS (Apple Silicon)

### 💻 บรรทัดคำสั่ง — สำหรับนักพัฒนา

โคลนรีโพแล้วรัน pipeline ด้วยตัวเอง: เริ่มที่ [สิ่งที่ต้องมี](#สิ่งที่ต้องมี)

Agent ควรเริ่มจาก [`AGENTS.md`](../../AGENTS.md)

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>เปิด <a href="../assets/demo.mp4">demo.mp4</a> ในรีโพนี้</sub>
</p>

เดโมอีกชิ้น:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

รายงานการวินิจฉัย (`diagnostics.html`):

https://github.com/user-attachments/assets/0474ba58-dea7-4538-82a9-cbe35e437c44

## สิ่งที่ต้องมี

Python 3.11+ หลัง clone แล้วให้สร้าง virtualenv และติดตั้ง dependency จากนั้นจะใช้คำสั่ง `m2mr` ได้:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# ติดตั้ง dependency และโปรเจกต์นี้ chumpy (แพ็กเกจเก่าใน dependency chain)
# import pip ในสคริปต์ setup ของมัน จึงล้มเหลวด้วย "No module named 'pip'"
# ภายใต้ isolated build ที่เป็นค่าเริ่มต้นของ pip ให้ติดตั้งมันก่อนโดยปิด
# isolation แล้วค่อยติดตั้งโปรเจกต์นี้
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

ขั้นตอนนี้ไม่ได้ดาวน์โหลด inference weight (GVHMR และอื่น ๆ) การรัน `m2mr run` ครั้งแรกจะดึงมาไว้ที่ `weights/` (~5 GB ครั้งเดียวเท่านั้น) การรัน `m2mr run --detect-hands` ครั้งแรกจะดึง weight มือของ HaMeR มาไว้ที่ `weights/hamer/` ด้วย (~2.7 GB ครั้งเดียวเท่านั้น)

แนะนำให้ติดตั้ง ffmpeg (macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`)
pipeline รันได้แม้ไม่มี แต่วิดีโอที่ได้จะ **ไม่มีเสียง** และเล่นในเบราว์เซอร์ไม่ได้

## ก่อนรัน: วางไฟล์เหล่านี้ไว้ใน `assets/`

รีโพนี้ไม่ได้แนบไฟล์เหล่านี้มา คุณต้องหามาเอง ชื่อไฟล์ SMPL-X ต้องตรงกับตารางทุกตัวอักษร ส่วนชื่อไฟล์ FBX วิดีโอ และภาพตั้งได้ตามใจ การรันแต่ละครั้งต้องมี SMPL-X ตัวละคร Mixamo หนึ่งตัว และ **อย่างใดอย่างหนึ่ง** ระหว่างวิดีโอ **หรือ** ภาพนิ่ง ตัวละคร Mixamo ที่ export ใหม่จาก Cinema 4D ก็ใช้ได้เช่นกัน ดู [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md)

| ไฟล์ | ตำแหน่ง | แหล่งที่มา |
|---|---|---|
| โมเดลร่างกาย SMPL-X | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | ลงทะเบียนที่ [SMPL-X](https://smpl-x.is.tue.mpg.de/) แล้วดาวน์โหลด |
| FBX ตัวละคร Mixamo | `assets/mixamo/Y_Bot.fbx` | ใช้บัญชี Adobe ดาวน์โหลด Y Bot (หรือตัวละครอื่นที่ริกด้วย Mixamo) จาก [Mixamo](https://www.mixamo.com) |
| วิดีโอแอ็กชัน | `assets/video/<your_clip>.mp4` | คลิปที่มีคนเห็นชัด **เพียงคนเดียว** และ **อยู่ในเฟรมตั้งแต่หัวจรดเท้าตลอดเวลา** (เก็บไว้หลายไฟล์ได้ แต่ละครั้งจะใช้ไฟล์ที่เพิ่มล่าสุด) |
| ภาพท่าทาง (ไม่บังคับ) | `assets/image/<your_photo>.jpg` | ภาพถ่ายที่มีคนเห็นชัด **เพียงคนเดียว** และ **อยู่ในเฟรมตั้งแต่หัวจรดเท้า** ใช้กับ `--image` |
| มือขวา MANO (ใช้เมื่อ `--detect-hands` เท่านั้น) | `assets/body_models/mano/MANO_RIGHT.pkl` | ลงทะเบียนที่ [MANO](https://mano.is.tue.mpg.de/) แล้วดาวน์โหลด **Models & Code** การรันเฉพาะลำตัวไม่ต้องใช้ไฟล์นี้ |

หมายเหตุ: ไฟล์ที่ดาวน์โหลดจาก Mixamo ชื่อ `Y Bot.fbx` (**เว้นวรรค**) ต่างจาก `Y_Bot.fbx` (**ขีดล่าง**) ในตารางเพียงหนึ่งตัวอักษร
เปลี่ยนชื่อเป็นแบบขีดล่างแล้วจะกลายเป็น rig ค่าเริ่มต้น (`m2mr run` โดยไม่ต้องใส่ `--rig`) จะคงเว้นวรรคไว้ก็ได้ — ถ้าไม่มี `Y_Bot.fbx` ระบบจะใช้ `.fbx` ไฟล์แรกใน `assets/mixamo/`

`assets/video/` เก็บวิดีโอได้หลายไฟล์ ถ้าไม่ระบุ `--video` หรือ `--image` จะใช้ไฟล์ที่ **เพิ่มล่าสุด** ใน `assets/video/` และถ้าโฟลเดอร์นั้นว่าง จะใช้ภาพนิ่งล่าสุดใน `assets/image/` แทน
แต่ละคลิปหรือภาพต้องมีคนเพียงคนเดียว **อยู่ในเฟรมตั้งแต่หัวจรดเท้า** — ไม่ถูกตัดที่ขอบ `m2mr doctor` / `m2mr run` จะหยุดก่อนขั้นตอน extraction หากมีสองคนอยู่ในเฟรม

## เริ่มต้นอย่างรวดเร็ว

ผลลัพธ์จะอยู่ใน `outputs/<run-time>_<source>/` การรันด้วยวิดีโอจะเขียน `videos/` ส่วนการรันด้วยภาพนิ่งจะเขียน `images/`

### 1. ตรวจสอบ asset และ environment

สิ่งที่ขาดจะถูกพิมพ์ออกมาพร้อมแหล่งดาวน์โหลดและตำแหน่งที่ต้องวาง

```bash
m2mr doctor
```

`m2mr doctor` ตรวจการรันลำตัว ไม่ได้บังคับให้มีโมเดลมือ MANO ถ้าจะตรวจไฟล์เพิ่มและแพ็กเกจ Python ที่ใช้ตรวจนิ้วด้วย:

```bash
m2mr doctor --detect-hands
```

### 2. รันครั้งแรก: ให้มีผลลัพธ์บนหน้าจอ

ถ้าไม่ใส่แฟล็กใด ๆ คำสั่งนี้จะใช้ **ไฟล์ล่าสุดใน `assets/video/`** และ `assets/mixamo/Y_Bot.fbx`

```bash
m2mr run
```

นี่คือขั้นตอนที่ช้า การรันครั้งแรกจะดาวน์โหลด inference weight ~5 GB (ครั้งเดียวเท่านั้น) จากนั้นจึงสกัดการเคลื่อนไหวของคนจากวิดีโอ
บน CPU คลิปยาว ~30 วินาทีใช้เวลา extraction ประมาณ 8–15 นาที การรันครั้งต่อไปที่ยาวใกล้เคียงกัน เมื่อมี weight แล้ว ใช้ประมาณ 3–5 นาที
ขั้นตอน retargeting และ rendering มักใช้หนึ่งถึงสองนาที การใช้ skeleton ซ้ำด้วย `--skeleton` ในหัวข้อถัดไปจะข้าม extraction ทั้งหมดและเสร็จภายในไม่กี่สิบวินาที

เท้าที่เหยียบพื้นจะถูกตรึงไว้เป็นค่าเริ่มต้น: ฝ่าเท้าเมื่อฝ่าเท้าแตะพื้น และส้นเท้าเฉพาะตอนปลายเท้ายกขึ้น ถ้าเหยียดขาแล้วยังไปไม่ถึง สะโพกจะเลื่อนตาม จากนั้นฝ่าเท้าจะถูกวางบนพื้น (y = 0) `--no-foot-lock` เก็บ retarget ดิบไว้ เท้าจึงอาจลื่น แต่ฝ่าเท้าก็ยังถูกวางบนพื้น

### 3. การเคลื่อนไหวเดิม ตัวละครใหม่

ดาวน์โหลดตัวละครอื่นจาก Mixamo มาไว้ใน `assets/mixamo/` **อย่ารันใหม่โดยใส่แค่ `--rig`** — เพราะจะทำ extraction ที่ช้าซ้ำอีกรอบ
ใส่ `--skeleton` เพื่อใช้ skeleton จากการรันครั้งก่อน จากหลายนาทีจะเหลือเพียงไม่กี่สิบวินาที:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. วิดีโออื่น

`--video` ใช้เลือกคลิป ใช้ร่วมกับ `--rig` ได้อย่างอิสระ

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. ภาพนิ่ง (ท่าทางคงที่)

`--image` จะกู้คืน **ท่าทาง 3D แบบคงที่** จากภาพถ่ายของคนหนึ่งคน แล้ว retarget ไปยังตัวละคร Mixamo แบบเดียวกับการรันด้วยวิดีโอ พรีวิวประกอบด้วยภาพนิ่งสี่ภาพใน `images/` (มุมมองเดียวกับการรันด้วยวิดีโอ) และคลิปหมุนซ้าย/ขวา `before_after_360_compare.mp4` อย่าใส่ `--video` พร้อมกัน

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

ถ้าใส่ `--image` โดยไม่ระบุพาธ จะใช้ไฟล์ที่เพิ่มล่าสุดใน `assets/image/`

### 6. ตรวจการทะลุกันเอง

ทุกการรันจะตรวจตัวละครที่ได้ว่ามี **การทะลุกันเอง** หรือไม่ — คือส่วนหนึ่งของร่างกายเข้าไปอยู่ในอีกส่วน เช่น มืออยู่ในหัว — แล้วเขียน `diagnostics.json` เทอร์มินัลจะพิมพ์หนึ่งบรรทัด เช่น `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm` ไม่ได้ตรวจพื้น

หากต้องการตรวจการรันซ้ำ หรือดูว่าปัญหาอยู่ตรงไหน:

```bash
m2mr diagnose outputs/<run>                  # เขียน diagnostics.json ใหม่
m2mr diagnose outputs/<run> --visualize      # สร้าง diagnostics.html ด้วย: วิดีโอต้นฉบับข้างตัวละคร, timeline, รายการปัญหาที่คลิกได้
m2mr diagnose outputs/<run> --threshold-cm 2 # รายงานเฉพาะการทะลุที่ลึกกว่า 2 cm (ค่าเริ่มต้น 1)
```

แต่ละปัญหาใน `diagnostics.json` คือคู่ส่วนของร่างกาย พร้อมช่วงเฟรมที่ทะลุกัน เฟรมที่หนักที่สุด และความลึก หมายเลขเฟรมนับจาก 0 เหมือน timeline ของ Blender หลังนำเข้า glTF ส่วนที่ต่อกันด้วยข้อต่อ (ต้นแขนกับปลายแขน ลำตัวกับต้นขา …) จะไม่ถูกเปรียบเทียบ เพราะผิวบริเวณข้อต่อซ้อนกันในทุกท่า `diagnostics.html` ฝังวิดีโอต้นฉบับไว้ (ต้องมี `ffmpeg`) และโหลด three.js จาก CDN ดังนั้นมุมมอง 3D ต้องเชื่อมต่ออินเทอร์เน็ต มุมมองนี้วาดเครื่องหมายพื้นแบบติดที่ y = 0: กากบาททุก 0.5 ม. กากบาทที่ใหญ่ขึ้นทุกเมตร และกากบาทสีเขียวที่จุดกำเนิด เพื่อดูว่าตัวละครกำลังเคลื่อนที่หรือไม่ เลนสีอำพันเหนือแทร็กที่ทะลุกันใช้จดสิ่งที่ตาเห็น (ลากช่วง หรือ **In** / **Out**) รายการ **Notes** ทางขวาแสดงรายการเหล่านี้ คลิกแถวหนึ่งเพื่อกระโดดไปที่นั่น **Download notes** บันทึกโน้ตเหล่านี้พร้อมรายการที่ทะลุกัน ไฟล์ใช้ชื่อของวิดีโอต้นฉบับ และบันทึกพาธของวิดีโอนั้น

### 7. นิ้ว (`--detect-hands`)

`m2mr run` ธรรมดาขยับเฉพาะลำตัว และปล่อยให้กระดูกนิ้วของ Mixamo อยู่ที่ท่าพัก `--detect-hands` เปิดโมเดลมือที่มากับตัวดึงท่าลำตัว เมื่อใช้ตัวดึงค่าเริ่มต้นอย่าง GVHMR โมเดลนั้นคือ [HaMeR](https://github.com/geopavlakos/hamer) HaMeR ตัดข้อมือจากคนและเฟรมที่ GVHMR เลือกไว้แล้ว ไม่ได้ไปหาคนที่สองในคลิป

**เวลาที่ใช้จะเพิ่มประมาณสองเท่า** คลิปที่ไม่มีแฟล็กแล้วจบในไม่กี่นาที จะใช้เวลาประมาณสองเท่าเมื่อใส่ `--detect-hands` เพราะรอบของมือวิ่งทับบนการดึงท่าลำตัว วิดีโอยาวควรวางเวลาส่วนนี้ไว้ก่อนเริ่ม

วาง `MANO_RIGHT.pkl` ตามตารางด้านบน แล้วจึงรัน:

```bash
m2mr doctor --detect-hands
m2mr run --detect-hands
m2mr run --video assets/video/dance.mp4 --detect-hands --hand-smooth 0.08
```

การรัน `--detect-hands` ครั้งแรกจะดาวน์โหลด weight ของ HaMeR ไปที่ `weights/hamer/` (~2.7 GB ครั้งเดียว) การหมุนของนิ้วถูกเขียนลง `skeleton_motion.npz` และขับกระดูกนิ้ว Mixamo 30 ชิ้นบนตัวละครที่มี skin ข้อมือที่รอบลำตัวมองไม่ชัด จะอยู่ที่ท่าพักสำหรับมือข้างนั้น

`--hand-smooth` คือจำนวนวินาทีที่ใช้เกลี่ยการหมุนเหล่านี้ ค่าเริ่มต้นคือ `0.08` ค่า `0` เก็บค่าประมาณดิบไว้ การเกลี่ยจะทำงานเมื่อไฟล์ skeleton มีท่ามืออยู่แล้ว รวมถึงการรันทีหลังที่นำไฟล์นั้นกลับมาใช้เพียงอย่างเดียว

เมื่อนำ skeleton ครั้งก่อนกลับมาใช้:

- ไฟล์มีท่ามืออยู่แล้ว: `--skeleton` ขับนิ้วได้เอง ไม่ต้องใส่ `--detect-hands` อีก
- ยังไม่มี แต่แคชลำตัวของการรันนั้นยังอยู่ข้าง ๆ (`cache/<clip>/0_input_video.mp4` พร้อม `preprocess/vitpose.pt` และ `preprocess/bbx.pt`): `--skeleton ... --detect-hands` เติมนิ้วได้โดยไม่ต้องดึงท่าลำตัวใหม่
- แคชนั้นหายไปแล้ว: รันวิดีโอหรือภาพอีกครั้งพร้อม `--detect-hands`

## ผลลัพธ์

การรัน `m2mr run` แต่ละครั้งจะสร้างไดเรกทอรีที่ตั้งชื่อตาม **เวลาที่คำสั่งเริ่มทำงาน** ไฟล์ที่ระดับบนสุดเหมือนกันทั้งวิดีโอและภาพนิ่ง มีเพียงโฟลเดอร์พรีวิวที่ต่างกัน

```
outputs/20260829_193205_dance/          # หรือ …_pose/ สำหรับภาพนิ่ง
├── run.json                            # เวลาเริ่ม อินพุต และคำสั่งทั้งหมด
├── skeleton_motion.npz                 # skeleton 3D ของคน (ใช้ซ้ำด้วย --skeleton)
├── mixamo_rotations.npz                # การหมุนของ Mixamo แยกตามกระดูก
├── mixamo_character.glb                # ตัวละครที่ skin แล้ว นำเข้า Blender / Unity
├── diagnostics.json                    # รายงานการทะลุกันเอง (ดูขั้นตอนที่ 6 ในเริ่มต้นอย่างรวดเร็ว)
├── diagnostics.html                    # มีเฉพาะหลัง `m2mr diagnose <run> --visualize`
└── videos/   หรือ   images/            # พรีวิว — ขึ้นกับอินพุต
```

**อินพุตวิดีโอ** จะเขียน `videos/` (อัตราส่วนภาพเดียวกับคลิป):

```
videos/
├── human_skeleton.mp4                  # skeleton 3D ของคนที่กู้คืนได้
├── mixamo_skeleton.mp4                 # skeleton ของ Mixamo rig
├── mixamo_character.mp4                # ตัวละคร Mixamo ที่ skin แล้ว
└── compare.mp4                         # 2×2: ต้นฉบับ (บนซ้าย) / skeleton Mixamo (บนขวา)
                                        #      skeleton คน (ล่างซ้าย) / ตัวละคร (ล่างขวา)
```

**อินพุตภาพนิ่ง** จะเขียน `images/` แทน (สี่มุมมองเดิม บวกภาพหมุนรอบตัว):

```
images/
├── human_skeleton.png                  # skeleton 3D ของคนที่กู้คืนได้
├── mixamo_skeleton.png                 # skeleton ของ Mixamo rig
├── mixamo_character.png                # ตัวละคร Mixamo ที่ skin แล้ว
├── compare.png                         # 2×2: ต้นฉบับ (บนซ้าย) / skeleton Mixamo (บนขวา)
│                                       #      skeleton คน (ล่างซ้าย) / ตัวละคร (ล่างขวา)
└── before_after_360_compare.mp4        # ซ้าย: ภาพต้นฉบับ
                                        # ขวา: หมุนรอบ rig ทีละ 10° (ครบหนึ่งรอบ)
```

เมื่อใส่ `--detect-hands` ไฟล์ `skeleton_motion.npz` จะเก็บการหมุนของนิ้วด้วย และ `mixamo_rotations.npz` กับ `mixamo_character.glb` จะมีกระดูกนิ้ว 30 ชิ้น ถ้าไม่มีแฟล็กนี้ และ skeleton ที่นำกลับมาใช้ก็ไม่มีท่ามือ กระดูกเหล่านั้นจะค้างที่ท่าพัก

เปิด `mixamo_character.glb` ใน Blender: File → Import → glTF 2.0 (.glb/.gltf) ถ้ากล้องหันไปที่พื้นที่ว่าง ให้เลือก mesh ของตัวละครแล้วใช้ View → Frame Selected กลุ่มทรงกลมที่หัวและมือคือการแสดงกระดูก ไม่ใช่ mesh: ใน Outliner ให้ซ่อน **Icosphere** และ **armature** แล้วปล่อยให้ mesh ที่ skin แล้วยังมองเห็นอยู่ ตั้งค่า FPS ของ scene ตาม `run.json` (`fps`) และตั้ง timeline เป็นเฟรม 0 ถึง `n_frames` − 1 เพื่อให้การเล่นตรงกับต้นฉบับและหมายเลขเฟรมตรงกับ `diagnostics.json` เปรียบเทียบการรันด้วยวิดีโอกับ `videos/mixamo_character.mp4` และการรันด้วยภาพนิ่งกับ `images/mixamo_character.png` หรือคลิปหมุนรอบ

## สัญญาอนุญาต

โค้ดในรีโพนี้ใช้สัญญาอนุญาต Apache-2.0 asset ที่คุณดาวน์โหลดเองมีเงื่อนไขของตัวเอง และห้ามแจกจ่ายต่อพร้อมกับรีโพนี้:

- **SMPL-X**: ต้องขอสิทธิ์จาก MPI โดยค่าเริ่มต้นใช้ได้เฉพาะงานวิจัย / การศึกษา / ศิลปะที่ไม่ใช่เชิงพาณิชย์ การใช้เชิงพาณิชย์ต้องทำข้อตกลงแยก
- **MANO** (เฉพาะเมื่อใช้ `--detect-hands`): ต้องขอสิทธิ์จาก MPI เช่นเดียวกับ SMPL-X วาง `MANO_RIGHT.pkl` ไว้ในเครื่อง และอย่าแจกจ่ายต่อ
- **Mixamo FBX**: ใช้ในผลิตภัณฑ์ที่เผยแพร่ได้ แต่ห้ามแจกจ่ายไฟล์ FBX ดิบเป็นชุด asset
- **GVHMR และ inference weight อื่น ๆ**: ดาวน์โหลดอัตโนมัติไปที่ `weights/` ในการรัน `m2mr run` ครั้งแรก ภายใต้สัญญาอนุญาตของแต่ละโปรเจกต์ต้นทาง
- **HaMeR**: โค้ดอนุมานในรีโพนี้เป็น MIT weight จะถูกดาวน์โหลดไปที่ `weights/hamer/` ในการรัน `m2mr run --detect-hands` ครั้งแรก ตามเงื่อนไขการเผยแพร่ของต้นทาง

## ติดต่อ

หากพบปัญหา ต้องการความช่วยเหลือในการตั้งค่าบนเครื่อง หรืออยากพูดคุยเรื่องความร่วมมือ ส่งอีเมลมาที่:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
