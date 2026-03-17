from __future__ import annotations

import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import PropertyGroup, Scene, WindowManager


class BroomSettings(PropertyGroup):
    PROP_NAME = "broom_settings"

    show_settings: BoolProperty(name="Show Settings", default=False)

    batch_on_save: BoolProperty(name="Batch On Save", default=False)

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
