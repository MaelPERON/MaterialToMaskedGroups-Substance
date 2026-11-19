# Materials to Masked Groups

**Turn DCC material assignments into Substance 3D Painter groups and geometry masks.**

Materials to Masked Groups (`mat2msk`) converts a JSON material assignment file into a clear, color-coded layer-stack structure. It is designed for solo artists and small workflows that need repeatable material separation, especially when masks should follow mesh names rather than manually-painted selections.

For each material, the plugin creates:

- One `MAT_<material>` group.
- One uniform base-color fill layer inside the group.
- A mesh-name geometry mask on the group.
- Stable or indexed colors for quick visual distinction.

## Installation

Download `material_to_masked_groups.zip` from the [GitHub Releases page](https://github.com/MaelPERON/material_to_masked_groups/releases).

Extract the archive so these folders exist in the Substance 3D Painter Python directory:

```text
<User Documents>\Adobe\Adobe Substance 3D Painter\python\
├── modules\
│   └── mat2msk\
├── plugins\
│   └── mat2msk_launcher.py
└── __init__.py
```

On Windows, the Python directory is usually:

```text
%USERPROFILE%\Documents\Adobe\Adobe Substance 3D Painter\python
```

If the plugin is installed from the repository instead of a release archive, run `test.bat` to copy the source files into that location.

Restart Substance 3D Painter after installation.

1. Open the **Python** menu.
2. Enable `Materials to Masked Groups`.
3. Open a project containing an imported mesh.
4. Confirm that **Mat2Msk** appears in the menu bar.

## Documentation

### JSON Syntax

The JSON file must contain a single object. Each property is a material name, and each value is an array of exact mesh names assigned to that material.

```json
{
  "foldTable_Alluminum": [
    "MSH_back_legs_support_upperside",
    "MSH_back_legs",
    "MSH_front_legs_tube"
  ],
  "foldTable_Pad": [
    "MSH_back_legs_upper_pads",
    "MSH_front_legs_foot_pads"
  ]
}
```

Mesh names are checked against the active texture set:

- Existing mesh names are included in the geometry mask.
- Missing mesh names are skipped and reported in a warning.
- An empty material or a material with no matching meshes still creates its group and fill layer.

The input format can be exported from a DCC or generated with a small script. A `scripts/` folder can be used for DCC-specific exporters, such as Blender scripts that convert material assignments and mesh names into this JSON structure.

### Substance Operator

Open:

```text
Mat2Msk > Import Materials as Groups
```

The import dialog asks for:

1. **JSON file** - Select the material-to-mesh mapping.
2. **Group prefix** - Defaults to `MAT_`.
3. **Hue mode**:
   - **Stable random hues** assigns one reproducible random hue per material name.
   - **Index / material count** assigns hues evenly from `0` to `1`, using `index / material_count`.

The generated groups are inserted at the top of the active texture set stack. If a matching `MAT_<material>` group already exists, Painter asks before replacing it.

Create the package for distribution with `build.bat`. It produces `material_to_masked_groups.zip` containing the `plugins/` and `modules/` folders.

## Authors

- [Mael PERON](https://www.github.com/MaelPERON)
