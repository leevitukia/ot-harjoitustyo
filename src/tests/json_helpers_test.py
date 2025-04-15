import unittest
import json
from entities.deck import Deck
from entities.flash_card import FlashCard, MultipleChoiceFlashCard, CardType
import services.json_helpers as json_helpers

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.decks: list[Deck] = []
        deck = Deck("Swedish 1")
        deck.add_card(FlashCard("Frukt", "Fruit"))
        self.decks.append(deck)

        deck = Deck("Swedish 2")
        deck.add_card(MultipleChoiceFlashCard("Frukt", ["Fruit", "Dog", "Apple", "Vegetable"], "Fruit"))
        self.decks.append(deck)
        
    def test_encodes_and_decodes_correctly(self):
        json_str: str = json_helpers.decks_to_json(self.decks)
        decks: list[Deck] = json_helpers.json_to_decks(json_str)
        self.assertEqual(decks, self.decks) 

    def test_encoder_fail(self):
        with self.assertRaises(TypeError):
            json.dumps(self, cls=json_helpers.DeckEncoder)
