"""Open the job output folder or the full log in the system file manager."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.types import Context, Operator

from ..i18n import t
from ..registration import safe_register_class, safe_unregister_class
from ..services.backend import open_path


class M2MR_OT_open_output(Operator):
    bl_idname = "m2mr.open_output"
    bl_label = "Open Output Folder"
    bl_description = "Open the Motion2MixamoRig job directory"

    def execute(self, context: Context):
        path = Path(context.scene.m2mr.job_output_dir).expanduser()
        if not path.is_dir():
            self.report({"ERROR"}, t("err_output_missing"))
            return {"CANCELLED"}
        try:
            open_path(path)
        except OSError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class M2MR_OT_view_log(Operator):
    bl_idname = "m2mr.view_log"
    bl_label = "View Full Log"
    bl_description = "Open the job log in the default text editor"

    def execute(self, context: Context):
        path = Path(context.scene.m2mr.job_log_path).expanduser()
        if not path.is_file():
            self.report({"ERROR"}, t("err_log_missing"))
            return {"CANCELLED"}
        try:
            open_path(path)
        except OSError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


def register() -> None:
    safe_register_class(M2MR_OT_open_output)
    safe_register_class(M2MR_OT_view_log)


def unregister() -> None:
    safe_unregister_class(M2MR_OT_view_log)
    safe_unregister_class(M2MR_OT_open_output)
