from random import shuffle

class Card:
    def __init__(self, val, suit):
        self.suit = suit
        self.val = val

    def __str__(self): #Overwrites the String fucntion
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        return '{}{}'.format(vals[self.val-2], self.suit)

    def __lt__(self, other): #Overwrites the less than function
        return self.val < other.val

    def __gt__(self, other): #Overwrites the greater than function
        return self.val > other.val

    def __eq__(self, other): #Overwrites the equal function
        return self.val == other.val


class Deck:
    def __init__(self, vals, suits):
        self.cards = []
        self.vals = vals
        self.suits = suits
        self.build()
    
    def __str__(self): #Overwrites the String fucntion
        return str([str(card) for card in self.cards])

    def build(self): #To build, rebuild a deck
        self.cards = []
        for suit in self.suits:
            for val in self.vals:
                self.cards.append(Card(val, suit))
        shuffle(self.cards)

    def draw(self):
        shuffle(self.cards)
        return self.cards.pop(-1)  # Removes and returns the top card