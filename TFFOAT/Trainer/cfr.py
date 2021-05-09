from gamestate import GameState
from node import Node
import numpy as np
import random
import itertools
import copy
import sys
import time
#sys.path.append('../modules')
#import validation as vald


# Vanilla, scalar-form/Simultaneous updates, no sampling
# Optional Weighting of max(t - d, 0)
class VCFRTrainer: 
    #can be perfect after 20000 iterations
    def __init__(self, gamestatetype):
        self.nodeMap = {} #Will contains all possible decision nodes
        self.gamestate = gamestatetype()

    def train(self, n_iterations=10000, weighting=False, d=1000):
        utility = 0
        for t in range(n_iterations):
            w = 1 if not weighting else max(t - d, 0)
            utility += self.cfr(copy.deepcopy(self.gamestate), 1, 1, w)
        return utility / n_iterations

    def cfr(self, gamestate, rp_1, rp_2, w):
        if gamestate.is_terminal(): #terminal node
            return gamestate.get_rewards() 

        utility = 0
        if gamestate.is_chance() == 'pr': #private chance node
            chance_outcomes = gamestate.get_private_chanceoutcomes()
            for outcome in chance_outcomes:
                next_gamestate = gamestate.handle_private_chance(outcome)
                utility += self.cfr(next_gamestate, rp_1, rp_2, w) * (1.0/ len(chance_outcomes))
            return utility
        elif gamestate.is_chance() == 'pu': #public chance node
            chance_outcomes = gamestate.get_public_chanceoutcomes()
            for outcome in chance_outcomes:
                next_gamestate = gamestate.handle_public_chance(outcome)
                utility += self.cfr(next_gamestate, rp_1, rp_2, w) * (1.0/ len(chance_outcomes))
            return utility


        player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate.get_representation(), n_actions)
        strategy = node.get_strategy()

        counterfactual_utility  = np.zeros(n_actions) # Counterfactual utility per action
        for ia, action in enumerate(possible_actions):
            next_gamestate = gamestate.handle_action(action)
            if player == 0:
                counterfactual_utility[ia] = -1 * self.cfr(next_gamestate, rp_1 * strategy[ia], rp_2, w)
            else:
                counterfactual_utility[ia] = -1 * self.cfr(next_gamestate, rp_1, rp_2 * strategy[ia], w)

        utility = sum(counterfactual_utility * strategy)
        regrets = counterfactual_utility - utility
        #regrets[regrets < 0] = 0 #negative regret removed (regret like values)
        if player == 0:
            node.cumulative_regrets += regrets * rp_2
            node.strategy_sum += rp_1 * strategy 
        else:
            node.cumulative_regrets += regrets * rp_1
            node.strategy_sum += rp_2 * strategy 
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
            nodestategy = node.get_average_strategy_with_threshold(0.01)
            strategy[key] = nodestategy
        return strategy


#[):not:(]CFR+, scalar-form/alternating updates, no sampling
#includes: weighting the stored strategy by max(t - d, 0), t = timestep, d a constant
#          regret matching plus (negative regret not stored)
class CFRPlusTrainer(VCFRTrainer):
    def __init__(self, gamestatetype):
        VCFRTrainer.__init__(self, gamestatetype)
        self.current_player = 0

    def train(self, n_iterations=10000, d=1000):
        utility = np.zeros(2)
        for t in range(n_iterations):
            for j in range(2): #alternating updates
                self.current_player = j
                utility[j] += self.cfr(copy.deepcopy(self.gamestate), 1, 1, max(t - d, 0))
        return utility / n_iterations

    def cfr(self, gamestate, rp_1, rp_2, w):
        if gamestate.is_terminal(): #terminal node
            return gamestate.get_rewards() 
        utility = 0
        if gamestate.is_chance() == 'pr': #private chance node
            chance_outcomes = gamestate.get_private_chanceoutcomes()
            outcome = np.random.choice(chance_outcomes, p=np.repeat((1.0/ len(chance_outcomes)),len(chance_outcomes)))
            next_gamestate = gamestate.handle_private_chance(outcome)
            return self.cfr(next_gamestate, rp_1, rp_2, w)
        elif gamestate.is_chance() == 'pu': #public chance node
            chance_outcomes = gamestate.get_public_chanceoutcomes()
            for outcome in chance_outcomes:
                next_gamestate = gamestate.handle_public_chance(outcome)
                utility += self.cfr(next_gamestate, rp_1, rp_2, w) * (1.0/ len(chance_outcomes))
            return utility

        player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate.get_representation(), n_actions)
        strategy = node.get_strategy()

        counterfactual_utility  = np.zeros(n_actions) # Counterfactual utility per action
        if player == self.current_player:
            for ia, action in enumerate(possible_actions):
                next_gamestate = gamestate.handle_action(action)
                counterfactual_utility[ia] = -self.cfr(next_gamestate, rp_1 * strategy[ia], rp_2, w) # M arrow
            utility = sum(counterfactual_utility * strategy)
            regrets = counterfactual_utility - utility 
            regrets[regrets < 0] = 0 #cfr+ negative regret removed
            if player == 0:
                node.cumulative_regrets += regrets * rp_2
                node.strategy_sum += rp_1 * strategy * w
            else:
                node.cumulative_regrets += regrets * rp_1
                node.strategy_sum += rp_2 * strategy * w
        else:
            for ia, action in enumerate(possible_actions):
                next_gamestate = gamestate.handle_action(action)
                counterfactual_utility[ia] = -self.cfr(next_gamestate, rp_1, rp_2 * strategy[ia], w) # M arrow
            utility = sum(counterfactual_utility * strategy)

        return utility




class PCSCFRPlusTrainer(VCFRTrainer):
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
