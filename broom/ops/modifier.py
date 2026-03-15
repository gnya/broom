from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import EnumProperty
from bpy.types import Operator
from broom.core import (
    modifier_naming,
    modifier_shrink_panel,
    modifier_subsurf_uv_smooth,
    modifier_subsurf_uv_smooth_items,
)
from broom.utils import override

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class VIEW3D_OT_broom_modifier_naming(Operator):
    bl_idname = "view3d.broom_modifier_naming"
    bl_label = "Modifier Naming"
    bl_description = "Modifier Naming"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        modifier_naming(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_modifier_shrink_panel(Operator):
    bl_idname = "view3d.broom_modifier_shrink_panel"
    bl_label = "Modifier Shrink Panel"
    bl_description = "Modifier Shrink Panel"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        modifier_shrink_panel(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_modifier_subsurf_uv_smooth(Operator):
    bl_idname = "view3d.broom_modifier_subsurf_uv_smooth"
    bl_label = "Modifier Subsurf UV Smooth"
    bl_description = "Modifier Subsurf UV Smooth"
    bl_options = {"REGISTER", "UNDO"}

    uv_smooth: EnumProperty(name="UV Smooth", items=modifier_subsurf_uv_smooth_items())

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        modifier_subsurf_uv_smooth(self.uv_smooth, self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(self, "uv_smooth")
