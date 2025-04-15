import json
from deck import Deck
from flash_card import FlashCard, MultipleChoiceFlashCard, CardType

class DeckEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Deck):
            return {
                "name": o.name,
                "cards": o.cards, 
            }
        if isinstance(o, FlashCard):
            card: dict = {"card_type": o.type.name,
                          "question": o.question,
                          "answer": o.answer, 
                          }
            if isinstance(o, MultipleChoiceFlashCard):
                card["choices"] = o.choices
            return card
        raise TypeError

def decks_to_json(decks: list[Deck]) -> str:
    return json.dumps(decks, cls=DeckEncoder)

def json_to_decks(json_str: str) -> list[Deck]:
    deck_objs: list[dict] = json.loads(json_str)
    decks: list[Deck] = []
    for deck_obj in deck_objs:
        deck = Deck(deck_obj["name"])
        for card_obj in deck_obj["cards"]:
            card: FlashCard = None
            card_type: CardType = CardType[card_obj["card_type"]]
            if card_type == CardType.STANDARD:
                card = FlashCard(card_obj["question"], card_obj["answer"])
            else:
                card = MultipleChoiceFlashCard(card_obj["question"],
                                               card_obj["choices"], card_obj["answer"])
            deck.add_card(card)
        decks.append(deck)
    return decks

def save_decks_to_file(decks: list[Deck]) -> None:
    json_str: str = decks_to_json(decks)
    with open("saved_decks.json", "w", encoding="utf-8") as file:
        file.write(json_str)

def load_decks_from_file() -> list[Deck]:
    try:
        with open("saved_decks.json", "r", encoding="utf-8") as file:
            json_str: str = file.read()
            return json_to_decks(json_str)
    except FileNotFoundError:
        return []
