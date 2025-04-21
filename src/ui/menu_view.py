from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout) # pylint: disable=no-name-in-module

class MenuView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()

        view_decks_btn = QPushButton("Decks")
        create_deck_btn = QPushButton("Create deck")

        view_decks_btn.clicked.connect(self.parent.show_decks_view)
        create_deck_btn.clicked.connect(self.parent.show_create_deck_view)

        layout.addWidget(view_decks_btn)
        layout.addWidget(create_deck_btn)
        layout.addStretch()

        self.setLayout(layout)
