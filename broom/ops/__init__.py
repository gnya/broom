from .constraint import (
    VIEW3D_OT_broom_constraint_naming,
    VIEW3D_OT_broom_constraint_shrink_panel,
)
from .mesh import (
    VIEW3D_OT_broom_mesh_naming,
    VIEW3D_OT_broom_mesh_show_unused_materials,
    VIEW3D_OT_broom_mesh_unused_vertex_groups,
)
from .modifier import (
    VIEW3D_OT_broom_modifier_naming,
    VIEW3D_OT_broom_modifier_shrink_panel,
    VIEW3D_OT_broom_modifier_subsurf_uv_smooth,
)
from .node_tree import (
    VIEW3D_OT_broom_node_tree_align_grid,
    VIEW3D_OT_broom_node_tree_hide_unused_sockets,
    VIEW3D_OT_broom_node_tree_show_users,
)

classes = (
    VIEW3D_OT_broom_modifier_subsurf_uv_smooth,
    VIEW3D_OT_broom_modifier_naming,
    VIEW3D_OT_broom_modifier_shrink_panel,
    VIEW3D_OT_broom_constraint_naming,
    VIEW3D_OT_broom_constraint_shrink_panel,
    VIEW3D_OT_broom_node_tree_show_users,
    VIEW3D_OT_broom_node_tree_align_grid,
    VIEW3D_OT_broom_node_tree_hide_unused_sockets,
    VIEW3D_OT_broom_mesh_naming,
    VIEW3D_OT_broom_mesh_unused_vertex_groups,
    VIEW3D_OT_broom_mesh_show_unused_materials,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
