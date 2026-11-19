import hashlib
import json
import random
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


def hue_for_material(
    material_name: str,
    index: int,
    count: int,
    mode: str,
) -> float:
    """Return a stable random hue, or the optional index/count hue.

    Args:
        material_name: The name of the material.
        index: The index of the material in the list.
        count: The total number of materials.
        mode: The hue mode, either "random" or "index".

    Returns:
        A float representing the hue in the range [0.0, 1.0].
    """
    if mode == "index":
        return index / count
    digest = hashlib.sha256(material_name.encode("utf-8")).digest()
    return random.Random(digest).random()
