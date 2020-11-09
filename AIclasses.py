import random as rnd


class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def getcard(self):
        return '{} of {}'.format(self.val, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

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


newdeck = Deck()
for i in range(4):
    print(newdeck.cards[i].getcard())
newdeck.shuffle()
for i in range(4):
    print(i)
    print(newdeck.cards[i].getcard())
