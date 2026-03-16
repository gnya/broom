from __future__ import annotations

from typing import Literal

import bpy
from bpy.props import EnumProperty, PointerProperty
from bpy.types import PropertyGroup, Scene, WindowManager
from broom.utils import enum_to_items

BroomViewModeItems = Literal["SINGLE", "BATCH"]


class BroomSettings(PropertyGroup):
    PROP_NAME = "broom_settings"

    view_mode: EnumProperty(
        items=enum_to_items(BroomViewModeItems), name="View Mode", default="SINGLE"
    )

    @staticmethod
    def instance(id: Scene) -> BroomSettings:
        return getattr(id, BroomSettings.PROP_NAME)

    @staticmethod
    def register():
        setattr(Scene, BroomSettings.PROP_NAME, PointerProperty(type=BroomSettings))

    @staticmethod
    def unregister():
        delattr(Scene, BroomSettings.PROP_NAME)


class BroomTemp(PropertyGroup):
    PROP_NAME = "broom_temp"

    @staticmethod
    def instance() -> BroomTemp:
        id = bpy.context.window_manager

        return getattr(id, BroomTemp.PROP_NAME)

    @staticmethod
    def register():
        setattr(WindowManager, BroomTemp.PROP_NAME, PointerProperty(type=BroomTemp))

    @staticmethod
    def unregister():
        delattr(WindowManager, BroomTemp.PROP_NAME)
