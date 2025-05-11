import json
from entities.deck import Deck
from entities.flash_card import FlashCard, MultipleChoiceFlashCard, CardType
import ui.ui_utils


class DeckEncoder(json.JSONEncoder):
    """
    A json encoder for encoding decks and cards to JSON
    """
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
                          "successes": o.successes,
                          "fails": o.fails, 
                          }
            if isinstance(o, MultipleChoiceFlashCard):
                card["choices"] = o.choices
            return card
        raise TypeError

def decks_to_json(decks: list[Deck]) -> str:
    """
    Converts a list of decks to a JSON string
    Args:
        decks: the list of decks to convert
    """
    return json.dumps(decks, cls=DeckEncoder)

def json_to_decks(json_str: str) -> list[Deck]:
    """
    Converts a JSON string to a list of decks
    Args:
        json_str: the JSON string to convert
    """
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

def save_decks_to_file(decks: list[Deck], file_name: str = "saved_decks.json") -> None:
    """
    Converts a list of decks to JSON and saves them to a file
    Args:
        decks: the list of decks to save
        file_name: the file path of the JSON file, defaults to saved_decks.json in the working directory
    """
    json_str: str = decks_to_json(decks)
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(json_str)

def load_decks_from_file(file_path: str = "") -> list[Deck]:
    """
    Loads a list of decks from the provided JSON file
    Args:
        file_path: the path to a json file
    """
    try:
        if file_path == "":
            file_path = ui.ui_utils.get_file_path("json (*.json)")

        with open(file_path, "r", encoding="utf-8") as file:
            json_str: str = file.read()
            return json_to_decks(json_str)
    except FileNotFoundError:
        return []
