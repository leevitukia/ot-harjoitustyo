import unittest
from flash_card import MultipleChoiceFlashCard

class TestMultipleChoiceFlashCard(unittest.TestCase):
    def setUp(self):
        self.choices = ["Dog", "Koira", "Blank", "Blank"]
        self.card = MultipleChoiceFlashCard("Hund", self.choices, "Dog")

    def test_question_correct(self):
        self.assertEqual(self.card.question, "Hund")

    def test_answer_correct(self):
        self.assertEqual(self.card.answer, "Dog")

    def test_check_correct_answer(self):
        self.assertTrue(self.card.check_answer("  dOg    "))

    def test_check_incorrect_answer(self):
        self.assertFalse(self.card.check_answer("koira"))
