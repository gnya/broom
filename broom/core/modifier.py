from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Literal

from broom.utils import (
    enum_to_items,
    modifier_itr,
    object_itr,
    parse_nodes_modifier_io,
    unique_name,
)

if TYPE_CHECKING:
    from bpy._typing.rna_enums import SubdivisionUvSmoothItems, WmReportItems

    Report = Callable[[set[WmReportItems] | None, str], None]
else:
    SubdivisionUvSmoothItems = Literal[
        "NONE",
        "PRESERVE_CORNERS",
        "PRESERVE_CORNERS_AND_JUNCTIONS",
        "PRESERVE_CORNERS_JUNCTIONS_AND_CONCAVE",
        "PRESERVE_BOUNDARIES",
        "SMOOTH_ALL",
    ]


def modifier_shrink_panel(report: Report = print):
    for obj in object_itr():
        for modifier in modifier_itr(obj):
            if modifier.show_expanded:
                report(
                    {"INFO"},
                    f"Shrink modifier panel. : {obj.name} {modifier.name}",
                )
                modifier.show_expanded = False


def modifier_subsurf_uv_smooth_items() -> list[tuple[str, str, str]]:
    return enum_to_items(SubdivisionUvSmoothItems)


def modifier_subsurf_uv_smooth(type: SubdivisionUvSmoothItems, report: Report = print):
    for obj in object_itr():
        for modifier in modifier_itr(obj, "SUBSURF"):
            if modifier.uv_smooth != type:
                report(
                    {"INFO"},
                    f"Change uv_smooth settings. : {obj.name} {modifier.name} ({type})",
                )
                modifier.uv_smooth = type


def modifier_naming(report: Report = print):
    for obj in object_itr():
        names = []

        for modifier in modifier_itr(obj):
            name = modifier.type
            subnames = []

            match name:
                case "SUBSURF":
                    name = "Subdivision"
                case "NODES":
                    name = "Geometry Nodes"
                case _:
                    name = name.replace("_", " ").title()

            if (target := getattr(modifier, "object", None)) is not None:
                subnames.append(target.name)

            if (target := getattr(modifier, "target", None)) is not None:
                subnames.append(target.name)

            if (subtarget := getattr(modifier, "subtarget", "")) != "":
                subnames.append(subtarget)

            if (vertex_group := getattr(modifier, "vertex_group", "")) != "":
                subnames.append(vertex_group)

            if (node_group := getattr(modifier, "node_group", None)) is not None:
                name = node_group.name

                inputs, _ = parse_nodes_modifier_io(modifier)

                for input in inputs.values():
                    if input["name"] in {"object", "target"}:
                        if (subname := getattr(input["default"], "name", "")) != "":
                            subnames.append(subname)

            if subnames:
                name += f" ({', '.join(subnames)})"

            name = unique_name(names, name)

            if name != modifier.name:
                report(
                    {"INFO"},
                    f"Rename modifier. : {obj.name} `{modifier.name}` to `{name}`",
                )
                modifier.name = name

            names.append(name)
