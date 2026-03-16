from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from broom.utils import override

from .base import BroomOperator

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context


class OUTLINER_OT_broom_orphans_purge(BroomOperator):
    broom_domain = "outliner"
    broom_name = "orphans_purge"
    bl_label = "Outliner Orphans Purge"
    bl_description = "Outliner Orphans Purge"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        return bpy.ops.outliner.orphans_purge("INVOKE_DEFAULT", do_recursive=True)
