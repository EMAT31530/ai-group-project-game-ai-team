from generic import *


def rank(cards):
    ranks = {
        'KK': 1,
        'QQ': 2,
        'JJ': 3,
        'KQ': 4, 'QK': 4,
        'KJ': 5, 'JK': 5,
        'QJ': 6, 'JQ': 6,
        'K': 7, 'Q': 8, 'J': 9
    }
    return ranks[cards]


class Deck:  # Object to represent deck throughout game
    def __init__(self):
        self.cards = []
        self.build()

    def __str__(self):  # Overwrites the String fucntion
        return str([str(card) for card in self.cards])

    def build(self):  # To build a deck, can be used to rebuild also
        self.cards = []
        vals = ['J', 'Q', 'K']
        for suit in range(2):  # ["Hearts", "Diamonds"]
            for i in range(0, 3):
                self.cards.append(vals[i])
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(-1)  # Removes and returns the top card


class Player:
    def __init__(self, card):
        self.card = card
        self.bet_amount = 1


class Leduc(GameState):
    def __init__(self):
        self.num_players = 2
        self.history = [' ']

        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.pot = 2

        self.active_player = 0
        self.players = []
        self.deck = Deck()
        for i in range(2):
            self.players.append(Player(self.deck.draw()))

    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street == 0:
            return fold

        check =  history_str.endswith('ch'*2)
        fullraise = history_str.endswith('c')
        return fold or check or fullraise

    def get_rewards(self):
        prev_action = self.history[-1]
        player = self.get_active_player()

        if prev_action == 'f':
            return (self.pot - player.bet_amount)

        opponent = self.players[(self.active_player+1)%2]
        player_rank = rank(player.card + self.community_card)
        opponent_rank = rank(opponent.card + self.community_card)
        if player_rank < opponent_rank:
            return self.pot - player.bet_amount
        else:
            return -(self.pot - opponent.bet_amount)

    def get_actions(self):
        prev_action = self.history[-1]
        if prev_action in [' ','ch']:
            return ['ch', 'r']
        elif prev_action=='r':
            return ['f', 'c', 'rr']
        elif prev_action=='rr':
            return ['f', 'c']

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        next_state.history.append(action)

        active_player = next_state.get_active_player()
        next_state.active_player = (next_state.active_player + 1) % self.num_players

        if action in ['r','rr','c']:
            next_state.pot += 2 * (self.street + 1)
            active_player.bet_amount += 2 * (self.street + 1)

        check = self.history[-1] == 'ch' and action == 'ch'
        call = action == 'c'
        if self.street == 0 and (call or check):
            next_state.perform_flop()

        return next_state

    def perform_flop(self):
        self.street = 1
        self.active_player = 0
        self.community_card = self.deck.draw()
        self.history.append(' ')

    def get_active_player(self):
        return self.players[self.active_player]

    def get_index(self, player):
        return self.players.index(player)

    def get_representation(self):
        player = self.get_active_player()
        hand = player.card if self.street == 0 else player.card+self.community_card
        hand_rank = rank(hand)
        history_str = "/".join(self.history)
        return '{}-{}'.format(hand_rank, history_str)




if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 20000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = MCCFRTrainer()

    print("Running CFR for 1000 iterations")
    trainer.train(Leduc, 1000)
    print("Resetting strategy sums")
    trainer.reset()

    util = trainer.train(Leduc, n_iterations=iterations)
    print('Completed {}+1000 iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(trainer.nodeMap)))


    display_results(util, trainer.get_final_strategy())

    if len(sys.argv) > 2:
        filename = str(sys.argv[2]).lower()
        exportJson(trainer.get_final_strategy(), filename)
        print('Exported trained strategy as {}.json '.format(filename))
