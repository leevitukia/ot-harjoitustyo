import unittest
from flash_card import FlashCard

class TestFlashCard(unittest.TestCase):
    def setUp(self):
        self.card = FlashCard("Hund", "Dog")


    def test_question_correct(self):
        self.assertEqual(self.card.question, "Hund")

    def test_answer_correct(self):
        self.assertEqual(self.card.answer, "Dog")
