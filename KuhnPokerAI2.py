from generickuhn import *
import numpy as np
import random as rnd
import validation as vald
#taken from https://github.com/IanSullivan/PokerCFR under MIT license

class AiKuhnBotTrainer2(AiKuhn):
    #Training function
    def train(self, n_iterations=10000):
        expected_game_value = 0
        for _ in range(n_iterations):
            # Regrets reset after half way through
            if _ == n_iterations//2:
                for _, v in self.nodeMap.items():
                    v.strategy_sum = np.zeros(v.n_actions)
                    expected_game_value = 0
            for j in range(2):
                self.current_player = j
                rnd.shuffle(self.deck)
                expected_game_value += self.cfr('', 1, 1, 1)

        expected_game_value /= n_iterations
        display_results(expected_game_value, self.nodeMap)

    #The Counterfactual Regret Minimisation function
    def cfr(self, history, pr_1, pr_2, sample_prob):
        n = len(history)
        player = n % 2
        player_card = self.deck[0] if player == 0 else self.deck[1]

        if is_terminal(history):
            card_player = self.deck[0] if player == 0 else self.deck[1]
            card_opponent = self.deck[1] if player == 0 else self.deck[0]
            reward = roundWinnings(history, card_player, card_opponent)
            return reward

        node = self.get_node(player_card, history, Node2)
        strategy = node.strategy

        # Counterfactual utility per action.
        action_utils = np.zeros(self.n_actions)
        if player == self.current_player:
            if player == 0:
                node.reach_pr += pr_1
            else:
                node.reach_pr += pr_2

            for act in range(self.n_actions):
                p = node.get_p(act)

                if rnd.random() > p:
                    action_utils[act] = 0
                else:
                    next_history = history + node.action_dict[act]
                    if player == 0:
                        action_utils[act] = -1 * self.cfr(next_history, pr_1 * strategy[act], pr_2, sample_prob * p)
                    else:
                        action_utils[act] = -1 * self.cfr(next_history, pr_1, pr_2 * strategy[act], sample_prob * p)
            # Utility of information set.
            util = np.sum(action_utils * strategy)
            regrets = action_utils - util
            regrets = (pr_2 if player == 0 else pr_1) * regrets
            node.regret_sum += regrets
            node.update_strategy()
        else:
            #  second player, no regrets are calculated only one branch is explore, Monte Carlo
            # at random probability take the greedy path other wise explore based on the strategy
            a = node.get_action(strategy)
            next_history = history + node.action_dict[a]
            util = -1 * self.cfr(next_history, pr_1, pr_2, sample_prob)

        return util

class Node2(Node):
    def __init__(self, key, action_dict, n_actions=2):
        Node.__init__(self, key, action_dict, n_actions)
        self.beta = 1000
        self.epsilon = 0.05

    def get_p(self, act):
        if self.reach_pr_sum != 0:
            strategy = self.strategy_sum / self.reach_pr_sum
        else:
            strategy = self.strategy_sum

        normalising_sum = np.sum(strategy)
        if normalising_sum > 0:
            strategy = (self.beta + strategy) / (self.beta + normalising_sum)
        else:
            strategy = np.repeat((1 + self.beta) / (self.beta + self.n_actions), self.n_actions)
        return max(strategy[act], self.epsilon)

    def get_action(self, strategy):
        return np.random.choice(self.possible_actions, p=strategy)
