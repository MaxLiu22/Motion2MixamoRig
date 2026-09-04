"""Check the configured External Python and Motion2MixamoRig install."""

from __future__ import annotations

import subprocess

import bpy
from bpy.types import Context, Operator

from ..i18n import encode, t
from ..preferences import get_preferences
from ..registration import safe_register_class, safe_unregister_class
from ..services.backend import (
    build_doctor_argv,
    build_version_argv,
    directory_exists,
    job_output_dir,
    launch_process,
    python_exists,
    subprocess_env,
)
from .runtime import JobRuntime, attach, is_busy


class M2MR_OT_check_environment(Operator):
    bl_idname = "m2mr.check_environment"
    bl_label = "Check Environment"
    bl_description = "Verify External Python and that Motion2MixamoRig can run doctor"

    def execute(self, context: Context):
        if is_busy():
            self.report({"ERROR"}, t("err_busy"))
            return {"CANCELLED"}

        prefs = get_preferences(context)
        python = prefs.python_path
        project = prefs.project_dir
        props = context.scene.m2mr

        if not python_exists(python):
            props.env_status = "ERROR"
            props.env_message = "err_python"
            self.report({"ERROR"}, t("err_python"))
            return {"CANCELLED"}
        if not directory_exists(project):
            props.env_status = "ERROR"
            props.env_message = "err_project"
            self.report({"ERROR"}, t("err_project"))
            return {"CANCELLED"}

        try:
            version = subprocess.run(
                build_version_argv(python),
                capture_output=True,
                text=True,
                timeout=8,
                shell=False,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            props.env_status = "ERROR"
            props.env_message = "err_python"
            self.report({"ERROR"}, f"{t('err_python')}: {exc}")
            return {"CANCELLED"}

        version_text = (version.stdout or version.stderr or "").strip()
        if version.returncode != 0:
            props.env_status = "ERROR"
            props.env_message = "err_python"
            self.report({"ERROR"}, t("err_python"))
            return {"CANCELLED"}

        output_dir = job_output_dir(project, "_env_check")
        output_dir.mkdir(parents=True, exist_ok=True)
        log_path = output_dir / "doctor.log"
        header = f"{version_text}\n"
        log_path.write_text(header, encoding="utf-8")

        try:
            process, log_file = launch_process(
                build_doctor_argv(python),
                cwd=project,
                log_path=log_path,
                env=subprocess_env(project),
            )
        except OSError as exc:
            props.env_status = "ERROR"
            props.env_message = f"err_python: {exc}"
            self.report({"ERROR"}, f"{t('err_python')}: {exc}")
            return {"CANCELLED"}

        try:
            log_file.close()
        except OSError:
            pass

        props.env_status = "CHECKING"
        props.env_message = encode("env_checking_fmt", version=version_text)
        attach(
            JobRuntime(
                kind="doctor",
                process=process,
                owned_pid=process.pid,
                output_dir=output_dir,
                log_path=log_path,
                progress_path=output_dir / "progress.jsonl",
                log_file=None,
                extra={"python_version": version_text},
            )
        )
        self.report({"INFO"}, t("info_started_env", version=version_text))
        return {"FINISHED"}


def register() -> None:
    safe_register_class(M2MR_OT_check_environment)


def unregister() -> None:
    safe_unregister_class(M2MR_OT_check_environment)
