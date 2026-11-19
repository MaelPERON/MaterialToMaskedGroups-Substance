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
