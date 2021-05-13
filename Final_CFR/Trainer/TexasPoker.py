from gamestate import GameState
from operator import itemgetter
import random
import copy 
import itertools
import /TexasModules/ranking as rank

class TaxasRules():
    def __init__(self):
        self.lookuptable = {
            '2♥': 0, '3♥': 1, '4♥': 2, '5♥': 3, '6♥': 4, '7♥': 5, '8♥': 6, '9♥': 7, 
            '10♥': 8,'11♥': 9, '12♥': 10, '13♥': 11, '14♥': 12, '2♦': 13, '3♦': 14, '4♦': 15,
            '5♦': 16, '6♦': 17, '7♦': 18, '8♦': 19, '9♦': 20, '10♦': 21, '11♦': 22, '12♦': 23,
            '13♦': 24, '14♦': 25, '2♣': 26, '3♣': 27, '4♣': 28, '5♣': 29, '6♣': 30, '7♣': 31, '8♣': 32,
            '9♣': 33, '10♣': 34, '11♣': 35, '12♣': 36, '13♣': 37, '14♣': 38, '2♠': 39, '3♠': 40,
            '4♠': 41, '5♠': 42, '6♠': 43, '7♠': 44, '8♠': 45, '9♠': 46, '10♠': 47, '11♠': 48, '12♠': 49,
            '13♠': 50, '14♠': 51}
        self.hand_size = 2
    
    @staticmethod
    def build_deck_and_hands():
        deck = []
        for suit in range(4):
            for i in range(2, 15):
                deck.append(str(i)+'♥♦♣♠'[suit])
        random.shuffle(deck)

        comb_hands = itertools.combinations(deck, 2)
        enum_hands = list(enumerate(comb_hands))
        return deck,enum_hands

    @staticmethod
    def get_rank(cards):
        return rank.ranking(cards)
    

class NoLimit(GameState):
    def __init__(self, deck, hands):
        self.history = [' ']
        self.street = 'p' #p,f,t,r
        self.board = []
        self.current_bets = [0, 0]
        self.active_player = 0

        self.deck = deck
        self.hands = hands
        if hands[0] != []:
            self.ranks_tuple = self.sort_by_ranking()

    def is_terminal(self): #btec for now
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street != 'r':
            return fold
        else:
            check = history_str.endswith('ch'*2)
            call = history_str.endswith('c')
            allin = history_str.contains('Arc') #contains is placeholder
            return fold or check or call or allin

    def is_chance(self):
        call = action == 'c'
        check = self.history[-1] == 'ch' and action == 'ch'
        allin = ['Ar', 'c'] in self.history #needs to change ofc
        return call or check or allin


    def get_payoff(self):
        player = self.get_active_player_index()
        return self.current_bets[1 - player]

    def get_actions(self):
        prev_action = self.history[-1]
        raises = ARNOLD.getraises() #if no limit

        fullraise = ''.join([x[0] for x in self.history]).endswith('r'*4)
        if prev_action in [' ','ch']:
            return ['ch'] + raises
        elif prev_action[0]=='r':
            return ['f', 'c'] if fullraise else ['f', 'c'] + raises
        elif prev_action == 'Ar': #all in
            return ['f', 'c']

    def get_public_chanceoutcomes(self):
        if self.street == 'p': #cringe implementation, maybe not acc idk
            return itertools.combinations(self.deck, 3)
        return self.deck

    def get_private_chanceoutcomes(self):
        return self.deck 

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        next_state.history.append(action)

        player = next_state.get_active_player_index()
        next_state.active_player = (next_state.active_player + 1) % 2

        if action[0] == 'r': #raise
            next_state.current_bets[player] += int(action[0:])
        elif action == 'Ai': #all in
            next_state.current_bets[player] = 20000
        if action == 'c': #call
            next_state.current_bets[player] = next_state.current_bets[(player+1)%2]
        return next_state

    #need something with the fact the outcome must be three cards 
    # on the flop for in the cfr algorithm
    def handle_public_chance(self, outcome): #only public chance node is the flop
        next_state = copy.deepcopy(self)
        next_state.active_player = 0
        next_state.history.append(' ') #dummy action
        for card in outcome:
            next_state.board.append(card)
        next_state.filterer(outcome)

        if self.street == 'p':
            next_state.street = 'f'
        elif self.street == 'f':
            next_state.street = 't'
        elif self.street == 't':
            next_state.ranks_tuple = next_state.sort_by_ranking()
            next_state.street = 'r'

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
        return Tom_Arnold.representation(cards)

    def filterer(self, cards): #returns filtered list
        f = lambda hand: not any(i in hand[1] for i in cards)
        self.hands = list(filter(f,self.hands))
   
    def sort_by_ranking(self):
        g = lambda hand: [hand[0], TexasRules.get_rank(list(hand[1])+self.board)]
        ranking_list = list(map(g, self.hands))
        sorted_list = list(sorted(ranking_list, key=itemgetter(1)))
        return sorted_list


