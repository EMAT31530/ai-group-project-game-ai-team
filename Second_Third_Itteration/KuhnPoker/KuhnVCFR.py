import time
import sys
from KuhnModules import *
sys.path.append('../modules')
from validation import exportJson
#taken from https://github.com/IanSullivan/PokerCFR under MIT license


class AIKuhn:
    def __init__(self):
        self.nodeMap = {} #Will contains all possible nodes
        self.action_dict = {0: 'p', 1: 'b'}
        self.expected_game_value = 0
        self.current_player = 0
        self.deck = np.array([0, 1, 2]) #three card kuhn poker deck
        self.n_actions = 2 #number of possible actions (pass, bet)

    def train(self, n_iterations=50000):
        self.expected_game_value = 0
        for _ in range(n_iterations):
            rnd.shuffle(self.deck)
            self.expected_game_value += self.cfr('', 1, 1)
            for _, v in self.nodeMap.items():
                v.update_strategy()

        self.expected_game_value /= n_iterations

    def cfr(self, history, pr_1, pr_2):
        n = len(history)
        is_player_1 = n % 2 == 0
        player_card = self.deck[0] if is_player_1 else self.deck[1]

        if is_terminal(history):
            card_player = self.deck[0] if is_player_1 else self.deck[1]
            card_opponent = self.deck[1] if is_player_1 else self.deck[0]
            reward = get_reward(history, card_player, card_opponent)
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

    def compose_key(self, card, history):
        key = str(card) + " " + history
        return key

    def get_node(self, card, history, Node):
        key = self.compose_key(card, history)
        if key not in self.nodeMap:
            newnode = Node(key, self.action_dict)
            self.nodeMap[key] = newnode
            return newnode
        return self.nodeMap[key]

    def get_final_strategy(self):
        strategy = {}
        for x in self.nodeMap:
            strategy[x] = self.nodeMap[x].get_average_strategy()
        return strategy

class Node:
    def __init__(self, key, action_dict):
        self.key = key #the label of  the node in the form: [cards previous actions]
        self.action_dict = action_dict #dictionary to label each action
        self.n_actions = len(action_dict) #the number of possible actions taken from said node

        self.regret_sum = np.zeros(self.n_actions) #the sum of the regret at each iteration (for each action)
        self.strategy_sum = np.zeros(self.n_actions) # the sum of the strategy at each iteration (for each action)

        #the strategy(probability of choosing each action) from each node, updated for each iteration
        self.strategy = np.repeat(1/self.n_actions, self.n_actions) #initially, equal probability of each action occuring

        self.reach_pr = 0 #probablity of reaching said node (based on the strategy of previous nodes) for an individual iteration
        self.reach_pr_sum = 0 #the sum over all iterations

    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy
        self.reach_pr_sum += self.reach_pr
        self.strategy = self.get_strategy()
        self.reach_pr = 0

    def normalise(self, strategy):
            if sum(strategy) > 0:
                strategy /= sum(strategy)
            else:
                strategy = np.repeat(1/self.n_actions, self.n_actions)
            return strategy

    def get_strategy(self):
        regrets = self.regret_sum
        regrets[regrets < 0] = 0
        normalising_sum = sum(regrets)
        if normalising_sum > 0:
            return regrets / normalising_sum
        else:
            return np.repeat(1/self.n_actions, self.n_actions)

    def get_average_strategy(self):
        strategy = self.strategy_sum / self.reach_pr_sum
        total = sum(strategy)
        strategy /= total
        return list(strategy)

    def __str__(self):
        strategies = ['{:03.2f}'.format(x)
                      for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 100000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = AIKuhn()
    trainer.train(n_iterations=iterations)
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(sys.getsizeof(trainer)))

    display_results(trainer.expected_game_value, trainer.nodeMap)

    if len(sys.argv) > 2:
        filename = str(sys.argv[2]).lower()
        exportJson(trainer.get_final_strategy(), filename)
        print('Exported trained strategy as {}.json '.format(filename))
