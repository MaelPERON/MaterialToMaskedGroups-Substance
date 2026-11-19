try:
    from PySide6 import QtGui, QtWidgets
except ImportError:
    from PySide2 import QtGui, QtWidgets

import substance_painter as sp
import substance_painter.colormanagement
import substance_painter.layerstack
import substance_painter.project
import substance_painter.textureset
import substance_painter.ui

PLUGIN_NAME = "Materials to Masked Groups"
_plugin_widgets: list[QtWidgets.QWidget] = []

_MODULES = Path(__file__).resolve().parents[1] / "modules"
if str(_MODULES) not in sys.path:
    sys.path.insert(0, str(_MODULES))


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

def start_plugin() -> None:
    menu = QtWidgets.QMenu("Mat2Msk")
    action = QtGui.QAction(
        "Import Materials as Groups", triggered=None
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
