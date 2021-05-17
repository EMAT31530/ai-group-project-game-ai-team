import numpy as np
import copy 
from itertools import combinations
from operator import itemgetter


class GenericPoker:
    def __init__(self, rules, vectorised=False):
        self.rules = rules

        self.round = 0 
        self.history = []
        self.community_cards = []
        self.current_bets = np.repeat(self.rules.blinds, 2)
        self.active_player = 0
        self.deck = self.rules.deck.copy()

        self.vectorised = vectorised
        self.ranks_tuple = []
        if self.vectorised:
            self.hands = list(enumerate(combinations(self.deck, self.rules.hand_size)))
            if self.rules.finalround == 0:
                self.sort_by_ranking()
        else:
            self.hands = [[],[]]
        
    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.round != self.rules.finalround:
            return fold

        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return fold or check or call

    def is_fold(self):
        history_str = ''.join(self.history)
        return history_str.endswith('f')

    def is_chance(self):
        if self.round == self.rules.finalround:
            return False
        history_str = ''.join(self.history)
        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return call or check

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        player = next_state.get_active_player_index()

        if action == 'r':
            if next_state.current_bets[player] < next_state.current_bets[1 - player]:
                next_state.current_bets[player] += 2 * self.rules.round_s[self.round].raise_amount
            else:
                next_state.current_bets[player] += self.rules.round_s[self.round].raise_amount
        elif action == 'c':
            next_state.current_bets[player] = next_state.current_bets[1-player]
        
        next_state.history.append(action)
        next_state.active_player = (1- player)
        return next_state

    def handle_public_chance(self, outcome):
        next_state = copy.deepcopy(self)
        next_state.round += 1
        next_state.active_player = 0
        next_state.history.append('d') #dummy action
        for card in outcome:
            next_state.community_cards.append(card)

        if next_state.vectorised:
            #following each public chance event, hand filtering can be computed
            next_state.filterer(next_state.community_cards)
            if next_state.round == next_state.rules.finalround:
                #following final chance event sorting can be computed!
                next_state.sort_by_ranking()
        return next_state

    def handle_private_chance(self, outcome):
        next_state = copy.deepcopy(self)
        player = next_state.get_active_player_index()
        next_state.active_player = (1 - player)
        next_state.hands[player].append(outcome)
        next_state.deck.remove(outcome)
        return next_state

    def get_payoff(self):
        player = self.get_active_player_index()
        return self.current_bets[1 - player]

    def get_actions(self):
        history_str = ''.join(self.history)
        if self.history == [] or history_str.endswith(('d','ch')):
            return ['ch', 'r']
        elif history_str.endswith('r'* self.rules.round_s[self.round].num_raises):
            return ['f', 'c']
        elif history_str.endswith('r'):
            return ['f', 'c', 'r']

    def get_public_chanceoutcomes(self):
        return list(combinations(self.deck, self.rules.round_s[self.round].n_communitycards))

    def get_private_chanceoutcomes(self):
        return self.deck 

    def get_rank(self, hand):
        hand_to_rank = list(hand) + self.community_cards
        return self.rules.get_rank(hand_to_rank)

    def get_representation(self, hand):
        hand_to_rrepresent = list(hand) + self.community_cards
        return self.rules.get_representation(hand_to_rrepresent, self.history)

    def get_active_player_index(self):
        return self.active_player

    def filterer(self, cards): #returns filtered list
        f = lambda hand: not any(i in hand[1] for i in cards)
        self.hands = list(filter(f,self.hands))
   
    def sort_by_ranking(self):
        g = lambda hand: [hand[0], self.get_rank(hand[1]), hand[1]]
        ranking_list = list(map(g, self.hands))
        self.ranks_tuple = list(sorted(ranking_list, key=itemgetter(1)))
