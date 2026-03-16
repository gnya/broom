from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import BoolProperty, PointerProperty
from bpy.types import NodeTree
from broom.core import (
    node_tree_align_grid,
    node_tree_hide_unused_sockets,
    node_tree_show_users,
)
from broom.utils import override

from .base import BroomOperator

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class NODE_TREE_OT_broom_show_users(BroomOperator):
    broom_domain = "node_tree"
    broom_name = "show_users"
    bl_label = "Node Tree Show Users"
    bl_description = "Node Tree Show Users"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        node_tree_show_users(self.get_prop(context, "node_tree"), self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(*self.prop_ptr(context, "node_tree"))

    @classmethod
    def register(cls):
        cls.register_prop(
            "node_tree",
            PointerProperty(
                type=NodeTree,
                name="Node Tree",
            ),
        )


class NODE_TREE_OT_broom_align_grid(BroomOperator):
    broom_domain = "node_tree"
    broom_name = "align_grid"
    bl_label = "Node Tree Align Grid"
    bl_description = "Node Tree Align Grid"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        node_tree_align_grid(self.report)

        return {"FINISHED"}


class NODE_TREE_OT_broom_hide_unused_sockets(BroomOperator):
    broom_domain = "node_tree"
    broom_name = "hide_unused_sockets"
    bl_label = "Node Tree Hide Unused Sockets"
    bl_description = "Node Tree Hide Unused Sockets"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        node_tree_hide_unused_sockets(self.get_prop(context, "input_only"), self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(*self.prop_ptr(context, "input_only"))

    @classmethod
    def register(cls):
        cls.register_prop(
            "input_only",
            BoolProperty(
                name="Input Only",
                default=True,
            ),
        )
