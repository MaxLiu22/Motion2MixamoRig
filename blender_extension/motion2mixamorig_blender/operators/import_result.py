"""Import a generated mixamo_character.glb and set the scene timeline."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.types import Context, Operator

from ..i18n import t
from ..registration import safe_register_class, safe_unregister_class
from ..services.backend import collection_name_for_source
from ..services.result_reader import RunResult, blender_frame_settings, read_run_json


def _import_gltf(filepath: str) -> None:
    if hasattr(bpy.ops.import_scene, "gltf"):
        bpy.ops.import_scene.gltf(filepath=filepath)
        return
    if hasattr(bpy.ops.wm, "gltf_import"):
        bpy.ops.wm.gltf_import(filepath=filepath)
        return
    raise RuntimeError("Blender glTF importer is not available")


def _view3d_region(area):
    for region in area.regions:
        if region.type == "WINDOW":
            return region
    return None


def _frame_selected(context: Context) -> None:
    wm = context.window_manager
    if wm is None:
        return
    for window in wm.windows:
        screen = window.screen
        if screen is None:
            continue
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            region = _view3d_region(area)
            if region is None:
                continue
            try:
                with context.temp_override(window=window, area=area, region=region):
                    bpy.ops.view3d.view_selected()
                return
            except Exception:
                return


def apply_scene_frames(scene, fps: float | None, n_frames: int | None) -> None:
    if fps is None or n_frames is None:
        return
    settings = blender_frame_settings(fps, n_frames)
    scene.render.fps = int(settings["fps"])
    scene.render.fps_base = float(settings["fps_base"])
    scene.frame_start = int(settings["frame_start"])
    scene.frame_end = int(settings["frame_end"])


_BUBBLE_VERTEX_LIMIT = 500


def hide_joint_bubbles(armature, imported_objects) -> None:
    """Turn off the outliner eye on Mixamo joint-bubble objects. Do not delete them.

    Blender's glTF importer assigns a small Icosphere as every bone's custom
    shape. Hiding that object (and disabling armature Shapes) removes the
    cluster of spheres; the Icosphere and bone custom_shape links stay.
    """
    imported = set(imported_objects)
    shape_objects = []
    if armature is not None and getattr(armature, "pose", None) is not None:
        seen: set = set()
        for bone in armature.pose.bones:
            shape = bone.custom_shape
            if shape is None or shape in seen or shape not in imported:
                continue
            seen.add(shape)
            shape_objects.append(shape)
        data = armature.data
        if hasattr(data, "show_bone_custom_shapes"):
            data.show_bone_custom_shapes = False
        if hasattr(data, "display_type"):
            data.display_type = "STICK"
        # Hide the armature object itself. The skinned mesh stays visible
        # and still deforms; this is the Outliner eye that removes the
        # floating joint spheres.
        try:
            armature.hide_set(True)
        except Exception:
            armature.hide_viewport = True

    extra = [
        obj
        for obj in imported
        if obj.type == "MESH"
        and obj.name.rsplit(".", 1)[0] == "Icosphere"
        and len(obj.data.vertices) <= _BUBBLE_VERTEX_LIMIT
        and obj not in shape_objects
    ]
    shape_objects.extend(extra)

    for obj in shape_objects:
        if obj.type == "ARMATURE":
            continue
        if obj.type == "MESH" and len(obj.data.vertices) > _BUBBLE_VERTEX_LIMIT:
            continue
        try:
            obj.hide_set(True)
        except Exception:
            pass
        obj.hide_viewport = True


def import_generated_character(
    context: Context,
    result: RunResult,
    *,
    source_name: str,
) -> None:
    if result.glb_path is None or not result.glb_path.is_file():
        raise FileNotFoundError("Result GLB not found")

    # glTF keys are in seconds; Blender converts them with the scene FPS at
    # import time. Set that first or a 24 fps default will stretch the clip.
    apply_scene_frames(context.scene, result.fps, result.n_frames)

    existing = set(bpy.data.objects)
    _import_gltf(str(result.glb_path))
    new_objects = [obj for obj in bpy.data.objects if obj not in existing]
    if not new_objects:
        raise RuntimeError("glTF import produced no objects")

    collection_name = collection_name_for_source(source_name)
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(collection)

    for obj in new_objects:
        for user in list(obj.users_collection):
            user.objects.unlink(obj)
        if obj.name not in collection.objects:
            collection.objects.link(obj)

    armature = next((obj for obj in new_objects if obj.type == "ARMATURE"), None)
    hide_joint_bubbles(armature, new_objects)
    view_layer = context.view_layer
    for obj in list(view_layer.objects):
        obj.select_set(False)
    visible_mesh = next(
        (
            obj
            for obj in new_objects
            if obj.type == "MESH" and not obj.hide_get() and obj.name.rsplit(".", 1)[0] != "Icosphere"
        ),
        None,
    )
    focus = visible_mesh or armature
    if focus is not None:
        focus.select_set(True)
        view_layer.objects.active = focus
        try:
            _frame_selected(context)
        except Exception:
            pass
    elif new_objects:
        new_objects[0].select_set(True)
        view_layer.objects.active = new_objects[0]


class M2MR_OT_import_result(Operator):
    bl_idname = "m2mr.import_result"
    bl_label = "Import Generated Character"
    bl_description = "Import mixamo_character.glb from the last Motion2MixamoRig job"

    def execute(self, context: Context):
        props = context.scene.m2mr
        run_dir = Path(props.job_output_dir).expanduser() if props.job_output_dir else None
        if run_dir is None or not run_dir.is_dir():
            self.report({"ERROR"}, t("err_no_job_folder"))
            return {"CANCELLED"}

        result = read_run_json(run_dir)
        if result.glb_path is None or not result.glb_path.is_file():
            props.job_error = "err_glb"
            self.report({"ERROR"}, t("err_glb"))
            return {"CANCELLED"}

        try:
            import_generated_character(
                context,
                result,
                source_name=props.job_source_name or run_dir.name,
            )
        except Exception as exc:
            props.import_note = "generation_import_failed"
            props.job_error = f"generation_import_failed: {exc}"
            self.report({"ERROR"}, f"{t('generation_import_failed')}: {exc}")
            return {"CANCELLED"}

        props.job_glb_path = str(result.glb_path)
        props.import_note = ""
        if props.job_status in {"import_failed", "completed"}:
            props.job_status = "completed"
            props.job_error = ""
        self.report({"INFO"}, t("info_imported", name=result.glb_path.name))
        return {"FINISHED"}


def register() -> None:
    safe_register_class(M2MR_OT_import_result)


def unregister() -> None:
    safe_unregister_class(M2MR_OT_import_result)
