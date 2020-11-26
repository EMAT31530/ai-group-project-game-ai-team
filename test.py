import random as rnd
from ranking import *
from AIclasses import *

"""
#test for straight flush
test_2 = Hand()
test_2.addCard(Card("Spades",4))
test_2.addCard(Card("Hearts",12))
print(test_2)
numsame = num_same(test_2)
numsuit= num_suit(test_2)
print(numsame.keys())
print(numsame.values())
print(numsame)
print(numsuit)
"""

"""
#test for straight flush
for i in range(3):
    card = Card("Spades", i + 2)
    test_2.addCard(card)
for i in range(3, 6):
    card = Card("Spades", i + 2)
    test_2.addCard(card)

test_2.addCard(card)

print(straight_flush(test_2))
"""

"""
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
print(four_of_a_kind(test_3))
"""

"""
#test for full house
test_4 = Hand()
cards = []
cards.append(Card("Spades", 4))
cards.append(Card("Spades", 7))
cards.append(Card("Clubs", 4))
cards.append(Card("Hearts", 4))
cards.append(Card("Diamonds", 7))
cards.append(Card("Clubs", 10))
cards.append(Card("Clubs", 10))
for i in range(7):
    test_4.addCard(cards[i])
print(full_house(test_4))
"""

"""
#test for straight
test_5 = Hand()
for i in range(3):
    card = Card("Spades", i + 2)
    test_5.addCard(card)
for i in range(4, 8):
    card = Card("Spades", i + 2)
    test_5.addCard(card)


print(test_5.cards)
print(straight(test_5))
"""

"""
#test for high_card
print(high_card(num_same(test_5), 7))
"""

"""
#test for flush
print(flush(test_5))
"""

import time
#test for overall ranking function
"""
n = 10000
count = 0.0
for i in range(n):
    test_6 = Hand()
    deck = Deck()
    deck.build()
    for i in range(2):
        test_6.addCard(deck.draw())
    t1 = time.perf_counter()
    test_6.ranking()
    t2 = time.perf_counter()
    count += (t2 - t1)
    #print(str(test_6))
    #print(test_6.ranking())

print(count/n)
#takes an average of 2.2e-05 to 2.6e-05 for each ranking
"""
"""
#debug section
test_7 = Hand()
import numpy as np
cards = []
cards.append(Card("Hearts", 3))
cards.append(Card("Clubs", 3))
cards.append(Card("Diamonds", 13))
cards.append(Card("Spades", 9))
cards.append(Card("Diamonds", 9))
cards.append(Card("Hearts", 10))
cards.append(Card("Diamonds", 8))
for card in cards:
    test_7.addCard(card)
print(two_pair(test_7))
"""

#test for comparison method
import numpy as np
n = 100
a = []
for i in range(n):
    test_8 = Hand()
    deck = Deck()
    deck.build()
    for j in range(7):
        test_8.addCard(deck.draw())
    a.append(test_8)
    if i >= 1:
        print(a[i].ranking())
        print(a[i] > a[i - 1])