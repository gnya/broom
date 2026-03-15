from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Callable

from broom.utils import armature_itr, object_itr

if TYPE_CHECKING:
    from bpy._typing.rna_enums import WmReportItems
    from bpy.types import ID, Armature, Constraint, Driver, Modifier, Object

    Report = Callable[[set[WmReportItems] | None, str], None]


def _get_object_data(data: Any, prop: str) -> ID | None:
    return getattr(getattr(data, prop, None), "data", None)


def _collect_using_bones_from_constraint(
    constraint: Constraint, armature: Armature
) -> set[str]:
    using = set()

    if (
        (constraint.owner_space == "CUSTOM" or constraint.target_space == "CUSTOM")
        and _get_object_data(constraint, "space_object") == armature
        and constraint.space_subtarget != ""
    ):
        using.add(constraint.space_subtarget)

    if (
        _get_object_data(constraint, "target") == armature
        and getattr(constraint, "subtarget", "") != ""
    ):
        using.add(constraint.subtarget)

    if (
        _get_object_data(constraint, "pole_target") == armature
        and getattr(constraint, "subtarget", "") != ""
    ):
        using.add(constraint.pole_subtarget)

    for target in getattr(constraint, "targets", []):
        if (
            _get_object_data(target, "target") == armature
            and getattr(target, "subtarget", "") != ""
        ):
            using.add(target.subtarget)

    return using


def _collect_using_bones_from_driver(driver: Driver, armature: Armature) -> set[str]:
    using = set()

    for variable in driver.variables:
        for target in variable.targets:
            if _get_object_data(target, "id") == armature:
                if target.bone_target != "":
                    using.add(target.bone_target)

                if match := re.search(r'bones\["([^"]+)"\]', target.data_path):
                    using.add(match.group(1))

    return using


def _collect_using_bones_from_modifier(
    modifier: Modifier, armature: Armature
) -> set[str]:
    using = set()

    if (
        _get_object_data(modifier, "object") == armature
        and getattr(modifier, "subtarget", "") != ""
    ):
        using.add(modifier.subtarget)

    return using


def _collect_using_bones_from_object(obj: Object, armature: Armature) -> set[str]:
    using = set()

    if obj.type == "ARMATURE" and obj.data is not None:
        for bone in obj.pose.bones:
            if obj.data == armature and bone.custom_shape_transform is not None:
                using.add(bone.custom_shape_transform.name)

            for constraint in bone.constraints:
                using |= _collect_using_bones_from_constraint(constraint, armature)

    if any(m.type == "ARMATURE" and m.object.data == armature for m in obj.modifiers):
        for vertex_group in obj.vertex_groups:
            if vertex_group.name in armature.bones:
                using.add(vertex_group.name)

    for constraint in obj.constraints:
        using |= _collect_using_bones_from_constraint(constraint, armature)

    for driver in getattr(obj.animation_data, "drivers", []):
        using |= _collect_using_bones_from_driver(driver.driver, armature)

    for modifier in obj.modifiers:
        using |= _collect_using_bones_from_modifier(modifier, armature)

    return using


def _collect_using_bones(armature: Armature) -> set[str]:
    using = set()

    for bone in armature.bones:
        if (
            bone.bbone_handle_type_start != "AUTO"
            and bone.bbone_custom_handle_start is not None
        ):
            using.add(bone.bbone_custom_handle_start.name)

        if (
            bone.bbone_handle_type_end != "AUTO"
            and bone.bbone_custom_handle_end is not None
        ):
            using.add(bone.bbone_custom_handle_end.name)

    for obj in object_itr():
        using |= _collect_using_bones_from_object(obj, armature)

    return using


def armature_show_unused_bones(report: Report = print):
    for armature in armature_itr():
        using = _collect_using_bones(armature)

        for bone in armature.bones:
            if bone.name not in using and len(bone.children) == 0:
                report(
                    {"INFO"},
                    f"Unused bone found. : {armature.name} {bone.name}",
                )
