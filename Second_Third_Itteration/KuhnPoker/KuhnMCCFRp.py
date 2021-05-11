import time
import sys
from KuhnModules import *
from KuhnVCFR import AIKuhn, Node
sys.path.append('../modules')
from validation import exportJson
#taken from https://github.com/IanSullivan/PokerCFR under MIT license


class AIKuhn2(AIKuhn):
    #Training function
    def train(self, n_iterations=10000):
        for _ in range(n_iterations):
            # Regrets reset after half way through
            if _ == n_iterations//2:
                for _, v in self.nodeMap.items():
                    v.strategy_sum = np.zeros(v.n_actions)
                    self.expected_game_value = 0
            for j in range(2):
                self.current_player = j
                rnd.shuffle(self.deck)
                self.expected_game_value += self.cfr('', 1, 1, 1)

        self.expected_game_value /= n_iterations

    #The Counterfactual Regret Minimisation function
    def cfr(self, history, pr_1, pr_2, sample_prob):
        n = len(history)
        player = n % 2
        player_card = self.deck[0] if player == 0 else self.deck[1]

        if is_terminal(history):
            card_player = self.deck[0] if player == 0 else self.deck[1]
            card_opponent = self.deck[1] if player == 0 else self.deck[0]
            reward = get_reward(history, card_player, card_opponent)
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
    def __init__(self, key, action_dict):
        Node.__init__(self, key, action_dict)
        self.possible_actions = [x for x in action_dict]
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 10000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = AIKuhn2()
    trainer.train(n_iterations=iterations)
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(sys.getsizeof(trainer)))

    display_results(trainer.expected_game_value, trainer.nodeMap)

    if len(sys.argv) > 2:
        filename = str(sys.argv[2]).lower()
        exportJson(trainer.get_final_strategy(), filename)
        print('Exported trained strategy as {}.json '.format(filename))
