from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Panel
from broom.ops import (
    VIEW3D_OT_broom_constraint_naming,
    VIEW3D_OT_broom_constraint_shrink_panel,
    VIEW3D_OT_broom_modifier_naming,
    VIEW3D_OT_broom_modifier_shrink_panel,
    VIEW3D_OT_broom_modifier_subsurf_uv_smooth,
    VIEW3D_OT_broom_node_tree_align_grid,
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

        layout.operator(
            VIEW3D_OT_broom_modifier_naming.bl_idname,
            text="Modifier Naming",
        )
        layout.operator(
            VIEW3D_OT_broom_modifier_shrink_panel.bl_idname,
            text="Modifier Shrink Panel",
        )
        layout.operator_menu_enum(
            VIEW3D_OT_broom_modifier_subsurf_uv_smooth.bl_idname,
            "uv_smooth",
            text="Modifier Subsurf UV Smooth",
        )

        layout.separator()

        layout.operator(
            VIEW3D_OT_broom_constraint_naming.bl_idname,
            text="Constraint Naming",
        )
        layout.operator(
            VIEW3D_OT_broom_constraint_shrink_panel.bl_idname,
            text="Constraint Shrink Panel",
        )

        layout.separator()

        layout.operator(
            VIEW3D_OT_broom_node_tree_show_users.bl_idname,
            text="NodeTree Show Users",
        )
        layout.operator(
            VIEW3D_OT_broom_node_tree_align_grid.bl_idname,
            text="NodeTree Align Grid",
        )
