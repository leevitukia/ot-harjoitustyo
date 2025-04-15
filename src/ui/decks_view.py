from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QVBoxLayout)
from .ui_utils import clear_layout

class DecksView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.view_layout = QVBoxLayout()

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(self.parent.show_menu)
        self.view_layout.addWidget(back_btn)

        self.decks_container = QVBoxLayout()
        self.view_layout.addLayout(self.decks_container)

        self.view_layout.addStretch()
        self.setLayout(self.view_layout)

    def refresh_deck_list(self):
        clear_layout(self.decks_container)

        unnamed_deck_counter = 1
        for i, deck in enumerate(self.parent.decks):
            name = deck.name
            if deck.name.strip() == "":
                name = f"Unnamed deck {unnamed_deck_counter}"
                unnamed_deck_counter += 1

            deck_btn = QPushButton(name)
            deck_btn.clicked.connect(lambda _, idx=i: self.parent.show_deck(idx))
            self.decks_container.addWidget(deck_btn)
