from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator
from broom.core import (
    node_tree_align_grid,
    node_tree_hide_unused_sockets,
    node_tree_show_users,
)
from broom.utils import override

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class VIEW3D_OT_broom_node_tree_show_users(Operator):
    bl_idname = "view3d.broom_node_tree_show_users"
    bl_label = "Node Tree Show Users"
    bl_description = "Node Tree Show Users"
    bl_options = {"REGISTER", "UNDO"}

    node_tree_name: StringProperty(name="Node Tree Name")

    # TODO リンクされたNodeTreeに対応する
    node_tree_library: StringProperty(name="Node Tree Library")

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        if self.node_tree_library == "":
            node_tree = bpy.data.node_groups.get(self.node_tree_name, None)
        else:
            node_tree = bpy.data.node_groups.get(
                (self.node_tree_name, self.node_tree_library)
            )

        node_tree_show_users(node_tree, self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop_search(self, "node_tree_name", bpy.data, "node_groups")


class VIEW3D_OT_broom_node_tree_align_grid(Operator):
    bl_idname = "view3d.broom_node_tree_align_grid"
    bl_label = "Node Tree Align Grid"
    bl_description = "Node Tree Align Grid"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        node_tree_align_grid(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_node_tree_hide_unused_sockets(Operator):
    bl_idname = "view3d.broom_node_tree_hide_unused_sockets"
    bl_label = "Node Tree Hide Unused Sockets"
    bl_description = "Node Tree Hide Unused Sockets"
    bl_options = {"REGISTER", "UNDO"}

    input_only: BoolProperty(name="Input Only", default=True)

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        node_tree_hide_unused_sockets(self.input_only, self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(self, "input_only")
