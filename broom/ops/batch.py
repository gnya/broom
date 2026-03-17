from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Operator
from broom.utils import override

from .base import batch

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context


class VIEW3D_OT_broom_batch(Operator):
    bl_idname = "view3d.broom_batch"
    bl_label = "View3D Batch"
    bl_description = "View3D Batch"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        batch(context.scene, self.report)

        return {"FINISHED"}
