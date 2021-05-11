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