"""Reload-safe class registration.

Installing a zip over an enabled extension imports a new class object while
Blender still holds the previous one. Operators and panels stay on
``bpy.types``. Preferences and property groups do not: Blender 5.2 keeps
those only on the RNA subclass list, so a ``bpy.types`` lookup misses them
and the next ``register_class`` reports "already registered".
"""

from __future__ import annotations

import bpy

# Bases whose subclasses Blender may keep off ``bpy.types``.
_SUBCLASS_ROOTS = (
    "AddonPreferences",
    "PropertyGroup",
    "Operator",
    "Panel",
    "Menu",
    "Header",
    "UIList",
)


def _registered_classes(name: str) -> list[type]:
    found: list[type] = []
    seen: set[int] = set()

    def add(cls) -> None:
        if not isinstance(cls, type) or cls.__name__ != name or id(cls) in seen:
            return
        seen.add(id(cls))
        found.append(cls)

    add(getattr(bpy.types, name, None))
    for root_name in _SUBCLASS_ROOTS:
        root = getattr(bpy.types, root_name, None)
        if root is None:
            continue
        for subclass in root.__subclasses__():
            add(subclass)
    return found


def _unregister_named(name: str) -> None:
    for existing in _registered_classes(name):
        if not getattr(existing, "is_registered", False):
            continue
        try:
            bpy.utils.unregister_class(existing)
        except Exception:
            pass


def safe_register_class(cls) -> None:
    _unregister_named(cls.__name__)
    try:
        bpy.utils.register_class(cls)
    except ValueError as exc:
        if "already registered" not in str(exc):
            raise
        _unregister_named(cls.__name__)
        bpy.utils.register_class(cls)


def safe_unregister_class(cls) -> None:
    _unregister_named(cls.__name__)
