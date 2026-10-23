"""Import a generated mixamo_character.glb and set the scene timeline."""

from __future__ import annotations

import math
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


_MARKER_FLAG = "m2mr_floor_markers"
_MARKER_STEP = 0.5
_MARKER_PAD = 1.5


def _marker_material(name: str, rgba: tuple[float, float, float, float]):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    mat.diffuse_color = rgba
    tree = mat.node_tree
    bsdf = tree.nodes.get("Principled BSDF") if tree is not None else None
    if bsdf is not None and "Base Color" in bsdf.inputs:
        bsdf.inputs["Base Color"].default_value = rgba
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 1.0
    return mat


def _clear_floor_markers(collection) -> None:
    for obj in list(collection.objects):
        if not obj.get(_MARKER_FLAG):
            continue
        mesh = obj.data if obj.type == "MESH" else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def _hips_travel(context: Context, armature):
    """World XY bounds of the hips across the timeline. Blender is Z-up."""
    bone = None
    if armature is not None and getattr(armature, "pose", None) is not None:
        for candidate in armature.pose.bones:
            if candidate.name.lower().endswith("hips"):
                bone = candidate
                break
    if bone is None:
        return None
    scene = context.scene
    span = max(0, int(scene.frame_end) - int(scene.frame_start))
    stride = max(1, span // 120)
    original = scene.frame_current
    # A hidden armature drops out of the depsgraph, so the pose would stay
    # on the rest hips and the markers would miss the travel.
    was_hidden = False
    was_viewport = bool(armature.hide_viewport)
    try:
        was_hidden = bool(armature.hide_get())
    except Exception:
        was_hidden = False
    xs: list[float] = []
    ys: list[float] = []
    try:
        armature.hide_viewport = False
        try:
            armature.hide_set(False)
        except Exception:
            pass
        frame = int(scene.frame_start)
        last = int(scene.frame_end)
        while frame <= last:
            scene.frame_set(frame)
            context.view_layer.update()
            co = armature.matrix_world @ bone.head
            xs.append(float(co.x))
            ys.append(float(co.y))
            if frame == last:
                break
            frame = min(last, frame + stride)
    finally:
        scene.frame_set(original)
        armature.hide_viewport = was_viewport
        if was_hidden:
            try:
                armature.hide_set(True)
            except Exception:
                pass
    if not xs:
        return None
    return min(xs), max(xs), min(ys), max(ys)


def _add_floor_markers(context: Context, collection, armature) -> None:
    """One mesh of floor crosses on Z=0, covering where the hips travel.

    Replaced on the next import into the same collection. glTF Y-up lands on
    Blender Z-up, so the grounded sole plane is z=0.
    """
    _clear_floor_markers(collection)
    travel = _hips_travel(context, armature)
    if travel is None:
        min_x, max_x, min_y, max_y = -2.0, 2.0, -2.0, 2.0
    else:
        min_x, max_x, min_y, max_y = travel
        min_x -= _MARKER_PAD
        max_x += _MARKER_PAD
        min_y -= _MARKER_PAD
        max_y += _MARKER_PAD
    step = _MARKER_STEP
    x0, x1 = math.floor(min_x / step) * step, math.ceil(max_x / step) * step
    y0, y1 = math.floor(min_y / step) * step, math.ceil(max_y / step) * step
    nx = int(round((x1 - x0) / step))
    ny = int(round((y1 - y0) / step))
    if (nx + 1) * (ny + 1) > 2500:
        step = 1.0
        x0, x1 = math.floor(min_x), math.ceil(max_x)
        y0, y1 = math.floor(min_y), math.ceil(max_y)
        nx = int(round(x1 - x0))
        ny = int(round(y1 - y0))

    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    slots: list[int] = []
    z = 0.002

    def plus(x: float, y: float, arm: float, thick: float, slot: int) -> None:
        bars = (
            (x - arm, y - thick, x + arm, y - thick, x + arm, y + thick, x - arm, y + thick),
            (x - thick, y - arm, x + thick, y - arm, x + thick, y + arm, x - thick, y + arm),
        )
        for b in bars:
            o = len(verts)
            verts.extend((
                (b[0], b[1], z), (b[2], b[3], z), (b[4], b[5], z), (b[6], b[7], z),
            ))
            faces.append((o, o + 1, o + 2, o + 3))
            slots.append(slot)

    for ix in range(nx + 1):
        for iy in range(ny + 1):
            x = x0 + ix * step
            y = y0 + iy * step
            origin = abs(x) < 1e-3 and abs(y) < 1e-3
            metre = abs(x - round(x)) < 1e-3 and abs(y - round(y)) < 1e-3
            if origin:
                plus(x, y, 0.16, 0.016, 2)
            elif metre:
                plus(x, y, 0.10, 0.012, 1)
            else:
                plus(x, y, 0.055, 0.010, 0)

    mesh = bpy.data.meshes.new("Floor Markers")
    mesh.from_pydata(verts, [], faces)
    grey = _marker_material("M2MR Floor Marker", (0.54, 0.54, 0.54, 1.0))
    metre_mat = _marker_material("M2MR Floor Marker Metre", (0.82, 0.82, 0.82, 1.0))
    origin_mat = _marker_material("M2MR Floor Marker Origin", (0.463, 0.725, 0.0, 1.0))
    mesh.materials.append(grey)
    mesh.materials.append(metre_mat)
    mesh.materials.append(origin_mat)
    for poly, slot in zip(mesh.polygons, slots):
        poly.material_index = slot
    mesh.update()

    obj = bpy.data.objects.new("Floor Markers", mesh)
    obj[_MARKER_FLAG] = True
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    collection.objects.link(obj)
    visible = True
    props = getattr(getattr(context, "scene", None), "m2mr", None)
    if props is not None:
        visible = bool(props.show_floor_markers)
    apply_floor_marker_visibility(visible)


def apply_floor_marker_visibility(visible: bool) -> None:
    """Show or hide every floor-marker mesh. The result panel drives this."""
    for obj in list(bpy.data.objects):
        if not obj.get(_MARKER_FLAG):
            continue
        obj.hide_viewport = not visible
        try:
            obj.hide_set(not visible)
        except Exception:
            pass


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

    try:
        _add_floor_markers(context, collection, armature)
    except Exception as exc:
        print(f"Motion2MixamoRig floor markers skipped: {exc}")


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
