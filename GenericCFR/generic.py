from abc import ABC, abstractmethod
import numpy as np
import random
import copy
import sys
import time
sys.path.append('../modules')
import validation as vald


class GameState(ABC):
    #To check if the current gamestate is a terminal state
    @abstractmethod
    def is_terminal(self):
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
    def handle_action(self, player, action):
        pass

    #To get the active player from the current state
    @abstractmethod
    def get_active_player(self):
        pass

    #Maps a player to an intager
    @abstractmethod
    def get_index(self, player):
        pass

    #To get the representative key of a given state
    @abstractmethod
    def get_representation(self):
        pass


class MCCFRTrainer:
    def __init__(self):
        self.nodeMap = {} #Will contains all possible nodes
        self.current_player = 0

    def reset(self):
        for node in self.nodeMap.values():
            node.strategy_sum *=0

    def train(self, gamestatetype, n_iterations=10000):
        gamestate = gamestatetype()
        util = 0
        for _ in range(n_iterations):
            util += self.trainingIteration(gamestate)
        return util / n_iterations

    def trainingIteration(self, gamestate):
        gamestate.__init__()
        util = 0
        for j in range(gamestate.num_players):
            reach_probabilities = np.ones(gamestate.num_players)
            self.current_player = j
            util += self.cfr(copy.deepcopy(gamestate), reach_probabilities)
        return util

    def trainWExploitability(self, gamestatetype, n_iterations=50000, n_intervals=100):
        gamestate = gamestatetype()
        exploitability_list = []
        for _ in range(1, n_iterations):
            if _ % n_intervals == 0:
                exploitability_list.append(compute_exploitability(gamestatetype, self.nodeMap)[0])

            self.trainingIteration(gamestate)

        return exploitability_list

    def cfr(self, gamestate, reach_prs):
        if gamestate.is_terminal():
            return gamestate.get_rewards()

        active_player = gamestate.get_active_player()
        player_index = gamestate.get_index(active_player)
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate.get_representation(), n_actions)
        strategy = node.get_strategy()

        # Counterfactual utility per action.

        if player_index == self.current_player:
            counterfactual_utility  = np.zeros(n_actions)
            node.strategy_sum += reach_prs[player_index] * strategy

            for i, action in enumerate(possible_actions): #WE WANT PRUNING
                next_gamestate = gamestate.handle_action(active_player, action)

                next_reach_prs = reach_prs
                next_reach_prs[player_index] *= strategy[i]

                counterfactual_utility[i] = -1 * self.cfr(next_gamestate, next_reach_prs)

            # Utility of information set.
            util = np.sum(counterfactual_utility * strategy)

            for i, action in enumerate(possible_actions):
                cf_reach_prob = self.get_counterfactual_reach_probability(reach_prs, player_index)
                regrets = counterfactual_utility[i]- util
                node.cumulative_regrets[i] += cf_reach_prob * regrets

        else:
            action = np.random.choice(possible_actions, p=strategy) #SOME nuance to the choice of action (GREED)
            next_gamestate = gamestate.handle_action(active_player, action)
            util = -1 * self.cfr(next_gamestate, reach_prs)

        return util

    def get_counterfactual_reach_probability(self, reach_prs, player_index):
        return np.prod(reach_prs[:player_index]) * np.prod(reach_prs[player_index + 1:])

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
        strategy = np.maximum(0, self.cumulative_regrets)
        return self.normalise(strategy)

    def get_average_strategy(self):
        return self.normalise(self.strategy_sum.copy())

    def get_average_strategy_with_threshold(self, threshold):
        avg_strategy = self.get_average_strategy()
        avg_strategy[avg_strategy < threshold] = 0
        return list(self.normalise(avg_strategy))




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
