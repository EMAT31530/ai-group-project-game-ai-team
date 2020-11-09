import random as rnd


class Card:  # Object to represent individual cards
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.visible = False  # If card is visible to other players

    def __str__(self):  # Overwrites the String fucntion
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        return '{} of {}'.format(vals[self.val-1], self.suit)

    def __lt__(self, other):  # Overwrites the less than function
        return self.val < other.val

    def __gt__(self, other):  # Overwrites the greater than function
        return self.val > other.val


class Deck:  # Object to represent deck throughout game
    def __init__(self):
        self.cards = []
        self.build()

    def __str__(self):  # Overwrites the String fucntion
        return str([str(card) for card in self.cards])

    def build(self):
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for i in range(1, 14):
                self.cards.append(Card(suit, i))

    def shuffle(self):
        rnd.shuffle(self.cards)

    def draw(self, burn=False):
        if burn:
            del self.cards[-1]
        return self.cards.pop(-1)


class Hand:  # Object to represent player hands
    def __init__(self):
        self.cards = []


newdeck = Deck()
print(newdeck)
newdeck.draw(burn=True)
print(newdeck)
