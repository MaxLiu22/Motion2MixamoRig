"""Single in-memory job plus a bpy.app.timers poller.

Importing this module does not start a process or touch the filesystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import bpy

from ..services.backend import kill_process, tail_text, terminate_process
from ..services.errors import classify_log_text, key_for_code
from ..services.job_monitor import latest_progress, read_progress_file
from ..services.result_reader import read_run_json

_TIMER_INTERVAL = 0.25
_KILL_AFTER_S = 4.0


@dataclass
class JobRuntime:
    kind: str
    process: Any
    owned_pid: int
    output_dir: Path
    log_path: Path
    progress_path: Path
    log_file: Any = None
    cancelled: bool = False
    finished: bool = False
    cancel_started: float = 0.0
    source_name: str = ""
    auto_import: bool = True
    extra: dict[str, Any] = field(default_factory=dict)


_runtime: JobRuntime | None = None


def get_runtime() -> JobRuntime | None:
    return _runtime


def is_busy() -> bool:
    runtime = _runtime
    if runtime is None or runtime.finished or runtime.process is None:
        return False
    return runtime.process.poll() is None


def attach(runtime: JobRuntime) -> None:
    global _runtime
    _runtime = runtime
    _start_timer()


def _start_timer() -> None:
    if not bpy.app.timers.is_registered(_poll):
        bpy.app.timers.register(_poll, first_interval=_TIMER_INTERVAL, persistent=True)


def stop_timer() -> None:
    if bpy.app.timers.is_registered(_poll):
        bpy.app.timers.unregister(_poll)


def _close_log(runtime: JobRuntime) -> None:
    log_file = runtime.log_file
    runtime.log_file = None
    if log_file is not None:
        try:
            log_file.close()
        except OSError:
            pass


def shutdown() -> None:
    """Called from addon unregister: drop the timer and stop our process."""
    global _runtime
    stop_timer()
    runtime = _runtime
    _runtime = None
    if runtime is None:
        return
    if runtime.process is not None and runtime.process.poll() is None:
        terminate_process(runtime.process)
        try:
            runtime.process.wait(timeout=1.0)
        except Exception:
            kill_process(runtime.process)
    _close_log(runtime)


def request_cancel() -> bool:
    runtime = _runtime
    if runtime is None or runtime.process is None:
        return False
    if runtime.process.pid != runtime.owned_pid:
        return False
    if runtime.process.poll() is not None:
        return False
    runtime.cancelled = True
    import time

    runtime.cancel_started = time.monotonic()
    terminate_process(runtime.process)
    return True


def _tag_redraw() -> None:
    wm = bpy.context.window_manager
    if wm is None:
        return
    for window in wm.windows:
        screen = window.screen
        if screen is None:
            continue
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


def _props():
    scene = bpy.context.scene
    return getattr(scene, "m2mr", None)


def _poll() -> float | None:
    runtime = _runtime
    if runtime is None:
        return None
    props = _props()
    if props is None:
        return _TIMER_INTERVAL

    if runtime.kind == "doctor":
        _poll_doctor(runtime, props)
    else:
        _poll_run(runtime, props)

    _tag_redraw()
    if runtime.finished:
        stop_timer()
        return None
    return _TIMER_INTERVAL


def _poll_doctor(runtime: JobRuntime, props) -> None:
    import time

    code = runtime.process.poll()
    log = tail_text(runtime.log_path, max_lines=80, max_chars=8000)
    if runtime.cancelled and code is None:
        if time.monotonic() - runtime.cancel_started > _KILL_AFTER_S:
            kill_process(runtime.process)
        return
    if code is None:
        props.env_status = "CHECKING"
        props.env_message = "env_running_doctor"
        return

    _close_log(runtime)
    runtime.finished = True
    from ..services.backend import interpret_doctor_output

    try:
        full = Path(runtime.log_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        full = log
    status, message = interpret_doctor_output(code, full)
    props.env_status = status
    props.env_message = message
    if runtime.cancelled:
        props.env_status = "ERROR"
        props.env_message = "env_cancelled"


def _poll_run(runtime: JobRuntime, props) -> None:
    import time

    events = read_progress_file(runtime.progress_path)
    latest = latest_progress(events)
    if latest is not None:
        props.job_stage = latest.stage
        props.job_progress = latest.progress
        if latest.stage == "failed" and latest.message:
            props.job_error = latest.message

    props.job_output_dir = str(runtime.output_dir)
    props.job_log_path = str(runtime.log_path)

    code = runtime.process.poll()
    if runtime.cancelled and code is None:
        props.job_status = "cancelling"
        props.job_stage = "cancelled"
        if time.monotonic() - runtime.cancel_started > _KILL_AFTER_S:
            kill_process(runtime.process)
        return
    if code is None:
        props.job_status = "running"
        return

    _close_log(runtime)
    runtime.finished = True
    _finish_run(runtime, props, code)


def _finish_run(runtime: JobRuntime, props, code: int) -> None:
    if runtime.cancelled:
        props.job_status = "cancelled"
        props.job_stage = "cancelled"
        props.job_error = "cancelled"
        return

    result = read_run_json(runtime.output_dir)
    if result.status == "completed" and result.glb_path is not None:
        props.job_status = "completed"
        props.job_stage = "done"
        props.job_progress = 1.0
        props.job_glb_path = str(result.glb_path)
        props.job_error = ""
        props.import_note = ""
        if runtime.auto_import:
            from .import_result import import_generated_character

            try:
                import_generated_character(
                    bpy.context,
                    result,
                    source_name=runtime.source_name or props.job_source_name,
                )
            except Exception as exc:
                props.job_status = "import_failed"
                props.import_note = "generation_import_failed"
                props.job_error = f"generation_import_failed: {exc}"
        return

    if result.status == "failed":
        props.job_status = "failed"
        props.job_stage = result.stage or "failed"
        props.job_error = key_for_code(result.error_code or "PIPELINE_FAILED")
        if result.glb_path is not None:
            props.job_glb_path = str(result.glb_path)
        return

    if result.status == "glb_missing":
        props.job_status = "failed"
        props.job_error = "err_glb"
        return

    if result.status == "invalid":
        props.job_status = "failed"
        props.job_error = "err_json"
        return

    try:
        log = Path(runtime.log_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        log = ""
    error_code, _message = classify_log_text(log)
    if not log.strip() or error_code == "PROCESS_EXITED":
        from ..i18n import encode

        message = encode("err_process_exited_code", code=code)
    elif code not in (0, None) and error_code == "PIPELINE_FAILED":
        from ..i18n import encode

        message = encode("err_process_exited_code", code=code)
    else:
        message = key_for_code(error_code)
    props.job_status = "failed"
    props.job_stage = "failed"
    props.job_error = message


def register() -> None:
    return


def unregister() -> None:
    shutdown()
