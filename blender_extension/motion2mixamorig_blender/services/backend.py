"""Command construction, process launch, and filesystem helpers.

No Blender imports. Paths are passed as list arguments with shell=False so
spaces in Windows/macOS paths stay intact.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def as_user_path(value: str | Path) -> Path:
    return Path(value).expanduser()


def python_exists(python: str | Path) -> bool:
    path = as_user_path(python)
    return bool(str(python).strip()) and path.is_file()


def directory_exists(path: str | Path) -> bool:
    return bool(str(path).strip()) and as_user_path(path).is_dir()


def file_exists(path: str | Path) -> bool:
    return bool(str(path).strip()) and as_user_path(path).is_file()


def build_version_argv(python: str | Path) -> list[str]:
    return [os.fspath(as_user_path(python)), "--version"]


def build_doctor_argv(python: str | Path) -> list[str]:
    return [os.fspath(as_user_path(python)), "-m", "motion2mixamorig.cli", "doctor"]


def build_run_argv(
    python: str | Path,
    *,
    source_type: str,
    source: str | Path,
    rig: str | Path,
    device: str,
    output_dir: str | Path,
    progress_jsonl: str | Path,
    preview: bool,
) -> list[str]:
    """Build `external-python -m motion2mixamorig.cli run ...` as a list."""
    if source_type not in {"video", "image"}:
        raise ValueError(f"source_type must be 'video' or 'image', got {source_type!r}")
    if device not in {"cpu", "cuda", "mps"}:
        raise ValueError(f"device must be cpu, cuda, or mps, got {device!r}")

    cmd = [
        os.fspath(as_user_path(python)),
        "-m",
        "motion2mixamorig.cli",
        "run",
        "--device",
        device,
        "--rig",
        os.fspath(as_user_path(rig)),
        "--output-dir",
        os.fspath(as_user_path(output_dir)),
        "--progress-jsonl",
        os.fspath(as_user_path(progress_jsonl)),
    ]
    flag = "--image" if source_type == "image" else "--video"
    cmd.extend([flag, os.fspath(as_user_path(source))])
    if not preview:
        cmd.append("--no-preview")
    return cmd


_BLENDER_ENV_DROP = (
    "PYTHONHOME",
    "PYTHONPATH",
    "PYTHONEXECUTABLE",
    "PYTHONUSERBASE",
    "PYTHONSTARTUP",
    "__PYVENV_LAUNCHER__",
    "BLENDER_SYSTEM_PYTHON",
    "DYLD_LIBRARY_PATH",
    "DYLD_FRAMEWORK_PATH",
    "DYLD_INSERT_LIBRARIES",
    "DYLD_FALLBACK_LIBRARY_PATH",
)


def subprocess_env(project_dir: str | Path) -> dict[str, str]:
    """Build an env for External Python that does not inherit Blender's interpreter."""
    env = os.environ.copy()
    for key in _BLENDER_ENV_DROP:
        env.pop(key, None)
    if "PATH" in env:
        env["PATH"] = os.pathsep.join(
            part
            for part in env["PATH"].split(os.pathsep)
            if "Blender.app" not in part and "Blender/" not in part
        )
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = os.pathsep.join(
            part
            for part in env["LD_LIBRARY_PATH"].split(os.pathsep)
            if "blender" not in part.lower()
        )
        if not env["LD_LIBRARY_PATH"]:
            env.pop("LD_LIBRARY_PATH", None)
    root = os.fspath(as_user_path(project_dir))
    env["PYTHONPATH"] = root
    env["PYTHONUNBUFFERED"] = "1"
    return env


def validate_run_inputs(
    *,
    python: str | Path,
    project_dir: str | Path,
    source: str | Path,
    rig: str | Path,
    busy: bool,
) -> list[str]:
    errors: list[str] = []
    if busy:
        errors.append("err_busy")
    if not python_exists(python):
        errors.append("err_python")
    if not directory_exists(project_dir):
        errors.append("err_project")
    if not file_exists(source):
        errors.append("err_source")
    if not file_exists(rig):
        errors.append("err_rig")
    return errors


def new_job_id(source_stem: str, now: datetime | None = None) -> str:
    stamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in source_stem)
    safe = safe.strip("_") or "job"
    return f"{stamp}_{safe[:40]}"


def job_output_dir(project_dir: str | Path, job_id: str) -> Path:
    return as_user_path(project_dir) / "outputs" / "blender_jobs" / job_id


def collection_name_for_source(source_stem: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in source_stem)
    safe = safe.strip("_") or "character"
    return f"M2MR_{safe[:80]}"


def launch_process(
    argv: list[str],
    *,
    cwd: str | Path,
    log_path: str | Path,
    env: dict[str, str] | None = None,
) -> tuple[subprocess.Popen, object]:
    """Start a child process; stdout/stderr go to `log_path`.

    Returns `(process, log_file)` — the caller must keep the file open until
    the process exits, then close it.
    """
    log = Path(log_path)
    log.parent.mkdir(parents=True, exist_ok=True)
    header = " ".join(os.fspath(part) for part in argv) + "\n"
    log.write_text(header, encoding="utf-8")
    log_file = open(log, "ab", buffering=0)
    kwargs: dict = {
        "args": list(argv),
        "cwd": os.fspath(as_user_path(cwd)),
        "stdout": log_file,
        "stderr": subprocess.STDOUT,
        "stdin": subprocess.DEVNULL,
        "shell": False,
        "env": env,
    }
    if sys.platform == "win32":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        kwargs["start_new_session"] = True
    process = subprocess.Popen(**kwargs)
    return process, log_file


def terminate_process(process: subprocess.Popen) -> None:
    """Stop only this plugin-owned process (and its process group on POSIX)."""
    if process.poll() is not None:
        return
    if sys.platform == "win32":
        process.terminate()
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError):
        try:
            process.terminate()
        except OSError:
            pass


def kill_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    if sys.platform == "win32":
        process.kill()
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        try:
            process.kill()
        except OSError:
            pass


def open_path(path: str | Path) -> None:
    target = os.fspath(as_user_path(path))
    if sys.platform == "win32":
        os.startfile(target)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", target], shell=False)
    else:
        subprocess.Popen(["xdg-open", target], shell=False)


def tail_text(path: str | Path, max_lines: int = 12, max_chars: int = 2400) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        return ""
    try:
        data = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    lines = data.splitlines()
    text = "\n".join(lines[-max_lines:])
    if len(text) > max_chars:
        text = text[-max_chars:]
    return text


def interpret_doctor_output(exit_code: int | None, stdout: str) -> tuple[str, str]:
    """Return `('READY'|'ERROR', short message)` from `m2mr doctor` output.

    Missing default videos/images in `assets/` is not an error for the add-on:
    the user picks files in the panel.
    """
    text = stdout or ""
    low = text.lower()
    if "no module named 'motion2mixamorig'" in low or "no module named motion2mixamorig" in low:
        return "ERROR", "err_package"

    blocking: list[str] = []
    if _doctor_line_missing(text, "python module") or "no module named" in low:
        if "torch" in low or "gvhmr" in low or "cv2" in low or "numpy" in low:
            blocking.append("err_package")
    if _doctor_line_missing(text, "SMPL-X") or _doctor_line_bad(text, "SMPL-X"):
        blocking.append("err_smplx")
    if blocking:
        seen: list[str] = []
        for item in blocking:
            if item not in seen:
                seen.append(item)
        return "ERROR", "+".join(seen)

    if exit_code not in (0, None):
        if _doctor_line_missing(text, "input source") or _doctor_line_missing(text, "Mixamo rig"):
            return "READY", "env_ready_choose"
        code, _message = classify_log_text_safe(text)
        from .errors import key_for_code

        if code != "PIPELINE_FAILED":
            return "ERROR", key_for_code(code)
        return "ERROR", "env_check_failed"

    return "READY", "env_ready"


def classify_log_text_safe(text: str) -> tuple[str, str]:
    from .errors import classify_log_text

    return classify_log_text(text)


def _doctor_line_missing(text: str, label: str) -> bool:
    needle = label.lower()
    for line in text.splitlines():
        if "[missing]" in line.lower() and needle in line.lower():
            return True
    return False


def _doctor_line_bad(text: str, label: str) -> bool:
    needle = label.lower()
    for line in text.splitlines():
        if "[invalid]" in line.lower() and needle in line.lower():
            return True
    return False
