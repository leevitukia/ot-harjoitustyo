from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel,#pylint is complaining for no reason
                              QVBoxLayout, QHBoxLayout)

from entities.deck import Deck
from entities.flash_card import FlashCard, MultipleChoiceFlashCard
from ui.ui_utils import clear_layout

class CardView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.deck: Deck = None
        self.current_index: int = 0
        self.flipped: bool = False
        self.view_layout = QVBoxLayout()
        self.card_layout = QVBoxLayout()
        self.nav_buttons = QHBoxLayout()

        menu_btn = QPushButton("Go back")
        menu_btn.clicked.connect(self.parent.show_decks_view)
        self.view_layout.addWidget(menu_btn)

        self.view_layout.addLayout(self.card_layout)
        self.view_layout.addLayout(self.nav_buttons)
        self.setLayout(self.view_layout)

    def show_card(self, index: int):
        clear_layout(self.card_layout)
        card: FlashCard = self.deck.cards[index]
        self.current_index = index
        if not isinstance(card, MultipleChoiceFlashCard):
            card_btn = QPushButton(card.question)
            card_btn.clicked.connect(self._flip_card)
            self.card_layout.addWidget(card_btn)
        else:
            label = QLabel(card.question)
            self.card_layout.addWidget(label)
            for option in card.choices:
                btn = QPushButton(option)
                correct_answer: bool = option == card.answer
                btn.clicked.connect(lambda _, a=correct_answer:
                                    self._flip_card(a)
                                    )
                self.card_layout.addWidget(btn)

        self._create_nav_buttons()

    def _flip_card(self, answered_correctly: bool = False):
        card: FlashCard = self.deck.cards[self.current_index]
        self.flipped = not self.flipped
        if not isinstance(card, MultipleChoiceFlashCard):
            card_btn: QPushButton = self.card_layout.itemAt(0).widget()
            text: str = card.answer if self.flipped else card.question
            card_btn.setText(text)
        else:
            clear_layout(self.card_layout)
            label = QLabel()
            if answered_correctly:
                label.setText("Correct!")
            else:
                label.setText(f"Incorrect! The answer is {card.answer}")
            self.card_layout.addWidget(label)

    def set_deck(self, deck: Deck):
        self.deck = deck

    def _create_nav_buttons(self):
        clear_layout(self.nav_buttons)
        if self.current_index > 0:
            prev_btn = QPushButton("Previous card")
            prev_btn.clicked.connect(lambda: self.show_card(self.current_index - 1))
            self.nav_buttons.addWidget(prev_btn)

        if self.current_index < self.deck.card_count() - 1:
            next_btn = QPushButton("Next card")
            next_btn.clicked.connect(lambda: self.show_card(self.current_index + 1))
            self.nav_buttons.addWidget(next_btn)
