from generic import *
import ranking as rank


class Deck:  # Object to represent deck throughout game
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):  # To build a deck, can be used to rebuild also
        self.cards = []
        for suit in range(4):
            for i in range(2, 15):
                self.cards.append(str(i)+'♥♦♣♠'[suit])
        self.shuffle()

    def shuffle(self):
        rnd.shuffle(self.cards)

    def draw(self, burn=False):
        if burn:  # Removes the top card from the deck
            del self.cards[-1]
        return self.cards.pop(-1)  # Removes and returns the top card

class Player:  # Object to represent player
    def __init__(self):
        self.hand = []
        self.bet_amount = 0
        self.state = 0  # 0: in round, 1: called, 2: folded, 3: for blinds so they act last, 4: all in, 5: player has checked, 6: player is not permitted to raise


class NoLimit(Gamestate):
    def __init__(self):
        self.num_players = 2
        self.history = [' ']

        self.street = 'p' #p,f,t,r
        self.board = []
        self.pot = 0

        self.active_player = 0
        self.players = [Player(),Player()]
        self.deck = Deck()
        for i in range(2):
            self.players[0].append(self.deck.draw())
            self.players[1].append(self.deck.draw())

    def is_terminal(self): #btec for now
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')

        check =  history_str.endswith('ch'*2) and self.street == 'r'
        fullraise = history_str.endswith('rrrrc') and self.street == 'r'
        return fold or check or fullraise

    def get_rewards(self):
        prev_action = self.history[-1]
        player = self.get_active_player()

        if prev_action == 'f':
            return (self.pot - player.bet_amount)

        opponent = self.players[(self.active_player+1)%2]
        player_rank = rank.ranking(player.hand, self.board)
        opponent_rank = rank.ranking(opponent.hand, self.board)
        if player_rank < opponent_rank:
            return self.pot - player.bet_amount
        elif player_rank > opponent_rank:
            return -(self.pot - opponent.bet_amount)
        else:
            return 0

    def get_actions(self):
        return getActions(self, player)

    def handle_action(self, player, action):
        return handleAction(self, player, action)

    def get_active_player(self):
        return self.players[self.active_player]

    def get_index(self, player):
        return self.players.index(player)

    def get_representation(self):
        return getRepresentation(self)
