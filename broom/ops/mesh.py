from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import StringProperty
from bpy.types import Operator
from broom.core import (
    mesh_naming,
    mesh_show_dirty_transforms,
    mesh_show_unused_materials,
    mesh_show_unused_vertex_groups,
)
from broom.utils import override

if TYPE_CHECKING:
    from bpy._typing.rna_enums import OperatorReturnItems
    from bpy.types import Context, Event


class VIEW3D_OT_broom_mesh_naming(Operator):
    bl_idname = "view3d.broom_mesh_naming"
    bl_label = "Mesh Naming"
    bl_description = "Mesh Naming"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_naming(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_mesh_unused_vertex_groups(Operator):
    bl_idname = "view3d.broom_mesh_unused_vertex_groups"
    bl_label = "Mesh Unused Vertex Groups"
    bl_description = "Mesh Unused Vertex Groups"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_show_unused_vertex_groups(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_mesh_show_unused_materials(Operator):
    bl_idname = "view3d.broom_mesh_show_unused_materials"
    bl_label = "Mesh Show Unused Materials"
    bl_description = "Mesh Show Unused Materials"
    bl_options = {"REGISTER", "UNDO"}

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_show_unused_materials(self.report)

        return {"FINISHED"}


class VIEW3D_OT_broom_mesh_show_dirty_transforms(Operator):
    bl_idname = "view3d.broom_mesh_show_dirty_transforms"
    bl_label = "Mesh Show Dirty Transforms"
    bl_description = "Mesh Show Dirty Transforms"
    bl_options = {"REGISTER", "UNDO"}

    exclude_pattern: StringProperty(name="Exclude Pattern", default="(WGT|CUSTOMSHAPE)")

    @override
    def execute(self, context: Context) -> set[OperatorReturnItems]:
        mesh_show_dirty_transforms(self.exclude_pattern, self.report)

        return {"FINISHED"}

    @override
    def invoke(self, context: Context, event: Event) -> set[OperatorReturnItems]:
        return context.window_manager.invoke_props_dialog(self)

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.prop(self, "exclude_pattern")
