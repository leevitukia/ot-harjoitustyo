from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QVBoxLayout, QHBoxLayout,
                              QLabel)
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

            deck_layout = QHBoxLayout()

            deck_label = QLabel(name)
            deck_layout.addWidget(deck_label)

            flip_btn = QPushButton("Flip / multiple choice") #TODOO give stuff smarter names
            flip_btn.clicked.connect(lambda _, idx=i: self.parent.show_deck(idx))
            deck_layout.addWidget(flip_btn)

            exact_answer_btn = QPushButton("Exact answer")
            exact_answer_btn.clicked.connect(lambda _, idx=i: 
                                             self.parent.show_answer_card_view(idx))
            deck_layout.addWidget(exact_answer_btn)

            self.decks_container.addLayout(deck_layout)
