"""Per-scene UI and job state."""

from __future__ import annotations

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup, Scene

from .registration import safe_register_class, safe_unregister_class


_SOURCE_TYPE_ITEMS = ()
_DEVICE_ITEMS = ()
_EXTRACTOR_ITEMS = ()


def _source_type_items(self, context):
    from .i18n import t

    global _SOURCE_TYPE_ITEMS
    _SOURCE_TYPE_ITEMS = (
        ("VIDEO", t("source_video"), t("source_video_desc")),
        ("IMAGE", t("source_image"), t("source_image_desc")),
    )
    return _SOURCE_TYPE_ITEMS


def _update_show_floor_markers(self, context) -> None:
    from .operators.import_result import apply_floor_marker_visibility

    apply_floor_marker_visibility(bool(self.show_floor_markers))
    screen = getattr(context, "screen", None) if context is not None else None
    if screen is None:
        return
    for area in screen.areas:
        if area.type == "VIEW_3D":
            area.tag_redraw()


def _extractor_items(self, context):
    from .i18n import t

    global _EXTRACTOR_ITEMS
    _EXTRACTOR_ITEMS = (
        ("gvhmr", "GVHMR", t("extractor_gvhmr_desc")),
    )
    return _EXTRACTOR_ITEMS


def _device_items(self, context):
    from .i18n import t

    global _DEVICE_ITEMS
    _DEVICE_ITEMS = (
        ("cpu", "CPU", t("device_cpu_desc")),
        ("cuda", "CUDA", t("device_cuda_desc")),
        ("mps", "MPS", t("device_mps_desc")),
    )
    return _DEVICE_ITEMS


class M2MRProperties(PropertyGroup):
    source_type: EnumProperty(
        name="Source Type",
        items=_source_type_items,
    )
    source_path: StringProperty(
        name="Source File",
        subtype="FILE_PATH",
        maxlen=2048,
        default="",
    )
    rig_path: StringProperty(
        name="Mixamo Rig FBX",
        subtype="FILE_PATH",
        maxlen=2048,
        default="",
    )
    device: EnumProperty(
        name="Device",
        items=_device_items,
    )
    extractor: EnumProperty(
        name="Body Model",
        description="How the video or still becomes a 3D skeleton",
        items=_extractor_items,
    )
    detect_hands: BoolProperty(
        name="Detect Hands",
        description=(
            "Also run the hand model that belongs to the selected body model "
            "(GVHMR uses HaMeR). Off leaves the fingers at rest. "
            "The run takes about twice as long"
        ),
        default=False,
    )
    hand_smooth: FloatProperty(
        name="Finger Smoothing",
        description="Smooth detected finger rotations over this many seconds. 0 keeps the raw estimate",
        default=0.08,
        min=0.0,
        max=2.0,
        step=1,
        precision=2,
    )
    generate_preview: BoolProperty(
        name="Generate Preview Videos",
        description="Also render preview videos/images (slower)",
        default=False,
    )

    env_status: EnumProperty(
        name="Environment",
        items=(
            ("NOT_CHECKED", "Not checked", ""),
            ("CHECKING", "Checking", ""),
            ("READY", "Ready", ""),
            ("ERROR", "Error", ""),
        ),
        default="NOT_CHECKED",
    )
    env_message: StringProperty(name="Environment message", default="", maxlen=512)

    setup_status: StringProperty(name="Runtime setup status", default="idle", maxlen=64)
    setup_progress: FloatProperty(name="Runtime setup progress", default=0.0, min=0.0, max=1.0)
    setup_message: StringProperty(name="Runtime setup message", default="", maxlen=512)
    show_advanced: BoolProperty(name="Advanced", default=False)
    show_setup: BoolProperty(name="Setup", description="Show or hide the Setup section", default=True)

    job_status: StringProperty(name="Job status", default="idle", maxlen=64)
    job_stage: StringProperty(name="Job stage", default="", maxlen=64)
    job_progress: FloatProperty(name="Progress", default=0.0, min=0.0, max=1.0)
    job_error: StringProperty(name="Job error", default="", maxlen=512)
    job_glb_path: StringProperty(name="GLB path", default="", maxlen=2048, subtype="FILE_PATH")
    job_output_dir: StringProperty(name="Output folder", default="", maxlen=2048, subtype="DIR_PATH")
    job_log_path: StringProperty(name="Log path", default="", maxlen=2048, subtype="FILE_PATH")
    job_id: StringProperty(name="Job id", default="", maxlen=128)
    job_source_name: StringProperty(name="Source name", default="", maxlen=128)
    import_note: StringProperty(name="Import note", default="", maxlen=512)
    show_floor_markers: BoolProperty(
        name="Floor Markers",
        description="Show or hide the floor markers",
        default=True,
        update=_update_show_floor_markers,
    )

    # First-run model download, filled in by the job poller.
    dl_active: BoolProperty(name="Downloading models", default=False)
    dl_done: FloatProperty(name="Downloaded bytes", default=0.0)
    dl_total: FloatProperty(name="Total bytes", default=0.0)
    dl_rate: FloatProperty(name="Download speed (bytes/s)", default=0.0)
    dl_eta: FloatProperty(name="Seconds left", default=-1.0)


def register() -> None:
    safe_register_class(M2MRProperties)
    Scene.m2mr = bpy.props.PointerProperty(type=M2MRProperties)


def unregister() -> None:
    if hasattr(Scene, "m2mr"):
        del Scene.m2mr
    safe_unregister_class(M2MRProperties)
