from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Panel
from broom.ops import (
    VIEW3D_OT_broom_armature_show_unused_bones,
    VIEW3D_OT_broom_constraint_naming,
    VIEW3D_OT_broom_constraint_shrink_panel,
    VIEW3D_OT_broom_mesh_naming,
    VIEW3D_OT_broom_mesh_show_unused_materials,
    VIEW3D_OT_broom_mesh_unused_vertex_groups,
    VIEW3D_OT_broom_modifier_naming,
    VIEW3D_OT_broom_modifier_shrink_panel,
    VIEW3D_OT_broom_modifier_subsurf_uv_smooth,
    VIEW3D_OT_broom_node_tree_align_grid,
    VIEW3D_OT_broom_node_tree_hide_unused_sockets,
    VIEW3D_OT_broom_node_tree_show_users,
)
from broom.utils import override

if TYPE_CHECKING:
    from bpy.types import Context


class VIEW3D_PT_broom(Panel):
    bl_idname = "VIEW3D_PT_broom"
    bl_label = "Broom"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Broom"

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.label(text="Modifier", icon="MODIFIER")
        layout.operator(
            VIEW3D_OT_broom_modifier_naming.bl_idname,
            text="Naming",
        )
        layout.operator(
            VIEW3D_OT_broom_modifier_shrink_panel.bl_idname,
            text="Shrink Panel",
        )
        layout.operator(
            VIEW3D_OT_broom_modifier_subsurf_uv_smooth.bl_idname,
            text="Subsurf UV Smooth",
        )

        layout.separator()

        layout.label(text="Constraint", icon="CONSTRAINT")
        layout.operator(
            VIEW3D_OT_broom_constraint_naming.bl_idname,
            text="Naming",
        )
        layout.operator(
            VIEW3D_OT_broom_constraint_shrink_panel.bl_idname,
            text="Shrink Panel",
        )

        layout.separator()

        layout.label(text="NodeTree", icon="NODE")
        layout.operator(
            VIEW3D_OT_broom_node_tree_show_users.bl_idname,
            text="Show Users",
        )
        layout.operator(
            VIEW3D_OT_broom_node_tree_align_grid.bl_idname,
            text="Align Grid",
        )
        layout.operator(
            VIEW3D_OT_broom_node_tree_hide_unused_sockets.bl_idname,
            text="Hide Unused Sockets",
        )

        layout.separator()

        layout.label(text="Mesh", icon="MESH_DATA")
        layout.operator(
            VIEW3D_OT_broom_mesh_naming.bl_idname,
            text="Naming",
        )
        layout.operator(
            VIEW3D_OT_broom_mesh_unused_vertex_groups.bl_idname,
            text="Unused Vertex Groups",
        )
        layout.operator(
            VIEW3D_OT_broom_mesh_show_unused_materials.bl_idname,
            text="Unused Materials",
        )

        layout.separator()

        layout.label(text="Armature", icon="ARMATURE_DATA")
        layout.operator(
            VIEW3D_OT_broom_armature_show_unused_bones.bl_idname,
            text="Show Unused Bones",
        )
