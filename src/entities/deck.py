from entities.flash_card import FlashCard

class Deck:
    """
    A collection of flashcards 

    Attributes:
        cards: a list of flashcards
        name: the name of the deck
    """
    def __init__(self, name: str = ""):
        """
        Creates a new Deck.

        Args:
            name (str): The name of the deck, defaults to an empty string
        """
        self.cards: list[FlashCard] = []
        self.name = name

    def card_count(self) -> int:
        """
        Returns the amount of cards in the deck
        """
        return len(self.cards)

    def add_card(self, card: FlashCard):
        """
        Adds a card to the deck
        Args:
            card: The card to add.
        """
        self.cards.append(card)

    def __eq__(self, other):
        if not isinstance(other, Deck):
            return False
        return (
            self.name == other.name and
            self.cards == other.cards
        )
