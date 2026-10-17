"""Diagnostics frame bar actions: jump to a frame, step to the next / previous problem."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.app.handlers import persistent
from bpy.props import IntProperty
from bpy.types import Context, Operator

from ..i18n import t
from ..registration import safe_register_class, safe_unregister_class
from ..services.diagnostics_reader import MARKER_PREFIX, load_diagnostics, step_problem


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
        run_dir = context.scene.m2mr.job_output_dir
        report = load_diagnostics(Path(run_dir).expanduser()) if run_dir else None
        target = step_problem(report, context.scene.frame_current, self.direction) if report else None
        if target is None:
            self.report({"INFO"}, t("diag_no_more"))
            return {"CANCELLED"}
        context.scene.frame_set(target)
        return {"FINISHED"}


class M2MR_OT_diag_toggle_time(Operator):
    bl_idname = "m2mr.diag_toggle_time"
    bl_label = "Frames / Seconds"
    bl_description = "Show frame numbers or seconds, here and in Blender's timeline"

    def execute(self, context: Context):
        props = context.scene.m2mr
        props.diag_show_time = not props.diag_show_time
        # The timeline, dope sheet, graph and NLA editors follow the same switch.
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                for space in area.spaces:
                    if hasattr(space, "show_seconds"):
                        space.show_seconds = props.diag_show_time
                area.tag_redraw()
        return {"FINISHED"}


class M2MR_OT_diag_markers(Operator):
    bl_idname = "m2mr.diag_markers"
    bl_label = "Mark on Timeline"
    bl_description = "Add a timeline marker at the worst frame of each intersecting pair"

    def execute(self, context: Context):
        run_dir = context.scene.m2mr.job_output_dir
        report = load_diagnostics(Path(run_dir).expanduser()) if run_dir else None
        if report is None:
            self.report({"ERROR"}, t("diag_missing"))
            return {"CANCELLED"}
        markers = context.scene.timeline_markers
        for m in [m for m in markers if m.name.startswith(MARKER_PREFIX)]:
            markers.remove(m)
        for issue in report["issues"]:
            name = f"{MARKER_PREFIX}{'-'.join(issue['parts'])} {issue['max_depth_cm']:.1f}cm"
            markers.new(name[:63], frame=int(issue["worst_frame"]))
        self.report({"INFO"}, t("diag_markers_added", n=len(report["issues"])))
        return {"FINISHED"}


class M2MR_OT_diag_clear_markers(Operator):
    bl_idname = "m2mr.diag_clear_markers"
    bl_label = "Clear Markers"
    bl_description = "Remove the timeline markers added by Diagnostics (your own markers stay)"

    def execute(self, context: Context):
        markers = context.scene.timeline_markers
        for m in [m for m in markers if m.name.startswith(MARKER_PREFIX)]:
            markers.remove(m)
        return {"FINISHED"}


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


CLASSES = (M2MR_OT_diag_jump, M2MR_OT_diag_step, M2MR_OT_diag_toggle_time, M2MR_OT_diag_markers, M2MR_OT_diag_clear_markers)


def register() -> None:
    for cls in CLASSES:
        safe_register_class(cls)
    if _redraw_sidebar not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(_redraw_sidebar)


def unregister() -> None:
    if _redraw_sidebar in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(_redraw_sidebar)
    for cls in reversed(CLASSES):
        safe_unregister_class(cls)
