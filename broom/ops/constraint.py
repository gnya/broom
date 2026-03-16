from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Operator
from broom.core import constraint_naming, constraint_shrink_panel
from broom.utils import override

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context


class VIEW3D_OT_broom_constraint_naming(Operator):
    bl_idname = "view3d.broom_constraint_naming"
    bl_label = "Constraint Naming"
    bl_description = "Constraint Naming"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        constraint_naming(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_constraint_shrink_panel(Operator):
    bl_idname = "view3d.broom_constraint_shrink_panel"
    bl_label = "Constraint Shrink Panel"
    bl_description = "Constraint Shrink Panel"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        constraint_shrink_panel(self.report)

        return {"FINISHED"}
