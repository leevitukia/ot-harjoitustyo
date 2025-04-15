from PySide6.QtWidgets import QVBoxLayout, QWidget # pylint: disable=no-name-in-module

def clear_layout(layout: QVBoxLayout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        widget: QWidget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())
