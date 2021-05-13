from players import Player, AiPlayer
import copy
from terminal_playing_cards import View

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
        key = repr[card.value] + self.history
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

leducrules = Rules({"J": {"diamonds": 1, "hearts": 1}, 
    "Q": {"diamonds": 2, "hearts": 2}, "K": {"diamonds": 3, "hearts": 3}}, 
    {'check': 'ch', 'fold': 'f', 'call': 'c', 'raise': 'r', 'reraise': 'rr'}, 
    20 )

class Leduc():
    def __init__(self):
        self.history = [' ']
        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.current_bets = [0,0]
        self.deck = 0
        self.active_player = 0

    def get_rank(cards):
        ranks = {
            'KK': 1,
            'QQ': 2,
            'JJ': 3,
            'KQ': 4, 'QK': 4,
            'KJ': 5, 'JK': 5,
            'QJ': 6, 'JQ': 6,
            'K': 7, 'Q': 8, 'J': 9
        }
        return str(ranks[cards[0]])

    def actions(action):
        acts = 'ur mu'
        return acts[action]

    def new_round(self):
        self.history = [' ']
        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.pot = 2
        self.deck = Deck()
        for player in self.players:
            player.card = self.deck.draw()
            player.bet_amount = 1
        self.players.reverse()

    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street == 0:
            return fold

        check =  history_str.endswith('ch'*2)
        fullraise = history_str.endswith('c')
        return fold or check or fullraise

    def get_rewards(self):
        index = self.active_player
        opp_index = (self.active_player+1)%2
        plyr = self.players[index]
        opp = self.players[opp_index]


        prev_action = self.history[-1]

        rwds = [self.pot - player.bet_amount for player in self.players]
        winr = index
        if prev_action == 'f':
            rwds[opp_index] = -(opp.bet_amount)
            return rwds, index

        player_rank = rank(plyr.card + self.community_card)
        opponent_rank = rank(opp.card + self.community_card)

        if player_rank < opponent_rank:
            rwds[opp_index] = -(opp.bet_amount)
        else:
            rwds[index] = -(plyr.bet_amount)
            winr = opp_index
        return rwds, winr


    def get_actions(self):
        prev_action = self.history[-1]
        if prev_action in [' ','ch']:
            return ['Check', 'Raise']
        elif prev_action=='r':
            return ['Fold', 'Call', 'Reraise']
        elif prev_action=='rr':
            return ['Fold', 'Call']

    def handle_action(self, action):
        player = self.get_active_player()
        print("{} has chosen to {}.".format(player.name, action))

        act = actions(action.lower())


        if act in ['r','rr','c']:
            self.pot += 2 * (self.street + 1)
            player.bet_amount += 2 * (self.street + 1)

        check = self.history[-1] == 'ch' and act == 'ch'
        self.history.append(act)
        self.active_player = (self.active_player + 1) % self.num_players


        if self.street == 0 and (act == 'c' or check):
            self.perform_flop()

    def perform_flop(self):
        self.street = 1
        self.active_player = 0
        self.community_card = self.deck.draw()
        print('com card = {}'.format(self.community_card))
        self.history.append(' ')

    def get_active_player(self):
        return self.players[self.active_player]

    def get_representation(self):
        player = self.get_active_player()
        hand = player.card if self.street == 0 else player.card+self.community_card
        hand_rank = rank(hand)
        history_str = "/".join(self.history)
        return '{}-{}'.format(hand_rank, history_str)

    def display_round_str(self):
        print(str(self.get_active_player()))
        if self.street ==1:
            print("And the community card is {}.".format(self.community_card))