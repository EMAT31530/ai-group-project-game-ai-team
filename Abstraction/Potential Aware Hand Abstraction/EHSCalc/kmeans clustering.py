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
    unserialized_data = pickle.load(handle)
prefloplist = sorted(list(unserialized_data.values()))

with open('floptable.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)
floplist = sorted(list(unserialized_data.values()))

with open('turntable.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)
turnlist = sorted(list(unserialized_data.values()))

with open('rivertable.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)
riverlist = sorted(list(unserialized_data.values()))


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


print(preflopclusters)
print(flopclusters)
print(turnclusters)
print(riverclusters)

"""
TO DO

need a function to look up hands, get the ehs, then find the closest cluster to it
should be very easy, job for tomorrow maybe

"""
