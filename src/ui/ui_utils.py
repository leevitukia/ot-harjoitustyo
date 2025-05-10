from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QFileDialog # pylint: disable=no-name-in-module

def clear_layout(layout: QVBoxLayout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        widget: QWidget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())

def create_alert(message: str):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Alert")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()

def get_file_path(filter: str = "All files (*)") -> str:
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(None, "Select a File", "", filter)
    return file_path
