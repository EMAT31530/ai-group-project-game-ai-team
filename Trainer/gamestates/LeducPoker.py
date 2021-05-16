from Trainer.gamestates.gamestate import GameState
from operator import itemgetter
import random
import copy 
import itertools

class LeducRules():
    def __init__(self):
        self.lookuptable = {'J♥': 0, 'Q♥': 1, 'K♥': 2, 'J♦': 3, 'Q♦': 4, 'K♦': 5}
        self.hand_size = 1
    
    @staticmethod
    def build_deck_and_hands():
        deck = []
        vals = ['J', 'Q', 'K']
        for suit in range(2):
            for i in range(0, 3):
                deck.append(vals[i]+'♥♦'[suit])
        random.shuffle(deck)

        comb_hands = itertools.combinations(deck, 1)
        enum_hands = list(enumerate(comb_hands))
        return deck,enum_hands


class Leduc(GameState):
    def __init__(self, deck, hands, vectorised=False):
        self.history = []
        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_cards = []
        self.current_bets = [1, 1]
        self.active_player = 0

        self.deck = deck
        self.hands = hands
        self.ranks_tuple = []
        self.vectorised = vectorised

    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street == 0:
            return fold

        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return fold or check or call

    def is_fold(self):
        history_str = ''.join(self.history)
        return history_str.endswith('f')

    def is_chance(self):
        history_str = ''.join(self.history)
        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return call or check

    def get_payoff(self):
        player = self.get_active_player_index()
        return self.current_bets[1 - player]

    def get_actions(self):
        history_str = ''.join(self.history)
        if self.history == [] or history_str.endswith(('d','ch')):
            return ['ch', 'r']
        elif history_str.endswith('r'):
            return ['f', 'c', 'R']
        elif history_str.endswith('R'):
            return ['f', 'c']

    def get_public_chanceoutcomes(self):
        return self.deck

    def get_private_chanceoutcomes(self):
        return self.deck 

    def get_rank(self, cards):
        ranks = {
        'KK': 9,
        'QQ': 8,
        'JJ': 7,
        'KQ': 6, 'QK': 6,
        'KJ': 5, 'JK': 5,
        'QJ': 4, 'JQ': 4,
        'K': 3, 'Q': 2, 'J': 1
        }
        cardz = list(cards) + self.community_cards
        repr = ''.join([x[0] for x in cardz])
        return ranks[repr]

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        player = next_state.get_active_player_index()
        if action == 'r':
            next_state.current_bets[player] += 2 * (next_state.street + 1)
        elif action == 'R':
            next_state.current_bets[player] += 4 * (next_state.street + 1)
        elif action == 'c':
            next_state.current_bets[player] = next_state.current_bets[1-player]
        next_state.history.append(action)
        next_state.active_player = (1- player)
        return next_state

    def handle_public_chance(self, outcome): #only public chance node is the flop
        next_state = copy.deepcopy(self)
        next_state.street = 1
        next_state.active_player = 0
        next_state.history.append('d') #dummy action
        next_state.community_cards.append(outcome)
        if self.vectorised:
            #following each public chance event, hand filtering can be computed
            next_state.filterer(next_state.community_cards)
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

    def get_active_player_index(self):
        return self.active_player

    def get_representation(self, cards):
        cardz = list(cards) + self.community_cards
        repr = ''.join([x[0] for x in cardz])
        history_str = ".".join(self.history)
        return '{}-{}'.format(repr, history_str)

    def filterer(self, cards): #returns filtered list
        f = lambda hand: not any(i in hand[1] for i in cards)
        self.hands = list(filter(f,self.hands))
   
    def sort_by_ranking(self):
        g = lambda hand: [hand[0], self.get_rank(hand[1]), hand[1]]
        ranking_list = list(map(g, self.hands))
        self.ranks_tuple = list(sorted(ranking_list, key=itemgetter(1)))

