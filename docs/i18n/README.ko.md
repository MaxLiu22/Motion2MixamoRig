# Motion2MixamoRig

<p align="center">
  <a href="#사전-요구-사항"><img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white"></a>
  <a href="user-guide.ko.md"><img alt="Blender 4.2+" src="https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white"></a>
  <a href="https://github.com/MaxLiu22/Motion2MixamoRig/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MaxLiu22/Motion2MixamoRig?style=social"></a>
</p>

![Motion2MixamoRig](../assets/repo_poster.png)

<p align="center">
  <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="../../README.md">English</a> · 한국어 · <a href="README.ja.md">日本語</a> · <a href="README.de.md">Deutsch</a> · <a href="README.ru.md">Русский</a> · <a href="README.ar.md">العربية</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.fil.md">Filipino</a> · <a href="README.th.md">ไทย</a> · <a href="README.fr.md">Français</a> · <a href="README.es-MX.md">Español</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.ne.md">नेपाली</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.pl.md">Polski</a> · <a href="README.nl.md">Nederlands</a>
</p>

영상 속 사람의 동작 — 또는 사진 속 자세 — 를 Adobe Mixamo rig 3D 캐릭터로 옮깁니다.

게임 개발자를 위한 도구입니다. **한 사람만** 나오는 동작 영상(또는 사진)과 Mixamo 캐릭터를 넣으면 미리보기와, Blender / Unity에 바로 넣을 수 있는 스키닝된 캐릭터 파일(`.glb`)을 생성합니다.

> Motion2MixamoRig는 아직 실험 단계입니다. v0.1.7은 명령줄 파이프라인입니다. 이 저장소의 Blender 4.2+ Extension은 같은 파이프라인을 외부 Python에서 실행합니다. 소스에서 애드온 빌드하기: [`blender_extension/README.md`](../../blender_extension/README.md).

## 두 가지 사용 방법

### 🎨 Blender에서 — 코딩 없이

1. [최신 릴리스](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)에서 내 플랫폼용 zip(예: `motion2mixamorig-<version>-macos-arm64.zip`)을 다운로드합니다.
2. Blender: **Edit → Preferences → Get Extensions → ∨ → Install from Disk…** → zip 선택.
3. 3D Viewport → **N** 누르기 → **Motion2MixamoRig** 탭 → **런타임 설치 (원클릭)** (Install Runtime (one click)).
4. **SMPL-X 모델 선택…** (Choose SMPL-X Model…)으로 모델(무료 다운로드)을 지정하고, Mixamo 캐릭터 FBX를 고릅니다.
5. 한 사람이 나오는 영상 선택 → **모션 생성** (Generate Motion).

단계별 안내, 팁, 업데이트 방법: **[사용 가이드](user-guide.ko.md)**. macOS (Apple Silicon)에서 테스트했습니다.

### 💻 명령줄 — 개발자용

저장소를 클론하고 파이프라인을 직접 실행하세요. [사전 요구 사항](#사전-요구-사항)부터 시작하면 됩니다.

Agent는 먼저 [`AGENTS.md`](../../AGENTS.md)를 읽어 주세요.

https://github.com/user-attachments/assets/37c67642-f36c-4815-bcf3-028ed9546a2f

<p align="center">
  <sub>이 저장소의 <a href="../assets/demo.mp4">demo.mp4</a>를 열어 주세요.</sub>
</p>

다른 데모:

https://github.com/user-attachments/assets/073f20c8-7283-4209-98e8-f247228bfd56

## 사전 요구 사항

Python 3.11+가 필요합니다. 클론한 뒤 가상환경을 만들고 의존성을 설치하면 `m2mr` 명령을 쓸 수 있습니다:

```bash
git clone https://github.com/MaxLiu22/Motion2MixamoRig.git
cd Motion2MixamoRig
python -m venv .venv && source .venv/bin/activate

# 의존성과 이 프로젝트를 설치합니다. chumpy(의존성 체인의 오래된 패키지)의
# 빌드 스크립트가 pip를 import하는데, pip 기본 격리 빌드에서는
# "No module named 'pip'"로 실패합니다. 격리를 끄고(--no-build-isolation)
# 먼저 설치한 뒤 이 프로젝트를 설치하세요.
pip install --upgrade pip setuptools wheel \
  && pip install "numpy>=1.26" \
  && pip install --no-build-isolation "chumpy==0.70" \
  && pip install -e .
```

추론 가중치(GVHMR 등)는 이 단계에서 받지 않습니다. 첫 `m2mr run` 때 `weights/`로 자동 다운로드됩니다(약 5 GB, 한 번만).

ffmpeg도 권장합니다(macOS: `brew install ffmpeg`, Ubuntu: `apt install ffmpeg`).
없어도 실행되지만, 출력 영상에 **소리가 없고** 브라우저에서 바로 재생되지 않습니다.

## 실행 전: 이것을 `assets/`에 넣으세요

이 저장소는 해당 파일을 포함하지 않습니다. 직접 준비해야 합니다. SMPL-X 파일명은 아래 표와 한 글자도 같아야 합니다. FBX, 영상, 사진 이름은 상관없습니다. 한 번의 실행에는 SMPL-X, Mixamo 캐릭터, 그리고 **영상 또는 사진 중 하나**가 필요합니다. Cinema 4D에서 다시 내보낸 Mixamo 캐릭터 FBX도 사용할 수 있습니다. 자세한 내용은 [`docs/c4d-fbx-support.md`](../c4d-fbx-support.md)를 참고하세요.

| 무엇 | 어디에 | 어디서 |
|---|---|---|
| SMPL-X 바디 모델 | `assets/body_models/smplx/SMPLX_NEUTRAL.npz` | [SMPL-X](https://smpl-x.is.tue.mpg.de/)에서 등록한 뒤 다운로드 |
| Mixamo 캐릭터 FBX | `assets/mixamo/Y_Bot.fbx` | Adobe 계정으로 [Mixamo](https://www.mixamo.com)에서 Y Bot(또는 다른 Mixamo rig 캐릭터) 다운로드 |
| 동작 영상 | `assets/video/<your_clip>.mp4` | **사람 한 명만**, 잘 보이고, **머리부터 발끝까지 영상 내내 화면 안에** (여러 파일 가능, 실행마다 가장 최근에 넣은 것 사용) |
| 자세 사진(선택) | `assets/image/<your_photo>.jpg` | **사람 한 명만**, 잘 보이고, **머리부터 발끝까지 화면 안에**. `--image`와 함께 사용 |

주의: Mixamo에서 받은 파일은 `Y Bot.fbx`(**공백**)이고, 표의 `Y_Bot.fbx`(**밑줄**)과 한 글자 다릅니다.
밑줄로 바꾸면 기본 rig가 되어 `m2mr run`에 `--rig` 없이 씁니다. 이름을 안 바꿔도 됩니다 — `Y_Bot.fbx`가 없으면 `assets/mixamo/`의 첫 `.fbx`를 씁니다.

`assets/video/`에는 영상을 여러 개 넣을 수 있습니다. `--video`나 `--image`를 지정하지 않으면 **`assets/video/`에 가장 마지막에 넣은** 파일을 쓰고, 그 폴더가 비어 있으면 `assets/image/`의 최신 사진을 씁니다.
각 영상이나 사진에는 사람이 한 명만 나와야 하고, **머리부터 발끝까지 화면 안**에 있어야 하며 화면 밖으로 나가면 안 됩니다. `m2mr doctor` / `m2mr run`이 두 명이 보이면 추출 전에 멈춥니다.

## 빠른 시작

결과는 `outputs/<실행시각>_<입력명>/`에 있습니다. 영상 입력은 `videos/`, 사진 입력은 `images/`에 씁니다.

### 1. 자산과 환경 확인

빠진 것은 어디서 받고 어디에 넣을지 함께 출력합니다.

```bash
m2mr doctor
```

### 2. 첫 실행: 화면에 결과 띄우기

플래그 없이 실행하면 **`assets/video/`에서 가장 최근 파일**과 `assets/mixamo/Y_Bot.fbx`를 씁니다.

```bash
m2mr run
```

이 단계가 가장 느립니다. 첫 실행은 약 5 GB 추론 가중치를 받은 뒤(한 번만) 영상에서 사람 동작을 추출합니다.
약 30초 영상은 CPU에서 추출에 대략 8–15분, 가중치가 이미 있으면 비슷한 길이에 3–5분입니다.
리타게팅과 렌더링은 보통 1–2분입니다. 다음 절의 `--skeleton`으로 스켈레톤을 재사용하면 추출을 건너뛰어 수십 초면 끝납니다.

### 3. 같은 동작, 다른 캐릭터

Mixamo에서 다른 캐릭터를 `assets/mixamo/`에 넣으세요. **`--rig`만 바꿔 다시 돌리지 마세요** — 느린 추출이 그대로 반복됩니다.
`--skeleton`으로 이전 실행의 스켈레톤을 재사용하면 몇 분이 수십 초가 됩니다:

```bash
m2mr run --skeleton outputs/<previous-run-dir>/skeleton_motion.npz --rig assets/mixamo/Vampire.fbx
```

### 4. 다른 영상

`--video`로 클립을 고릅니다. `--rig`와 자유롭게 조합됩니다.

```bash
m2mr run --video assets/video/dance.mp4 --rig assets/mixamo/Vampire.fbx
```

### 5. 사진(정적 자세)

`--image`는 **한 사람** 사진에서 **정적 3D 자세**를 복원한 뒤, 영상 실행과 같은 경로로 Mixamo 캐릭터에 옮깁니다. 미리보기는 `images/`의 네 장(영상 실행과 같은 뷰)과 좌우 비교 궤도 클립 `before_after_360_compare.mp4`입니다. `--video`와 함께 쓰지 마세요.

```bash
m2mr run --image assets/image/pose.jpg
m2mr run --image assets/image/pose.jpg --rig assets/mixamo/Vampire.fbx
```

경로 없이 `--image`만 쓰면 `assets/image/`에 가장 최근에 넣은 파일을 씁니다.

### 6. 자기 교차(파고듦) 확인

모든 실행은 완성된 캐릭터의 **자기 교차**(한 신체 부위가 다른 부위로 파고드는 것, 예: 손이 머리 안으로 들어감)도 확인하고 `diagnostics.json`을 씁니다. 터미널에는 `diagnostics: 14 self-intersection(s) over 116 of 719 frames, deepest 7.87 cm` 같은 한 줄이 출력됩니다. 바닥은 확인하지 않습니다.

실행을 다시 확인하거나 문제를 눈으로 보려면:

```bash
m2mr diagnose outputs/<run>                  # diagnostics.json 다시 쓰기
m2mr diagnose outputs/<run> --visualize      # diagnostics.html도 생성: 원본 영상과 캐릭터 나란히, 타임라인, 클릭 가능한 문제 목록
m2mr diagnose outputs/<run> --threshold-cm 2 # 2 cm보다 깊은 파고듦만 보고 (기본값 1)
```

`diagnostics.json`의 각 문제는 신체 부위 한 쌍과, 두 부위가 교차하는 프레임 범위, 가장 심한 프레임과 그 깊이입니다. 프레임 번호는 glTF를 Blender로 임포트한 뒤의 타임라인처럼 0부터 셉니다. 관절로 이어진 부위(위팔과 아래팔, 몸통과 허벅지 등)는 비교하지 않습니다. 어떤 자세에서도 관절 주변의 피부가 겹치기 때문입니다. `diagnostics.html`은 원본 영상을 포함하고(`ffmpeg` 필요) three.js를 CDN에서 불러오므로, 3D 뷰에는 인터넷 연결이 필요합니다.

## 출력

각 `m2mr run`은 **명령이 시작된 시각**으로 디렉터리를 만듭니다. 루트의 파일은 영상과 사진이 같고, 미리보기 폴더만 달라집니다.

```
outputs/20260829_193205_dance/          # 사진 실행은 …_pose/
├── run.json                            # 시작 시각, 입력, 전체 명령
├── skeleton_motion.npz                 # 인체 3D 스켈레톤 (--skeleton으로 재사용)
├── mixamo_rotations.npz                # Mixamo 본별 회전
├── mixamo_character.glb                # 스키닝된 캐릭터, Blender / Unity에 임포트
├── diagnostics.json                    # 자기 교차 보고서 (빠른 시작 6단계 참고)
├── diagnostics.html                    # `m2mr diagnose <run> --visualize` 실행 후에만
└── videos/   또는   images/            # 미리보기 — 입력에 따라 결정
```

**영상 입력**은 `videos/`에 씁니다(클립과 같은 화면비):

```
videos/
├── human_skeleton.mp4                  # 복원한 인체 3D 스켈레톤
├── mixamo_skeleton.mp4                 # Mixamo rig 스켈레톤
├── mixamo_character.mp4                # 스키닝된 Mixamo 캐릭터
└── compare.mp4                         # 2×2: 원본(좌상) / Mixamo 스켈레톤(우상)
                                        #      인체 스켈레톤(좌하) / 캐릭터(우하)
```

**사진 입력**은 대신 `images/`에 씁니다(같은 네 뷰 + 궤도):

```
images/
├── human_skeleton.png                  # 복원한 인체 3D 스켈레톤
├── mixamo_skeleton.png                 # Mixamo rig 스켈레톤
├── mixamo_character.png                # 스키닝된 Mixamo 캐릭터
├── compare.png                         # 2×2: 원본(좌상) / Mixamo 스켈레톤(우상)
│                                       #      인체 스켈레톤(좌하) / 캐릭터(우하)
└── before_after_360_compare.mp4        # 왼쪽: 원본 사진
                                        # 오른쪽: 10° 궤도(한 바퀴)
```

`mixamo_character.glb`는 Blender에서 File → Import → glTF 2.0 (.glb/.gltf)로 엽니다. 카메라가 빈 곳을 보고 있으면 캐릭터 메시를 선택한 뒤 View → Frame Selected. 머리와 손의 구체들은 메시가 아니라 본 표시입니다. Outliner에서 **Icosphere**와 **armature**를 숨기고, 스키닝된 메시는 그대로 두세요. 재생이 원본과 같고 프레임 번호가 `diagnostics.json`과 맞으려면, 장면 FPS는 `run.json`의 `fps`로, 타임라인은 0부터 `n_frames` − 1 프레임까지로 맞추세요. 영상 실행은 `videos/mixamo_character.mp4`와, 사진 실행은 `images/mixamo_character.png` 또는 궤도 클립과 비교하세요.

## 라이선스

이 저장소의 코드는 Apache-2.0입니다. 직접 받은 자산은 각 조항이 있으며 이 저장소와 함께 재배포하면 안 됩니다:

- **SMPL-X**: MPI에서 배포가 제한됨. 기본은 비상업 연구 / 교육 / 예술; 상업 이용은 별도 계약
- **Mixamo FBX**: 제품에 넣어도 됨; 원본 FBX를 에셋 팩으로 재배포하면 안 됨
- **GVHMR 및 기타 추론 가중치**: 첫 `m2mr run` 때 `weights/`로 자동 다운로드, 각 업스트림 라이선스

## 문의

문제가 있으시거나, 로컬 설치에 도움이 필요하시거나, 협업을 논의하고 싶으시면 이메일로 연락해 주세요:
[maxliu2022sz@gmail.com](mailto:maxliu2022sz@gmail.com)

## Star History

<a href="https://star-history.com/#MaxLiu22/Motion2MixamoRig&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MaxLiu22/Motion2MixamoRig&type=Date" />
  </picture>
</a>
