"""
File for calculating win probability for hands at flop, river, turn.
Then will group them into lookup tables for use for k means clustering
"""
import random
from math import comb
import pickle


def build_deck():  # To build a deck, can be used to rebuild also
    cards = []
    for suit in range(4):
        for i in range(2, 15):
            cards.append(str(i)+'♥♦♣♠'[suit])
    return cards


# gets all possible preflop hands in a file
def handsget():
    deck = build_deck()
    allhands = []
    for i in range(0, comb(52,2)):
        hand = random.sample(deck, 2)
        handfound = False
        # if hand is not found, add to the list
        while handfound is False:
            hand = random.sample(deck, 2)
            if hand not in allhands:
                allhands.append(hand)
                handfound = True
    # pickle allows easy file read and write
    with open('allhands.txt', 'wb') as fp:
        pickle.dump(allhands, fp)


# gets all flops possible with current hand selected
def flopget():
    deck = build_deck()
    allflops = []
    for i in range(0, comb(52,3)):
        hand = random.sample(deck, 3)
        handfound = False
        while handfound is False:
            hand = random.sample(deck, 3)
            if hand not in allflops:
                allflops.append(hand)
                handfound = True
    with open('allflops.txt', 'wb') as fp:
        pickle.dump(allflops, fp)


# gets all turns possible with current hand selected
# takes approximately 15 minutes
def turnget():
    deck = build_deck()
    allturns = []
    for i in range(0, comb(52,4)):
        hand = random.sample(deck, 4)
        handfound = False
        while handfound is False:
            hand = random.sample(deck, 4)
            if hand not in allturns:
                allturns.append(hand)
                handfound = True
    with open('allturns.txt', 'wb') as fp:
        pickle.dump(allturns, fp)


# gets all  possible with current hand selected
# will take ages 
def riverget():
    deck = build_deck()
    allrivers = []
    for i in range(0, comb(52,5)):
        hand = random.sample(deck, 5)
        handfound = False
        while handfound is False:
            hand = random.sample(deck, 5)
            if hand not in allrivers:
                allrivers.append(hand)
                handfound = True
    with open('allrivers.txt', 'wb') as fp:
        pickle.dump(allrivers, fp)


"""
handsget()
with open ('allhands.txt', 'rb') as fp:
    allhands = pickle.load(fp)
print(allhands)
"""

"""
flopget()
with open ('allflops.txt', 'rb') as fp:
    allflops = pickle.load(fp)
print(allflops)
"""

"""
turnget()
with open ('allturns.txt', 'rb') as fp:
    allturns = pickle.load(fp)
print(allturns)
"""

riverget()
"""
with open ('allrivers.txt', 'rb') as fp:
    allrivers = pickle.load(fp)
print(allrivers)
"""

# on comparison, iterate through all flops and remove any flop that contains either of the cards
