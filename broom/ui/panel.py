from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Panel
from broom.ops import (
    ARMATURE_OT_broom_rotation_mode,
    ARMATURE_OT_broom_show_unused_bones,
    BroomOperator,
    CONSTRAINT_OT_broom_naming,
    CONSTRAINT_OT_broom_shrink_panel,
    MESH_OT_broom_naming,
    MESH_OT_broom_show_dirty_transforms,
    MESH_OT_broom_show_unused_materials,
    MESH_OT_broom_show_unused_vertex_groups,
    MODIFIER_OT_broom_naming,
    MODIFIER_OT_broom_shrink_panel,
    MODIFIER_OT_broom_subsurf_uv_smooth,
    NODE_TREE_OT_broom_align_grid,
    NODE_TREE_OT_broom_hide_unused_sockets,
    NODE_TREE_OT_broom_show_users,
    OUTLINER_OT_broom_orphans_purge,
)
from broom.props import BroomSettings
from broom.utils import override

if TYPE_CHECKING:
    from bpy.types import Context, UILayout


def _draw_operator(
    layout: UILayout,
    type: type[BroomOperator],
    settings: BroomSettings,
    name: str = "",
    prop_names: dict[str, str] = {},
):
    if settings.view_mode == "SINGLE":
        layout.operator(type.bl_idname, text=name)
    elif settings.view_mode == "BATCH":
        col = layout.box().column(align=True)
        col.prop(settings, type.broom_name_full, text=name)

        if len(type.broom_props.items()) > 0:
            row = col.row(align=True)
            row.separator(factor=3.0)
            sub_col = row.column(align=True)

            for prop, prop_full in type.broom_props.items():
                if prop in prop_names:
                    prop_name = prop_names[prop]
                else:
                    prop_name = prop.replace("_", " ").title()

                sub_col.prop(settings, prop_full, text=prop_name)


class VIEW3D_PT_broom(Panel):
    bl_idname = "VIEW3D_PT_broom"
    bl_label = "Broom"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Broom"

    @override
    def draw(self, context: Context):
        settings = BroomSettings.instance(context.scene)

        layout = self.layout
        layout.prop(settings, "view_mode", expand=True)

        col = layout.column(align=True)
        col.label(text="Blender File", icon="BLENDER")
        _draw_operator(
            col,
            OUTLINER_OT_broom_orphans_purge,
            settings,
            "Orphans Purge",
        )

        col = layout.column(align=True)
        col.label(text="Modifier", icon="MODIFIER")
        _draw_operator(
            col,
            MODIFIER_OT_broom_naming,
            settings,
            "Naming",
        )
        _draw_operator(
            col,
            MODIFIER_OT_broom_shrink_panel,
            settings,
            "Shrink Panel",
        )
        _draw_operator(
            col,
            MODIFIER_OT_broom_subsurf_uv_smooth,
            settings,
            "Subsurf UV Smooth",
            {"uv_smooth": ""},
        )

        col = layout.column(align=True)
        col.label(text="Constraint", icon="CONSTRAINT")
        _draw_operator(
            col,
            CONSTRAINT_OT_broom_naming,
            settings,
            "Naming",
        )
        _draw_operator(
            col,
            CONSTRAINT_OT_broom_shrink_panel,
            settings,
            "Shrink Panel",
        )

        col = layout.column(align=True)
        col.label(text="Node Tree", icon="NODE")
        _draw_operator(
            col,
            NODE_TREE_OT_broom_show_users,
            settings,
            "Show Users",
            {"node_tree": ""},
        )
        _draw_operator(
            col,
            NODE_TREE_OT_broom_align_grid,
            settings,
            "Align Grid",
        )
        _draw_operator(
            col,
            NODE_TREE_OT_broom_hide_unused_sockets,
            settings,
            "Hide Unused Sockets",
            {"input_only": "Input Only"},
        )

        col = layout.column(align=True)
        col.label(text="Mesh", icon="MESH_DATA")
        _draw_operator(
            col,
            MESH_OT_broom_naming,
            settings,
            "Naming",
        )
        _draw_operator(
            col,
            MESH_OT_broom_show_unused_vertex_groups,
            settings,
            "Unused Vertex Groups",
        )
        _draw_operator(
            col,
            MESH_OT_broom_show_unused_materials,
            settings,
            "Unused Materials",
        )
        _draw_operator(
            col,
            MESH_OT_broom_show_dirty_transforms,
            settings,
            "Dirty Transforms",
            {"exclude_pattern": ""},
        )

        col = layout.column(align=True)
        col.label(text="Armature", icon="ARMATURE_DATA")
        _draw_operator(
            col,
            ARMATURE_OT_broom_show_unused_bones,
            settings,
            "Show Unused Bones",
        )
        _draw_operator(
            col,
            ARMATURE_OT_broom_rotation_mode,
            settings,
            "Rotation Mode",
            {"rotation_mode": "", "exclude_pattern": ""},
        )
