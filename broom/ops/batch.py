from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.app.handlers import persistent, save_pre
from bpy.types import Operator

from broom.props import BroomSettings
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

    @staticmethod
    @persistent
    def _batch_on_save(dummy: str):
        if BroomSettings.instance(bpy.context.scene).batch_on_save:
            batch(bpy.context.scene, print)

    @staticmethod
    def register():
        if VIEW3D_OT_broom_batch._batch_on_save not in save_pre:
            save_pre.append(VIEW3D_OT_broom_batch._batch_on_save)

    @staticmethod
    def unregister():
        if VIEW3D_OT_broom_batch._batch_on_save in save_pre:
            save_pre.remove(VIEW3D_OT_broom_batch._batch_on_save)
