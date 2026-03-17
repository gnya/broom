from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from broom.props import BroomSettings, BroomTemp

if TYPE_CHECKING:
    from bpy._typing.rna_enums import WmReportItems
    from bpy.types import Context, PropertyGroup, Scene

    Report = Callable[[set[WmReportItems] | None, str], None]


class BroomOperator(Operator):
    broom_domain: str = ""
    broom_name: str = ""
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    bl_idname = ""
    broom_name_full: str = ""
    broom_props: dict[str, str] = {}

    def prop_ptr(self, context: Context, prop: str) -> tuple[PropertyGroup, str]:
        settings = BroomSettings.instance(context.scene)
        prop_full = f"{self.broom_name_full}_{prop}"

        if settings.show_settings:
            return settings, prop_full
        else:
            return BroomTemp.instance(), prop_full

    def get_prop(self, context: Context, name: str) -> Any:
        return getattr(*self.prop_ptr(context, name))

    @classmethod
    def register_prop(cls, name: str, value: Any):
        prop_full = f"{cls.broom_name_full}_{name}"
        cls.broom_props[name] = prop_full
        setattr(BroomTemp, prop_full, value)
        setattr(BroomSettings, prop_full, value)


def batch(scene: Scene, report: Report = print):
    settings = BroomSettings.instance(scene)

    for cls in BroomOperator.__subclasses__():
        if getattr(settings, cls.broom_name_full, False):
            idname = cls.bl_idname.split(".")
            operator = getattr(getattr(bpy.ops, idname[0], None), idname[1], None)

            if operator is not None:
                report({"INFO"}, f"Run operator. : {cls.bl_label}")
                operator()


def pre_register():
    for operator in BroomOperator.__subclasses__():
        if operator.bl_idname == "":
            setattr(
                operator,
                "bl_idname",
                f"{operator.broom_domain}.broom_{operator.broom_name}",
            )

        if operator.broom_name_full == "":
            setattr(
                operator,
                "broom_name_full",
                f"{operator.broom_domain}_{operator.broom_name}",
            )

        setattr(operator, "broom_props", {})


def post_register():
    for operator in BroomOperator.__subclasses__():
        setattr(
            BroomSettings,
            operator.broom_name_full,
            BoolProperty(
                name=f"Enable {operator.bl_label}",
                description=f"Enable {operator.bl_label}".capitalize(),
                default=False,
            ),
        )
