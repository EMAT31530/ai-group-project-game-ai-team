import numpy as np
from node import Node
import copy

#dont have a paper for this in vector alternating form but the paper of cfr+ says its a 
#thing so maybe its mentioned in the base cfr paper....
class VectorAlternatingVCFR:
    def __init__(self, gamestatetype, rules):
        self.node_map = {}
        self.rules = rules()
        self.current_player = 0
        deck, hands = self.rules.build_deck_and_hands()
        self.gamestate = gamestatetype(deck, hands)
        self.private_states = len(self.gamestate.hands)
        self.orighands = [i[1] for i in self.gamestate.hands]
        
    def train(self, n_iterations=10000):
        #fci represents the fixed probability of each private state (hole cards in poker)
        self.fci = np.repeat(1.0/self.private_states, self.private_states)
        util = 0
        for _ in range(n_iterations):
            for j in range(2): #alternating updates
                self.current_player = j
                rps_1 = np.ones(self.private_states)
                rps_2 = np.ones(self.private_states)
                util += sum(self.cfr(copy.deepcopy(self.gamestate), rps_1, rps_2))
        return (util) / (n_iterations)

    def cfr(self, gamestate, rps_1, rps_2):
        if gamestate.is_terminal():
            return self.terminal_node(gamestate, rps_2)
        if gamestate.is_chance():
            return self.chance_node(gamestate, rps_1, rps_2)
        #if gamestate.is_decision():
        else:
            return self.decision_node(gamestate, rps_1, rps_2)

    def terminal_node(self, gamestate, rps_2):
        return self.fci * self.get_utility(gamestate, rps_2 * self.fci)
    
    def chance_node(self, gamestate, rps_1, rps_2): #no sampling
        chance_outcomes = gamestate.get_public_chanceoutcomes()
        chance_prob = 1.0/len(chance_outcomes)
        utility  = np.zeros(self.private_states) # average utility per comb
        for outcome in chance_outcomes:
            next_gamestate = gamestate.handle_public_chance(outcome)
            utility += self.cfr(next_gamestate, rps_1, rps_2) 
        return utility * chance_prob

    def decision_node(self, gamestate, rps_1, rps_2):
        active_player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)
        #invalid hands are filtered at each public chance node
        keys, indicies_grouping = self.group_hands_by_key(gamestate)
        #e.g. key1, [1,3,5,6] so key1 represents hands at index 1,3,5,6

        f = lambda key: self.get_node(key, n_actions)
        temp_node_vec = list(map(f, keys)) 
        g = lambda x: x.get_strategy()
        temp_strategy_vec = np.array(list(map(g, temp_node_vec))) 

        strategy_vec = np.zeros((self.private_states, n_actions)) 
        node_vec = [0] * self.private_states
        for iI, indicies in enumerate(indicies_grouping):
            strategy = temp_strategy_vec[iI]
            node = temp_node_vec[iI]
            for index in indicies:
                strategy_vec[index] = strategy
                node_vec[index] = node

        utility  = np.zeros(self.private_states) # average utility per comb
        counterfactual_utility = np.zeros((n_actions, self.private_states))
        for ia, action in enumerate(possible_actions):
            if active_player == self.current_player:
                new_rps_1 = rps_1 * strategy_vec[:,ia] #unitwise numpy multiplication
                next_gamestate = gamestate.handle_action(action)
                temputil = self.cfr(next_gamestate, new_rps_1, rps_2) 
                counterfactual_utility[ia] = temputil # M arrow
                utility += temputil * strategy_vec[:,ia] #unitwise numpy multiplication

            else: #for other player no regrets calculated
                new_rps_2 = rps_2 * strategy_vec[:,ia] #unitwise numpy multiplication
                next_gamestate = gamestate.handle_action(action)
                utility += self.cfr(next_gamestate, rps_1, new_rps_2) # M arrow

        if active_player == self.current_player:
            for iI, node in enumerate(node_vec):
                if node!=0:
                    regrets = counterfactual_utility[:,iI] - utility[iI]
                    strategy = rps_1[iI] * strategy_vec[iI]
                    self.update_node(node, regrets, strategy)             
        return utility
    
    def update_node(self, node, regret, strategy):
        node.cumulative_regrets += regret
        node.strategy_sum += strategy

    def get_utility(self, gamestate, pi):
        lookuptable = self.rules.lookuptable
        utility = np.zeros(self.private_states)
        player = gamestate.get_active_player_index() 
        payoff = gamestate.get_payoff()
        
        if gamestate.is_fold():
            totalpi = sum(pi)
            removecr = np.zeros(len(lookuptable))
            for index, rank in gamestate.ranks_tuple:
                hand = self.orighands[index]
                for card in hand:
                    removecr[lookuptable[card]] += pi[index] 
                
            for index, rank in gamestate.ranks_tuple:
                hand = self.orighands[index]
                temppi = totalpi
                for card in hand:
                    temppi -= removecr[lookuptable[card]]
                utility[index] += temppi * payoff

            return utility if player == self.current_player else -utility

        wincr = np.zeros(len(lookuptable))
        winsum = 0
        j = 0    
        for index, rank in gamestate.ranks_tuple:
            hand = self.orighands[index]
            while gamestate.ranks_tuple[j][1] < rank: #rank of opp hand
                opp_index = gamestate.ranks_tuple[j][0]
                winsum += pi[opp_index] 
                ophand = self.orighands[opp_index]
                for card in ophand:
                    wincr[lookuptable[card]] += pi[opp_index] 
                j += 1 
            for card in hand:
                winsum -= wincr[lookuptable[card]]
            utility[index] += winsum * payoff

        losecr = np.zeros(len(lookuptable))
        losesum = 0
        j = len(gamestate.ranks_tuple) - 1
        reversed_tuple = gamestate.ranks_tuple.copy()
        reversed_tuple.reverse()
        for index, rank in reversed_tuple:
            hand = self.orighands[index]
            while gamestate.ranks_tuple[j][1] > rank:
                opp_index = gamestate.ranks_tuple[j][0]
                losesum += pi[opp_index] 
                ophand = self.orighands[opp_index]
                for card in ophand:
                    losecr[lookuptable[card]] += pi[opp_index] 
                j -= 1
            for card in hand:
                losesum -= losecr[lookuptable[card]]
            utility[index] -= losesum * payoff
        return utility
    
    def group_hands_by_key(self, gamestate):
        keys = {}
        for hand in gamestate.hands:
            key = gamestate.get_representation(hand[1])
            if key not in keys:
                keys[key] = []
            keys[key].append(hand[0])
        return zip(*keys.items()) #[0] = keys, [1] = weightings

    def get_node(self, key, n_actions):
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
        return 'Vanilla CFR (Vector/Alternating)'

    
#https://webdocs.cs.ualberta.ca/~bowling/papers/12aamas-pcs.pdf
class PublicCSCFRTrainer(VectorAlternatingVCFR):
    #monte carlo Public Chance Sampling so only chance nodes encountered are public nodes
    def chance_node(self, gamestate, rps_1, rps_2):
        chance_outcomes = gamestate.get_public_chanceoutcomes()
        chance_probs = np.repeat(1.0/len(chance_outcomes),len(chance_outcomes))
        outcome = np.random.choice(chance_outcomes, p=chance_probs)
        next_gamestate = gamestate.handle_public_chance(outcome)
        return self.cfr(next_gamestate, rps_1, rps_2)

    def update_node(self, node, regret, strategy):
        regret[regret < 0] = 0 #negative regret is not stored
        node.cumulative_regrets += regret
        node.strategy_sum += strategy

    def __name__(self):
        return 'Public Chance Sampling CFR'


#donny work idk why sad, will come back to
class OpponentPublicCSCFRTrainer(PublicCSCFRTrainer):
    def train(self, n_iterations=10000):
        #fci represents the fixed probability of each private state (hole cards in poker)
        self.fci = np.repeat(1.0/self.private_states, self.private_states)
        util = 0
        for _ in range(n_iterations):
            next_gamestate = self.sample_one_hand(self.gamestate)
            for j in range(2): #alternating updates
                self.current_player = j
                rps_1 = np.ones(self.private_states)
                rp_2 = 1
                util += self.cfr(copy.deepcopy(next_gamestate), rps_1, rp_2)
        return sum((util) / (n_iterations))

    def sample_one_hand(self, gamestate):
        next_gamestate = copy.deepcopy(gamestate)
        sample_num = np.random.choice(range(len(gamestate.hands)), p=self.fci)
        sample = gamestate.hands[sample_num][1]
        for card in sample:
            next_gamestate.deck.remove(card)
        next_gamestate.filterer(sample)
        next_gamestate.ranks_tuple = next_gamestate.sort_by_ranking()
        self.sampled_hand = sample
        return next_gamestate

    def terminal_node(self, gamestate, rp_2):
        return self.fci * self.get_utility(gamestate, rp_2)

    def decision_node(self, gamestate, rps_1, rp_2):
        active_player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        utility  = np.zeros(self.private_states) # average utility per comb
        counterfactual_utility = np.zeros((n_actions, self.private_states))
        if active_player == self.current_player:
            keys, indicies_grouping = self.group_hands_by_key(gamestate)
            f = lambda key: self.get_node(key, n_actions)
            temp_node_vec = list(map(f, keys)) 
            g = lambda x: x.get_strategy()
            temp_strategy_vec = np.array(list(map(g, temp_node_vec))) 

            strategy_vec = np.zeros((self.private_states, n_actions)) 
            node_vec = [0] * self.private_states
            for Ii, indicies in enumerate(indicies_grouping):
                strategy = temp_strategy_vec[Ii]
                node = temp_node_vec[Ii]
                for index in indicies:
                    strategy_vec[index] = strategy
                    node_vec[index] = node


            for ia, action in enumerate(possible_actions):
                    new_rps_1 = rps_1 * strategy_vec[:,ia] #unitwise numpy multiplication
                    next_gamestate = gamestate.handle_action(action)
                    temputil = self.cfr(next_gamestate, new_rps_1, rp_2) 
                    counterfactual_utility[ia] = temputil # M arrow
                    utility += temputil * strategy_vec[:,ia] #unitwise numpy multiplication

            for iI, node in enumerate(node_vec):
                if node!=0:
                    regrets = (counterfactual_utility[:,iI] - utility[iI]) * rp_2
                    strategy = rps_1[iI] * strategy_vec[iI]
                    self.update_node(node, regrets, strategy)   
            
        else: #for other player no regrets calculated
            node = self.get_node(gamestate.get_representation(self.sampled_hand), n_actions)
            strategy = node.get_strategy()
            for ia, action in enumerate(possible_actions):
                next_gamestate = gamestate.handle_action(action)
                utility = self.cfr(next_gamestate, rps_1, rp_2 * strategy[ia]) # M arrow
        return utility

    def get_utility(self, gamestate, rp_2):
        utility = np.zeros(self.private_states)
        player = gamestate.get_active_player_index() 
        payoff = gamestate.get_payoff()

        if gamestate.is_fold():
            for index, _ in gamestate.hands:
                utility[index] = payoff
            return utility if player == self.current_player else -utility
       
        opprank = gamestate.get_rank(self.sampled_hand)
        for index, rank in gamestate.ranks_tuple:
            if rank > opprank:
                utility[index] = payoff
            elif rank < opprank:
                utility[index] = -payoff

        return utility

    def __name__(self):
        return 'Opponent Public Chance Sampling CFR'

#does work nice
class SelfPublicCSCFRTrainer(OpponentPublicCSCFRTrainer):
    def train(self, n_iterations=10000):
        #fci represents the fixed probability of each private state (hole cards in poker)
        self.fci = np.repeat(1.0/self.private_states, self.private_states)
        util = 0
        for _ in range(n_iterations):
            next_gamestate = self.sample_one_hand(self.gamestate)
            for j in range(2): #alternating updates
                self.current_player = j
                rps_1 = 1
                rps_2 = np.ones(self.private_states)
                util += self.cfr(copy.deepcopy(next_gamestate), rps_1, rps_2)
        return (util) / (n_iterations)

    def terminal_node(self, gamestate, rps_2):
        return self.get_utility(gamestate, self.fci * rps_2)

    def decision_node(self, gamestate, rps_1, rps_2):
        active_player = gamestate.get_active_player_index()
        possible_actions = gamestate.get_actions()
        n_actions = len(possible_actions)

        utility  = 0 # average utility per comb
        counterfactual_utility = np.zeros(n_actions)
        if active_player == self.current_player:
            node = self.get_node(gamestate.get_representation(self.sampled_hand), n_actions)
            strategy = node.get_strategy()
            for ia, action in enumerate(possible_actions):
                next_gamestate = gamestate.handle_action(action)
                temputil = self.cfr(next_gamestate, rps_1 * strategy[ia], rps_2) # M arrow
                counterfactual_utility[ia] = temputil
                utility += temputil * strategy[ia]

            regrets = counterfactual_utility - utility
            strategy = rps_1 * strategy
            self.update_node(node, regrets, strategy)   
            
        else: #for other player no regrets calculated
            keys, indicies_grouping = self.group_hands_by_key(gamestate)
            f = lambda key: self.get_node(key, n_actions)
            temp_node_vec = list(map(f, keys)) 
            g = lambda x: x.get_strategy()
            temp_strategy_vec = np.array(list(map(g, temp_node_vec))) 

            strategy_vec = np.zeros((self.private_states, n_actions))
            for i, indicies in enumerate(indicies_grouping):
                strategy = temp_strategy_vec[i]
                node = temp_node_vec[i]
                for index in indicies:
                    strategy_vec[index] = strategy

            for ia, action in enumerate(possible_actions):
                    new_rps_2 = rps_2 * strategy_vec[:,ia] #unitwise numpy multiplication
                    next_gamestate = gamestate.handle_action(action)
                    temputil = self.cfr(next_gamestate, rps_1, new_rps_2)
                    utility += temputil #unitwise numpy multiplication   

        return utility

    def get_utility(self, gamestate, rps_2):
        player = gamestate.get_active_player_index() 
        payoff = gamestate.get_payoff()

        if gamestate.is_fold():
            utility = payoff * sum(rps_2)
            return utility if player == self.current_player else -utility

        rp2_sum = 0
        rank = gamestate.get_rank(self.sampled_hand)
        for index, opprank in gamestate.ranks_tuple:
            if rank > opprank:
                rp2_sum += rps_2[index]
            elif rank < opprank:
                rp2_sum -= rps_2[index]
        return payoff * rp2_sum

    def __name__(self):
        return 'Self Public Chance Sampling CFR'


#https://arxiv.org/pdf/1407.5042.pdf
class CFRPlusTrainer(VectorAlternatingVCFR):
    def train(self, n_iterations=10000, d=500):
        #fci represents the fixed probability of each private state (hole cards in poker)
        self.fci = np.repeat(1.0/self.private_states, self.private_states)
        util = 0
        for t in range(n_iterations):
            self.w = max(t - d, 0) #weights later strategy updates
            for j in range(2): #alternating updates
                self.current_player = j
                rps_1 = np.ones(self.private_states)
                rps_2 = np.ones(self.private_states)
                util += sum(self.cfr(copy.deepcopy(self.gamestate), rps_1, rps_2))
        return (util) / (n_iterations)

    def update_node(self, node, regret, strategy):
        regret[regret < 0] = 0 #negative regret is not stored
        node.cumulative_regrets += regret
        node.strategy_sum += strategy * self.w

    def __name__(self):
        return 'CFR+'