from __future__ import annotations

from typing import TYPE_CHECKING

from mathutils import Vector

if TYPE_CHECKING:
    from bpy.types import Node


def node_abs_location(node: Node) -> Vector:
    if node.parent:
        return node.location.copy() + node_abs_location(node.parent)
    else:
        return node.location.copy()
