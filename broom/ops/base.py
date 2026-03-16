from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bpy.props import BoolProperty
from bpy.types import Operator
from broom.props import BroomSettings

if TYPE_CHECKING:
    from bpy.types import Context


class BroomOperator(Operator):
    broom_domain: str = ""
    broom_name: str = ""
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    bl_idname = ""
    broom_name_full: str = ""
    broom_props: dict[str, str] = {}

    def prop_ptr(self, context: Context, name: str) -> tuple[BroomSettings, str]:
        return (
            BroomSettings.instance(context.scene),
            f"{self.broom_name_full}_{name}",
        )

    def get_prop(self, context: Context, name: str) -> Any:
        return getattr(*self.prop_ptr(context, name))

    @classmethod
    def register(cls):
        setattr(
            BroomSettings,
            cls.broom_name_full,
            BoolProperty(name=f"Enable {cls.bl_label}", default=False),
        )

    @classmethod
    def register_prop(cls, name: str, property: Any):
        cls.broom_props[name] = f"{cls.broom_name_full}_{name}"
        setattr(BroomSettings, cls.broom_props[name], property)


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
                default=False,
            ),
        )
