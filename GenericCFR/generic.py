from abc import ABC, abstractmethod
import numpy as np
import random
import copy

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
        #next_state = copy.deepcopy(self)

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
        self.expected_game_value = 0

    def reset(self):
        for node in self.nodeMap.values():
            node.strategy_sum = np.zeros(node.n_actions)
        self.expected_game_value = 0

    def train(self, gamestatetype, n_iterations=10000):
        for _ in range(n_iterations):
            if _ == (1000):
                print("Resetting after {} iterations!".format(_))
                self.reset()


            newgamestate = gamestatetype()
            for j in range(2):
                reach_probabilities = np.ones(newgamestate.num_players)
                self.current_player = j
                self.expected_game_value += self.cfr(copy.deepcopy(newgamestate), reach_probabilities)

        self.expected_game_value /= n_iterations

    def cfr(self, gamestate, reach_prs):
        if gamestate.is_terminal():
            reward = gamestate.get_rewards()
            return reward

        active_player = gamestate.get_active_player()
        player_index = gamestate.get_index(active_player)
        opponent = (player_index+1)%2 #ONLY FOR TWO PLAYERS GAMES
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate)
        strategy = node.get_strategy()

        # Counterfactual utility per action.

        if player_index == self.current_player:
            counterfactual_utility  = np.zeros(n_actions)
            reach_pr = reach_prs[player_index]
            node.cumulative_reach_pr += reach_pr
            node.strategy_sum += reach_pr * strategy

            for i, action in enumerate(possible_actions): #WE WANT PRUNING
                next_gamestate = gamestate.handle_action(active_player, action)

                next_reach_prs = reach_prs
                next_reach_prs[player_index] *= strategy[i]

                counterfactual_utility[i] = -1 * self.cfr(next_gamestate, next_reach_prs)

            # Utility of information set.
            util = np.sum(counterfactual_utility * strategy)

            regrets = counterfactual_utility - util
            regrets *= reach_prs[opponent]
            node.cumulative_regrets += regrets

        else:
            action = np.random.choice(possible_actions, p=strategy) #SOME nuance to the choice of action (GREED)
            next_gamestate = gamestate.handle_action(active_player, action)
            util = -1 * self.cfr(next_gamestate, reach_prs)

        return util

    def get_node(self, gamestate):
        key = gamestate.get_representation()
        if key not in self.nodeMap:
            newnode = Node(key, len(gamestate.get_actions()))
            self.nodeMap[key] = newnode
            return newnode
        return self.nodeMap[key]

    def get_final_strategy(self):
        strategy = {}
        for key, node in self.nodeMap:
            nodestategy = node.get_average_strategy_with_threshold(0.01)
            strategy[key] = nodestategy
        return strategy






class Node:
    def __init__(self, key, n_actions):
        self.key = key #REMOVE ONCE TESTED WORKING FOR KUHN
        self.n_actions = n_actions #the number of possible actions taken from said node

        self.cumulative_regrets = np.zeros(self.n_actions) #the sum of the regret at each iteration (for each action)
        self.strategy_sum = np.zeros(self.n_actions) # the sum of the strategy at each iteration (for each action)
        self.cumulative_reach_pr = 0

    def normalise(self, normalisee):
        normaliser = sum(normalisee)
        if normaliser > 0:
            normalisedvalues = normalisee / normaliser
        else:
            normalisedvalues = np.repeat(1.0 / self.n_actions, self.n_actions)
        return normalisedvalues

    def get_strategy(self):
        strategy = np.maximum(0, self.cumulative_regrets)
        return self.normalise(strategy)

    def get_average_strategy(self):
        if self.cumulative_reach_pr==0:
            strategy = self.strategy_sum.copy()
        else:
            strategy = self.strategy_sum.copy() / self.cumulative_reach_pr.copy()
        return self.normalise(strategy)

    def get_average_strategy_with_threshold(self, threshold):
        avg_strategy = self.get_average_strategy()
        avg_strategy[avg_strategy < threshold] = 0
        return self.normalize(avg_strategy)

    #str which works for kuhn idk about others :P
    def __str__(self):
        strategies = ['{:03.2f}'.format(x)
                      for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)
