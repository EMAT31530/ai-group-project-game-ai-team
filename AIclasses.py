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

def high_card(card_nums, num = 5): #card_nums is a dictionary here but this could be changed
    #assuming here that the hand inputted will not have any pairs or anything
    if len(card_nums) == 0:
        return 0 #convention
    card_nums = sort_by_key(card_nums, True)
    cards = list(card_nums.keys())
    if len(cards) < num:
        return cards #output here is a list; in previous functions the output is a tuple - not sure of an easy way to adapt this
    else:
        return cards[:num]

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
        if len(list(card_nums.keys())) == 1:
            return list(card_nums.keys())[0], 0 #if the hand is only four cards (not technically possible in a poker game but anyway) then by default return the four of a kind and zero
        else:
            card_nums.pop(main_card)
            other_card = high_card(card_nums, 1) 
            return main_card, other_card

def full_house(hand):
    card_nums = num_same(hand)
    keys = list(card_nums.keys()) #making a quick list of the keys and values to make things easier
    vals = list(card_nums.values())
    if vals[0] != 3 or len(vals) == 1: #require a three of a kind and a pair as well
        return False
    elif vals[1] == 1: 
        return False
    else:
        if vals[1] == 3: #if we have two three of a kinds (rare but possible) then we choose the higher ranking as our three of a kind and the lower as our pair
            return max(keys[0], keys[1]), min(keys[0], keys[1])
        elif len(vals) > 2 and vals[2] == 2: #if we have a three of a kind and two pairs then we must choose the higher ranking of the two pairs
            #also the and statement will evaluate to see if the length is long enough for vals[2] to exist before referencing it
            return keys[0], max(keys[1], keys[2])
        else:
            return keys[0], keys[1]
        
def flush(hand):
    card_suits = num_suit(hand)
    if list(card_suits.values())[0] < 5:
        return False
    else:
        suit_hand = Hand() #code mostly copied from straight flush function
        suit = list(card_suits.keys())[0]
        for i in hand.cards:
            if i.suit == suit:
                suit_hand.addCard(i)
        return high_card(num_same(suit_hand)), suit
    
def straight(hand):
    return consecutive(hand) #recall that this is either false or the bottom card of the straight
    
def trips(hand): #three of a kind
    card_nums = num_same(hand)
    keys = list(card_nums.keys())
    vals = list(card_nums.values())
    if not vals[0] == 3:
        return False
    elif len(vals) > 1 and vals[1] != 1:
        return False
    else:
        card_nums.pop(keys[0])
        order = high_card(card_nums, 2)
        if len(vals) == 2:
            return keys[0], order[:1]
        else:
            return keys[0], order[:2]
        
def two_pair(hand):
    card_nums = num_same(hand)
    keys = list(card_nums.keys())
    vals = list(card_nums.values())
    if len(vals) == 1 or not(vals[0] == 2 and vals[1] == 2):
        return False
    else:
        if len(vals) >= 3 and vals[2] == 2: #possibility of the legendary three pair
            pairs = keys[:3].sort()
            card_nums.pop(pairs[0])
            card_nums.pop(pairs[1])
            if card_nums == {}:
                return pairs[0], pairs[1]
            else:
                return pairs[0], pairs[1], high_card(card_nums, 1)
        else:
            if len(vals) == 2:
                pairs = keys.sort()
                return pairs[0], pairs[1]
            else:
                pairs = keys[:2].sort()
                card_nums.pop(pairs[0])
                card_nums.pop(pairs[1])
                return pairs[0], pairs[1], high_card(card_nums, 1)
                
def pair(hand):
    card_nums = num_same(hand)
    keys = list(card_nums.keys())
    vals = list(card_nums.values())
    if not vals[0] == 2:
        return False
    else:
        if len(vals) != 1 and vals[1] != 1:
            return False
        else:
            card_nums.pop(keys[0])
            return keys[0], high_card(card_nums)
        
"""
The stuff left to do on this algorithm:
    Tidy it up, maybe in a different file?
    Combine these into a ranking method for a hand (in the hand class)
    And then also have something to compare two different hands and say which one wins
"""

