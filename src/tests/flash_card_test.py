import unittest
from entities.flash_card import FlashCard

class TestFlashCard(unittest.TestCase):
    def setUp(self):
        self.card = FlashCard("Hund", "Dog")

    def test_question_correct(self):
        self.assertEqual(self.card.question, "Hund")

    def test_answer_correct(self):
        self.assertEqual(self.card.answer, "Dog")

    def test_check_correct_answer(self):
        self.assertTrue(self.card.check_answer("  dOg    "))

    def test_check_incorrect_answer(self):
        self.assertFalse(self.card.check_answer("koira"))

    def test_eq_op(self):
        self.assertNotEqual(self.card, list())
