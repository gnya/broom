from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bpy.types import bpy_struct


def has_driver(data: bpy_struct[Any], property: str) -> bool:
    animation_data = getattr(data.id_data, "animation_data", None)

    if animation_data is None:
        return False

    path = data.path_from_id(property)

    for d in animation_data.drivers:
        if d.data_path == path:
            return True

    return False
