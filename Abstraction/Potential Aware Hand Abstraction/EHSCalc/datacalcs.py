"""
File for calculating win probability for hands at flop, river, turn.
Then will group them into lookup tables for use for k means clustering
"""
import random
from math import comb
import pickle
import itertools

def build_deck():  # To build a deck, can be used to rebuild also
    cards = []
    for suit in range(4):
        for i in range(10, 15):
            cards.append(str(i)+'♥♦♣♠'[suit])
    return cards


# gets all possible preflop hands in a file
def handsget():
    deck = build_deck()
    allhands  =list(itertools.combinations(deck, 2))
    # pickle allows easy file read and write
    with open('allhands.txt', 'wb') as fp:
        pickle.dump(allhands, fp)


# gets all flops possible with current hand selected
def flopget():
    deck = build_deck()
    allflops = list(itertools.combinations(deck, 3))
    with open('allflops.txt', 'wb') as fp:
        pickle.dump(allflops, fp)


# gets all turns possible with current hand selected
# takes approximately 15 minutes
def turnget():
    deck = build_deck()
    allturns = list(itertools.combinations(deck, 4))

    with open('allturns.txt', 'wb') as fp:
        pickle.dump(allturns, fp)


# gets all  possible with current hand selected
# will take ages
def riverget():
    deck = build_deck()
    allrivers = list(itertools.combinations(deck, 5))
    with open('allrivers.txt', 'wb') as fp:
        pickle.dump(allrivers, fp)


handsget()

with open('allhands.txt', 'rb') as fp:
    allhands = pickle.load(fp)
# print(allhands)


flopget()
with open('allflops.txt', 'rb') as fp:
    allflops = pickle.load(fp)
# print(allflops)


turnget()
with open('allturns.txt', 'rb') as fp:
    allturns = pickle.load(fp)
# print(allturns)

riverget()

with open('allrivers.txt', 'rb') as fp:
    allrivers = pickle.load(fp)
print(len(allhands))
# on comparison, iterate through all flops and remove any flop that contains either of the cards
