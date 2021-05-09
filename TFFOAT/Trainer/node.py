import numpy as np

class Node:
    def __init__(self, n_actions):
        self.cumulative_regrets = np.zeros(n_actions) #the sum of the regret at each iteration (for each action)
        self.strategy_sum = np.zeros(n_actions) # the sum of the strategy at each iteration (for each action)

    def normalise(self, normalisee):
        normaliser = sum(normalisee)
        if normaliser > 0:
            normalisedvalues = normalisee / normaliser
        else:
            normalisedvalues = np.repeat(1.0 / len(normalisee), len(normalisee))
        return normalisedvalues

    def get_strategy(self):
        regrets = self.cumulative_regrets.copy()
        regrets[regrets < 0] = 0
        return self.normalise(regrets)

    def get_average_strategy(self):
        return self.normalise(self.strategy_sum.copy())

    def get_average_strategy_with_threshold(self, threshold):
        avg_strategy = self.get_average_strategy().copy()
        avg_strategy[avg_strategy < threshold] = 0
        return list(self.normalise(avg_strategy))


    #  Takes in the action played at the node, and returns the likelihood it will be explored.
    #  Epsilon is the minimum possible percentage that the action will be taken.  Epsilon is 0.05 or 5% here.  So at the very least the information set will seen
    #  5% of the time
    #  Beta is a normalizing hyperparam to make sure that early in the training cycle actions are still explored.  Beta is 1000 here.  So for example if the values
    #  are 0 out of ten, instead of given an answer of 0 in the early iterations it will return a value of .99 or { (0 + beta)/10 + beta), (1000/1010) }.  Later in the
    #  training beta should become negligable, example would be 60000/80000 = 0.75, with beta is would be 61000/81000 = 0.753.  The beta param has little impact on the
    #  final answer at the end of training
    def get_pruning_prob(self, i):
        beta = 1000
        epsilon = 0.5
        normalizing_sum = np.sum(self.strategy_sum)
        if normalizing_sum > 0:
            strategy = (beta + strategy) / (beta + normalizing_sum)
        else:
            strategy = np.repeat((1 + beta) / (beta + len(self.strategy_sum)), len(self.strategy_sum))
        return max(strategy[i], epsilon)