# coding: utf-8
# Author: Mael PERON (https://github.com/MaelPERON)
# Source: https://github.com/MaelPERON/substance_materials_to_masked_groups

"""Export the selected meshes and their materials to a JSON file for use in Substance Painter."""

import bpy
import json
import os
from pathlib import Path

filescene = bpy.data.filepath
if not filescene:
    raise ValueError("No .blend file is currently open. "
                     "Please open a .blend file before running this script.")

meshes = set([obj.data for obj
              in bpy.context.selected_objects
              if obj.type == 'MESH'])

materials: dict[str, list[str]] = {}

for mesh in meshes:
    mesh: bpy.types.Mesh
    _materials = set([mat for mat in mesh.materials if mat is not None])
    _material = next(iter(_materials), None)
    if _material is not None:
        obj = materials.get(_material.name)
        if obj is None:
            materials[_material.name] = [mesh.name]
        else:
            obj.append(mesh.name)


output_file = Path(filescene).with_suffix('.json')
with open(output_file, 'w') as f:
    json.dump(materials, f, indent=4)

print(f"Material to mesh mapping saved to {output_file}")
os.startfile(os.path.dirname(output_file))
