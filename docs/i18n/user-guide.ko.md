# Blender용 Motion2MixamoRig — 사용 가이드

<p align="center">
  <a href="user-guide.zh-Hans.md">简体中文</a> · <a href="user-guide.zh-Hant.md">繁體中文</a> · <a href="../user-guide.md">English</a> · 한국어 · <a href="user-guide.ja.md">日本語</a> · <a href="user-guide.de.md">Deutsch</a> · <a href="user-guide.ru.md">Русский</a> · <a href="user-guide.ar.md">العربية</a> · <a href="user-guide.vi.md">Tiếng Việt</a> · <a href="user-guide.fil.md">Filipino</a> · <a href="user-guide.th.md">ไทย</a> · <a href="user-guide.fr.md">Français</a> · <a href="user-guide.es-MX.md">Español</a> · <a href="user-guide.tr.md">Türkçe</a> · <a href="user-guide.ne.md">नेपाली</a> · <a href="user-guide.id.md">Bahasa Indonesia</a> · <a href="user-guide.pl.md">Polski</a> · <a href="user-guide.nl.md">Nederlands</a> · <a href="user-guide.it.md">Italiano</a> · <a href="user-guide.pt-BR.md">Português (Brasil)</a> · <a href="user-guide.uk.md">Українська</a> · <a href="user-guide.cs.md">Čeština</a> · <a href="user-guide.hi.md">हिन्दी</a> · <a href="user-guide.sv.md">Svenska</a>
</p>

한 사람이 나오는 영상을 Blender 안에서 애니메이션된 Mixamo 캐릭터로 바꿉니다.
코딩이나 터미널은 필요 없습니다.

<!-- video: link the tutorial video here -->

> 지금까지 **macOS (Apple Silicon)** 에서만 테스트했습니다. Windows 버전은 곧 나옵니다.

## 준비물

- **Blender 4.2 이상**
- 첫 설정을 위한 **인터넷 연결**
- **약 8 GB의 여유 디스크 공간** (런타임 ~1.3 GB + 모델 ~5.6 GB)
- **무료 SMPL-X 계정**과 **무료 Adobe 계정** (Mixamo용). 4단계와 5단계를 참고하세요

## 1. 애드온 다운로드

[최신 릴리스](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)에서
내 컴퓨터에 맞는 zip을 다운로드하세요.

| 내 컴퓨터 | 파일 |
| --- | --- |
| Apple Silicon Mac (M1/M2/M3/M4) | `motion2mixamorig-<version>-macos-arm64.zip` |
| Windows | **곧 나옵니다** |

예를 들어 `motion2mixamorig-0.1.8-macos-arm64.zip`에서 `0.1.8`은 애드온
버전, `macos-arm64`는 플랫폼입니다. 잘못된 파일을 고르면 Blender가 설치를
거부하고 필요한 플랫폼을 알려 줍니다.

압축을 **풀지 마세요**. Blender가 zip을 직접 설치합니다.

## 2. Blender에 설치

1. **Edit → Preferences → Get Extensions**
2. 오른쪽 위의 작은 **∨** 클릭 → **Install from Disk…**
3. zip을 선택합니다. 목록에 **Motion2MixamoRig**가 활성화된 상태로 나타납니다.
4. Preferences를 닫습니다. 3D Viewport에서 **N**을 누른 뒤 오른쪽의
   **Motion2MixamoRig** 탭을 클릭합니다.

<!-- screenshot: Install from Disk menu -->

## 3. 런타임 설치 (한 번만)

패널에서 **런타임 설치 (원클릭)** (Install Runtime (one click))을 클릭합니다.

애드온이 자체 Python과 라이브러리(~1.4 GB)를 `~/Motion2MixamoRig/`에
다운로드합니다. 컴퓨터의 다른 부분은 건드리지 않습니다. 몇 분 정도 걸리며,
진행 표시줄에 현재 단계가 표시됩니다.

<!-- screenshot: Install Runtime button and progress -->

## 4. SMPL-X 바디 모델 받기

SMPL-X는 애드온에 필요한 무료 바디 모델입니다. 라이선스상 저희가 함께 배포할
수 없으므로, 한 번만 직접 다운로드해 주세요.

1. [smpl-x.is.tue.mpg.de](https://smpl-x.is.tue.mpg.de/)를 열고 **Register**로
   가입합니다. 라이선스에 동의하고 이메일 인증을 완료합니다.
2. 로그인한 뒤 **Download**를 열고 SMPL-X 모델(**NPZ** 버전)을
   다운로드합니다.
3. 압축을 풀고 **`SMPLX_NEUTRAL.npz`** 파일을 찾습니다.
4. Blender에서 **SMPL-X 모델 선택…** (Choose SMPL-X Model…)을 클릭하고 그
   파일을 고릅니다. 그러면 패널에 **SMPL-X 모델: 확인됨** (SMPL-X model: found)이
   표시됩니다.

<!-- screenshot: SMPL-X download page -->

## 5. Mixamo 캐릭터 받기

1. [mixamo.com](https://www.mixamo.com/)을 열고 Adobe 계정으로 로그인합니다.
2. **Characters** 탭 → 캐릭터 선택 (예: **Y Bot**)
3. **Download** → Format **FBX Binary (.fbx)**, Pose **T-pose** → Download

<!-- screenshot: Mixamo download dialog -->

## 6. 모션 생성

**입력** (Input) 상자에서:

1. **소스 유형** (Source Type): 비디오 (자세 하나만이라면 이미지)
2. **소스 파일** (Source File): 사용할 클립. **처음부터 끝까지 정확히 한 사람이,
   머리부터 발끝까지 화면 안에** 나와야 합니다.
3. **Mixamo 리그 FBX** (Mixamo Rig FBX): 5단계에서 받은 캐릭터
4. **손 검출** (Detect Hands)은 꺼져 있습니다. 손가락을 움직이고 싶을 때만 켭니다.
   그다음 **MANO 손 모델 선택…** (Choose MANO Hand Model…)을 눌러 `MANO_RIGHT.pkl`을 고릅니다.
   이 파일은 SMPL-X와 같은 방법으로 받습니다.
   [mano.is.tue.mpg.de](https://mano.is.tue.mpg.de/)에 등록하고 **Models & Code**를 받아 압축을 풉니다.
   손을 처음 처리할 때는 약 **2.7 GB**를 한 번 더 받으며, 몸만 돌릴 때의 대략 두 배가 걸립니다. 켜면 **Finger Smoothing (seconds)**도 나타납니다. 손가락 움직임을 부드럽게 합니다. 기본값은 0.08초이고, 0이면 감지된 그대로입니다.
5. **모션 생성** (Generate Motion) 클릭

작업이 끝나면 애니메이션된 캐릭터가 씬에 자동으로 가져와집니다. 바닥에 디딘 발은 그 자리에 남고, 발바닥은 Blender 바닥에 놓입니다. 그 바닥에 **바닥 마커** (Floor Markers) 메시가 추가됩니다(0.5 m마다 십자). 진행 / 결과의 **바닥 마커** (Floor Markers) 체크박스로 보이거나 숨깁니다.

### 첫 실행은 시간이 더 걸립니다 — 정상입니다

처음 실행할 때 애드온이 약 **5.6 GB**의 모델을 다운로드합니다. 패널에 다운로드
크기, 속도, 남은 시간이 표시됩니다. 모델은 한 번만 다운로드됩니다.

그 후 영상은 내 컴퓨터에서 처리됩니다. Mac CPU에서는 10초짜리 클립에 몇 분이
걸립니다. 실행 중에도 Blender를 계속 사용할 수 있으며, **취소** (Cancel)를
누르면 작업이 중지됩니다.

## 좋은 결과를 위한 팁

- 한 사람만, 전신이 보이고 화면 가장자리에서 잘리지 않게
- 흔들리지 않는 카메라, 밝은 조명, 헐렁하거나 펄럭이는 옷보다는 단순한 옷
- 짧은 클립(5–20초)이 더 빠르니 먼저 시도해 보세요

## 새 버전으로 업데이트

애드온은 자주 업데이트됩니다. 업데이트 방법:

1. [최신 릴리스](https://github.com/MaxLiu22/Motion2MixamoRig/releases/latest)에서
   최신 zip을 다운로드합니다.
2. **Get Extensions** → 이전 **Motion2MixamoRig**를 제거하고, Blender를 완전히
   종료(**Cmd+Q**)한 뒤 다시 열고 새 zip을 설치합니다.
3. 패널에서 **런타임 업데이트** (Update Runtime)를 클릭합니다.

업데이트해도 다운로드한 모델은 유지되므로 금방 끝납니다. 설치된 버전은
**Get Extensions**에서 애드온 옆에 표시됩니다.

## 패널

- **제목 옆의 ⚙** 버튼으로 **설정** (Setup) 상자를 보이거나 숨깁니다.
- **설정**: 언어, 런타임, SMPL-X, **장치** (Device) (CPU가 안전한 선택),
  그리고 **환경 확인** (Check Environment).
- **입력**: 애니메이션할 대상, **바디 모델** (Body Model, GVHMR), **손 검출** (Detect Hands).
- **진행 / 결과** (Progress / Result): 진행 상황, 최근 로그, 그리고 작업 후에는
  **생성된 캐릭터 가져오기** (Import Generated Character),
  **바닥 마커** (Floor Markers) 체크박스,
  **출력 폴더 열기** (Open Output Folder), **전체 로그 보기** (View Full Log).
- **진단**(Diagnostics): 캐릭터의 신체 부위가 서로 파고든 곳(손이 머리 안으로 들어가거나, 팔짱을 낄 때 팔끼리 겹치는
  경우 등). 막대의 빨간 칸은 문제가 있는 프레임이며, 클릭하면 그곳으로 이동합니다. 막대 아래의 삼각형은 현재 프레임을 따라가고, 그
  아래에 이 프레임에서 파고든 부위와 깊이가 표시됩니다. **이전** / **다음**(Previous / Next)으로 문제 사이를
  이동합니다. **HTML 보고서 열기**(Open HTML Report)는 원본 영상과 캐릭터를 나란히 보여 주는 보고서를 웹
  브라우저에서 엽니다(처음에는 만드는 데 약 15초 걸립니다). 원본 영상을 보려면 컴퓨터에 ffmpeg가 있어야 합니다(Mac에서는 `brew install ffmpeg`). 없으면 캐릭터는 나오고, 옆의 영상은 비어 있습니다. 캐릭터는 0.5 m마다 놓인 고정된 바닥 십자 위에 서 있어서, 미끄러지는지 볼 수 있습니다. 빨간 트랙 위의 호박색 레인은 눈으로 본 문제를 적는 곳입니다. 오른쪽 **노트**(Notes) 목록에 나오며, 한 줄을 클릭하면 그곳으로 이동합니다. **노트 다운로드**(Download notes)는 이 메모와 교차 시각을 한 파일로 저장합니다. 파일 이름은 그 영상의 이름입니다.

애드온은 19개 언어를 지원합니다. **자동 (Blender / 시스템)** (Auto (Blender / System))은
Blender의 언어를 따릅니다. **설정** 상자의 **UI 언어** (UI Language)에서 바꿀 수
있습니다.

## 문제가 생겼을 때

| 화면에 보이는 내용 | 해결 방법 |
| --- | --- |
| **런타임 설치 실패** (Runtime installation failed) | 인터넷 연결을 확인하고 버튼을 다시 클릭하세요. 로그: `~/Motion2MixamoRig/logs/setup.log` |
| **SMPL-X 모델: 없음** (SMPL-X model: missing) | 4단계를 다시 진행하고 `SMPLX_NEUTRAL.npz`를 선택하세요 |
| **MANO 손 모델: 없음** (MANO hand model: missing) | **손 검출**을 켠 뒤 **MANO 손 모델 선택…**에서 `MANO_RIGHT.pkl`을 고르세요 |
| **Mixamo FBX가 올바르지 않습니다** (Mixamo FBX invalid) | 캐릭터를 **FBX Binary**, **T-pose**로 다시 다운로드하세요 |
| **입력에 여러 사람이 있습니다** (Input contains multiple people) | 한 사람만 나오는 클립을 사용하세요 |
| **입력에서 사람을 찾지 못했습니다** (No person was detected in the input) | 전신이 보이고 조명이 충분한지 확인하세요 |
| **파이프라인 프로세스가 예기치 않게 종료되었습니다** (Pipeline process exited unexpectedly) | **전체 로그 보기**를 클릭하세요 |

도움을 요청할 때는 로그를 첨부하고 사용 중인 애드온 버전을 알려 주세요.

## 제거

1. **Get Extensions** → **Motion2MixamoRig** 제거.
2. **`~/Motion2MixamoRig`** 폴더(홈 폴더 → `Motion2MixamoRig`)를 삭제합니다.
   애드온을 제거해도 이 폴더는 삭제되지 **않으며**, 약 7 GB의 런타임과 모델,
   그리고 `app/outputs/`에 생성된 결과가 들어 있습니다.

## 라이선스

Motion2MixamoRig는 **비상업적 용도로만** 사용할 수 있습니다. 상업적 사용을
허용하지 않는 라이선스의 연구용 모델(GVHMR, SMPL-X 등)에 의존하기 때문입니다.
[`NOTICE.md`](../../NOTICE.md)를 참고하세요.
