from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Callable

from broom.utils import (
    constraint_itr,
    has_driver,
    object_itr,
    pose_bone_itr,
    unique_name,
)

if TYPE_CHECKING:
    from bpy._typing.rna_enums import WmReportItems
    from bpy.types import Object, PoseBone

    Report = Callable[[set[WmReportItems] | None, str], None]


def _shrink_panel(source: Object | PoseBone, report: Report = print):
    for constraint in constraint_itr(source):
        if constraint.show_expanded:
            report(
                {"INFO"},
                f"Shrink constraint panel. : {source.name} {constraint.name}",
            )
            constraint.show_expanded = False


def constraint_shrink_panel(report: Report = print):
    for obj in object_itr():
        _shrink_panel(obj, report)

        for bone in pose_bone_itr(obj):
            _shrink_panel(bone)


def _naming(source: Object | PoseBone, report: Report = print):
    names = []

    for constraint in constraint_itr(source):
        name = constraint.type
        subnames = []

        match name:
            case "IK":
                name = "IK"
            case "TRANSFORM":
                name = "Transformation"
            case _:
                name = name.replace("_", " ").title()

        if match := re.match(r".*(\s\(|,\s)(X|Y|Z|FK|IK),?.*\)", constraint.name):
            subnames.append(match.group(2))

        if (
            target := getattr(constraint, "target", None)
        ) is not None and target != constraint.id_data:
            subnames.append(target.name)

        if (subtarget := getattr(constraint, "subtarget", "")) != "":
            subnames.append(subtarget)

        if (
            influence := getattr(constraint, "influence", 1.0)
        ) < 1.0 and not has_driver(constraint, "influence"):
            digit = math.floor(math.log10(influence)) if influence > 0.0 else 0

            subnames.append(f"{influence:.{-digit}f}")

        if subnames:
            name += f" ({', '.join(subnames)})"

        name = unique_name(names, name)

        if name != constraint.name:
            report(
                {"INFO"},
                f"Rename constraint. : {source.name} `{constraint.name}` to `{name}`",
            )
            constraint.name = name

        names.append(name)


def constraint_naming(report: Report = print):
    for obj in object_itr():
        _naming(obj, report)

        for bone in pose_bone_itr(obj):
            _naming(bone)
