from TerminalPlayer.players import Player, AiPlayer
import copy
from terminal_playing_cards import View
import numpy as np

class Rules:
    def __init__(self, DECK_SPEC, Action_Spec, start_money):
        self.DECK_SPEC = DECK_SPEC
        self.Action_Spec = Action_Spec
        self.start_money = start_money

class PlayKuhn:
    def __init__(self, deck, players, rules):
        self.history = ''
        self.active_player = 0
        self.deck = deck
        self.players = players
        self.reset_deck = copy.deepcopy(deck)
        self.rules = rules

    def get_rank(self, card):
        return card.value

    def start_round(self):
        self.history = ''
        self.active_player = 0
        self.players.reverse()
        self.deck = copy.deepcopy(self.reset_deck)
        self.deck.shuffle()
        for player in self.players:
            player.cards = [self.deck.pop()]

    def is_terminal(self):
        terminal_strings = ['pp', 'bb', 'bp']
        return self.history[-2:] in terminal_strings

    def is_chance(self):
        return False

    def get_actions(self):
        if self.history in ['','p']:
            return ['Check', 'Bet']
        elif self.history[-1] == 'b':
            return ['Fold', 'Call']

    def get_rewards(self):
        plyr = self.get_active_player_index()
        opp = (1 - plyr)
        player_card = self.get_rank(self.players[plyr].cards[0])
        opponent_card = self.get_rank(self.players[opp].cards[0])

        if self.history[-1] == 'p':
            rwds = [-1,-1]
            if self.history[-2:] == 'pp': #double pass
                winr = plyr if player_card > opponent_card else opp
            else: #bet followed by fold
                winr = plyr
        else: #double bet
            rwds = [-2,-2]
            winr = plyr if player_card > opponent_card else opp

        rwds[winr] *= -1
        for ip, player in enumerate(self.players):
            player.money += rwds[ip]

        return rwds[winr], self.players[winr]

    def handle_action(self, action):
        self.active_player = (1 - self.active_player)
        self.history += action

    def get_active_player(self):
        return self.players[self.active_player]

    def get_active_player_index(self):
        return self.active_player

    def get_representation(self, card):
        repr = {
        3: 'K',
        2: 'Q',
        1: 'J'
        }
        key = repr[card[0].value] + self.history
        return key

    def display_round_str(self, round, terminal=False):
        for player in self.players:
            if type(player) != AiPlayer:
                human = player
            else:
                Ai = player
        human_hand = View(human.cards)
        print('Round: {}. In your hand you have:'.format(round))
        print(human_hand)
        if not terminal:
            print('You have £{}, the Ai has £{}.\n'.format(human.money, Ai.money))
        
        for ia, action in enumerate(self.history):
            acting_player = self.players[ia%2]
            print('{} chose to {}'.format(acting_player.name, 
            action))

        if terminal:
            prize, winner = self.get_rewards()
            print("\n{} wins £{}!\n".format(winner.name, prize))
            print('You now have £{}, and the Ai has £{}.\n'.format(human.money, Ai.money))

class PlayLeduc():
    def __init__(self, deck, players, rules):
        self.history = []
        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = []
        self.current_bets = [1,1]
        self.players = players
        self.rules = rules
        self.deck = 0
        self.reset_deck = copy.deepcopy(deck)
        self.active_player = 0

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
        repr = ''.join([x.face for x in cards])
        return ranks[repr]

    def start_round(self):
        self.history = []
        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = []
        self.active_player = 0
        self.current_bets = np.ones(2)
        self.players.reverse()
        self.deck = copy.deepcopy(self.reset_deck)
        self.deck.shuffle()
        for player in self.players:
            player.cards = [self.deck.pop()]

    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street == 0:
            return fold

        check =  history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return fold or check or call

    def is_chance(self):
        history_str = ''.join(self.history)
        check =  history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return check or call

    def get_actions(self):
        history_str = ''.join(self.history)
        if self.history == [] or history_str.endswith(('d','ch')):
            return ['Check', 'Raise']
        elif history_str.endswith('r'):
            return ['Fold', 'Call', 'reraise']
        elif history_str.endswith('R'):
            return ['Fold', 'Call']

    def get_rewards(self):
        plyr = self.get_active_player_index()
        opp = (1 - plyr)
        player_card = self.get_rank(self.players[plyr].cards)
        opponent_card = self.get_rank(self.players[opp].cards)


        prev_action = self.history[-1]
        rwds = -1 * self.current_bets
        if prev_action == 'f':
            winr = plyr
            rwds[winr] = self.current_bets[opp]
        else:
            if player_card < opponent_card:
                winr = plyr 
                rwds[winr] *= -1
            elif player_card > opponent_card:
                winr = opp 
                rwds[winr] *= -1
            else:
                return 0, 0
            

        
        for ip, player in enumerate(self.players):
            player.money += rwds[ip]

        return rwds[winr], self.players[winr]

    def handle_action(self, action):
        player = self.get_active_player_index()
        self.active_player = (1 - player)
        self.history.append(action)
        if action == 'r':
            self.current_bets[player] += 2 * (self.street + 1)
        elif action == 'R':
            self.current_bets[player] += 4 * (self.street + 1)
        elif action == 'c':
            self.current_bets[player] = self.current_bets[1-player]
            
    def handle_chance(self):
        self.street = 1
        self.active_player = 0
        self.community_card.append(self.deck.pop())
        self.history.append('d')

    def get_active_player(self):
        return self.players[self.active_player]

    def get_active_player_index(self):
        return self.active_player

    def get_representation(self, cards):
        hand_rank = self.get_rank(cards + self.community_card)
        history_str = ".".join(self.history)
        return '{}-{}'.format(hand_rank, history_str)

    def display_round_str(self, round, terminal=False):
        for player in self.players:
            if type(player) != AiPlayer:
                human = player
            else:
                Ai = player
        human_hand = View(human.cards)
        board_hand = View(self.community_card)
        flop='preflop'
        if self.street == 1:
            print('On the board there is: {}'.format(board_hand))
            flop = 'postflop'

        print('Round: {}, {}. In your hand you have:'.format(round, flop))
        print(human_hand)
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
