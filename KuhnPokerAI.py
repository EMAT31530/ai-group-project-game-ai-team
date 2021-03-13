import numpy as np
import random as rnd
import validation as vald
from generickuhn import *
#taken from https://github.com/IanSullivan/PokerCFR under MIT license

class AiKuhnBotTrainer(AiKuhn):
    #Training function
    def train(self, n_iterations=50000):
        expected_game_value = 0
        for _ in range(n_iterations):
            rnd.shuffle(self.deck)
            expected_game_value += self.cfr('', 1, 1)
            for _, v in self.nodeMap.items():
                v.update_strategy()

        expected_game_value /= n_iterations
        display_results(expected_game_value, self.nodeMap)

    def trainWcomparison(self, dummyai, n_iterations=50000, n_intervals=1000):
        for _ in range(n_iterations):
            if _ % n_intervals == 0:
                cur_aistrat = self.get_aistrategy()
                if _ == 0:
                    cur_aistrat = vald.importJson('defaultkuhn')

                cur_winrate = list(np.zeros(len(dummyai)))

                for j in range(len(dummyai)):
                    winstatistics = self.play_vs_dummy(cur_aistrat, dummyai[j])
                    cur_winrate[j] = winstatistics
                self.winrate[_] = cur_winrate

            rnd.shuffle(self.deck)
            self.cfr('', 1, 1)
            for _, v in self.nodeMap.items():
                v.update_strategy()
        vald.exportJson(self.winrate, 'winr8_{}_3'.format(n_iterations))

    #The Counterfactual Regret Minimisation function
    def cfr(self, history, pr_1, pr_2):
        n = len(history)
        is_player_1 = n % 2 == 0
        player_card = self.deck[0] if is_player_1 else self.deck[1]

        if is_terminal(history):
            card_player = self.deck[0] if is_player_1 else self.deck[1]
            card_opponent = self.deck[1] if is_player_1 else self.deck[0]
            reward = roundWinnings(history, card_player, card_opponent)
            return reward

        node = self.get_node(player_card, history, Node)
        strategy = node.strategy

        # Counterfactual utility per action.
        action_utils = np.zeros(self.n_actions)

        for act in range(self.n_actions):
            next_history = history + node.action_dict[act]
            if is_player_1:
                action_utils[act] = -1 * self.cfr(next_history, pr_1 * strategy[act], pr_2)
            else:
                action_utils[act] = -1 * self.cfr(next_history, pr_1, pr_2 * strategy[act])

        # Utility of information set.
        util = sum(action_utils * strategy)
        regrets = action_utils - util
        if is_player_1:
            node.reach_pr += pr_1
            node.regret_sum += pr_2 * regrets
        else:
            node.reach_pr += pr_2
            node.regret_sum += pr_1 * regrets

        return util
