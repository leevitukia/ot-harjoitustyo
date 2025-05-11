from enum import Enum

class CardType(Enum):
    """
    Enum of the flashcard types

    Attributes:
        STANDARD: A basic flashcard with a single correct answer
        MULTIPLE_CHOICE: A flashcard with multiple choices
    """
    STANDARD = "Standard"
    MULTIPLE_CHOICE = "Multiple choice"

class FlashCard:
    """
    A basic flashcard with a question and an answer

    Attributes:
        question: The question on the flashcard
        answer: The correct answer to the question
        type: The type of the flashcard
        successes: The number of times the card was answered correctly
        fails: The number of times the card was answered incorrectly
    """
    def __init__(self, question: str, answer: str):
        """
        Initializes a standard flashcard

        Args:
            question: The question on the flashcard
            answer: The correct answer to the question
        """
        self.question = question
        self.answer = answer
        self.type = CardType.STANDARD
        self.successes = 0
        self.fails = 0

    def check_answer(self, answer: str) -> bool:
        """
        Checks if the provided answer is correct

        Args:
            answer: The answer to check
        """
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
    """
    A multiple choice flashcard with a question and multiple options

    Attributes:
        question: The question on the flashcard
        answer: The correct answer to the question
        type: The type of the flashcard
        successes: The number of times the card was answered correctly
        choices: The answer options to show to the user
        fails: The number of times the card was answered incorrectly
    """
    def __init__(self, question: str, choices: list[str], answer: str):
        """
        Initializes a multiple choice flashcard

        Args:
            question: The question on the flashcard
            choices: A list of answer options
            answer: The correct answer to the question
        """
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
