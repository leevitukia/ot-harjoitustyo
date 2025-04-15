from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel,#pylint is complaining for no reason
                              QVBoxLayout, QHBoxLayout, QLineEdit,
                              QStackedWidget)
from deck import Deck
from flash_card import FlashCard, MultipleChoiceFlashCard, CardType
from ui.ui_utils import clear_layout

class CreateCardView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.deck: Deck = None
        self.card_type: CardType = None

        self.view_layout = QVBoxLayout()

        #menu_btn = QPushButton("Back to Menu")
        #menu_btn.clicked.connect(self.parent.show_menu)
        #self.view_layout.addWidget(menu_btn)

        self.content_layout = QVBoxLayout()
        self.view_layout.addLayout(self.content_layout)

        self.setLayout(self.view_layout)

    def set_deck_and_type(self, deck: Deck, card_type: CardType):
        self.deck = deck
        self.card_type = card_type
        self._setup_ui()

    def _create_back_button(self):
        menu_btn = QPushButton("Go Back")
        menu_btn.clicked.connect(
            lambda: self.parent.show_create_deck_view(self.deck)
        )
        self.content_layout.addWidget(menu_btn)

    def _setup_ui(self):
        clear_layout(self.content_layout)
        self._create_back_button()
        question_layout = QHBoxLayout()
        question_label = QLabel("Question:")
        self.question_input = QLineEdit()
        question_layout.addWidget(question_label)
        question_layout.addWidget(self.question_input)
        self.content_layout.addLayout(question_layout)

        self.answer_inputs = []

        answer_layout = QHBoxLayout()
        answer_label = QLabel("Correct answer:")
        self.correct_answer_input = QLineEdit()
        self.answer_inputs.append(self.correct_answer_input)
        answer_layout.addWidget(answer_label)
        answer_layout.addWidget(self.correct_answer_input)
        self.content_layout.addLayout(answer_layout)

        print(self.card_type.value)
        if self.card_type == CardType.MULTIPLE_CHOICE:
            for i in range(3):
                option_layout = QHBoxLayout()
                option_label = QLabel(f"Option {i + 2}:")
                option_input = QLineEdit()
                self.answer_inputs.append(option_input)
                option_layout.addWidget(option_label)
                option_layout.addWidget(option_input)
                self.content_layout.addLayout(option_layout)

        add_btn = QPushButton("Add card to deck")
        add_btn.clicked.connect(self._add_card_to_deck)
        self.content_layout.addWidget(add_btn)

    def _add_card_to_deck(self):
        question = self.question_input.text()
        correct_answer = self.correct_answer_input.text()

        if self.card_type == CardType.STANDARD:
            card = FlashCard(question, correct_answer)
        else:
            choices = [input.text() for input in self.answer_inputs]
            card = MultipleChoiceFlashCard(question, choices, correct_answer)

        self.deck.add_card(card)
        self.parent.show_create_deck_view(self.deck)