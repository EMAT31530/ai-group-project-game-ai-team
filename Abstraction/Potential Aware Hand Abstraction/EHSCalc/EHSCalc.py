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


with open('allrivers.txt', 'rb') as fp:
    totalrivers = pickle.load(fp)

# royal version of texas
def build_deck():  # To build a deck, can be used to rebuild also
    cards = []
    for suit in range(4):
        for i in range(10, 15):
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
    prunedrivers = [i for i in allrivers if not (currhand[0] in i or currhand[1] in i)]

    return(prunedhands, prunedflops, prunedturns, prunedrivers)


# flop winrate tester

# totaltally=0
# win% = (wintally / totaltally)* 100
# discuss possibility of tie? look it up
# floptable= {}
# floptable[currhand] = win%
# CHECK THIS function


def prefloptable():
    # iterate through each hands
    prefloptable = {}
    counter = 0
    for currhand in totalhands:
        counter += 1
        # one loop of this will calculate EHS for 1 hand, 1325 to go
        wintally = 0
        totaltally = 0
        handsdone = []
        handsdone.append(currhand)
        prunedhands = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)[0]
        # hand to remove, keep track of hands that have been removed before
        for opphand in [x for x in prunedhands if x not in handsdone]:
            # list comprehension
            # need to then remove this hand
            handsdone.append(opphand)
            totaltally += 1
            myrank = rank.ranking(list(currhand), [])
            opprank = rank.ranking(list(opphand), [])
            # how to deal with ties? figure it out
            if myrank > opprank:
                wintally += 1
            else:
                pass
        # need to consider ties
        totalwinrate = (wintally / totaltally) * 100
        prefloptable[currhand] = totalwinrate

    # Store data (serialize)
    with open('prefloptable.pickle', 'wb') as handle:
        pickle.dump(prefloptable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return prefloptable


"""
prefloptable()
# Load data (deserialize)
with open('prefloptable.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)

print(unserialized_data[('12♠', '14♠')])
"""


# time taken = ??
def floptable():
    # iterate through each hands
    floptable = {}
    counter = 0
    for currhand in totalhands:
        counter += 1
        # one loop of this will calculate EHS for 1 hand, 1325 to go
        wintally = 0
        totaltally = 0
        handsdone = []
        handsdone.append(currhand)
        prunedhands = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)[0]
        # hand to remove, keep track of hands that have been removed before
        for opphand in [x for x in prunedhands if x not in handsdone]:
            # need to then remove this hand
            handsdone.append(opphand)
            # removes illegal hands, flops, turns, rivers
            current = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)
            final = pruner(opphand, current[0], current[1], current[2], current[3])
            # checking every flop for each hand
            for flop in final[1]:
                totaltally += 1
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
        print(totalwinrate)
        print(counter)

    # Store data (serialize)
    with open('floptable.pickle', 'wb') as handle:
        pickle.dump(floptable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return floptable


"""
# Load data (deserialize)
with open('floptable.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)

print(unserialized_data)

"""
def turntable():
    # iterate through each hands
    turntable = {}
    counter = 0
    for currhand in totalhands:
        counter += 1
        # one loop of this will calculate EHS for 1 hand, 1325 to go
        wintally = 0
        totaltally = 0
        handsdone = []
        handsdone.append(currhand)
        prunedhands = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)[0]
        # hand to remove, keep track of hands that have been removed before
        for opphand in [x for x in prunedhands if x not in handsdone]:
            # need to then remove this hand
            handsdone.append(opphand)
            # removes illegal hands, flops, turns, rivers
            current = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)
            final = pruner(opphand, current[0], current[1], current[2], current[3])
            for flop in final[2]:
                totaltally += 1
                myrank = rank.ranking(list(currhand), list(flop))
                opprank = rank.ranking(list(opphand), list(flop))
                # how to deal with ties? figure it out
                if myrank > opprank:
                    wintally += 1
                else:
                    pass

        # need to consider ties
        totalwinrate = (wintally / totaltally) * 100
        turntable[currhand] = totalwinrate
        print(totalwinrate)
        print(counter)

    # Store data (serialize)
    with open('turntable.pickle', 'wb') as handle:
        pickle.dump(turntable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return turntable




def rivertable():
    # iterate through each hands
    rivertable = {}
    counter = 0
    for currhand in totalhands:
        counter += 1
        # one loop of this will calculate EHS for 1 hand, 1325 to go
        wintally = 0
        totaltally = 0
        handsdone = []
        handsdone.append(currhand)
        prunedhands = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)[0]
        # hand to remove, keep track of hands that have been removed before
        for opphand in [x for x in prunedhands if x not in handsdone]:
            # need to then remove this hand
            handsdone.append(opphand)
            # removes illegal hands, flops, turns, rivers
            current = pruner(currhand, totalhands, totalflops, totalturns, totalrivers)
            final = pruner(opphand, current[0], current[1], current[2], current[3])
            for flop in final[3]:
                totaltally += 1
                myrank = rank.ranking(list(currhand), list(flop))
                opprank = rank.ranking(list(opphand), list(flop))
                # how to deal with ties? figure it out
                if myrank > opprank:
                    wintally += 1
                else:
                    pass

        # need to consider ties
        totalwinrate = (wintally / totaltally) * 100
        rivertable[currhand] = totalwinrate
        print(totalwinrate)
        print(counter)

    # Store data (serialize)
    with open('rivertable.pickle', 'wb') as handle:
        pickle.dump(rivertable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return rivertable

rivertable()
"""
pseudocode for flop?

combine all hands and flop combinations


for hand in allhands:
    handflopdict={}
    handflopdict[hand]=[]
    for flops in allflops:
        handflopdict[hand].append(hand+flop)




wineratelist = np.zeros(self.number_of_hands)




        def sort_by_ranking(hands):
            g = lambda hand: [hand[0], self.get_rank(hand[1]), hand[1]]
            ranking_list = list(map(g, hands))
            return list(sorted(ranking_list, key=itemgetter(0)))

        ranks_tuple = sort_by_ranking(list(enumerate(hands)))


        winsum = 0
        j = 0

        for index, rank, hand in ranks_tuple:

            while gamestate.ranks_tuple[j][0] < rank: #rank of opp hand

                winsum += 1
                j += 1

            wineratelist[index] += winsum



        losesum = 0
        j = len(ranks_tuple) - 1
        reversed_tuple = ranks_tuple.copy()
        reversed_tuple.reverse()
        for index, rank, hand in reversed_tuple:
            while ranks_tuple[j][1] > rank:
                losesum += 1
                j -= 1

            wineratelist[index] -= losesum


        return winratelist
"""
