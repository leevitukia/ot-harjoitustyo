from PySide6.QtWidgets import (QWidget, QPushButton, # pylint: disable=no-name-in-module
                              QLabel,#pylint is complaining for no reason
                              QVBoxLayout, QHBoxLayout)
from entities.deck import Deck
from entities.flash_card import CardType

class CardSelectionView(QWidget):
    """
    A view for selecting the type of a flashcard during its creation

    Attributes:
        parent: The parent of the view
        deck: The deck that the current card is a part of
        view_layout: the layout of the widget
        content_layout: the layout for the content of the view
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.deck: Deck = None
        self.view_layout = QVBoxLayout()

        self.content_layout = QVBoxLayout()
        self.view_layout.addLayout(self.content_layout)
        self.setLayout(self.view_layout)

        back_btn = QPushButton("Go Back")
        back_btn.clicked.connect(lambda: self.parent.show_create_deck_view(self.deck))
        self.content_layout.addWidget(back_btn)

        type_label = QLabel("Select card type:")
        self.content_layout.addWidget(type_label)

        buttons_layout = QHBoxLayout()

        for enum_val in CardType:
            btn = QPushButton(enum_val.value)
            btn.clicked.connect(
                lambda _, e=enum_val: self.parent.show_create_card_view(self.deck, e)
            )
            buttons_layout.addWidget(btn)

        self.content_layout.addLayout(buttons_layout)


    def set_deck(self, deck: Deck):
        """
        Sets the active deck of the view
        Args:
            deck: the deck to set as active
        """
        self.deck = deck
