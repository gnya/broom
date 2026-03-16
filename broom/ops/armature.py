from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import EnumProperty, StringProperty
from broom.core import (
    armature_rotation_mode,
    armature_rotation_mode_items,
    armature_show_unused_bones,
)
from broom.utils import override

from .base import BroomOperator

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class ARMATURE_OT_broom_show_unused_bones(BroomOperator):
    broom_domain = "armature"
    broom_name = "show_unused_bones"
    bl_label = "Armature Show Unused Bones"
    bl_description = "Armature Show Unused Bones"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        armature_show_unused_bones(self.report)

        return {"FINISHED"}


class ARMATURE_OT_broom_rotation_mode(BroomOperator):
    broom_domain = "armature"
    broom_name = "rotation_mode"
    bl_label = "Armature Rotation Mode"
    bl_description = "Armature Rotation Mode"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        armature_rotation_mode(
            self.get_prop(context, "rotation_mode"),
            self.get_prop(context, "exclude_pattern"),
            self.report,
        )

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(*self.prop_ptr(context, "rotation_mode"))
        layout.prop(*self.prop_ptr(context, "exclude_pattern"))

    @classmethod
    def register(cls):
        cls.register_prop(
            "rotation_mode",
            EnumProperty(
                name="Rotation Mode",
                items=armature_rotation_mode_items(),
                default="XYZ",
            ),
        )

        cls.register_prop(
            "exclude_pattern",
            StringProperty(
                name="Exclude Pattern",
                default="(ORG|MCH|DEF|VIS)",
            ),
        )
