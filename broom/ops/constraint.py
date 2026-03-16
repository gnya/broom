from __future__ import annotations

from typing import TYPE_CHECKING

from broom.core import constraint_naming, constraint_shrink_panel
from broom.utils import override

from .base import BroomOperator

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context


class CONSTRAINT_OT_broom_naming(BroomOperator):
    broom_domain = "constraint"
    broom_name = "naming"
    bl_label = "Constraint Naming"
    bl_description = "Constraint Naming"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        constraint_naming(self.report)

        return {"FINISHED"}


class CONSTRAINT_OT_broom_shrink_panel(BroomOperator):
    broom_domain = "constraint"
    broom_name = "shrink_panel"
    bl_label = "Constraint Shrink Panel"
    bl_description = "Constraint Shrink Panel"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        constraint_shrink_panel(self.report)

        return {"FINISHED"}
