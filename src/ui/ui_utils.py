from PySide6.QtWidgets import QBoxLayout, QWidget, QMessageBox, QFileDialog # pylint: disable=no-name-in-module

def clear_layout(layout: QBoxLayout):
    """
    Removes all the elements from a QBoxLayout
    Args:
        layout: the QBoxLayout to clear
    """
    while layout.count() > 0:
        item = layout.takeAt(0)
        widget: QWidget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())

def create_alert(message: str):
    """
    Creates a popup alert with a custom message
    Args:
        message: the message to show to the user
    """
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Alert")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()

def get_file_path(filter: str = "All files (*)") -> str:
    """
    Creates a file selection pop up and returns the path to the file
    Args:
        filter: file types to filter for
    """
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(None, "Select a File", "", filter)
    return file_path
