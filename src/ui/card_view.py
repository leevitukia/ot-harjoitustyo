from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel,#pylint is complaining for no reason
                              QVBoxLayout, QHBoxLayout,
                              QLineEdit)

from entities.deck import Deck
from entities.flash_card import FlashCard, MultipleChoiceFlashCard, CardType
from ui.ui_utils import clear_layout, create_alert
import random

class CardView(QWidget):
    """
    A view for a single card

    Attributes:
        parent: The parent of the view
        deck: The deck that the current card is a part of
        current_index: the position of the current card in the deck
        flipped: whether or not the displayed card is flipped
        view_layout: the layout of the widget
        card_layout: the layout for elements related to the card
        nav_buttons: the layout for the next and previous card buttons
    """
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
        """
        Shows the card at the specified index
        Args:
            index: the index of the card to show
        """
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
        """
        Flips the card and alters the text based on if the user answered correctly or not
        Args:
            answered_correctly: whether or not the user answered correctly, defaults to False
        """
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
        """
        Edits the card at the specified index
        Args:
            index: the index of the card to edit
        """
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
                     answer: str, options: list[str] = None):
        """
        Updates the attributes of the card at the specified index
        Args:
            index: the index of the card
            question: the updated question
            answer: the updated answer
            options: the updated options, defaults to None
        """
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
        self.deck.cards[index] = card # necessary because list items apparently aren't passed by reference

    def set_deck(self, deck: Deck):
        self.deck = deck

    def _create_nav_buttons(self, edit = False):
        """
        Creates navigation buttons for the view
        Args:
            edit: if set to true the buttons will point to the edit view instead of the normal card view
        """
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
