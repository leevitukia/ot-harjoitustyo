from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel,#pylint is complaining for no reason
                              QVBoxLayout, QHBoxLayout,
                              QLineEdit)

from entities.deck import Deck
from entities.flash_card import FlashCard, MultipleChoiceFlashCard, CardType
from ui.ui_utils import clear_layout, create_alert
import random

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
            options = card.choices[:] # clones the list
            random.shuffle(options) # shuffles the options so that it isn't obvious which one is correct
            for option in options:
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

    def edit_card(self, index: int):
        clear_layout(self.card_layout)
        card: FlashCard = self.deck.cards[index]
        self.current_index = index

        question_layout = QHBoxLayout()
        question_label = QLabel("Question")
        question_input = QLineEdit(text=card.question)
        question_layout.addWidget(question_label)
        question_layout.addWidget(question_input)
        self.card_layout.addLayout(question_layout)

        save_btn = QPushButton("Save card")

        answer_layout = QHBoxLayout()
        answer_label = QLabel("Correct answer:")
        answer_input = QLineEdit(card.answer)
        answer_layout.addWidget(answer_label)
        answer_layout.addWidget(answer_input)
        self.card_layout.addLayout(answer_layout)

        
        if not isinstance(card, MultipleChoiceFlashCard):
            save_btn.clicked.connect(lambda:
                                self._update_card(index, question_input.text(),
                                answer_input.text(), 
                                None))
        else:
            option_inputs: list[QLineEdit] = [answer_input]
            for i, option in enumerate(card.choices[1:]):
                option_layout = QHBoxLayout()
                option_label = QLabel(f"Option {i + 2}:")
                option_input = QLineEdit(option)
                option_layout.addWidget(option_label)
                option_layout.addWidget(option_input)
                option_inputs.append(option_input)
                self.card_layout.addLayout(option_layout)

            save_btn.clicked.connect(lambda:
                                self._update_card(index, question_input.text(),
                                answer_input.text(), 
                                [x.text() for x in option_inputs]))
            

        self.card_layout.addWidget(save_btn)

        self._create_nav_buttons(edit=True)

    def _update_card(self, index: int, question: str, 
                     answer: str, options: list[str]):
        card: FlashCard = self.deck.cards[index]
        qna_empty: bool = "" in [question.strip(), answer.strip()]
        options_empty = card.type == CardType.MULTIPLE_CHOICE and "" in [option.strip() for option in options]
        print(qna_empty)
        print(options_empty)
        if qna_empty or options_empty:
            create_alert("All fields must be filled out")
            return
        
        card.question = question
        card.answer = answer
        if isinstance(card, MultipleChoiceFlashCard):
            card.choices = options
        self.deck.cards[index] = card

    def set_deck(self, deck: Deck):
        self.deck = deck

    def _create_nav_buttons(self, edit = False):
        clear_layout(self.nav_buttons)
        if self.current_index > 0:
            prev_btn = QPushButton("Previous card")
            if edit:
                prev_btn.clicked.connect(lambda: self.edit_card(self.current_index - 1))
            else:
                prev_btn.clicked.connect(lambda: self.show_card(self.current_index - 1))
            self.nav_buttons.addWidget(prev_btn)

        if self.current_index < self.deck.card_count() - 1:
            next_btn = QPushButton("Next card")
            if edit:
                next_btn.clicked.connect(lambda: self.edit_card(self.current_index + 1))
            else:
                next_btn.clicked.connect(lambda: self.show_card(self.current_index + 1))
            self.nav_buttons.addWidget(next_btn)
