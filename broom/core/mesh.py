from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

import bmesh
from bpy.utils import flip_name

from broom.utils import object_itr, parse_nodes_modifier_io

if TYPE_CHECKING:
    from bpy._typing.rna_enums import WmReportItems
    from bpy.types import Mesh, Object

    Report = Callable[[set[WmReportItems] | None, str], None]


def mesh_naming(report: Report = print):
    data_users: dict[Mesh, list[Object]] = {}

    for mesh in object_itr("MESH"):
        if (data := mesh.data) is not None:
            if data not in data_users:
                data_users[data] = []

            data_users[data].append(mesh)

    for data, users in data_users.items():
        if len(users) == 1:
            name = users[0].name
        else:
            name_parts = list(zip(*[m.name.split(".") for m in users]))

            if len(name_parts) > 0:
                name_parts = [n[0] for n in name_parts if all(p == n[0] for p in n)]

            if len(name_parts) > 0:
                name = ".".join(name_parts)
            else:
                report({"WARNING"}, f"Can't rename mesh data. : {data.name}")
                name = data.name

        if data.name != name:
            report({"INFO"}, f"Rename mesh data. : `{data.name}` to `{name}`")
            data.name = name


def mesh_show_unused_vertex_groups(report: Report = print):
    for mesh in object_itr("MESH"):
        using = set()
        filled = set()
        use_mirror = False

        for modifier in mesh.modifiers:
            match modifier.type:
                case "ARMATURE":
                    if modifier.object is not None:
                        for bone in modifier.object.data.bones:
                            if bone.use_deform:
                                using.add(bone.name)
                case "CLOTH":
                    for prop in {
                        "vertex_group_bending",
                        "vertex_group_intern",
                        "vertex_group_mass",
                        "vertex_group_pressure",
                        "vertex_group_shear_stiffness",
                        "vertex_group_shrink",
                        "vertex_group_structural_stiffness",
                    }:
                        if (vertex_group := getattr(modifier.settings, prop, "")) != "":
                            using.add(vertex_group)
                case "FLUID":
                    if (
                        vertex_group := modifier.flow_settings.density_vertex_group
                    ) != "":
                        using.add(vertex_group)
                case "SOFT_BODY":
                    for prop in {
                        "vertex_group_goal",
                        "vertex_group_mass",
                        "vertex_group_spring",
                    }:
                        if (vertex_group := getattr(modifier.settings, prop, "")) != "":
                            using.add(vertex_group)
                case "NODES":
                    inputs, outputs = parse_nodes_modifier_io(modifier)

                    for input in inputs.values():
                        if (
                            input.get("use_attribute", False)
                            and input.get("attribute_name", "") != ""
                        ):
                            using.add(input["attribute_name"])

                    for output in outputs.values():
                        if (
                            output.get("use_attribute", False)
                            and output.get("attribute_name", "") != ""
                        ):
                            using.add(output["attribute_name"])
                case "MIRROR":
                    if modifier.use_mirror_vertex_groups:
                        use_mirror = True
                case _:
                    pass

            if (vertex_group := getattr(modifier, "vertex_group", "")) != "":
                using.add(vertex_group)

        if mesh.data is not None:
            filled_index = set()

            for vertex in mesh.data.vertices:
                for vertex_group in vertex.groups:
                    if vertex_group.weight > 0.0:
                        filled_index.add(vertex_group.group)

            for index in filled_index:
                filled.add(mesh.vertex_groups[index].name)

        for vertex_group in mesh.vertex_groups:
            if vertex_group.name not in using:
                report(
                    {"INFO"},
                    f"Unused vertex group found. : {mesh.name} {vertex_group.name}",
                )

            if vertex_group.name not in filled and (
                not use_mirror or flip_name(vertex_group.name) not in filled
            ):
                report(
                    {"INFO"},
                    f"Empty vertex group found. : {mesh.name} {vertex_group.name}",
                )


def mesh_show_unused_materials(report: Report = print):
    for mesh in object_itr("MESH"):
        if mesh.data is not None:
            using = set()

            for polygon in mesh.data.polygons:
                using.add(polygon.material_index)

            unused = set(range(len(mesh.material_slots))) - using

            for index in unused:
                material = mesh.material_slots[index].material

                if material is None:
                    report(
                        {"INFO"},
                        f"Empty material slot found. : {mesh.name} slot:{index}",
                    )
                else:
                    report(
                        {"INFO"},
                        f"Unused material slot found. : {mesh.name} {material.name}",
                    )


def mesh_show_dirty_transforms(exclude_pattern: str, report: Report = print):
    for mesh in object_itr("MESH"):
        if not mesh.matrix_basis.is_identity and (
            exclude_pattern == "" or not re.search(exclude_pattern, mesh.name)
        ):
            report(
                {"INFO"},
                f"Dirty transform mesh found. : {mesh.name}",
            )


def mesh_unselect_vertices(report: Report = print):
    for mesh in object_itr("MESH"):
        if mesh.data is not None:
            is_edit_mode = mesh.mode == "EDIT"

            if is_edit_mode:
                bm = bmesh.from_edit_mesh(mesh.data)
                verts = bm.verts
                edges = bm.edges
                faces = bm.faces
            else:
                verts = mesh.data.vertices
                edges = mesh.data.edges
                faces = mesh.data.polygons

            for vert in verts:
                vert.select = False

            for edge in edges:
                edge.select = False

            for face in faces:
                face.select = False

            if is_edit_mode:
                bmesh.update_edit_mesh(mesh.data)
