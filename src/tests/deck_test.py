import unittest
from entities.deck import Deck
from entities.flash_card import FlashCard

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_initializes_correctly(self):
        self.assertEqual(self.deck.name, "")
        self.assertEqual(self.deck.card_count(), 0)


    def test_add_card(self):
        card: FlashCard = FlashCard("Hund", "Dog")
        self.assertEqual(self.deck.card_count(), 0)

        self.deck.add_card(card)

        self.assertEqual(self.deck.card_count(), 1)

    def test_name(self):
        name: str = "Test"
        deck = Deck(name)
        self.assertEqual(deck.name, name)
