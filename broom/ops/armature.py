from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Operator
from broom.core import armature_show_unused_bones
from broom.utils import override

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context


class VIEW3D_OT_broom_armature_show_unused_bones(Operator):
    bl_idname = "view3d.broom_armature_show_unused_bones"
    bl_label = "Armature Show Unused Bones"
    bl_description = "Armature Show Unused Bones"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        armature_show_unused_bones(self.report)

        return {"FINISHED"}
