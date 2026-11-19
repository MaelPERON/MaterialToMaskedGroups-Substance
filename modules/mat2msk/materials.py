import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MaterialEntry:
    name: str
    mesh_names: tuple[str, ...]


def load_materials(path: str | Path) -> list[MaterialEntry]:
    """Load and validate the supported material-to-mesh JSON format.

    Args:
        path: The path to the JSON file.

    Returns:
        A list of MaterialEntry objects.
    """
    try:
        with Path(path).open("r", encoding="utf-8") as source:
            data: Any = json.load(source)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read JSON file: {error}") from error

    if not isinstance(data, dict) or not data:
        raise ValueError("The JSON root must be a non-empty object.")

    entries: list[MaterialEntry] = []
    for material_name, mesh_names in data.items():
        if not isinstance(material_name, str) or not material_name.strip():
            raise ValueError("Material names must be non-empty strings.")
        if not isinstance(mesh_names, list) or not all(
            isinstance(mesh_name, str) and mesh_name.strip()
            for mesh_name in mesh_names
        ):
            raise ValueError(
                f"Material '{material_name}' must contain a list of mesh names."
            )
        entries.append(
            MaterialEntry(
                material_name,
                tuple(dict.fromkeys(mesh_names)),
            )
        )
    return entries
