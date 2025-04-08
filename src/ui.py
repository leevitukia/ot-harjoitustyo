import tkinter as tk
from deck import Deck
from flash_card import FlashCard, MultipleChoiceFlashCard, CardType

class UI: # TODO: switch from tkinter to something else
    def __init__(self):
        self.window = tk.Tk()
        self.decks: list[Deck] = []
        self.create_menu()
        self.window.mainloop()

    def create_ui(self):
        self.window = tk.Tk()
        self.create_menu()
        self.window.mainloop()

    def create_menu(self):
        self.clear()

        tk.Button(self.window, text="View decks", fg="blue",
                  command=self.view_decks).grid(row=0, column=0)

        tk.Button(self.window, text="Create deck", fg='blue',
                  command=self.create_deck).grid(row=1, column=0)
        self.window.title('Flashcard App')
        self.window.geometry("300x200+10+10")

    def view_decks(self):
        self.clear()
        unnamed_deck_counter: int = 1
        for i, deck in enumerate(self.decks):
            name: str = deck.name
            if deck.name.strip() == "":
                name = f"Unnamed deck {unnamed_deck_counter}"
                unnamed_deck_counter += 1
            tk.Button(self.window, text=name, fg="blue",
                      command=lambda i=i: self.view_deck(i)).grid(row=i, column=0)

    def view_deck(self, index: int):
        self.clear()
        deck: Deck = self.decks[index]
        self.view_card(deck, 0)

    def view_card(self, deck: Deck, index: int, flipped: bool = False):
        if index >= deck.card_count() or index < 0:
            self.create_menu()

        card = deck.cards[index]

        if card.type == CardType.STANDARD:
            self.view_standard_flashcard(deck, index, flipped)
        elif card.type == CardType.MULTIPLE_CHOICE:
            self.view_multiple_choice_flashcard(deck, index, flipped)

    def create_next_and_previous_buttons(self, deck: Deck, index: int, row: int):
        if index > 0:
            tk.Button(self.window, text="Previous card", fg="blue",
                      command=lambda: self.view_card(deck, index-1),
                      padx=30, pady=30).grid(row=row, column=0)

        if index < deck.card_count() - 1:
            tk.Button(self.window, text="Next card", fg="blue",
                      command=lambda: self.view_card(deck, index+1),
                      padx=30, pady=30).grid(row=row, column=1)

    def view_standard_flashcard(self, deck: Deck, index: int, flipped: bool = False):
        self.clear()
        tk.Button(self.window, text="Menu", fg="blue",
                  command=self.create_menu).grid(row=0, column=0)

        card: FlashCard = deck.cards[index]
        label_text: str = "Answer" if flipped else "Question"
        card_text: str = card.answer if flipped else card.question
        tk.Label(self.window, text=label_text).grid(row=1, column=0)
        tk.Button(self.window, text=card_text, fg="blue",
                  command=lambda: self.view_card(deck, index, not flipped),
                  padx=30, pady=30).grid(row=2, column=0)


    def view_multiple_choice_flashcard(self, deck: Deck, index: int,
                                       flipped: bool = False, correct: bool = False):
        self.clear()
        tk.Button(self.window, text="Menu", fg="blue",
                  command=self.create_menu).grid(row=0, column=0)

        card: MultipleChoiceFlashCard = deck.cards[index]

        if flipped:
            label_text: str = "Correct!" if correct else f"Incorrect! The answer is {card.answer}"
            tk.Label(self.window, text=label_text).grid(row=1, column=0)
        else:
            tk.Label(self.window, text="Choices").grid(row=1, column=0)
            for i, choice in enumerate(card.choices):
                is_correct_answer: bool = card.check_answer(choice)

                tk.Button(self.window, text=choice, fg="blue",
                    command=lambda b=is_correct_answer:
                    self.view_multiple_choice_flashcard(deck, index, True, b),
                    padx=20, pady=5).grid(row=2+i, column=0)
        row = 3
        if not flipped:
            row += len(card.choices)
        self.create_next_and_previous_buttons(deck, index, row)


    def add_deck_and_go_back(self, deck: Deck, name: str):
        deck.name = name
        self.decks.append(deck)
        self.create_menu()

    def create_deck(self, deck: Deck = None):
        self.clear()
        if deck is None:
            deck = Deck()

        deck_name = tk.Entry(self.window)
        tk.Label(self.window, text="Deck name").grid(row=0, column=0)

        finish = tk.Button(
            self.window, text="Finish deck", fg='green',
            command=lambda: self.add_deck_and_go_back(deck, deck_name.get()))

        add_card = tk.Button(
            self.window, text="Add card to deck", fg='green',
            command=lambda: self.create_and_add_card(deck))

        deck_name.grid(row=0, column=1)
        add_card.grid(row=4, column=1)
        finish.grid(row=6, column=2)


    def add_card_to_deck(self, deck: Deck, question: str, entries: list[tk.Entry]):
        correct_answer = entries[0].get()
        if len(entries) == 1:
            card: FlashCard = FlashCard(question, correct_answer)
        else:
            choices: list[str] = [x.get() for x in entries]
            card: FlashCard = MultipleChoiceFlashCard(question, choices, correct_answer)
        deck.add_card(card)
        self.create_deck(deck)


    def create_and_add_card(self, deck: Deck, card_type: CardType = None):
        self.clear()
        tk.Button(self.window, text="Menu", fg="blue",
                  command=self.create_menu).grid(row=0, column=0)
        if card_type is None:
            tk.Button(
            self.window, text="Standard", fg='green',
            command=lambda: self.create_and_add_card(deck, CardType.STANDARD)
            ).grid(row=2, column=0)
            tk.Button(
            self.window, text="Multiple choice", fg='green',
            command=lambda: self.create_and_add_card(deck, CardType.MULTIPLE_CHOICE)
            ).grid(row=2, column=1)
        else:
            tk.Label(self.window, text="Question: ").grid(row=2, column=0)
            question = tk.Entry(self.window)
            question.grid(row=2, column=1)
            entries: list[tk.Entry] = []
            tk.Label(self.window, text="Correct answer: ").grid(row=3, column=0)
            entries.append(tk.Entry(self.window))
            entries[0].grid(row=3, column=1)
            if card_type == CardType.MULTIPLE_CHOICE:
                for i in range(3):
                    tk.Label(self.window, text=f"Option {i + 2}: ").grid(row=4 + i, column=0)
                    entries.append(tk.Entry(self.window))

                for entry in range(1,4):
                    entries[entry].grid(row=3 + entry, column=1)

            tk.Button(
            self.window, text="Add card to deck", fg='green',
            command=lambda: self.add_card_to_deck(deck, question.get(), entries)
            ).grid(row=3 + len(entries), column=1)



    def clear(self):
        for child in self.window.winfo_children():
            child.destroy()
