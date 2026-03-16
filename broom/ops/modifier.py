from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import EnumProperty
from broom.core import (
    modifier_naming,
    modifier_shrink_panel,
    modifier_subsurf_uv_smooth,
    modifier_subsurf_uv_smooth_items,
)
from broom.utils import override

from .base import BroomOperator

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class MODIFIER_OT_broom_naming(BroomOperator):
    broom_domain = "modifier"
    broom_name = "naming"
    bl_label = "Modifier Naming"
    bl_description = "Modifier Naming"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        modifier_naming(self.report)

        return {"FINISHED"}


class MODIFIER_OT_broom_shrink_panel(BroomOperator):
    broom_domain = "modifier"
    broom_name = "shrink_panel"
    bl_label = "Modifier Shrink Panel"
    bl_description = "Modifier Shrink Panel"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        modifier_shrink_panel(self.report)

        return {"FINISHED"}


class MODIFIER_OT_broom_subsurf_uv_smooth(BroomOperator):
    broom_domain = "modifier"
    broom_name = "subsurf_uv_smooth"
    bl_label = "Modifier Subsurf UV Smooth"
    bl_description = "Modifier Subsurf UV Smooth"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        modifier_subsurf_uv_smooth(self.get_prop(context, "uv_smooth"), self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(*self.prop_ptr(context, "uv_smooth"))

    @classmethod
    def register(cls):
        cls.register_prop(
            "uv_smooth",
            EnumProperty(
                name="UV Smooth",
                items=modifier_subsurf_uv_smooth_items(),
            ),
        )
