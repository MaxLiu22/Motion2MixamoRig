"""Motion2MixamoRig Blender Extension: UI + external `m2mr` process control."""

from __future__ import annotations

bl_info = {
    "name": "Motion2MixamoRig",
    "author": "Max Liu",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Motion2MixamoRig",
    "description": "Transfer human motion from video to Mixamo characters",
    "category": "Animation",
}

from . import operators, panels, preferences, properties


def register() -> None:
    try:
        unregister()
    except Exception:
        pass
    preferences.register()
    properties.register()
    operators.register()
    panels.register()


def unregister() -> None:
    try:
        panels.unregister()
    except Exception:
        pass
    try:
        operators.unregister()
    except Exception:
        pass
    try:
        properties.unregister()
    except Exception:
        pass
    try:
        preferences.unregister()
    except Exception:
        pass
