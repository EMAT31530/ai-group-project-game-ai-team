import random as rnd

class Card:  # Object to represent individual cards
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.visible = False  # If card is visible to other players

    def __str__(self):  # Overwrites the String fucntion
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        return '{} of {}'.format(vals[self.val-2], self.suit)

    def __repr__(self):  # The Formal String representation of the object
        return '(val={}, suit={})'.format(self.val, self.suit)

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

    def build(self):  # To build a deck, can be used to rebuild also
        self.cards = []
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for i in range(2, 15):
                self.cards.append(Card(suit, i))
        self.shuffle()

    def shuffle(self):
        rnd.shuffle(self.cards)

    def draw(self, burn=False):
        if burn:  # Removes the top card from the deck
            del self.cards[-1]
        return self.cards.pop(-1)  # Removes and returns the top card


class Hand:  # Object to represent player hands
    def __init__(self):
        self.cards = []

    def __str__(self):  # Overwrites the String fucntion
        return str([str(card) for card in self.cards])

    def addCard(self, card):
        self.cards.append(card)

    def ranking(self):
        import ranking as rnk
        # attempted to do something better than ton of if statements
        """
        x = False
        while x != True:
            x = rnk.straight_flush(self)
            x = rnk.four_of_a_kind(self)
            x = rnk.full_house(self)
            x = rnk.flush(self)
            x = rnk.straight(self)
            x = rnk.trips(self)
            x = rnk.two_pair(self)
            x = rnk.pair(self)
        card_nums = rnk.num_same(self)
        return rnk.high_card(card_nums, sub = False)
        

        # hopefully identical function, speed 5.954329999999987e-06
        # faster? think i know why
        # the checker function is very long, downside if there is a bug, will be hard to find
        rnk.checker(self)
"""


        x = rnk.straight_flush(self)
        if x != False:
            return x
        x = rnk.four_of_a_kind(self)
        if x != False:
            return x
        x = rnk.full_house(self)
        if x != False:
            return x
        x = rnk.flush(self)
        if x != False:
            return x
        x = rnk.straight(self)
        if x != False:
            return x
        x = rnk.trips(self)
        if x != False:
            return x
        x = rnk.two_pair(self)
        if x != False:
            return x
        x = rnk.pair(self)
        if x != False:
            return x
        card_nums = rnk.num_same(self)
        return rnk.high_card(card_nums, sub = False)
        
    def __gt__(self, other): #other is also a hand object, compares two hand rankings
        rnk_1 = self.ranking()
        rnk_2 = other.ranking()
        for i in range(len(rnk_1)): #iterates through ranking; will return True if first differing element of rankings is greater for rnk_1, and False otherwise
            if rnk_1[i] > rnk_2[i]:
                return True
            if rnk_1[i] < rnk_2[i]:
                return False
        return False
    
    def __lt__(self, other): #ditto
        rnk_1 = self.ranking()
        rnk_2 = other.ranking()
        for i in range(len(rnk_1)):
            if rnk_1[i] < rnk_2[i]:
                return True
            if rnk_1[i] > rnk_2[i]:
                return False
        return False
    
    def __eq__(self, other): #ditto
        rnk_1 = self.ranking()
        rnk_2 = other.ranking()
        for i in range(len(rnk_1)):
            if rnk_1[i] != rnk_2[i]:
                return False
        return True
        
# ___Just some btec stuff to get an idea of what we would need to do___
class Player:  # Object to represent player
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.hand = Hand()
        self.money = 0


class Round:
    def __init__(self, players, bigBlind):
        self.pot = 0
        self.board = Hand()
        self.bigBlind = bigBlind
        self.players = players

    def roundstart(self):
        for i in range(2):
            for player in self.players:
                player.hand.addCard(self.deck.draw(burn=True))

    def boarddraw(self, i):  # For drawing for flop/turn/river
        for j in range(i):
            self.board.addCard(self.deck.draw(burn=True))


class Game:  # Object to represent game
    def __init__(self, players):
        self.players = players  # Pre created list of players
        self.deck = Deck()





#newdeck = Deck()
#print(newdeck)
#newdeck.draw(burn=True)
#print(newdeck)
