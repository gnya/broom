from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import StringProperty
from broom.core import (
    mesh_naming,
    mesh_show_dirty_transforms,
    mesh_show_unused_materials,
    mesh_show_unused_vertex_groups,
)
from broom.utils import override

from .base import BroomOperator

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class MESH_OT_broom_naming(BroomOperator):
    broom_domain = "mesh"
    broom_name = "naming"
    bl_label = "Mesh Naming"
    bl_description = "Mesh Naming"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_naming(self.report)

        return {"FINISHED"}


class MESH_OT_broom_show_unused_vertex_groups(BroomOperator):
    broom_domain = "mesh"
    broom_name = "show_unused_vertex_groups"
    bl_label = "Mesh Show Unused Vertex Groups"
    bl_description = "Mesh Show Unused Vertex Groups"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_show_unused_vertex_groups(self.report)

        return {"FINISHED"}


class MESH_OT_broom_show_unused_materials(BroomOperator):
    broom_domain = "mesh"
    broom_name = "show_unused_materials"
    bl_label = "Mesh Show Unused Materials"
    bl_description = "Mesh Show Unused Materials"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_show_unused_materials(self.report)

        return {"FINISHED"}


class MESH_OT_broom_show_dirty_transforms(BroomOperator):
    broom_domain = "mesh"
    broom_name = "show_dirty_transforms"
    bl_label = "Mesh Show Dirty Transforms"
    bl_description = "Mesh Show Dirty Transforms"

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_show_dirty_transforms(
            self.get_prop(context, "exclude_pattern"), self.report
        )

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(*self.prop_ptr(context, "exclude_pattern"))

    @classmethod
    def register(cls):
        cls.register_prop(
            "exclude_pattern",
            StringProperty(
                name="Exclude Pattern",
                default="(WGT|CUSTOMSHAPE)",
            ),
        )
