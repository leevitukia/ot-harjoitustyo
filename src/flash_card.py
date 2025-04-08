from enum import Enum

class CardType(Enum):
    STANDARD = "standard"
    MULTIPLE_CHOICE = "multiple_choice"

class FlashCard:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer
        self.type = CardType.STANDARD

    def check_answer(self, answer: str) -> bool:
        return answer.strip().lower() == self.answer.strip().lower()

class MultipleChoiceFlashCard(FlashCard):
    def __init__(self, question: str, choices: list[str], answer: str):
        if answer not in choices:
            raise ValueError("Answer must be one of the provided choices")
        super().__init__(question, answer)
        self.choices: list[str] = choices
        self.type = CardType.MULTIPLE_CHOICE
