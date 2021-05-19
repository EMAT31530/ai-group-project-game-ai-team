import random
import pickle
import numpy as np
import statistics
from sklearn.cluster import KMeans


"""
abstraction
work out clusters, choose a number of them
work out strategies for clusters


then for each hand searched at each stage
find which cluster it is closest too
then use that strategy
abstraction done
"""

# loading all EHS tables
with open('prefloptable.pickle', 'rb') as handle:
    preflopdict = pickle.load(handle)
prefloplist = sorted(list(preflopdict.values()))

with open('floptable.pickle', 'rb') as handle:
    flopdict = pickle.load(handle)
floplist = sorted(list(flopdict.values()))

with open('turntable.pickle', 'rb') as handle:
    turndict = pickle.load(handle)
turnlist = sorted(list(turndict.values()))

with open('rivertable.pickle', 'rb') as handle:
    riverdict = pickle.load(handle)
riverlist = sorted(list(riverdict.values()))


# ehs list is sorted list of ehs, n is number of clusters
def clustergetter(ehslist, n):
    data = np.array(ehslist)
    clusterlist = KMeans(n_clusters=n).fit(data.reshape(-1, 1))
    clusterlist.predict(data.reshape(-1,1))
    clusters = []
    for i in sorted(clusterlist.cluster_centers_):
        clusters.append(i[0])
    return(clusters)


# clustering preflop, flop, turn, river EHS values
preflopclusters = clustergetter(prefloplist, 10)
flopclusters = clustergetter(floplist, 10)
turnclusters = clustergetter(turnlist, 10)
riverclusters = clustergetter(riverlist, 10)

clusterlists = [preflopclusters, flopclusters, turnclusters, riverclusters]
"""
function that takes in the stage and a given hand, returns the closest cluster
to the hands ehs value at certain stage
gamestage 0 preflop 1 flop 2 turn 3 river
"""


# inefficient, can make better another time
def get_repr(hand, gamestage):
    # btec cluster list saving, can do it nicely a different time
    labelledclusters = {}
    if gamestage == 0:
        with open('prefloptable.pickle', 'rb') as handle:
            preflopdict = pickle.load(handle)
        key_list = list(preflopdict.keys())
        val_list = list(preflopdict.values())
        # labels clusters
        for i in clusterlists[0]:
            closest = min(val_list, key=lambda x: abs(x-i))
            labelledclusters[i] = key_list[val_list.index(closest)]

        ehs = preflopdict[hand]
        closestcluster = min(clusterlists[0], key=lambda x: abs(x-ehs))
        return labelledclusters[closestcluster]

    elif gamestage == 1:
        with open('floptable.pickle', 'rb') as handle:
            flopdict = pickle.load(handle)
        key_list = list(flopdict.keys())
        val_list = list(flopdict.values())
        # labels clusters
        for i in clusterlists[1]:
            closest = min(val_list, key=lambda x: abs(x-i))
            labelledclusters[i] = key_list[val_list.index(closest)]

        ehs = flopdict[hand]
        closestcluster = min(clusterlists[1], key=lambda x: abs(x-ehs))
        return labelledclusters[closestcluster]

    elif gamestage == 2:
        with open('turntable.pickle', 'rb') as handle:
            turndict = pickle.load(handle)
        key_list = list(turndict.keys())
        val_list = list(turndict.values())
        # labels clusters
        for i in clusterlists[2]:
            closest = min(val_list, key=lambda x: abs(x-i))
            labelledclusters[i] = key_list[val_list.index(closest)]

        ehs = turndict[hand]
        closestcluster = min(clusterlists[2], key=lambda x: abs(x-ehs))
        return labelledclusters[closestcluster]

    elif gamestage == 3:
        with open('rivertable.pickle', 'rb') as handle:
            riverdict = pickle.load(handle)
        key_list = list(riverdict.keys())
        val_list = list(riverdict.values())
        # labels clusters
        for i in clusterlists[3]:
            closest = min(val_list, key=lambda x: abs(x-i))
            labelledclusters[i] = key_list[val_list.index(closest)]

        ehs = riverdict[hand]
        closestcluster = min(clusterlists[3], key=lambda x: abs(x-ehs))
        return labelledclusters[closestcluster]

# print(get_repr(('11♥', '13♦'), 1))
