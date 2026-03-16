from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bpy.props import BoolProperty
from bpy.types import Operator
from broom.props import BroomSettings, BroomTemp

if TYPE_CHECKING:
    from bpy.types import Context, PropertyGroup


class BroomOperator(Operator):
    broom_domain: str = ""
    broom_name: str = ""
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    bl_idname = ""
    broom_name_full: str = ""
    broom_props: dict[str, str] = {}

    def prop_ptr(self, context: Context, name: str) -> tuple[PropertyGroup, str]:
        settings = BroomSettings.instance(context.scene)
        prop_full = f"{self.broom_name_full}_{name}"

        if settings.view_mode == "SINGLE":
            return BroomTemp.instance(), prop_full
        elif settings.view_mode == "BATCH":
            return settings, prop_full
        else:
            raise ValueError(f"Unknown view mode. : {settings.view_mode}")

    def get_prop(self, context: Context, name: str) -> Any:
        return getattr(*self.prop_ptr(context, name))

    @classmethod
    def register_prop(cls, name: str, property: Any):
        prop_full = f"{cls.broom_name_full}_{name}"
        cls.broom_props[name] = prop_full
        setattr(BroomTemp, prop_full, property)
        setattr(BroomSettings, prop_full, property)


def pre_register(ops: list[type[BroomOperator]]):
    for operator in ops:
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


def post_register(ops: list[type[BroomOperator]]):
    for operator in ops:
        setattr(
            BroomSettings,
            f"{operator.broom_domain}_{operator.broom_name}",
            BoolProperty(
                name=f"Enable {operator.bl_label}",
                description=f"Enable {operator.bl_label}".capitalize(),
                default=False,
            ),
        )
