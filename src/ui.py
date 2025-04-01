import tkinter as tk
from deck import Deck
from flash_card import FlashCard

def create_ui():
    global window 
    window = tk.Tk()
    create_menu()
    window.mainloop()
    
def create_menu():
    global window
    clear()

    tk.Button(window, text="View decks", fg="blue", command=view_decks).grid(row=0, column=0)

    tk.Button(window, text="Create deck", fg='blue', command=create_deck).grid(row=1, column=0)
    window.title('Flashcard App')
    window.geometry("300x200+10+10")

def view_decks():
    global window
    clear()
    unnamed_deck_counter: int = 1
    for i, deck in enumerate(decks):
        name: str = deck.name
        if deck.name.strip() == "":
            name = f"Unnamed deck {unnamed_deck_counter}"
            unnamed_deck_counter += 1
        tk.Button(window, text=name, fg="blue", command=lambda: view_deck(i)).grid(row=i, column=0)


def view_deck(index: int):
    global window
    clear()
    deck: Deck = decks[index]
    view_card(deck, 0)



def view_card(deck: Deck, index: int, flipped: bool = False):
    global window
    clear()

    if index >= deck.card_count() or index < 0:
        create_menu()

    tk.Button(window, text="Menu", fg="blue", command=create_menu).grid(row=0, column=0)

    card: FlashCard = deck.cards[index]
    label_text: str = "Answer" if flipped else "Question"
    card_text: str = card.answer if flipped else card.question
    tk.Label(window, text=label_text).grid(row=1, column=0)
    tk.Button(window, text=card_text, fg="blue", command=lambda: view_card(deck, index, not flipped), padx=30, pady=30).grid(row=2, column=0)

    if index > 0:
        tk.Button(window, text="Previous card", fg="blue", command=lambda: view_card(deck, index-1), padx=30, pady=30).grid(row=3, column=0)

    if index < deck.card_count() - 1:
        tk.Button(window, text="Next card", fg="blue", command=lambda: view_card(deck, index+1), padx=30, pady=30).grid(row=3, column=1)




def create_deck():
    global window
    clear()
    new_deck = Deck()

    def add_deck_and_go_back():
        new_deck.name = deck_name.get()
        decks.append(new_deck)
        create_menu()

    def add_card_to_deck():
        new_card = FlashCard(question.get(), answer.get())
        question.delete(0, tk.END)
        answer.delete(0, tk.END)
        new_deck.add_card(new_card)


    deck_name = tk.Entry(window)
    tk.Label(window, text="Deck name").grid(row=0, column=0)
    cancel = tk.Button(window, text="Cancel", fg='red', command=create_menu)
    finish = tk.Button(window, text="Finish deck", fg='green', command=add_deck_and_go_back)
    add_card = tk.Button(window, text="Add card to deck", fg='green', command=add_card_to_deck)
    tk.Label(window, text="Question").grid(row=2)
    tk.Label(window, text="Answer").grid(row=3)
    question = tk.Entry(window)
    answer = tk.Entry(window)

    deck_name.grid(row=0, column=1)
    question.grid(row=2, column=1)
    answer.grid(row=3, column=1)
    add_card.grid(row=4, column=1)
    cancel.grid(row=6, column=1)
    finish.grid(row=6, column=2)
    

    
def clear():
    global window
    for child in window.winfo_children():
        child.destroy()


window: tk.Tk = None
decks: list[Deck] = []