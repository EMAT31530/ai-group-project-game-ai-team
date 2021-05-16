from Trainer.node import Node
import numpy as np
import random
import copy

# Vanilla, scalar-form/Simultaneous updates, no sampling
class VCFRTrainer:
    def __init__(self, gamestate):
        self.node_map = {} 
        self.nodes_touched = 0
        self.gamestate = gamestate
        
    def train(self, n_iterations=10000):
        utility = 0
        for _ in range(n_iterations):
            utility += self.cfr(copy.deepcopy(self.gamestate), 1, 1)
        return utility / n_iterations

    def cfr(self, gamestate, rps_1, rps_2):
        if gamestate.is_terminal():
            return self.terminal_node(gamestate)
        if gamestate.is_chance(): #public chance nodes
            return self.chance_node(gamestate, rps_1, rps_2)
        #for private chance nodes
        if any((len(hand)<self.gamestate.rules.hand_size) for hand in gamestate.hands):
            return self.private_chance_node(gamestate, rps_1, rps_2)
        #if gamestate.is_decision(): 
        else:
            return self.decision_node(gamestate, rps_1, rps_2)

    def terminal_node(self, gamestate):
        return self.get_utility(gamestate)

    def private_chance_node(self, gamestate, rps_1, rps_2):
        utility  = 0 # average utility per comb
        chance_outcomes = gamestate.get_private_chanceoutcomes()
        chance_prob = 1.0/len(chance_outcomes)
        for outcome in chance_outcomes:
            next_gamestate = gamestate.handle_private_chance(outcome)
            utility += self.cfr(next_gamestate, rps_1, rps_2) * chance_prob
        return utility
        
    def chance_node(self, gamestate, rps_1, rps_2):
        utility  = 0 # average utility per comb
        chance_outcomes = gamestate.get_public_chanceoutcomes()
        chance_prob = 1.0/len(chance_outcomes)
        for outcome in chance_outcomes:
            next_gamestate = gamestate.handle_public_chance(outcome)
            utility += self.cfr(next_gamestate, rps_1, rps_2) * chance_prob
        return utility

    def decision_node(self, gamestate, rp_1, rp_2):
        utility = 0
        player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate.get_representation(gamestate.hands[player]), n_actions)
        strategy = node.get_strategy()

        counterfactual_utility  = np.zeros(n_actions) # Counterfactual utility per action
        for ia, action in enumerate(possible_actions):
            next_gamestate = gamestate.handle_action(action)
            if player == 0:
                counterfactual_utility[ia] = -self.cfr(next_gamestate, rp_1 * strategy[ia], rp_2)
            else:
                counterfactual_utility[ia] = -self.cfr(next_gamestate, rp_1, rp_2 * strategy[ia])

        utility = np.sum(counterfactual_utility * strategy)
        regrets = counterfactual_utility - utility
        if player == 0:
            self.update_node(node, regrets * rp_2, rp_1 * strategy)
        else:
            self.update_node(node, regrets * rp_1, rp_2 * strategy)

        return utility

    def update_node(self, node, regret, strategy):
        node.cumulative_regrets += regret
        node.strategy_sum += strategy

    def get_utility(self, gamestate):
        player = gamestate.get_active_player_index() 
        payoff = gamestate.get_payoff()

        if gamestate.is_fold():
            utility = payoff
            return utility
            
        player_rank = gamestate.get_rank(gamestate.hands[player])
        opp_rank = gamestate.get_rank(gamestate.hands[1-player])
        if player_rank > opp_rank:
            return payoff
        elif player_rank < opp_rank:
            return -payoff
        else:
            return 0

    def group_hands_by_key(self, gamestate):
        keys = {}
        for hand in gamestate.hands:
            key = gamestate.get_representation(hand[1])
            if key not in keys:
                keys[key] = []
            keys[key].append(hand[0])
        return zip(*keys.items()) #[0] = keys, [1] = indicies

    def get_node(self, key, n_actions):
        self.nodes_touched += 1
        if key not in self.node_map:
            newnode = Node(n_actions)
            self.node_map[key] = newnode
            return newnode
        return self.node_map[key]

    def get_final_strategy(self):
        strategy = {}
        for key, node in self.node_map.items():
            nodestategy = node.get_average_strategy_with_threshold(0.01)
            strategy[key] = nodestategy
        return strategy

    def __name__(self):
        return 'Vanilla CFR (Scalar/Simultaneous)'


#http://www.mlanctot.info/files/papers/colt_ws_mccfr.pdf
class OutcomeSamplingCFRTrainer(VCFRTrainer):
    def __init__(self, gamestate):
        super().__init__(gamestate)
        self.epsilon = 0.9

    #here is where we will sample actions based on prob espilon = 0.6 greedy
    def decision_node(self, gamestate, rp_1, rp_2):
        utility = 0
        player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        node = self.get_node(gamestate.get_representation(gamestate.hands[player]), n_actions)
        strategy = node.get_strategy()

        counterfactual_utility = np.zeros(n_actions) # Counterfactual utility per action
        #epsilon greedy strategy
        if random.random() > self.epsilon: 
            probs = np.repeat((1.0/n_actions),n_actions)
            indexes = [np.random.choice(range(n_actions), p=probs)] #sampled action
        else:
            indexes = range(n_actions) #all actions
        for ia in indexes:
            next_gamestate = gamestate.handle_action(possible_actions[ia])
            if player == 0:
                counterfactual_utility[ia] = -self.cfr(next_gamestate, rp_1 * strategy[ia], rp_2)
            else:
                counterfactual_utility[ia] = -self.cfr(next_gamestate, rp_1, rp_2 * strategy[ia])
    
        utility = np.sum(counterfactual_utility * strategy)
        regrets = counterfactual_utility - utility
        if player == 0:
            self.update_node(node, regrets * rp_2, rp_1 * strategy)
        else:
            self.update_node(node, regrets * rp_1, rp_2 * strategy)
        return utility

    def __name__(self):
        return 'Outcome Sampling CFR'


#https://webdocs.cs.ualberta.ca/~bowling/papers/12aamas-pcs.pdf
class CSCFRTrainer(VCFRTrainer): #all chances sampled
    def train(self, n_iterations=10000):
        utility = 0
        for _ in range(n_iterations):
            next_gamestate = self.sample_hands(self.gamestate)
            utility += self.cfr(copy.deepcopy(next_gamestate), 1, 1)
        return utility / n_iterations

    def cfr(self, gamestate, rps_1, rps_2):
        if gamestate.is_terminal():
            return self.terminal_node(gamestate)
        if gamestate.is_chance(): #public chance nodes
            return self.chance_node(gamestate, rps_1, rps_2)
        #if gamestate.is_decision(): 
        else:
            return self.decision_node(gamestate, rps_1, rps_2)

    def sample_hands(self, gamestate):
        self.hands = [[],[]]
        next_gamestate = copy.deepcopy(gamestate)
        random.shuffle(next_gamestate.deck)
        for _ in range(self.gamestate.rules.hand_size):
            for i in range(2):
                deck_probs = np.repeat(1.0/len(next_gamestate.deck), len(next_gamestate.deck))
                sample_card = np.random.choice(next_gamestate.deck, p=deck_probs)
                self.hands[i].append(sample_card)
                next_gamestate.deck.remove(sample_card)
        next_gamestate.hands = self.hands
        return next_gamestate

    def chance_node(self, gamestate, rps_1, rps_2): #sample a chance
        chance_outcomes = gamestate.get_public_chanceoutcomes()
        chance_probs = np.repeat(1.0/len(chance_outcomes),len(chance_outcomes))
        outcome = np.random.choice(range(len(chance_outcomes)), p=chance_probs)
        next_gamestate = gamestate.handle_public_chance(chance_outcomes[outcome])
        return self.cfr(next_gamestate, rps_1, rps_2)

    def __name__(self):
        return 'Chance Sampling CFR'