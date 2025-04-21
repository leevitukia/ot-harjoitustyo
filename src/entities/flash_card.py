from enum import Enum

class CardType(Enum):
    STANDARD = "Standard"
    MULTIPLE_CHOICE = "Multiple choice"

class FlashCard:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer
        self.type = CardType.STANDARD
        self.successes = 0
        self.fails = 0

    def check_answer(self, answer: str) -> bool:
        answer_is_correct: bool = answer.strip().lower() == self.answer.strip().lower()
        if answer_is_correct:
            self.successes += 1
        else:
            self.fails += 1
        return answer_is_correct 

    def __eq__(self, other):
        if not isinstance(other, FlashCard):
            return False
        return (
            self.question == other.question and
            self.answer == other.answer and
            self.type == other.type
        )


class MultipleChoiceFlashCard(FlashCard):
    def __init__(self, question: str, choices: list[str], answer: str):
        if answer not in choices:
            raise ValueError("Answer must be one of the provided choices")
        super().__init__(question, answer)
        self.choices: list[str] = choices
        self.type = CardType.MULTIPLE_CHOICE

    def __eq__(self, other):
        if not isinstance(other, MultipleChoiceFlashCard):
            return False
        return (
            super().__eq__(other) and
            self.choices == other.choices
        )
