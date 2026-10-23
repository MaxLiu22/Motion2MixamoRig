"""Diagnostics box actions: jump to a frame, step between problems, open the HTML report."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.app.handlers import persistent
from bpy.props import IntProperty
from bpy.types import Context, Operator

from ..i18n import t
from ..preferences import get_preferences
from ..registration import safe_register_class, safe_unregister_class
from ..services.backend import (
    build_diagnose_argv,
    directory_exists,
    launch_process,
    open_path,
    python_exists,
    subprocess_env,
    terminate_process,
)
from ..services.diagnostics_reader import load_diagnostics, step_problem


def part_label(part: str) -> str:
    return t("part_" + part)


def pair_label(issue: dict) -> str:
    return " ↔ ".join(part_label(p) for p in issue.get("parts", []))


class M2MR_OT_diag_jump(Operator):
    bl_idname = "m2mr.diag_jump"
    bl_label = "Go to Frame"
    bl_description = "Go to this part of the clip"
    bl_options = {"INTERNAL"}

    frame: IntProperty(default=0)

    def execute(self, context: Context):
        context.scene.frame_set(self.frame)
        return {"FINISHED"}


class M2MR_OT_diag_step(Operator):
    bl_idname = "m2mr.diag_step"
    bl_label = "Next / Previous Problem"
    bl_description = "Go to the next or previous frame range with an intersection"
    bl_options = {"INTERNAL"}

    direction: IntProperty(default=1)

    def execute(self, context: Context):
        report = load_diagnostics(context.scene.m2mr.job_output_dir)
        target = step_problem(report, context.scene.frame_current, self.direction) if report else None
        if target is None:
            self.report({"INFO"}, t("diag_no_more"))
            return {"CANCELLED"}
        context.scene.frame_set(target)
        return {"FINISHED"}


_REPORT_HTML = "diagnostics.html"
_REPORT_JSON = "diagnostics.json"
_REPORT_LOG = "diagnose.log"
_REPORT_POLL_S = 0.5

# The one `m2mr diagnose --visualize` this add-on is waiting on (separate from
# the generate job, so it does not lock the panel).
_report: dict = {}


def report_state(run_dir: str) -> str:
    """'building', 'failed' or '' for the job folder shown in the panel."""
    if not run_dir or Path(run_dir).expanduser() != _report.get("dir"):
        return ""
    return _report.get("state", "")


def _report_is_current(run_dir: Path) -> bool:
    html, data = run_dir / _REPORT_HTML, run_dir / _REPORT_JSON
    return html.is_file() and (not data.is_file() or html.stat().st_mtime >= data.stat().st_mtime)


class M2MR_OT_diag_report(Operator):
    bl_idname = "m2mr.diag_report"
    bl_label = "Open HTML Report"
    bl_description = (
        "Open the interactive self-intersection report in the web browser. "
        "The first time, it is built in the background (about 15 seconds)"
    )
    bl_options = {"INTERNAL"}

    def execute(self, context: Context):
        run_dir = Path(context.scene.m2mr.job_output_dir).expanduser()
        if not run_dir.is_dir():
            self.report({"ERROR"}, t("err_output_missing"))
            return {"CANCELLED"}
        if _report_is_current(run_dir):
            open_path(run_dir / _REPORT_HTML)
            return {"FINISHED"}
        if _report.get("state") == "building":
            self.report({"INFO"}, t("diag_report_building"))
            return {"CANCELLED"}

        prefs = get_preferences(context)
        if not python_exists(prefs.python_path):
            self.report({"ERROR"}, t("err_python"))
            return {"CANCELLED"}
        try:
            process, log_file = launch_process(
                build_diagnose_argv(prefs.python_path, run_dir),
                cwd=prefs.project_dir if directory_exists(prefs.project_dir) else run_dir,
                log_path=run_dir / _REPORT_LOG,
                env=subprocess_env(prefs.project_dir),
            )
        except OSError as exc:
            self.report({"ERROR"}, f"{t('err_python')}: {exc}")
            return {"CANCELLED"}
        _report.clear()
        _report.update(dir=run_dir, process=process, log_file=log_file, state="building")
        if not bpy.app.timers.is_registered(_poll_report):
            bpy.app.timers.register(_poll_report, first_interval=_REPORT_POLL_S, persistent=True)
        self.report({"INFO"}, t("diag_report_building"))
        return {"FINISHED"}


def _poll_report() -> float | None:
    process = _report.get("process")
    if process is None:
        return None
    if process.poll() is None:
        return _REPORT_POLL_S
    try:
        _report["log_file"].close()
    except OSError:
        pass
    run_dir = _report["dir"]
    ok = process.returncode == 0 and (run_dir / _REPORT_HTML).is_file()
    _report.update(process=None, log_file=None, state="" if ok else "failed")
    if ok:
        open_path(run_dir / _REPORT_HTML)
    _redraw_sidebar(None)
    return None


def _stop_report() -> None:
    if bpy.app.timers.is_registered(_poll_report):
        bpy.app.timers.unregister(_poll_report)
    process = _report.get("process")
    if process is not None and process.poll() is None:
        terminate_process(process)
    if _report.get("log_file") is not None:
        try:
            _report["log_file"].close()
        except OSError:
            pass
    _report.clear()


@persistent
def _redraw_sidebar(scene, *_args) -> None:
    """The frame bar marks the current frame; keep it in step with playback and scrubbing."""
    wm = bpy.context.window_manager
    if wm is None:
        return
    for window in wm.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                for region in area.regions:
                    if region.type == "UI":
                        region.tag_redraw()


CLASSES = (M2MR_OT_diag_jump, M2MR_OT_diag_step, M2MR_OT_diag_report)


def register() -> None:
    for cls in CLASSES:
        safe_register_class(cls)
    if _redraw_sidebar not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(_redraw_sidebar)


def unregister() -> None:
    _stop_report()
    if _redraw_sidebar in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(_redraw_sidebar)
    for cls in reversed(CLASSES):
        safe_unregister_class(cls)
