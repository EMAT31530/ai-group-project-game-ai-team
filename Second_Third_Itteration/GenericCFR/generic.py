from abc import ABC, abstractmethod
import numpy as np
import random
import itertools
import copy
import sys
import time
#sys.path.append('../modules')
#import validation as vald

class GameState(ABC):
    #To initate a new gamestate
    @abstractmethod
    def initiate_round(self):
        pass

    #To check if the current gamestate is a terminal state
    @abstractmethod
    def is_terminal(self):
        pass

    #To check if the current gamestate is a chance state (i.e card draw)
    @abstractmethod
    def is_chance(self):
        pass

    #To get the payoff from a terminal state
    @abstractmethod
    def get_rewards(self):
        pass

    #To get the possible actions of said player from the current state
    @abstractmethod
    def get_actions(self, player):
        pass

    #To translate from the current state to a new state via the given action
    @abstractmethod
    def handle_action(self, action):
        pass

    #To translate from the current chance state to a new state
    @abstractmethod
    def sample_public_chance(self):
        pass

    #To get the active player from the current state
    @abstractmethod
    def get_active_player_index(self):
        pass

    #To get the representative key of a given state
    @abstractmethod
    def get_representation(self):
        pass

'''
    def trainWExploitability(self, gamestatetype, n_iterations=50000, n_intervals=100, d=250):
        gamestate = gamestatetype()
        exploitability_list = []
        for _ in range(1, n_iterations):
            if _ % n_intervals == 0:
                exploitability_list.append(compute_exploitability(gamestatetype, self.nodeMap)[0])

            self.trainingIteration(gamestate, d)

        return exploitability_list
'''

class PCSCFRPlusTrainer:
    def __init__(self):
        self.nodeMap = {} #Will contains all possible nodes
        self.current_player = 0

    def train(self, gamestatetype, n_iterations=10000, d=250):
        gamestate = gamestatetype()
        util = 0
        for t in range(n_iterations):
            gamestate.initiate_round()
            for j in range(2): #cfr+
                self.current_player = j
                util += self.cfr(copy.deepcopy(gamestate), 1, 1, max(t - d, 0))
        return util / (2*n_iterations)

    def cfr(self, gamestate, rp_1, rp_2, weighting):
        if gamestate.is_terminal():
            return gamestate.get_rewards()  #they incoperate reach reach_probabilities here?

        
        if gamestate.is_chance() == 'P': #monte carlo Chance Sampling
            next_gamestate = gamestate.sample_public_chance()
            return self.cfr(next_gamestate, rp_1, rp_2, weighting)
        
        player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate.get_representation(), n_actions)
        strategy = node.get_strategy()

        utility  = np.zeros(n_actions) # utility per action

        for ia, action in enumerate(possible_actions):
            if player == self.current_player:
                #Pruning minimal regret nodes
                p = node.get_pruning_prob(ia)
                random.random()
                if random.random() > p:
                    utility[ia] = 0
                else:
                    counterfactual_utility  = np.zeros(n_actions) # Counterfactual utility per action
                    next_gamestate = gamestate.handle_action(action)
                    counterfactual_utility[ia] = -1 * self.cfr(next_gamestate, rp_1 * strategy[ia], rp_2, weighting) # M arrow
                    utility[ia] = counterfactual_utility[ia] * strategy[ia]
            else:
                #regret not calculated for opponent
                next_gamestate = gamestate.handle_action(action)
                utility[ia] = -1 * self.cfr(next_gamestate, rp_1, rp_2 * strategy[ia], weighting) # M arrow

        if player == self.current_player:
            for ia, action in enumerate(possible_actions):
                #cfr+ negative regret ignored
                regrets = max(counterfactual_utility[ia] - utility[ia], 0) 
                node.cumulative_regrets[ia] += regrets * rp_2
                #cfr+ weighting later iterations
                node.strategy_sum[ia] += rp_1 * strategy[ia] * weighting 

        return utility

    def get_node(self, key, n_actions):
        if key not in self.nodeMap:
            newnode = Node(n_actions)
            self.nodeMap[key] = newnode
            return newnode
        return self.nodeMap[key]

    def get_final_strategy(self):
        strategy = {}
        for key, node in self.nodeMap.items():
            nodestategy = node.get_average_strategy_with_threshold(0.001)
            strategy[key] = nodestategy
        return strategy


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
        return self.normalise(self.cumulative_regrets)

    def get_average_strategy(self):
        return self.normalise(self.strategy_sum.copy())

    def get_average_strategy_with_threshold(self, threshold):
        avg_strategy = self.get_average_strategy()
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



def display_results(ev, node_map):
    print('\nplayer 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))
    print('\nplayer 1 strategies:')
    sorted_items = sorted(node_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))
    print('\nplayer 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))
