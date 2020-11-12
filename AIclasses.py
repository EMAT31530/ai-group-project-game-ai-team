import random as rnd
from ranking import *

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

#would it be possible to overwrite the greater than function so that e.g. "Jack" > 7 or would this not work?

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


def straight_flush(hand): #all the following functions check to see if you have the following hand
    card_suits = num_suit(hand)
    consec_cards = consecutive(hand)
    #am wondering if the first 3 functions should be class methods so we don't have to constantly call them
    if consec_cards == False or list(card_suits.values())[0] < 5:
        return False
    else:
        suit_hand = Hand() #create a pseudo hand of all the cards of the main suit and then call the straight fu
        suit = list(card_suits.keys())[0]
        for i in hand.cards:
            if i.suit == suit:
                suit_hand.addCard(i)
        return consecutive(suit_hand), suit

    
def four_of_a_kind(hand):
    card_nums = num_same(hand)
    if list(card_nums.values())[0] != 4:
        return False
    else:
        main_card = list(card_nums.keys())[0]
        other_card = high_card(card_nums.pop(main_card))[0] #calling a function that doesn't yet exist, it will be needed in lots of places
        return main_card, other_card
        
#test for straight flush
test_2 = Hand()
for i in range(3):
    card = Card("Spades", i + 2)
    test_2.addCard(card)
for i in range(3, 6):
    card = Card("Spades", i + 2)
    test_2.addCard(card)

test_2.addCard(card)
    
print(straight_flush(test_2))
    
#test for four of a kind
test_3 = Hand()
cards = []
cards.append(Card("Spades", 4))
cards.append(Card("Spades", 7))
cards.append(Card("Clubs", 4))
cards.append(Card("Hearts", 4))
cards.append(Card("Diamonds", 4))
cards.append(Card("Clubs", 5))
cards.append(Card("Clubs", 10))
for i in range(7):
    test_3.addCard(cards[i])
print(num_same(test_3))
#print(four_of_a_kind(test_3))

