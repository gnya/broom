from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator
from broom.core import (
    armature_rotation_mode,
    armature_rotation_mode_items,
    armature_show_unused_bones,
)
from broom.utils import override

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class VIEW3D_OT_broom_armature_show_unused_bones(Operator):
    bl_idname = "view3d.broom_armature_show_unused_bones"
    bl_label = "Armature Show Unused Bones"
    bl_description = "Armature Show Unused Bones"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        armature_show_unused_bones(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_armature_rotation_mode(Operator):
    bl_idname = "view3d.broom_armature_rotation_mode"
    bl_label = "Armature Rotation Mode"
    bl_description = "Armature Rotation Mode"
    bl_options = {"REGISTER", "UNDO"}

    rotation_mode: EnumProperty(
        name="Rotation Mode", items=armature_rotation_mode_items(), default="XYZ"
    )

    exclude_pattern: StringProperty(name="Exclude Pattern", default="(ORG|MCH|DEF|VIS)")

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        armature_rotation_mode(self.rotation_mode, self.exclude_pattern, self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(self, "rotation_mode")
        layout.prop(self, "exclude_pattern")
