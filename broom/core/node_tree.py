from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from broom.utils import (
    id_node_tree_user_itr,
    node_abs_location,
    node_connection_itr,
    node_itr,
)
from mathutils import Vector

if TYPE_CHECKING:
    from bpy._typing.rna_enums import WmReportItems
    from bpy.types import ID, Node, NodeTree

    Report = Callable[[set[WmReportItems] | None, str], None]


def node_tree_show_users(node_tree: NodeTree, report: Report = print):
    count = 0

    if node_tree is not None:
        for data in id_node_tree_user_itr():
            for node in node_itr(data, node_tree):
                report({"INFO"}, f"Node Tree user found. : {data.name} {node.name}")
                count += 1

    if count == 0:
        report({"INFO"}, "Node Tree user not found.")


def _nodes_align_grid_xy(nodes: list[Node], data: ID, report: Report = print):
    for node in nodes:
        grid_xy = node_abs_location(node) / 20.0
        error_x = grid_xy.x - round(grid_xy.x)
        error_y = grid_xy.y - round(grid_xy.y)

        if error_x != 0.0 or error_y != 0.0:
            report({"INFO"}, f"Align node location. : {data.name} {node.name}")
            node.location.x -= error_x * 20.0
            node.location.y -= error_y * 20.0


def _nodes_align_grid_w(nodes: list[Node], data: ID, report: Report = print):
    for node in nodes:
        grid_w = node.width / 20.0
        error_w = grid_w - round(grid_w)

        if error_w != 0.0 and node.bl_idname not in {"NodeReroute"}:
            report({"INFO"}, f"Align node width. : {data.name} {node.name}")
            node.width -= error_w * 20.0


def _nodes_align_grid(
    nodes: list[Node], node: Node | None, data: ID, report: Report = print
):
    if len(nodes) == 0:
        return
    elif node is None:
        node = nodes[0]

    node_is_reroute = node.bl_idname == "NodeReroute"
    node_grid_x = node_abs_location(node).x / 20.0
    node_grid_w = 0.0 if node_is_reroute else node.width / 20.0

    nodes.remove(node)

    for next in node_connection_itr(node):
        next_is_reroute = next.bl_idname == "NodeReroute"

        if next in nodes and not (node_is_reroute and next_is_reroute):
            next_grid_x = node_abs_location(next).x / 20.0
            next_grid_w = 0.0 if next_is_reroute else next.width / 20.0
            offset = 2.0 if node.parent == next.parent else 4.0

            if node_grid_x > next_grid_x:
                next_error_x = (next_grid_x + next_grid_w + offset) - node_grid_x
            else:
                next_error_x = next_grid_x - (node_grid_x + node_grid_w + offset)

            if next_error_x != 0.0:
                report({"INFO"}, f"Align node location. : {data.name} {node.name}")
                next.location.x -= next_error_x * 20.0

            _nodes_align_grid(nodes, next, data, report)


def _nodes_corner(nodes: list[Node]) -> Vector:
    corner = Vector((-float("inf"), -float("inf")))

    for node in nodes:
        location = node_abs_location(node)

        if getattr(node, "is_active_output", False):
            return location

        if node.bl_idname != "NodeFrame":
            if location.x > corner.x:
                corner.x = location.x

            if location.y > corner.y:
                corner.y = location.y

    return corner


def _nodes_align_corner(nodes: list[Node], data: ID, report: Report = print):
    default_corner = Vector((300.0, 300.0))
    corner = _nodes_corner(nodes)

    if corner != default_corner:
        offset = default_corner - corner

        for node in node_itr(data):
            if not node.parent:
                node.location += offset

        report({"INFO"}, f"Align nodes corner. : {data.name}")


def node_tree_align_grid(report: Report = print):
    for data in id_node_tree_user_itr():
        nodes = [n for n in node_itr(data) if n.bl_idname not in {"NodeFrame"}]

        _nodes_align_grid_xy(nodes, data, report)
        _nodes_align_grid_w(nodes, data, report)

        nodes_copy = nodes.copy()

        while len(nodes_copy) > 0:
            _nodes_align_grid(nodes_copy, None, data, report)

        _nodes_align_corner(nodes, data, report)


def node_tree_hide_unused_sockets(input_only: bool, report: Report = print):
    for data in id_node_tree_user_itr():
        for node in node_itr(data):
            for input in node.inputs:
                if (
                    len(input.links) == 0
                    and input.enabled
                    and not input.hide
                    and (input.hide_value or input.type in {"SHADER", "GEOMETRY"})
                ):
                    report(
                        {"INFO"},
                        f"Hide unused input. : {data.name} {node.name} {input.name}",
                    )
                    input.hide = True

            for output in node.outputs:
                if (
                    len(output.links) == 0
                    and output.enabled
                    and not output.hide
                    and not input_only
                ):
                    report(
                        {"INFO"},
                        f"Hide unused output. : {data.name} {node.name} {output.name}",
                    )
                    output.hide = True

        data.update_tag()
