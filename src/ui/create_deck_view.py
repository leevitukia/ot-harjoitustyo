from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel, QVBoxLayout,
                              QHBoxLayout, QLineEdit)
from entities.deck import Deck

class CreateDeckView(QWidget):
    def __init__(self, parent): # TODO_: split to multiple functions
        super().__init__()
        self.parent = parent
        self.deck = None

        layout = QVBoxLayout()

        menu_btn = QPushButton("Back to Menu")
        menu_btn.clicked.connect(self.parent.show_menu)
        layout.addWidget(menu_btn)

        name_layout = QHBoxLayout()
        name_label = QLabel("Deck name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        buttons_layout = QHBoxLayout()
        add_card_btn = QPushButton("Add card to deck")
        add_card_btn.clicked.connect(lambda: self.parent.show_card_selection_view(self.deck))

        finish_btn = QPushButton("Finish deck")
        finish_btn.clicked.connect(self.finish_deck)

        buttons_layout.addWidget(add_card_btn)
        buttons_layout.addWidget(finish_btn)
        layout.addLayout(buttons_layout)

        layout.addStretch()
        self.setLayout(layout)

    #show_create_card_view(self, deck: Deck, card_type: CardType = None):

    def set_deck(self, deck: Deck):
        self.deck = deck
        self.name_input.setText(deck.name)

    def finish_deck(self):
        self.deck.name = self.name_input.text()
        if self.deck not in self.parent.decks:
            self.parent.add_deck(self.deck)
        self.deck = None
        self.parent.show_menu()
