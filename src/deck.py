from flash_card import FlashCard

class Deck:
    def __init__(self, name: str=""):
        self.cards: list[FlashCard] = []
        self.name = name

    def card_count(self) -> int:
        return len(self.cards)

    def add_card(self, card: FlashCard):
        self.cards.append(card)
