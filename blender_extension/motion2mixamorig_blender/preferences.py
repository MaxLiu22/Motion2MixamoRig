"""Add-on preferences that persist across .blend files."""

from __future__ import annotations

import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import AddonPreferences, Context

from .registration import safe_register_class, safe_unregister_class


ADDON_ID = __package__


def _on_language_update(self, context: Context) -> None:
    wm = context.window_manager
    if wm is None:
        return
    for window in wm.windows:
        screen = window.screen
        if screen is None:
            continue
        for area in screen.areas:
            area.tag_redraw()


# Static items: identifiers must be valid Python names (no "-").
# A callback + default= is rejected by Blender during register_class.
_UI_LANGUAGE_ITEMS = (
    ("AUTO", "Auto (Blender / System)", ""),
    ("en", "English", ""),
    ("zh_CN", "中文", ""),
    ("ko", "한국어", ""),
    ("ja", "日本語", ""),
    ("de", "Deutsch", ""),
    ("ru", "Русский", ""),
    ("ar", "العربية", ""),
)


class M2MRPreferences(AddonPreferences):
    bl_idname = ADDON_ID

    python_path: StringProperty(
        name="External Python",
        description="Python interpreter that has Motion2MixamoRig installed (not Blender's Python)",
        subtype="FILE_PATH",
        maxlen=2048,
        default="",
    )
    project_dir: StringProperty(
        name="Project Directory",
        description="Motion2MixamoRig repository or install directory",
        subtype="DIR_PATH",
        maxlen=2048,
        default="",
    )
    ui_language: EnumProperty(
        name="UI Language",
        description="Plugin UI language. Auto follows Blender / the system language",
        items=_UI_LANGUAGE_ITEMS,
        default="AUTO",
        update=_on_language_update,
    )

    def draw(self, context: Context) -> None:
        from .i18n import t

        layout = self.layout
        layout.prop(self, "ui_language", text=t("ui_language"))
        layout.prop(self, "python_path", text=t("external_python"))
        layout.prop(self, "project_dir", text=t("project_directory"))
        layout.label(text=t("prefs_venv_hint"))


def get_preferences(context: Context | None = None) -> M2MRPreferences:
    ctx = context or bpy.context
    addons = ctx.preferences.addons
    if ADDON_ID in addons:
        return addons[ADDON_ID].preferences
    for key in addons.keys():
        if key.endswith(".motion2mixamorig") or key in {
            "motion2mixamorig",
            "motion2mixamorig_blender",
        }:
            return addons[key].preferences
    raise KeyError(f"Motion2MixamoRig add-on preferences not found ({ADDON_ID})")


def register() -> None:
    safe_register_class(M2MRPreferences)


def unregister() -> None:
    safe_unregister_class(M2MRPreferences)
