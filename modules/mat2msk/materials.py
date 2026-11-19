from dataclasses import dataclass

@dataclass(frozen=True)
class MaterialEntry:
    name: str
    mesh_names: tuple[str, ...]
