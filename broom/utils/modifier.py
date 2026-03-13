from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bpy.types import NodesModifier


def parse_nodes_modifier_io(
    modifier: NodesModifier,
) -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]]]:
    node_group = modifier.node_group

    if node_group is None:
        return {}, {}

    inputs: dict[int, dict[str, Any]] = {}
    outputs: dict[int, dict[str, Any]] = {}

    for property, value in modifier.items():
        io, num_and_prop = property.split("_", 1)
        num_and_prop = num_and_prop.split("_", 1)
        num = int(num_and_prop[0])
        prop = "" if len(num_and_prop) < 2 else num_and_prop[1]

        if io == "Input":
            if num not in inputs:
                inputs[num] = {}

            if prop == "":
                inputs[num]["default"] = value
            else:
                inputs[num][prop] = value
        elif io == "Output":
            if num not in outputs:
                outputs[num] = {}

            if prop == "":
                outputs[num]["default"] = value
            else:
                outputs[num][prop] = value

    mod_inputs = [i.name.lower() for i in node_group.inputs[1:]]
    mod_outputs = [i.name.lower() for i in node_group.outputs[1:]]

    for mod_input, input in zip(mod_inputs, inputs.values()):
        input["name"] = mod_input

    for mod_output, output in zip(mod_outputs, outputs.values()):
        output["name"] = mod_output

    return inputs, outputs
