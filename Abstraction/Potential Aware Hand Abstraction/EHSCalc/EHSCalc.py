import random
from math import comb
import pickle
import ranking as rank
import copy

with open('allhands.txt', 'rb') as fp:
    totalhands = pickle.load(fp)


with open('allflops.txt', 'rb') as fp:
    totalflops = pickle.load(fp)


with open('allturns.txt', 'rb') as fp:
    totalturns = pickle.load(fp)


with open ('allrivers.txt', 'rb') as fp:
    totalrivers = pickle.load(fp)


def build_deck():  # To build a deck, can be used to rebuild also
    cards = []
    for suit in range(4):
        for i in range(2, 15):
            cards.append(str(i)+'♥♦♣♠'[suit])
    return cards


deck = build_deck()
hand = random.sample(deck, 2)

"""
prune flops, turns, rivers from the current hand


compare current hand versus every other hand and every possible combination of
flop turn and river in those hands

tally wins versus ties? versus draws idk exactly how
store hand pair alongside probability it will win
"""



"""
print(allhands)
currhand = ['5♥', '11♦']
print(currhand)
print(len(allhands))
for x in allhands:
    if currhand[1] in x:
        allhands.remove(x)
        print("true")
    if currhand[0] in x:
        allhands.remove(x)
        print("true")
"""
currhand = ['5♥', '11♦']
prunedhands = [i for i in totalhands if not (currhand[0] in i or currhand[1] in i)]

"""
lst = copy.copy(allhands)
for i in lst[:]:
    for i in lst[:]:
        if currhand[0] in i or currhand[1] in i:
            print(i, currhand[0], currhand[1])
            lst.remove(i)
"""


def pruner(currhand, allhands, allflops, allturns, allrivers):
    # pruning the hands

    prunedhands = [i for i in allhands if not currhand[0] in i or currhand[1] in i]
    prunedflops = [i for i in allflops if not (currhand[0] in i or currhand[1] in i)]
    prunedturns = [i for i in allturns if not (currhand[0] in i or currhand[1] in i)]
    prunedrivers= [i for i in allrivers if not (currhand[0] in i or currhand[1] in i)]

    return(prunedhands, prunedflops, prunedturns, prunedrivers)


# flop winrate tester

# totaltally=0
# win% = (wintally / totaltally)* 100
# discuss possibility of tie? look it up
# floptable= {}
# floptable[currhand] = win%
# CHECK THIS function
def flopper():
    # iterate through each hands
    floptable = {}
    for currhand in totalhands:
        # one loop of this will calculate EHS for 1 hand, 1325 to go
        wintally = 0
        totaltally = 0
        handsdone = []

        # hand to remove, keep track of hands that have been removed before
        for opphand in [x for x in totalhands if x not in handsdone]:
            # list comprehension
            # need to then remove this hand
            handsdone.append(opphand)
            # removes illegal hands, flops, turns, rivers
            current = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)
            final = pruner(opphand, current[0], current[1], current[2], current[3])
            # myrank = rank.ranking(currhand, flop)
            # opprank = rank.ranking(opphand, flop)
            # test tomororw
            for flop in final[1]:
                totaltally += 1
                print(list(currhand))
                print(opphand)
                print(flop)
                myrank = rank.ranking(list(currhand), list(flop))
                opprank = rank.ranking(list(opphand), list(flop))
                # how to deal with ties? figure it out
                if myrank > opprank:
                    wintally += 1
                else:
                    pass
        # need to consider ties
        totalwinrate = (wintally / totaltally) * 100
        floptable[currhand] = totalwinrate
        return floptable

flopper()

"""
# turn function, river function is identical, can make them separate function for ease of use
# FIX THIS
def turner():
    # iterate through each hands
    for currhand in allhands:
        # one loop of this will calculate EHS for 1 hand, 1325 to go
        wintally = 0
        totaltally = 0
        for opphand in allhands\currhand:
            opphand = random.sample(allhands, 1)
            # removes illegal hands, flops, turns, rivers
            final = pruner(opphand, current[0], current[1], current[2], current[3])
            # myrank = rank.ranking(currhand, flop)
            # opprank = rank.ranking(opphand, flop)
            # test tomororw
            for flop in final[1]:
                totaltally += 1
                myrank = rank.ranking(currhand, flop)
                opprank = rank.ranking(opphand, flop)
                # how to deal with ties? figure it out
                if myrank > opprank:
                    wintally += 1
                else:
                    pass
        # need to consider ties
        totalwinrate = (wintally / totaltally) * 100
        floptable[currhand] = totalwinrate


"""









# return a list of lists? hands flop turn river
