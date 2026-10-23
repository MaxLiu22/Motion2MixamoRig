"""One-click runtime setup, and copying the user's SMPL-X model into place."""

from __future__ import annotations

import shutil
from pathlib import Path

import bpy
from bpy.props import StringProperty
from bpy.types import Context, Operator

from ..i18n import t
from ..preferences import get_preferences
from ..registration import safe_register_class, safe_unregister_class
from ..services.backend import directory_exists, launch_process
from ..services.runtime_setup import (
    app_dir,
    bootstrap_env,
    build_setup_argv,
    bundled_backend,
    default_home,
    setup_log_dir,
)
from .runtime import JobRuntime, attach, is_busy

SMPLX_RELATIVE = Path("assets") / "body_models" / "smplx" / "SMPLX_NEUTRAL.npz"
MANO_DIR = Path("assets") / "body_models" / "mano"


class M2MR_OT_setup_runtime(Operator):
    bl_idname = "m2mr.setup_runtime"
    bl_label = "Install Runtime"
    bl_description = (
        "Download Python and Motion2MixamoRig's dependencies into ~/Motion2MixamoRig "
        "(first time only; several GB)"
    )

    def execute(self, context: Context):
        if is_busy():
            self.report({"ERROR"}, t("err_busy"))
            return {"CANCELLED"}
        backend = bundled_backend()
        if backend is None:
            self.report({"ERROR"}, t("err_backend_missing"))
            return {"CANCELLED"}

        home = default_home()
        logs = setup_log_dir(home)
        logs.mkdir(parents=True, exist_ok=True)
        progress_path = logs / "setup_progress.jsonl"
        log_path = logs / "setup.log"
        try:
            process, log_file = launch_process(
                build_setup_argv(home, backend, progress_path),
                cwd=home,
                log_path=log_path,
                env=bootstrap_env(),
            )
        except OSError as exc:
            self.report({"ERROR"}, f"{t('setup_failed')}: {exc}")
            return {"CANCELLED"}

        props = context.scene.m2mr
        props.setup_status = "running"
        props.setup_progress = 0.0
        props.setup_message = ""
        attach(
            JobRuntime(
                kind="setup",
                process=process,
                owned_pid=process.pid,
                output_dir=logs,
                log_path=log_path,
                progress_path=progress_path,
                log_file=log_file,
                extra={"home": str(home)},
            )
        )
        self.report({"INFO"}, t("setup_started"))
        return {"FINISHED"}


class M2MR_OT_set_smplx(Operator):
    bl_idname = "m2mr.set_smplx"
    bl_label = "Choose SMPL-X Model"
    bl_description = "Pick the SMPLX_NEUTRAL.npz you downloaded; it is copied into the runtime"

    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.npz;*.pkl", options={"HIDDEN"})

    def invoke(self, context: Context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context: Context):
        src = Path(bpy.path.abspath(self.filepath))
        if not src.is_file():
            self.report({"ERROR"}, t("err_smplx"))
            return {"CANCELLED"}
        prefs = get_preferences(context)
        project = Path(prefs.project_dir) if directory_exists(prefs.project_dir) else app_dir(default_home())
        dest = project / SMPLX_RELATIVE
        if src.suffix.lower() == ".pkl":
            dest = dest.with_suffix(".pkl")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        self.report({"INFO"}, t("smplx_copied", path=str(dest)))
        return {"FINISHED"}


class M2MR_OT_set_mano(Operator):
    bl_idname = "m2mr.set_mano"
    bl_label = "Choose MANO Hand Model"
    bl_description = "Pick the MANO_RIGHT.pkl you downloaded; it is copied into the runtime"

    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.pkl;*.npz", options={"HIDDEN"})

    def invoke(self, context: Context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context: Context):
        src = Path(bpy.path.abspath(self.filepath))
        if not src.is_file() or src.suffix.lower() not in {".pkl", ".npz"}:
            self.report({"ERROR"}, t("err_mano"))
            return {"CANCELLED"}
        prefs = get_preferences(context)
        project = Path(prefs.project_dir) if directory_exists(prefs.project_dir) else app_dir(default_home())
        name = "MANO_RIGHT.npz" if src.suffix.lower() == ".npz" else "MANO_RIGHT.pkl"
        dest = project / MANO_DIR / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        self.report({"INFO"}, t("mano_copied", path=str(dest)))
        return {"FINISHED"}


CLASSES = (M2MR_OT_setup_runtime, M2MR_OT_set_smplx, M2MR_OT_set_mano)


def register() -> None:
    for cls in CLASSES:
        safe_register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        safe_unregister_class(cls)
