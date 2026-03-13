from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import bpy

if TYPE_CHECKING:
    from bpy._typing.rna_enums import ConstraintTypeItems, ObjectModifierTypeItems
    from bpy.types import Constraint, Modifier


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
