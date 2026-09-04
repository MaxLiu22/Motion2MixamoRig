"""Plugin UI strings. Languages match the repository README set."""

from __future__ import annotations

from typing import Any

LANGS = ("en", "zh-CN", "ko", "ja", "de", "ru", "ar")

# Blender EnumProperty identifiers cannot contain "-".
PREF_TO_LANG = {
    "en": "en",
    "zh_CN": "zh-CN",
    "ko": "ko",
    "ja": "ja",
    "de": "de",
    "ru": "ru",
    "ar": "ar",
}

_BLENDER_PREFIX = (
    ("zh", "zh-CN"),
    ("ko", "ko"),
    ("ja", "ja"),
    ("de", "de"),
    ("ru", "ru"),
    ("ar", "ar"),
)

STRINGS: dict[str, dict[str, str]] = {}


def _add(key: str, **langs: str) -> None:
    for lang in LANGS:
        STRINGS.setdefault(lang, {})[key] = langs.get(lang) or langs["en"]


_add(
    "section_setup",
    en="Setup",
    **{"zh-CN": "设置"},
    ko="설정",
    ja="セットアップ",
    de="Einrichtung",
    ru="Настройка",
    ar="إعداد",
)
_add(
    "section_input",
    en="Input",
    **{"zh-CN": "输入"},
    ko="입력",
    ja="入力",
    de="Eingabe",
    ru="Ввод",
    ar="إدخال",
)
_add(
    "section_progress",
    en="Progress / Result",
    **{"zh-CN": "进度 / 结果"},
    ko="진행 / 결과",
    ja="進行状況 / 結果",
    de="Fortschritt / Ergebnis",
    ru="Прогресс / результат",
    ar="التقدم / النتيجة",
)
_add(
    "external_python",
    en="External Python",
    **{"zh-CN": "外部 Python"},
    ko="외부 Python",
    ja="外部 Python",
    de="Externes Python",
    ru="Внешний Python",
    ar="Python الخارجي",
)
_add(
    "project_directory",
    en="Project Directory",
    **{"zh-CN": "项目目录"},
    ko="프로젝트 디렉터리",
    ja="プロジェクトディレクトリ",
    de="Projektverzeichnis",
    ru="Каталог проекта",
    ar="مجلد المشروع",
)
_add(
    "device",
    en="Device",
    **{"zh-CN": "设备"},
    ko="장치",
    ja="デバイス",
    de="Gerät",
    ru="Устройство",
    ar="الجهاز",
)
_add(
    "ui_language",
    en="UI Language",
    **{"zh-CN": "界面语言"},
    ko="UI 언어",
    ja="UI 言語",
    de="UI-Sprache",
    ru="Язык интерфейса",
    ar="لغة الواجهة",
)
_add(
    "lang_auto",
    en="Auto (Blender / System)",
    **{"zh-CN": "自动（跟随 Blender / 系统）"},
    ko="자동 (Blender / 시스템)",
    ja="自動（Blender / システム）",
    de="Automatisch (Blender / System)",
    ru="Авто (Blender / система)",
    ar="تلقائي (Blender / النظام)",
)
_add(
    "check_environment",
    en="Check Environment",
    **{"zh-CN": "检查环境"},
    ko="환경 확인",
    ja="環境を確認",
    de="Umgebung prüfen",
    ru="Проверить среду",
    ar="فحص البيئة",
)
_add(
    "environment_fmt",
    en="Environment: {status}",
    **{"zh-CN": "环境：{status}"},
    ko="환경: {status}",
    ja="環境: {status}",
    de="Umgebung: {status}",
    ru="Среда: {status}",
    ar="البيئة: {status}",
)
_add("env_not_checked", en="Not checked", **{"zh-CN": "未检查"}, ko="미확인", ja="未確認", de="Nicht geprüft", ru="Не проверено", ar="لم يُفحص")
_add("env_checking", en="Checking…", **{"zh-CN": "正在检查…"}, ko="확인 중…", ja="確認中…", de="Prüfung…", ru="Проверка…", ar="جاري الفحص…")
_add("env_ready", en="Ready", **{"zh-CN": "就绪"}, ko="준비됨", ja="準備完了", de="Bereit", ru="Готово", ar="جاهز")
_add("env_error", en="Error", **{"zh-CN": "错误"}, ko="오류", ja="エラー", de="Fehler", ru="Ошибка", ar="خطأ")
_add(
    "source_type",
    en="Source Type",
    **{"zh-CN": "来源类型"},
    ko="소스 유형",
    ja="ソースの種類",
    de="Quelltyp",
    ru="Тип источника",
    ar="نوع المصدر",
)
_add("source_video", en="Video", **{"zh-CN": "视频"}, ko="비디오", ja="動画", de="Video", ru="Видео", ar="فيديو")
_add("source_image", en="Image", **{"zh-CN": "图片"}, ko="이미지", ja="画像", de="Bild", ru="Изображение", ar="صورة")
_add(
    "source_video_desc",
    en="Single-person motion video",
    **{"zh-CN": "单人动作视频"},
    ko="1인 동작 영상",
    ja="一人のモーション動画",
    de="Video mit einer Person",
    ru="Видео с одним человеком",
    ar="فيديو حركة لشخص واحد",
)
_add(
    "source_image_desc",
    en="Single-person still photo",
    **{"zh-CN": "单人全身照片"},
    ko="1인 사진",
    ja="一人の静止画",
    de="Foto mit einer Person",
    ru="Фото одного человека",
    ar="صورة لشخص واحد",
)
_add(
    "source_file",
    en="Source File",
    **{"zh-CN": "来源文件"},
    ko="소스 파일",
    ja="ソースファイル",
    de="Quelldatei",
    ru="Файл источника",
    ar="ملف المصدر",
)
_add(
    "mixamo_rig",
    en="Mixamo Rig FBX",
    **{"zh-CN": "Mixamo 角色 FBX"},
    ko="Mixamo 리그 FBX",
    ja="Mixamo リグ FBX",
    de="Mixamo-Rig FBX",
    ru="Mixamo Rig FBX",
    ar="هيكل Mixamo FBX",
)
_add(
    "generate_preview",
    en="Generate Preview Videos",
    **{"zh-CN": "生成预览视频"},
    ko="미리보기 영상 생성",
    ja="プレビュー動画を生成",
    de="Vorschauvideos erzeugen",
    ru="Создавать превью-видео",
    ar="إنشاء فيديوهات المعاينة",
)
_add(
    "generate_motion",
    en="Generate Motion",
    **{"zh-CN": "生成动作"},
    ko="모션 생성",
    ja="モーションを生成",
    de="Motion erzeugen",
    ru="Сгенерировать движение",
    ar="توليد الحركة",
)
_add("status_fmt", en="Status: {status}", **{"zh-CN": "状态：{status}"}, ko="상태: {status}", ja="状態: {status}", de="Status: {status}", ru="Статус: {status}", ar="الحالة: {status}")
_add("stage_fmt", en="Stage: {stage}", **{"zh-CN": "阶段：{stage}"}, ko="단계: {stage}", ja="段階: {stage}", de="Phase: {stage}", ru="Этап: {stage}", ar="المرحلة: {stage}")
_add("progress", en="Progress", **{"zh-CN": "进度"}, ko="진행률", ja="進捗", de="Fortschritt", ru="Прогресс", ar="التقدم")
_add("recent_log", en="Recent log", **{"zh-CN": "最近日志"}, ko="최근 로그", ja="最近のログ", de="Aktuelles Protokoll", ru="Последний журнал", ar="السجل الأخير")
_add("cancel", en="Cancel", **{"zh-CN": "取消"}, ko="취소", ja="キャンセル", de="Abbrechen", ru="Отмена", ar="إلغاء")
_add(
    "generation_succeeded",
    en="Generation succeeded",
    **{"zh-CN": "生成成功"},
    ko="생성 성공",
    ja="生成に成功しました",
    de="Erzeugung erfolgreich",
    ru="Генерация выполнена",
    ar="تم التوليد بنجاح",
)
_add(
    "generation_import_failed",
    en="Generation succeeded, but automatic import failed",
    **{"zh-CN": "生成成功，但自动导入失败"},
    ko="생성은 성공했지만 자동 가져오기에 실패했습니다",
    ja="生成は成功しましたが、自動インポートに失敗しました",
    de="Erzeugung erfolgreich, automatischer Import fehlgeschlagen",
    ru="Генерация успешна, но автоимпорт не удался",
    ar="نجح التوليد، لكن الاستيراد التلقائي فشل",
)
_add("cancelled", en="Cancelled", **{"zh-CN": "已取消"}, ko="취소됨", ja="キャンセル済み", de="Abgebrochen", ru="Отменено", ar="أُلغي")
_add(
    "import_character",
    en="Import Generated Character",
    **{"zh-CN": "导入生成的角色"},
    ko="생성된 캐릭터 가져오기",
    ja="生成したキャラクターをインポート",
    de="Erzeugten Charakter importieren",
    ru="Импортировать персонажа",
    ar="استيراد الشخصية المولَّدة",
)
_add(
    "open_output",
    en="Open Output Folder",
    **{"zh-CN": "打开输出文件夹"},
    ko="출력 폴더 열기",
    ja="出力フォルダーを開く",
    de="Ausgabeordner öffnen",
    ru="Открыть папку результатов",
    ar="فتح مجلد الناتج",
)
_add(
    "view_log",
    en="View Full Log",
    **{"zh-CN": "查看完整日志"},
    ko="전체 로그 보기",
    ja="ログを表示",
    de="Vollständiges Protokoll",
    ru="Полный журнал",
    ar="عرض السجل الكامل",
)
_add("no_job_yet", en="No job yet", **{"zh-CN": "还没有任务"}, ko="아직 작업 없음", ja="まだジョブがありません", de="Noch kein Auftrag", ru="Заданий пока нет", ar="لا توجد مهمة بعد")
_add("glb_fmt", en="GLB: {name}", **{"zh-CN": "GLB：{name}"}, ko="GLB: {name}", ja="GLB: {name}", de="GLB: {name}", ru="GLB: {name}", ar="GLB: {name}")
_add(
    "prefs_venv_hint",
    en="Use the venv Python, not Blender's bundled interpreter.",
    **{"zh-CN": "请使用虚拟环境里的 Python，不要用 Blender 自带的解释器。"},
    ko="Blender 내장 인터프리터가 아니라 venv Python을 사용하세요.",
    ja="Blender 同梱の Python ではなく、venv の Python を指定してください。",
    de="Verwende das venv-Python, nicht den mitgelieferten Blender-Interpreter.",
    ru="Укажите Python из venv, не встроенный интерпретатор Blender.",
    ar="استخدم Python الخاص بالبيئة الافتراضية، وليس مفسر Blender.",
)
_add(
    "device_cpu_desc",
    en="Run extraction on CPU",
    **{"zh-CN": "使用 CPU 提取动作"},
    ko="CPU에서 추출",
    ja="CPU で抽出",
    de="Extraktion auf der CPU",
    ru="Извлечение на CPU",
    ar="الاستخراج على المعالج",
)
_add(
    "device_cuda_desc",
    en="Run extraction on an NVIDIA GPU",
    **{"zh-CN": "使用 NVIDIA GPU 提取动作"},
    ko="NVIDIA GPU에서 추출",
    ja="NVIDIA GPU で抽出",
    de="Extraktion auf einer NVIDIA-GPU",
    ru="Извлечение на GPU NVIDIA",
    ar="الاستخراج على معالج NVIDIA",
)
_add(
    "device_mps_desc",
    en="Run extraction on Apple Silicon",
    **{"zh-CN": "使用 Apple Silicon (MPS) 提取动作"},
    ko="Apple Silicon에서 추출",
    ja="Apple Silicon で抽出",
    de="Extraktion auf Apple Silicon",
    ru="Извлечение на Apple Silicon",
    ar="الاستخراج على Apple Silicon",
)
_add("status_idle", en="idle", **{"zh-CN": "空闲"}, ko="대기", ja="待機", de="inaktiv", ru="ожидание", ar="خامل")
_add("status_running", en="running", **{"zh-CN": "运行中"}, ko="실행 중", ja="実行中", de="läuft", ru="выполняется", ar="قيد التشغيل")
_add("status_cancelling", en="cancelling", **{"zh-CN": "正在取消"}, ko="취소 중", ja="キャンセル中", de="wird abgebrochen", ru="отмена", ar="جارٍ الإلغاء")
_add("status_completed", en="completed", **{"zh-CN": "已完成"}, ko="완료", ja="完了", de="abgeschlossen", ru="завершено", ar="مكتمل")
_add("status_failed", en="failed", **{"zh-CN": "失败"}, ko="실패", ja="失敗", de="fehlgeschlagen", ru="ошибка", ar="فشل")
_add("status_cancelled", en="cancelled", **{"zh-CN": "已取消"}, ko="취소됨", ja="キャンセル済み", de="abgebrochen", ru="отменено", ar="أُلغي")
_add("status_import_failed", en="import_failed", **{"zh-CN": "导入失败"}, ko="가져오기 실패", ja="インポート失敗", de="Import fehlgeschlagen", ru="ошибка импорта", ar="فشل الاستيراد")
_add("stage_preflight", en="preflight", **{"zh-CN": "预检查"}, ko="사전 검사", ja="事前チェック", de="Vorprüfung", ru="проверка", ar="فحص أولي")
_add("stage_extract", en="extract", **{"zh-CN": "提取动作"}, ko="추출", ja="抽出", de="Extraktion", ru="извлечение", ar="استخراج")
_add("stage_retarget", en="retarget", **{"zh-CN": "重定向"}, ko="리타깃", ja="リターゲット", de="Retargeting", ru="ретаргет", ar="إعادة توجيه")
_add("stage_export", en="export", **{"zh-CN": "导出"}, ko="내보내기", ja="書き出し", de="Export", ru="экспорт", ar="تصدير")
_add("stage_preview", en="preview", **{"zh-CN": "预览"}, ko="미리보기", ja="プレビュー", de="Vorschau", ru="превью", ar="معاينة")
_add("stage_done", en="done", **{"zh-CN": "完成"}, ko="완료", ja="完了", de="fertig", ru="готово", ar="تم")
_add("stage_failed", en="failed", **{"zh-CN": "失败"}, ko="실패", ja="失敗", de="fehlgeschlagen", ru="ошибка", ar="فشل")
_add("stage_cancelled", en="cancelled", **{"zh-CN": "已取消"}, ko="취소됨", ja="キャンセル済み", de="abgebrochen", ru="отменено", ar="أُلغي")
_add("err_python", en="External Python not found", **{"zh-CN": "找不到外部 Python"}, ko="외부 Python을 찾을 수 없습니다", ja="外部 Python が見つかりません", de="Externes Python nicht gefunden", ru="Внешний Python не найден", ar="لم يُعثر على Python الخارجي")
_add("err_package", en="Motion2MixamoRig package not installed", **{"zh-CN": "未安装 Motion2MixamoRig 软件包"}, ko="Motion2MixamoRig 패키지가 설치되지 않았습니다", ja="Motion2MixamoRig パッケージがインストールされていません", de="Motion2MixamoRig-Paket ist nicht installiert", ru="Пакет Motion2MixamoRig не установлен", ar="حزمة Motion2MixamoRig غير مثبتة")
_add("err_smplx", en="SMPL-X model missing", **{"zh-CN": "缺少 SMPL-X 模型"}, ko="SMPL-X 모델이 없습니다", ja="SMPL-X モデルがありません", de="SMPL-X-Modell fehlt", ru="Модель SMPL-X отсутствует", ar="نموذج SMPL-X مفقود")
_add("err_invalid_rig", en="Mixamo FBX invalid", **{"zh-CN": "Mixamo FBX 无效"}, ko="Mixamo FBX가 올바르지 않습니다", ja="Mixamo FBX が無効です", de="Mixamo-FBX ungültig", ru="Некорректный Mixamo FBX", ar="ملف Mixamo FBX غير صالح")
_add("err_multiple_people", en="Input contains multiple people", **{"zh-CN": "输入里有多个人"}, ko="입력에 여러 사람이 있습니다", ja="入力に複数人が写っています", de="Die Quelle enthält mehrere Personen", ru="Во входе несколько людей", ar="المصدر يحتوي على أكثر من شخص")
_add("err_no_person", en="No person was detected in the input", **{"zh-CN": "输入里没有检测到人"}, ko="입력에서 사람을 찾지 못했습니다", ja="入力から人物を検出できませんでした", de="Keine Person in der Quelle erkannt", ru="Человек во входе не обнаружен", ar="لم يُكتشف أي شخص في المصدر")
_add("err_cuda", en="CUDA unavailable", **{"zh-CN": "CUDA 不可用"}, ko="CUDA를 사용할 수 없습니다", ja="CUDA を利用できません", de="CUDA nicht verfügbar", ru="CUDA недоступна", ar="CUDA غير متاح")
_add("err_mps", en="Apple MPS unavailable", **{"zh-CN": "Apple MPS 不可用"}, ko="Apple MPS를 사용할 수 없습니다", ja="Apple MPS を利用できません", de="Apple MPS nicht verfügbar", ru="Apple MPS недоступен", ar="Apple MPS غير متاح")
_add("err_process_exited", en="Pipeline process exited unexpectedly", **{"zh-CN": "流水线进程意外退出"}, ko="파이프라인 프로세스가 예기치 않게 종료되었습니다", ja="パイプラインが予期せず終了しました", de="Pipeline-Prozess unerwartet beendet", ru="Процесс конвейера неожиданно завершился", ar="توقفت عملية المعالجة بشكل غير متوقع")
_add(
    "err_process_exited_code",
    en="Pipeline process exited unexpectedly (exit {code}). Open View Full Log; if the file is empty the CLI did not start.",
    **{"zh-CN": "流水线进程意外退出（退出码 {code}）。请打开「查看完整日志」；若文件是空的，说明 CLI 没有启动。"},
    ko="파이프라인 프로세스가 예기치 않게 종료되었습니다(종료 코드 {code}). 전체 로그를 확인하세요. 파일이 비어 있으면 CLI가 시작되지 않은 것입니다.",
    ja="パイプラインが予期せず終了しました（終了コード {code}）。完全なログを開いてください。空なら CLI は起動していません。",
    de="Pipeline-Prozess unerwartet beendet (Exit {code}). Öffne das vollständige Protokoll; ist die Datei leer, startete die CLI nicht.",
    ru="Процесс конвейера завершился (код {code}). Откройте полный журнал; пустой файл значит, что CLI не запустился.",
    ar="توقفت عملية المعالجة فجأة (رمز {code}). افتح السجل الكامل؛ إذا كان الملف فارغًا فلم يبدأ CLI.",
)
_add("err_glb", en="Result GLB not found", **{"zh-CN": "找不到结果 GLB"}, ko="결과 GLB를 찾을 수 없습니다", ja="結果の GLB が見つかりません", de="Ergebnis-GLB nicht gefunden", ru="Результирующий GLB не найден", ar="لم يُعثر على ملف GLB الناتج")
_add("err_json", en="Result JSON is invalid", **{"zh-CN": "结果 JSON 无效"}, ko="결과 JSON이 올바르지 않습니다", ja="結果 JSON が無効です", de="Ergebnis-JSON ungültig", ru="Некорректный JSON результата", ar="ملف JSON الناتج غير صالح")
_add("err_preflight", en="Input check failed", **{"zh-CN": "输入检查未通过"}, ko="입력 검사에 실패했습니다", ja="入力チェックに失敗しました", de="Eingabeprüfung fehlgeschlagen", ru="Проверка входа не пройдена", ar="فشل فحص المدخلات")
_add("err_pipeline", en="Motion2MixamoRig pipeline failed", **{"zh-CN": "Motion2MixamoRig 流水线失败"}, ko="Motion2MixamoRig 파이프라인이 실패했습니다", ja="Motion2MixamoRig パイプラインが失敗しました", de="Motion2MixamoRig-Pipeline fehlgeschlagen", ru="Конвейер Motion2MixamoRig не выполнен", ar="فشلت معالجة Motion2MixamoRig")
_add("err_busy", en="A Motion2MixamoRig job is already running", **{"zh-CN": "已有 Motion2MixamoRig 任务在运行"}, ko="이미 Motion2MixamoRig 작업이 실행 중입니다", ja="すでに Motion2MixamoRig ジョブが実行中です", de="Es läuft bereits ein Motion2MixamoRig-Auftrag", ru="Задание Motion2MixamoRig уже выполняется", ar="توجد مهمة Motion2MixamoRig قيد التشغيل")
_add("err_project", en="Project Directory does not exist", **{"zh-CN": "项目目录不存在"}, ko="프로젝트 디렉터리가 없습니다", ja="プロジェクトディレクトリが存在しません", de="Projektverzeichnis existiert nicht", ru="Каталог проекта не существует", ar="مجلد المشروع غير موجود")
_add("err_source", en="Source file not found", **{"zh-CN": "找不到来源文件"}, ko="소스 파일을 찾을 수 없습니다", ja="ソースファイルが見つかりません", de="Quelldatei nicht gefunden", ru="Файл источника не найден", ar="لم يُعثر على ملف المصدر")
_add("err_rig", en="Mixamo FBX not found", **{"zh-CN": "找不到 Mixamo FBX"}, ko="Mixamo FBX를 찾을 수 없습니다", ja="Mixamo FBX が見つかりません", de="Mixamo-FBX nicht gefunden", ru="Mixamo FBX не найден", ar="لم يُعثر على ملف Mixamo FBX")
_add("err_output_missing", en="Output folder not found", **{"zh-CN": "找不到输出文件夹"}, ko="출력 폴더를 찾을 수 없습니다", ja="出力フォルダーが見つかりません", de="Ausgabeordner nicht gefunden", ru="Папка результатов не найдена", ar="لم يُعثر على مجلد الناتج")
_add("err_log_missing", en="Log file not found", **{"zh-CN": "找不到日志文件"}, ko="로그 파일을 찾을 수 없습니다", ja="ログファイルが見つかりません", de="Protokolldatei nicht gefunden", ru="Файл журнала не найден", ar="لم يُعثر على ملف السجل")
_add("err_no_job_folder", en="No output folder from a previous job", **{"zh-CN": "还没有上次任务的输出文件夹"}, ko="이전 작업의 출력 폴더가 없습니다", ja="前回ジョブの出力フォルダーがありません", de="Kein Ausgabeordner eines vorherigen Auftrags", ru="Нет папки предыдущего задания", ar="لا يوجد مجلد ناتج من مهمة سابقة")
_add("err_no_cancel", en="No Motion2MixamoRig job to cancel", **{"zh-CN": "没有可取消的 Motion2MixamoRig 任务"}, ko="취소할 Motion2MixamoRig 작업이 없습니다", ja="キャンセルする Motion2MixamoRig ジョブがありません", de="Kein Motion2MixamoRig-Auftrag zum Abbrechen", ru="Нет задания Motion2MixamoRig для отмены", ar="لا توجد مهمة Motion2MixamoRig لإلغائها")
_add("env_ready_choose", en="Ready — choose a video/image and Mixamo FBX in the panel", **{"zh-CN": "就绪 — 在面板里选择视频/图片和 Mixamo FBX"}, ko="준비됨 — 패널에서 비디오/이미지와 Mixamo FBX를 선택하세요", ja="準備完了 — パネルで動画/画像と Mixamo FBX を選んでください", de="Bereit — wähle Video/Bild und Mixamo-FBX im Panel", ru="Готово — выберите видео/фото и Mixamo FBX на панели", ar="جاهز — اختر فيديو/صورة وملف Mixamo FBX من اللوحة")
_add("env_checking_fmt", en="Checking… {version}", **{"zh-CN": "正在检查… {version}"}, ko="확인 중… {version}", ja="確認中… {version}", de="Prüfung… {version}", ru="Проверка… {version}", ar="جاري الفحص… {version}")
_add("env_running_doctor", en="Running m2mr doctor…", **{"zh-CN": "正在运行 m2mr doctor…"}, ko="m2mr doctor 실행 중…", ja="m2mr doctor を実行中…", de="m2mr doctor läuft…", ru="Запуск m2mr doctor…", ar="جارٍ تشغيل m2mr doctor…")
_add("env_check_failed", en="Environment check failed", **{"zh-CN": "环境检查失败"}, ko="환경 확인에 실패했습니다", ja="環境確認に失敗しました", de="Umgebungsprüfung fehlgeschlagen", ru="Проверка среды не удалась", ar="فشل فحص البيئة")
_add("env_cancelled", en="Environment check cancelled", **{"zh-CN": "已取消环境检查"}, ko="환경 확인이 취소되었습니다", ja="環境確認をキャンセルしました", de="Umgebungsprüfung abgebrochen", ru="Проверка среды отменена", ar="أُلغي فحص البيئة")
_add("info_started_job", en="Started Motion2MixamoRig job {job}", **{"zh-CN": "已开始 Motion2MixamoRig 任务 {job}"}, ko="Motion2MixamoRig 작업 {job}을(를) 시작했습니다", ja="Motion2MixamoRig ジョブ {job} を開始しました", de="Motion2MixamoRig-Auftrag {job} gestartet", ru="Запущено задание Motion2MixamoRig {job}", ar="بدأت مهمة Motion2MixamoRig {job}")
_add("info_started_env", en="Started environment check with {version}", **{"zh-CN": "已开始环境检查（{version}）"}, ko="{version}(으)로 환경 확인을 시작했습니다", ja="{version} で環境確認を開始しました", de="Umgebungsprüfung mit {version} gestartet", ru="Проверка среды запущена ({version})", ar="بدأ فحص البيئة باستخدام {version}")
_add("info_cancelling", en="Cancelling Motion2MixamoRig job", **{"zh-CN": "正在取消 Motion2MixamoRig 任务"}, ko="Motion2MixamoRig 작업을 취소하는 중", ja="Motion2MixamoRig ジョブをキャンセルしています", de="Motion2MixamoRig-Auftrag wird abgebrochen", ru="Отмена задания Motion2MixamoRig", ar="جارٍ إلغاء مهمة Motion2MixamoRig")
_add("info_imported", en="Imported {name}", **{"zh-CN": "已导入 {name}"}, ko="{name}을(를) 가져왔습니다", ja="{name} をインポートしました", de="{name} importiert", ru="Импортировано: {name}", ar="تم استيراد {name}")
_add("cancelling_ellipsis", en="Cancelling…", **{"zh-CN": "正在取消…"}, ko="취소 중…", ja="キャンセル中…", de="Wird abgebrochen…", ru="Отмена…", ar="جارٍ الإلغاء…")

_CODE_TO_KEY = {
    "PYTHON_NOT_FOUND": "err_python",
    "PACKAGE_MISSING": "err_package",
    "SMPLX_MISSING": "err_smplx",
    "INVALID_RIG": "err_invalid_rig",
    "MULTIPLE_PEOPLE": "err_multiple_people",
    "NO_PERSON": "err_no_person",
    "CUDA_UNAVAILABLE": "err_cuda",
    "MPS_UNAVAILABLE": "err_mps",
    "PROCESS_EXITED": "err_process_exited",
    "GLB_MISSING": "err_glb",
    "JSON_INVALID": "err_json",
    "PREFLIGHT_FAILED": "err_preflight",
    "PIPELINE_FAILED": "err_pipeline",
}

_STATUS_KEYS = {
    "idle": "status_idle",
    "running": "status_running",
    "cancelling": "status_cancelling",
    "completed": "status_completed",
    "failed": "status_failed",
    "cancelled": "status_cancelled",
    "import_failed": "status_import_failed",
}

_STAGE_KEYS = {
    "preflight": "stage_preflight",
    "extract": "stage_extract",
    "retarget": "stage_retarget",
    "export": "stage_export",
    "preview": "stage_preview",
    "done": "stage_done",
    "failed": "stage_failed",
    "cancelled": "stage_cancelled",
}

_ENV_KEYS = {
    "NOT_CHECKED": "env_not_checked",
    "CHECKING": "env_checking",
    "READY": "env_ready",
    "ERROR": "env_error",
}

_ENGLISH_TO_KEY = {STRINGS["en"][key]: key for key in STRINGS["en"]}


def detect_system_language() -> str:
    locale_name = ""
    try:
        import bpy

        view = bpy.context.preferences.view
        locale_name = getattr(view, "language", "") or ""
        if not locale_name or locale_name in {"DEFAULT", "DEFAULT_SYSTEM"}:
            locale_name = getattr(bpy.app.translations, "locale", "") or ""
    except Exception:
        locale_name = ""
    if not locale_name:
        try:
            import locale

            locale_name = locale.getdefaultlocale()[0] or ""
        except Exception:
            locale_name = ""
    lowered = (locale_name or "en").replace("-", "_").lower()
    for prefix, mapped in _BLENDER_PREFIX:
        if lowered == prefix or lowered.startswith(prefix + "_"):
            return mapped
    return "en"


def current_language() -> str:
    try:
        import bpy

        addons = bpy.context.preferences.addons
        for addon in addons.values():
            prefs = getattr(addon, "preferences", None)
            choice = getattr(prefs, "ui_language", None)
            if choice:
                if choice == "AUTO":
                    return detect_system_language()
                mapped = PREF_TO_LANG.get(choice, choice)
                if mapped in STRINGS:
                    return mapped
    except Exception:
        pass
    return detect_system_language()


def t(key: str, **kwargs: Any) -> str:
    lang = current_language()
    catalog = STRINGS.get(lang) or STRINGS["en"]
    template = catalog.get(key) or STRINGS["en"].get(key) or key
    if not kwargs:
        return template
    try:
        return template.format(**kwargs)
    except Exception:
        return template


def encode(key: str, **kwargs: Any) -> str:
    """Store a translatable key plus format args so language can change later."""
    if not kwargs:
        return key
    payload = ",".join(f"{name}={value}" for name, value in kwargs.items())
    return f"{key}|{payload}"


def localize(text: str) -> str:
    """Translate a stored UI key, error code, or known English sentence."""
    if not text:
        return ""
    if "|" in text:
        key, payload = text.split("|", 1)
        if key in STRINGS["en"]:
            kwargs: dict[str, str] = {}
            for part in payload.split(","):
                if "=" in part:
                    name, value = part.split("=", 1)
                    kwargs[name] = value
            return t(key, **kwargs) if kwargs else t(key)
    if "+" in text and all(part in STRINGS["en"] for part in text.split("+")):
        return "; ".join(t(part) for part in text.split("+"))
    if text in STRINGS["en"]:
        return t(text)
    if text in _CODE_TO_KEY:
        return t(_CODE_TO_KEY[text])
    if text in _ENGLISH_TO_KEY:
        return t(_ENGLISH_TO_KEY[text])
    if ": " in text:
        head, rest = text.split(": ", 1)
        localized_head = localize(head)
        if localized_head != head:
            return f"{localized_head}: {rest}"
    return text


def status_label(status: str) -> str:
    key = _STATUS_KEYS.get(status)
    return t(key) if key else status


def stage_label(stage: str) -> str:
    return t(_STAGE_KEYS[stage]) if stage in _STAGE_KEYS else stage


def env_status_label(status: str) -> str:
    return t(_ENV_KEYS[status]) if status in _ENV_KEYS else status
