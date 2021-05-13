from gamestate import GameState
from operator import itemgetter
import random
import copy 

class KuhnRules():
    def __init__(self):
        self.lookuptable = {'J': 0, 'Q': 1, 'K': 2}
        self.hand_size = 1

    @staticmethod
    def build_deck_and_hands():
        deck = ['J', 'Q', 'K']
        random.shuffle(deck)
        enum_hands = list(enumerate(deck))
        return deck, enum_hands


class Kuhn(GameState):
    def __init__(self, deck, hands):
        self.history = ''
        self.active_player = 0
        self.deck = deck
        self.hands = hands
        if hands[0] != []:
            self.ranks_tuple = self.sort_by_ranking()
        #initial ranking of hands [in vectorisation]

    def is_terminal(self):
        terminal_strings = ['pp', 'bb', 'bp']
        return self.history[-2:] in terminal_strings

    def is_fold(self):
        return self.history[-2:] == 'bp'

    def is_chance(self): #no chance nodes in kuhn
        return False

    def get_payoff(self):
        return 1 if self.history[-1] == 'p' else 2

    def get_actions(self):
        return ['p', 'b']

    def get_public_chanceoutcomes(self):
        pass 

    def get_private_chanceoutcomes(self):
        return self.deck 

    def get_rank(self, card):
        ranks = {'K': 3, 'Q': 2, 'J': 1}
        return ranks[card[0]]

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        next_state.history += action
        player = next_state.get_active_player_index()
        next_state.active_player = (1 - player)
        return next_state

    def handle_private_chance(self, outcome):
        next_state = copy.deepcopy(self)
        player = next_state.get_active_player_index()
        next_state.active_player = (1 - player)
        next_state.hands[player].append(outcome)
        next_state.deck.remove(outcome)
        return next_state

    def handle_public_chance(self): #no public chance nodes in kuhn
        pass

    def get_active_player_index(self):
        return self.active_player

    def get_representation(self, card):
        key = card[0] + self.history
        return key

    def sort_by_ranking(self):
        g = lambda hand: [hand[0], self.get_rank(hand[1])]
        ranking_list = list(map(g, self.hands))
        return list(sorted(ranking_list, key=itemgetter(1)))

    def filterer(self, cards): #returns filtered list
        f = lambda hand: not any(i in hand[1] for i in cards)
        self.hands = list(filter(f,self.hands))

