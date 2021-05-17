from TerminalPlayer.players import Player, AiPlayer
import copy
from terminal_playing_cards import View
import numpy as np
from itertools import combinations


class PlayGeneric:
    def __init__(self, deck, players, rules):
        self.rules = rules
        self.history = []
        self.community_cards = []
        self.active_player = 0
        self.round = 0
        self.current_bets = np.repeat(self.rules.blinds, 2)
        self.deck = deck
        self.players = players
        self.reset_deck = copy.deepcopy(deck)

    def start_round(self):
        self.history = []
        self.community_cards = []
        self.active_player = 0
        self.round = 0
        self.current_bets = np.repeat(self.rules.blinds, 2)
        self.players.reverse()
        self.deck = copy.deepcopy(self.reset_deck)
        self.deck.shuffle()
        for _ in range(self.rules.hand_size):
            for player in self.players:
                player.cards = [self.deck.pop()]

    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.round != self.rules.finalround:
            return fold

        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return fold or check or call

    def is_chance(self):
        if self.round == self.rules.finalround:
            return False
        history_str = ''.join(self.history)
        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return call or check

    def get_actions(self):
        history_str = ''.join(self.history)
        if self.history == [] or history_str.endswith(('d','ch')):
            return ['Check', 'Raise']
        elif history_str.endswith('r'* self.rules.round_s[self.round].num_raises):
            return ['Fold', 'Call']
        elif history_str.endswith('r'):
            return ['Fold', 'Call', 'Raise']

    def get_rewards(self):
        plyr = self.get_active_player_index()
        opp = (1 - plyr)
        player_card = self.get_rank(self.players[plyr].cards)
        opponent_card = self.get_rank(self.players[opp].cards)

        rwds = -1 * self.current_bets
        if self.history[-1] == 'f':
            winr = plyr
            rwds[winr] = self.current_bets[opp]
        else:
            if player_card > opponent_card:
                winr = plyr 
                rwds[winr] *= -1
            elif player_card < opponent_card:
                winr = opp 
                rwds[winr] *= -1
            else:
                return 0, 0

        for ip, player in enumerate(self.players):
            player.money += rwds[ip]
        return rwds[winr], self.players[winr]

    def handle_chance(self):
        for _ in range(self.rules.round_s[self.round].n_communitycards):
            self.community_card.append(self.deck.pop())
        self.round += 1
        self.active_player = 0        
        self.history.append('d')

    def handle_action(self, action):
        player = self.get_active_player_index()

        if action == 'r':
            if self.current_bets[player] < self.current_bets[1 - player]:
                self.current_bets[player] += 2 * self.rules.round_s[self.round].raise_amount
            else:
                self.current_bets[player] += self.rules.round_s[self.round].raise_amount
        elif action == 'c':
            self.current_bets[player] = self.current_bets[1-player]

        self.history.append(action)
        self.active_player = (1- player)

    def handle_public_chance(self, outcome):
        self.round += 1
        self.active_player = 0
        self.history.append('d') #dummy action
        for card in outcome:
            self.community_cards.append(card)

    def get_active_player(self):
        return self.players[self.active_player]

    def get_active_player_index(self):
        return self.active_player

    def get_representation(self, hand):
        hand_to_rrepresent = list(hand) + self.community_cards
        return self.rules.get_representation(hand_to_rrepresent, self.history)

    def get_rank(self, hand):
        hand_to_rank = list(hand) + self.community_cards
        return self.rules.get_rank(hand_to_rank)

    def display_round_str(self, round, terminal=False):
        for player in self.players:
            if type(player) != AiPlayer:
                human = player
            else:
                Ai = player
        human_hand = View(human.cards)
        
        if self.community_cards != []:
            board_hand = View(self.community_cards)
            print('On the board there is: {}'.format(board_hand))

        print('Round: {}. In your hand you have:'.format(round))
        print(human_hand)
        print('ai has {}'.format(Ai.cards))
        if not terminal:
            print('You have £{}, the Ai has £{}.\n'.format(human.money, Ai.money))
            
        player = 0
        for action in self.history:
            acting_player = self.players[player%2]
            if action != 'd':
                print('{} chose to {}'.format(acting_player.name, action))
                player += 1
            else:
                player = 0
                print('')

        if terminal:
            prize, winner = self.get_rewards()
            if prize == 0:
                print('it was a draw!')
            else:
                print("\n{} wins £{}!\n".format(winner.name, prize))
                print('You now have £{}, and the Ai has £{}.\n'.format(human.money, Ai.money))
