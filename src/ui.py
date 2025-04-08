import tkinter as tk
from deck import Deck
from flash_card import FlashCard

class UI:
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
        self.clear()

        if index >= deck.card_count() or index < 0:
            self.create_menu()

        tk.Button(self.window, text="Menu", fg="blue",
                  command=self.create_menu).grid(row=0, column=0)

        card: FlashCard = deck.cards[index]
        label_text: str = "Answer" if flipped else "Question"
        card_text: str = card.answer if flipped else card.question
        tk.Label(self.window, text=label_text).grid(row=1, column=0)
        tk.Button(self.window, text=card_text, fg="blue",
                  command=lambda: self.view_card(deck, index, not flipped),
                  padx=30, pady=30).grid(row=2, column=0)

        if index > 0:
            tk.Button(self.window, text="Previous card", fg="blue",
                      command=lambda: self.view_card(deck, index-1),
                      padx=30, pady=30).grid(row=3, column=0)

        if index < deck.card_count() - 1:
            tk.Button(self.window, text="Next card", fg="blue",
                      command=lambda: self.view_card(deck, index+1),
                      padx=30, pady=30).grid(row=3, column=1)

    def add_deck_and_go_back(self, deck: Deck, name: str):
        deck.name = name
        self.decks.append(deck)
        self.create_menu()

    def add_card_to_deck(self, deck: Deck, q_entry: tk.Entry, a_entry: tk.Entry):
        new_card = FlashCard(q_entry.get(), a_entry.get())
        q_entry.delete(0, tk.END)
        a_entry.delete(0, tk.END)
        deck.add_card(new_card)

    def create_deck(self):
        self.clear()
        new_deck = Deck()

        deck_name = tk.Entry(self.window)
        tk.Label(self.window, text="Deck name").grid(row=0, column=0)

        tk.Label(self.window, text="Question").grid(row=2)
        tk.Label(self.window, text="Answer").grid(row=3)
        question = tk.Entry(self.window)
        answer = tk.Entry(self.window)

        cancel = tk.Button(self.window, text="Cancel", fg='red',
                           command=self.create_menu)

        finish = tk.Button(
            self.window, text="Finish deck", fg='green',
            command=lambda: self.add_deck_and_go_back(new_deck, deck_name.get()))

        add_card = tk.Button(
            self.window, text="Add card to deck", fg='green',
            command=lambda: self.add_card_to_deck(new_deck, question, answer))

        deck_name.grid(row=0, column=1)
        question.grid(row=2, column=1)
        answer.grid(row=3, column=1)
        add_card.grid(row=4, column=1)
        cancel.grid(row=6, column=1)
        finish.grid(row=6, column=2)

    def clear(self):
        for child in self.window.winfo_children():
            child.destroy()
