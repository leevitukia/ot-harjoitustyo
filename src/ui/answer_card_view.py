from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel, QLineEdit, #pylint is complaining for no reason
                              QVBoxLayout, QHBoxLayout)

from entities.deck import Deck
from entities.flash_card import FlashCard
from ui.ui_utils import clear_layout

class AnswerCardView(QWidget):
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

        question_label = QLabel(card.question)

        answer_label = QLabel("Answer:")
        answer_input = QLineEdit()
        submit_btn = QPushButton()

        submit_btn.clicked.connect(lambda: self._submit_answer(answer_input.text()))

        self.card_layout.addWidget(question_label)
        self.card_layout.addWidget(answer_label)
        self.card_layout.addWidget(answer_input)
        self.card_layout.addWidget(submit_btn)

        self._create_nav_buttons()


    def _submit_answer(self, answer: str):
        card: FlashCard = self.deck.cards[self.current_index]
        clear_layout(self.card_layout)
        label = QLabel()
        if card.check_answer(answer):
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
