import random as rnd
from ranking import *
from AIclasses import *


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
