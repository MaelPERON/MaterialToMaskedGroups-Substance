import colorsys
import sys
from pathlib import Path

try:
    from PySide6 import QtGui, QtWidgets  # type: ignore
except ImportError:
    from PySide2 import QtGui, QtWidgets  # type: ignore

import substance_painter as sp
import substance_painter.colormanagement
import substance_painter.layerstack
import substance_painter.project
import substance_painter.textureset
import substance_painter.ui

PLUGIN_NAME = "Materials to Masked Groups"
DEFAULT_PREFIX = "MAT_"
_plugin_widgets: list[QtWidgets.QWidget] = []

_MODULES = Path(__file__).resolve().parents[1] / "modules"
if str(_MODULES) not in sys.path:
    sys.path.insert(0, str(_MODULES))

from mat2msk.materials import MaterialEntry, hue_for_material, load_materials  # noqa: E402, E501


def _show_message(
    title: str, message: str, icon: QtWidgets.QMessageBox.Icon
) -> None:
    QtWidgets.QMessageBox(icon, title, message).exec_()


def _choose_import_options() -> tuple[str, str, str] | None:
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
        None, "Import Materials JSON", "", "JSON files (*.json)"
    )
    if not file_path:
        return None

    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Import Materials as Groups")
    form = QtWidgets.QFormLayout(dialog)
    prefix = QtWidgets.QLineEdit(DEFAULT_PREFIX)
    mode = QtWidgets.QComboBox()
    mode.addItem("Stable random hues", "random")
    mode.addItem("Index / material count", "index")
    form.addRow("Group prefix:", prefix)
    form.addRow("Hue mode:", mode)
    buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    form.addRow(buttons)
    if dialog.exec_() != QtWidgets.QDialog.Accepted:
        return None
    if not prefix.text().strip():
        _show_message(
            "Invalid prefix",
            "The group prefix cannot be empty.",
            QtWidgets.QMessageBox.Warning,
        )
        return None
    return file_path, prefix.text(), mode.currentData()


def _existing_groups(stack: object, names: set[str]) -> list[object]:
    return [
        node
        for node in sp.layerstack.get_root_layer_nodes(stack)
        if node.get_name() in names
    ]


def _make_group(
    stack: object,
    entry: MaterialEntry,
    hue: float,
    prefix: str,
    available_meshes: set[str],
) -> object:
    position = sp.layerstack.InsertPosition.from_textureset_stack(stack)
    group = sp.layerstack.insert_group(position)
    group.set_name(f"{prefix}{entry.name}")

    selected_meshes = [
        name for name in entry.mesh_names if name in available_meshes
    ]
    group.set_geometry_mask(
        sp.layerstack.GeometryMaskMeshParams(
            inclusion_list=True,
            meshes=selected_meshes,
        )
    )

    fill = sp.layerstack.insert_fill(
        sp.layerstack.InsertPosition.inside_node(
            group, sp.layerstack.NodeStack.Substack
        )
    )
    fill.set_name(entry.name)
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.8, 0.8)
    fill.set_source(
        sp.layerstack.ChannelType.BaseColor,
        sp.colormanagement.Color(red, green, blue),
    )
    return group


def import_materials() -> None:
    """Prompt for JSON and create the requested groups in the active stack."""
    if not sp.project.is_open():
        _show_message(
            "Materials to Masked Groups",
            "Open a project first.",
            QtWidgets.QMessageBox.Warning,
        )
        return

    options = _choose_import_options()
    if options is None:
        return
    file_path, prefix, hue_mode = options

    try:
        entries = load_materials(file_path)
        stack = sp.textureset.get_active_stack()
        available_meshes = set(stack.material().all_mesh_names())
        group_names = {f"{prefix}{entry.name}" for entry in entries}
        existing = _existing_groups(stack, group_names)
        if existing:
            answer = QtWidgets.QMessageBox.question(
                None,
                "Replace existing groups?",
                "Matching groups already exist. Replace them?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            if answer != QtWidgets.QMessageBox.Yes:
                return
    except (ValueError, RuntimeError, AttributeError) as error:
        _show_message("Import failed", str(error),
                      QtWidgets.QMessageBox.Critical)
        return

    for node in existing:
        sp.layerstack.delete_node(node)

    warnings: list[str] = []
    count = len(entries)
    for index, entry in enumerate(entries):
        missing = [name for name in entry.mesh_names
                   if name not in available_meshes]
        if missing:
            warnings.append(f"{entry.name}: missing {', '.join(missing)}")
        try:
            _make_group(
                stack,
                entry,
                hue_for_material(entry.name, index, count, hue_mode),
                prefix,
                available_meshes,
            )
        except (RuntimeError, ValueError, AttributeError) as error:
            _show_message("Import failed", str(error),
                          QtWidgets.QMessageBox.Critical)
            return

    if warnings:
        _show_message(
            "Import completed with warnings",
            "Some mesh names were not found:\n\n" + "\n".join(warnings),
            QtWidgets.QMessageBox.Warning,
        )


def start_plugin() -> None:
    menu = QtWidgets.QMenu("Mat2Msk")
    action = QtGui.QAction(
        "Import Materials as Groups", triggered=import_materials
    )
    menu.addAction(action)
    sp.ui.add_menu(menu)
    _plugin_widgets.extend((menu, action))


def close_plugin() -> None:
    for widget in _plugin_widgets:
        sp.ui.delete_ui_element(widget)
    _plugin_widgets.clear()


if __name__ == "__main__":
    start_plugin()
