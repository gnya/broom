from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import bpy

if TYPE_CHECKING:
    from bpy._typing.rna_enums import ObjectModifierTypeItems
    from bpy.types import Modifier


def modifier_itr(type: ObjectModifierTypeItems | None = None) -> Iterator[Modifier]:
    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if type is None or modifier.type == type:
                yield modifier
