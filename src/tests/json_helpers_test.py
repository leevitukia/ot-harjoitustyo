import unittest
import json
from entities.deck import Deck
from entities.flash_card import FlashCard, MultipleChoiceFlashCard, CardType
import services.json_helpers as json_helpers
import os

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.decks: list[Deck] = []
        deck = Deck("Swedish 1")
        deck.add_card(FlashCard("Frukt", "Fruit"))
        self.decks.append(deck)
        self.file_name = "test_deck.json"

        deck = Deck("Swedish 2")
        deck.add_card(MultipleChoiceFlashCard("Frukt", ["Fruit", "Dog", "Apple", "Vegetable"], "Fruit"))
        self.decks.append(deck)

        self.json_str:str = '[{"name": "Swedish 1", "cards": [{"card_type": "STANDARD", "question": "Frukt", "answer": "Fruit", "successes": 0, "fails": 0}]},' \
        ' {"name": "Swedish 2", "cards": [{"card_type": "MULTIPLE_CHOICE", "question": "Frukt", "answer": "Fruit", "successes": 0, "fails": 0, ' \
        '"choices": ["Fruit", "Dog", "Apple", "Vegetable"]}]}]'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        
    def test_encodes_and_decodes_correctly(self):
        json_str: str = json_helpers.decks_to_json(self.decks)
        decks: list[Deck] = json_helpers.json_to_decks(json_str)
        self.assertEqual(decks, self.decks) 

    def test_encoder_fail(self):
        with self.assertRaises(TypeError):
            json.dumps(self, cls=json_helpers.DeckEncoder)

    def test_saving(self):
        json_helpers.save_decks_to_file(self.decks, self.file_name)

        self.assertEqual(os.path.exists(self.file_name), True)

        with open(self.file_name, "r", encoding="utf-8") as file:
            json_str: str = file.read()
            self.assertEqual(json_str, self.json_str)

    def test_loading_file_exists(self):
        json_helpers.save_decks_to_file(self.decks, self.file_name)
        loaded_decks: list[Deck] = json_helpers.load_decks_from_file(self.file_name)
        self.assertEqual(loaded_decks, self.decks)

    def test_loading_file_doesnt_exist(self):
        loaded_decks: list[Deck] = json_helpers.load_decks_from_file("948590348543y3kg23u493284y92uhfeiugowie9wur32894h9ug58gwe7ueugyu48y32gbuy4hv32u4y2v94u23g8")
        self.assertNotEqual(loaded_decks, self.decks)

    
        

    

