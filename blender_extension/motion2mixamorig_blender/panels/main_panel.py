"""3D Viewport → Sidebar (N Panel) → Motion2MixamoRig."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.types import Context, Panel

from ..i18n import env_status_label, localize, stage_label, status_label, t
from ..operators.runtime import get_runtime
from ..preferences import get_preferences
from ..registration import safe_register_class, safe_unregister_class
from ..services.backend import tail_text


class M2MR_PT_main(Panel):
    # Blender draws bl_label after draw_header(), so the title is drawn there
    # instead, which lets the gear sit right after it.
    bl_label = ""
    bl_idname = "M2MR_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Motion2MixamoRig"

    def draw_header(self, context: Context) -> None:
        row = self.layout.row(align=True)
        row.alignment = "LEFT"  # size items to their content instead of stretching
        row.label(text="Motion2MixamoRig")
        # Borderless gear right after the title: shows / hides the Setup box.
        # A text glyph instead of icon="PREFERENCES": Blender icons have a fixed
        # size, while the glyph follows the (smaller) header font.
        # A text button keeps side padding; squeeze it so the glyph hugs the title.
        # 0.6 measured in Blender 5.2: at 0.54 and below the glyph is clipped away.
        gear = row.row(align=True)
        gear.scale_x = 0.6
        gear.prop(context.scene.m2mr, "show_setup", text="⚙", toggle=True, emboss=False)

    def draw(self, context: Context) -> None:
        layout = self.layout
        props = context.scene.m2mr
        prefs = get_preferences(context)
        runtime = get_runtime()
        busy = runtime is not None and not runtime.finished

        # Keep Setup visible while the runtime installs: its progress bar lives there.
        if props.show_setup or props.setup_status in {"running", "cancelling"}:
            self._draw_setup(layout, prefs, props, busy)
        self._draw_input(layout, prefs, props, busy)
        self._draw_progress(layout, props, busy)
        if not busy and props.job_output_dir:
            _draw_diagnostics(layout, context.scene)

    def _draw_setup(self, layout, prefs, props, busy: bool) -> None:
        box = layout.box()
        box.label(text=t("section_setup"))
        box.prop(prefs, "ui_language", text=t("ui_language"))
        self._draw_runtime(box, prefs, props, busy)
        box.prop(props, "device", text=t("device"))
        row = box.row()
        row.enabled = not busy
        row.operator("m2mr.check_environment", text=t("check_environment"), icon="CHECKMARK")
        box.label(text=t("environment_fmt", status=env_status_label(props.env_status)))
        if props.env_message:
            box.label(text=localize(props.env_message))

        box.prop(
            props,
            "show_advanced",
            text=t("advanced"),
            icon="TRIA_DOWN" if props.show_advanced else "TRIA_RIGHT",
            emboss=False,
        )
        if props.show_advanced:
            box.prop(prefs, "python_path", text=t("external_python"))
            box.prop(prefs, "project_dir", text=t("project_directory"))

    def _draw_runtime(self, box, prefs, props, busy: bool) -> None:
        from ..services.runtime_setup import default_home, installed_python

        installed = installed_python(default_home()) is not None
        sub = box.box()
        if props.setup_status in {"running", "cancelling"}:
            sub.label(text=t("setup_running"), icon="IMPORT")
            try:
                sub.progress(factor=float(props.setup_progress), type="BAR", text=props.setup_message[:80])
            except Exception:
                sub.label(text=props.setup_message[:96])
            sub.operator("m2mr.cancel_job", text=t("cancel"), icon="X")
            return
        row = sub.row()
        row.enabled = not busy
        row.scale_y = 1.3
        row.operator(
            "m2mr.setup_runtime",
            text=t("update_runtime") if installed else t("install_runtime"),
            icon="FILE_REFRESH" if installed else "IMPORT",
        )
        if props.setup_status == "done":
            sub.label(text=t("setup_done"), icon="CHECKMARK")
        elif props.setup_status == "failed":
            sub.label(text=t("setup_failed"), icon="ERROR")
            if props.setup_message:
                sub.label(text=props.setup_message[:96])
        elif not installed:
            sub.label(text=t("setup_hint"))

        smplx = Path(prefs.project_dir) / "assets" / "body_models" / "smplx" if prefs.project_dir else None
        found = bool(smplx) and any((smplx / name).is_file() for name in ("SMPLX_NEUTRAL.npz", "SMPLX_NEUTRAL.pkl"))
        row = sub.row()
        row.enabled = not busy
        row.operator("m2mr.set_smplx", text=t("choose_smplx"), icon="CHECKMARK" if found else "FILE_BLANK")
        sub.label(text=t("smplx_found") if found else t("smplx_missing"))

    def _draw_mano(self, box, prefs, busy: bool) -> None:
        from ..services.backend import mano_model_present

        found = bool(prefs.project_dir) and mano_model_present(prefs.project_dir)
        row = box.row()
        row.enabled = not busy
        row.operator("m2mr.set_mano", text=t("choose_mano"), icon="CHECKMARK" if found else "FILE_BLANK")
        box.label(text=t("mano_found") if found else t("mano_missing"))

    def _draw_input(self, layout, prefs, props, busy: bool) -> None:
        box = layout.box()
        box.label(text=t("section_input"))
        box.prop(props, "source_type", text=t("source_type"))
        box.prop(props, "source_path", text=t("source_file"))
        box.prop(props, "rig_path", text=t("mixamo_rig"))
        box.prop(props, "extractor", text=t("extractor"))
        box.prop(props, "detect_hands", text=t("detect_hands"))
        if props.detect_hands:
            box.label(text=t("detect_hands_slow"))
            box.prop(props, "hand_smooth", text=t("hand_smooth"))
            self._draw_mano(box, prefs, busy)
        box.prop(props, "generate_preview", text=t("generate_preview"))
        if not busy and _first_run(prefs):
            _draw_first_run_note(box)
        row = box.row()
        row.enabled = not busy
        row.scale_y = 1.4
        row.operator("m2mr.run_pipeline", text=t("generate_motion"), icon="PLAY")

    def _draw_progress(self, layout, props, busy: bool) -> None:
        box = layout.box()
        box.label(text=t("section_progress"))
        status = props.job_status or "idle"
        box.label(text=t("status_fmt", status=status_label(status)))

        if busy or status in {"running", "cancelling"}:
            if props.job_stage:
                box.label(text=t("stage_fmt", stage=stage_label(props.job_stage)))
            try:
                box.progress(factor=float(props.job_progress), type="BAR")
            except Exception:
                box.prop(props, "job_progress", text=t("progress"), slider=True)
            if props.dl_active:
                _draw_download(box, props)
            log_path = Path(props.job_log_path) if props.job_log_path else None
            log = tail_text(log_path, max_lines=8) if log_path else ""
            if log:
                log_box = box.box()
                log_box.label(text=t("recent_log"))
                for line in log.splitlines()[-8:]:
                    log_box.label(text=line[:96])
            box.operator("m2mr.cancel_job", text=t("cancel"), icon="X")
            return

        if status in {"completed", "import_failed", "failed", "cancelled"}:
            if props.job_stage:
                box.label(text=t("stage_fmt", stage=stage_label(props.job_stage)))
            if status == "completed":
                box.label(text=t("generation_succeeded"))
            elif status == "import_failed":
                box.label(text=t("generation_import_failed"))
            elif status == "cancelled":
                box.label(text=t("cancelled"))
            if props.job_error:
                box.label(text=localize(props.job_error))
            if props.job_glb_path:
                box.label(text=t("glb_fmt", name=Path(props.job_glb_path).name))
            row = box.row()
            row.operator("m2mr.import_result", text=t("import_character"), icon="IMPORT")
            box.prop(props, "show_floor_markers", text=t("show_floor_markers"))
            row = box.row()
            row.operator("m2mr.open_output", text=t("open_output"), icon="FILE_FOLDER")
            row.operator("m2mr.view_log", text=t("view_log"), icon="TEXT")
            return

        box.label(text=t("no_job_yet"))


_CELLS = 48


def _draw_playhead(box, cells, now: int) -> None:
    """Triangle under the bar cell that holds the current frame."""
    # Same buttons as the bar so the cells line up. The icon has to be on a
    # button too: an icon label keeps its full width and pushes the row right.
    row = box.row(align=True)
    row.scale_y = 0.6
    for cell in cells:
        here = cell.start <= now <= cell.end
        slot = row.row(align=True)
        slot.operator(
            "m2mr.diag_jump", text="", icon="TRIA_UP" if here else "NONE", emboss=False
        ).frame = cell.target


def _draw_diagnostics(layout, scene) -> None:
    """Frame bar of the job's self-intersections: red cells are frames to fix."""
    from ..operators.diagnostics import pair_label
    from ..services.diagnostics_reader import frame_cells, issues_at, load_diagnostics

    report = load_diagnostics(scene.m2mr.job_output_dir)
    box = layout.box()
    box.label(text=t("section_diagnostics"))
    if report is None:
        box.label(text=t("diag_missing"), icon="INFO")
        return
    summary = report["summary"]["self_intersection"]
    if not report["issues"]:
        box.label(text=t("diag_clean", cm=f"{report['threshold_cm']:g}"), icon="CHECKMARK")
        _draw_report_button(box, scene.m2mr.job_output_dir)
        return
    box.label(text=t("diag_summary", n=summary["issue_count"], cm=f"{summary['max_depth_cm']:g}"), icon="ERROR")

    # Frame bar: one button per cell, red where any frame in it intersects.
    # Click a cell to go there.
    now = scene.frame_current
    cells = frame_cells(report, _CELLS)
    bar = box.row(align=True)
    bar.scale_y = 1.5
    for cell in cells:
        slot = bar.row(align=True)
        slot.alert = cell.hit
        slot.operator("m2mr.diag_jump", text="", depress=cell.start <= now <= cell.end).frame = cell.target
    _draw_playhead(box, cells, now)

    n = int(report["frame_count"])
    # Thirds of the bar width, so the middle tick sits at the centre.
    axis = box.split(factor=1 / 3)
    axis.scale_y = 0.6
    axis.label(text="0")
    rest = axis.split(factor=0.5)
    for value, align in (((n - 1) // 2, "CENTER"), (n - 1, "RIGHT")):
        c = rest.row()
        c.alignment = align
        c.label(text=str(value))

    here = issues_at(report, now)
    status = box.column(align=True)
    if here:
        status.alert = True
        status.label(text=t("diag_frame_bad", f=now), icon="ERROR")
        for issue in sorted(here, key=lambda i: -i["max_depth_cm"]):
            status.label(text=f"    {pair_label(issue)}  {issue['max_depth_cm']:.1f} cm")
    else:
        status.label(text=t("diag_frame_ok", f=now), icon="CHECKMARK")
    nav = box.row(align=True)
    nav.operator("m2mr.diag_step", text=t("diag_prev"), icon="TRIA_LEFT").direction = -1
    nav.operator("m2mr.diag_step", text=t("diag_next"), icon="TRIA_RIGHT").direction = 1
    _draw_report_button(box, scene.m2mr.job_output_dir)


def _draw_report_button(box, run_dir: str) -> None:
    from ..operators.diagnostics import report_state

    state = report_state(run_dir)
    row = box.row()
    if state == "building":
        row.enabled = False
        row.operator("m2mr.diag_report", text=t("diag_report_building"), icon="SORTTIME")
        return
    row.operator("m2mr.diag_report", text=t("diag_report"), icon="URL")
    if state == "failed":
        box.label(text=t("diag_report_failed"), icon="ERROR")


def _first_run(prefs) -> bool:
    """Model weights not downloaded yet (only known once the project directory is set)."""
    from ..services.weights_download import weights_complete, weights_dir

    if not prefs.project_dir:
        return False
    return not weights_complete(weights_dir(prefs.project_dir))


def _draw_first_run_note(layout) -> None:
    note = layout.box()
    note.label(text=t("first_run_title"), icon="INFO")
    note.label(text=t("first_run_body"))
    note.label(text=t("first_run_once"))


def _format_eta(seconds: float) -> str:
    if seconds < 0:
        return t("dl_eta_unknown")
    if seconds < 60:
        return t("dl_eta_under_minute")
    return t("dl_eta_minutes", minutes=int(round(seconds / 60.0)))


def _draw_download(layout, props) -> None:
    sub = layout.box()
    sub.label(text=t("dl_title"), icon="IMPORT")
    total = props.dl_total or 1.0
    text = t(
        "dl_progress_fmt",
        done=f"{props.dl_done / 1e9:.1f}",
        total=f"{props.dl_total / 1e9:.1f}",
        rate=f"{props.dl_rate / 1e6:.1f}",
        eta=_format_eta(props.dl_eta),
    )
    try:
        sub.progress(factor=min(1.0, props.dl_done / total), type="BAR", text=text)
    except Exception:
        sub.label(text=text)
    sub.label(text=t("first_run_once"))


def register() -> None:
    safe_register_class(M2MR_PT_main)


def unregister() -> None:
    safe_unregister_class(M2MR_PT_main)
