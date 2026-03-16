from .armature import (
    ARMATURE_OT_broom_rotation_mode,
    ARMATURE_OT_broom_show_unused_bones,
)
from .base import BroomOperator
from .constraint import CONSTRAINT_OT_broom_naming, CONSTRAINT_OT_broom_shrink_panel
from .mesh import (
    MESH_OT_broom_naming,
    MESH_OT_broom_show_dirty_transforms,
    MESH_OT_broom_show_unused_materials,
    MESH_OT_broom_show_unused_vertex_groups,
)
from .modifier import (
    MODIFIER_OT_broom_naming,
    MODIFIER_OT_broom_shrink_panel,
    MODIFIER_OT_broom_subsurf_uv_smooth,
)
from .node_tree import (
    NODE_TREE_OT_broom_align_grid,
    NODE_TREE_OT_broom_hide_unused_sockets,
    NODE_TREE_OT_broom_show_users,
)
from .outliner import OUTLINER_OT_broom_orphans_purge

__all__ = [BroomOperator]

classes = (
    MODIFIER_OT_broom_subsurf_uv_smooth,
    MODIFIER_OT_broom_naming,
    MODIFIER_OT_broom_shrink_panel,
    CONSTRAINT_OT_broom_naming,
    CONSTRAINT_OT_broom_shrink_panel,
    NODE_TREE_OT_broom_show_users,
    NODE_TREE_OT_broom_align_grid,
    NODE_TREE_OT_broom_hide_unused_sockets,
    MESH_OT_broom_naming,
    MESH_OT_broom_show_unused_vertex_groups,
    MESH_OT_broom_show_unused_materials,
    ARMATURE_OT_broom_show_unused_bones,
    MESH_OT_broom_show_dirty_transforms,
    ARMATURE_OT_broom_rotation_mode,
    OUTLINER_OT_broom_orphans_purge,
)


def register():
    from bpy.utils import register_class

    from .base import post_register, pre_register

    pre_register(classes)

    for cls in classes:
        register_class(cls)

    post_register(classes)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
