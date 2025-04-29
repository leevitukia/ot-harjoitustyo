from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMenu, QMessageBox # pylint: disable=no-name-in-module
from entities.deck import Deck
from entities.flash_card import CardType
from ui.menu_view import MenuView
from ui.create_deck_view import CreateDeckView
from ui.create_card_view import CreateCardView
from ui.card_selection_view import CardSelectionView
from ui.decks_view import DecksView
from ui.card_view import CardView
from ui.answer_card_view import AnswerCardView
import services.json_helpers as json_helpers

class FlashcardApp(QMainWindow):
    def __init__(self): # TODO_: split to multiple functions
        super().__init__()
        self.decks: list[Deck] = []

        self.setWindowTitle('Flashcard App')

        screen = QApplication.primaryScreen().geometry()
        size: int = screen.height() / 2

        self.setGeometry((screen.width() - size) / 2, (screen.height() - size) / 2, size, size)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self._add_widgets_to_stack()
        self._create_top_bar()
        self.show_menu()

    def _add_widgets_to_stack(self):
        self.menu_view = MenuView(self)
        self.create_deck_view = CreateDeckView(self)
        self.create_card_view = CreateCardView(self)
        self.card_selection_view = CardSelectionView(self)
        self.decks_view = DecksView(self)
        self.card_view = CardView(self)
        self.answer_card_view = AnswerCardView(self)

        self.stack.addWidget(self.menu_view)
        self.stack.addWidget(self.create_deck_view)
        self.stack.addWidget(self.create_card_view)
        self.stack.addWidget(self.card_selection_view)
        self.stack.addWidget(self.decks_view)
        self.stack.addWidget(self.card_view)
        self.stack.addWidget(self.answer_card_view)

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu_view)

    def show_create_deck_view(self, deck: Deck = None):
        self.create_deck_view.set_deck(deck if deck else Deck())
        self.stack.setCurrentWidget(self.create_deck_view)

    def show_decks_view(self):
        self.decks_view.refresh_deck_list()
        self.stack.setCurrentWidget(self.decks_view)

    def show_deck(self, index: int):
        self.card_view.set_deck(self.decks[index])
        self.card_view.show_card(0)
        self.stack.setCurrentWidget(self.card_view)

    def show_create_card_view(self, deck: Deck, card_type: CardType):
        self.create_card_view.set_deck_and_type(deck, card_type)
        self.stack.setCurrentWidget(self.create_card_view)

    def show_card_selection_view(self, deck: Deck):
        self.card_selection_view.set_deck(deck)
        self.stack.setCurrentWidget(self.card_selection_view)

    def show_answer_card_view(self, index: int):
        self.answer_card_view.set_deck(self.decks[index])
        self.answer_card_view.show_card(0)
        self.stack.setCurrentWidget(self.answer_card_view)

    def add_deck(self, deck: Deck):
        self.decks.append(deck)

    def _load_decks(self):
        loaded_decks: list[Deck] = json_helpers.load_decks_from_file()
        if len(loaded_decks) != 0:
            self.decks = loaded_decks

    def _create_top_bar(self):
        menu_bar = self.menuBar()

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)
        save_decks = file_menu.addAction("Save Decks")
        save_decks.triggered.connect(lambda: json_helpers.save_decks_to_file(self.decks))
        load_decks = file_menu.addAction("Load Decks")
        load_decks.triggered.connect(self._load_decks)

def create_ui():
    app = QApplication([])

    window = FlashcardApp()
    window.show()

    app.exec()
