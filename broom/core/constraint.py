from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Callable

from broom.utils import constraint_itr, has_driver

if TYPE_CHECKING:
    from bpy._typing.rna_enums import WmReportItems

    Report = Callable[[set[WmReportItems] | None, str], None]


def constraint_shrink_panel(rigify: bool, report: Report = print):
    for constraint in constraint_itr(rigify=rigify):
        if constraint.show_expanded:
            report(
                {"INFO"},
                f"Shrink constraint panel. {constraint.id_data.name} : {constraint.name}",
            )
            constraint.show_expanded = False


def constraint_naming(rigify: bool, report: Report = print):
    for constraint in constraint_itr(rigify=rigify):
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

        if name != constraint.name:
            report(
                {"INFO"},
                f"Rename constraint. {constraint.id_data.name} : `{constraint.name}` to `{name}`",
            )
            constraint.name = name
