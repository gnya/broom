from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import bpy
from bpy.types import NodeTree

if TYPE_CHECKING:
    from bpy._typing.rna_enums import (
        ConstraintTypeItems,
        ObjectModifierTypeItems,
        ObjectTypeItems,
    )
    from bpy.types import ID, Armature, Constraint, Modifier, Node, Object


def object_itr(type: ObjectTypeItems | None = None) -> Iterator[Object]:
    for obj in bpy.data.objects:
        if type is None or obj.type == type:
            yield obj


def modifier_itr(type: ObjectModifierTypeItems | None = None) -> Iterator[Modifier]:
    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if type is None or modifier.type == type:
                yield modifier


def constraint_itr(
    type: ConstraintTypeItems | None = None, rigify: bool = True
) -> Iterator[Constraint]:
    for obj in bpy.data.objects:
        for constraint in obj.constraints:
            if type is None or constraint.type == type:
                yield constraint

        if obj.type == "ARMATURE" and (rigify or "rig_ui" not in obj.keys()):
            for bone in obj.pose.bones:
                for constraint in bone.constraints:
                    if type is None or constraint.type == type:
                        yield constraint


def node_connection_itr(node: Node) -> Iterator[Node]:
    for input in node.inputs:
        for link in input.links:
            yield link.from_node

    for output in node.outputs:
        for link in output.links:
            yield link.to_node


def node_itr(data: ID, node_tree: NodeTree | None = None) -> Iterator[Node]:
    data_node_tree = getattr(data, "node_tree", data)

    if isinstance(data_node_tree, NodeTree):
        for node in data_node_tree.nodes:
            if node_tree is None or node_tree == getattr(node, "node_tree", None):
                yield node


def armature_itr() -> Iterator[Armature]:
    for armature in bpy.data.armatures:
        yield armature


def id_node_tree_user_itr() -> Iterator[ID]:
    for data in bpy.data.node_groups:
        yield data

    for data in bpy.data.materials:
        if data.use_nodes:
            yield data

    for data in bpy.data.scenes:
        if data.use_nodes:
            yield data

    for data in bpy.data.linestyles:
        if data.use_nodes:
            yield data

    for data in bpy.data.lights:
        if data.use_nodes:
            yield data

    for data in bpy.data.worlds:
        if data.use_nodes:
            yield data

    for data in bpy.data.textures:
        if data.use_nodes:
            yield data
