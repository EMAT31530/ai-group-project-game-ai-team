import random as rnd
from ranking import *
from AIclasses import *
from KuhnPokerAI import *
from KuhnPokerAI2 import *
import time
import validation as vald
from statistics import *

#test for kuhn pokerai
'''
time1 = time.time()
trainer1 = AiKuhnBotTrainer()
trainer2 = AiKuhnBotTrainer2()
iterations = 10000
#trainer1.train(n_iterations=iterations)
trainer1.trainWcomparison(['passDummy','betDummy','defaultkuhn'],n_iterations=30000, n_intervals=10)
print('time ellapsed for {} iterations: '.format(iterations) + str(abs(time1 - time.time())))
'''
'''
time2 = time.time()
trainer2.train(n_iterations=iterations)
print('time ellapsed for {} iterations: '.format(iterations) + str(abs(time2 - time.time())))
'''
graphing(vald.importJson('winr8_30000_3'))

'''
strat = trainer.get_aistrategy()
print(strat)
vald.exportJson(strat,'AI1')
'''
#game = Game()


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
n = 10000
count = 0.0
for i in range(n):
    pocket_cards = Hand()
    board = Hand()
    deck = Deck()
    deck.build()
    for i in range(2):
        pocket_cards.addCard(deck.draw())
    t1 = time.perf_counter()
    pocket_cards.rankupd([])
    for i in range(5):
        board.addCard(deck.draw())
        #board.same_update()
        #board.suit_update()
        #pocket_cards
        pocket_cards.rankupd(board.cards)
    t2 = time.perf_counter()
    #print(pocket_cards.rank)
    #print(pocket_cards.num_suit)
    #print(str(pocket_cards))
    #print(str(board))
    #print(pocket_cards.rank)
    count += t2 - t1
print(count/n)
"""
#takes about 8.3e-05 secs to update the ranking over the course of the hand (kinda)

#running through the game a few times for testing
#game = Game(1)
#game.start()
