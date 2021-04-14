from generic import *
import sys
import time

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
        self.history = ['']

        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.pot = 2

        self.active_player = 0
        self.players = []
        self.deck = Deck()
        for i in range(2):
            self.players.append(Player(self.deck.draw()))


    def newround(self):
        self.street = 1
        self.active_player = 0
        self.community_card = self.deck.draw()
        self.history.append('')

    def is_terminal(self):
        fold = self.history[-1] == 'f'
        if self.street == 0:
            return fold

        check =  self.history[-2] ==  'ch' and self.history[-1] == 'ch'
        fullraise = self.history[-1] == 'c'
        return fold or check or fullraise

    def get_rewards(self):
        prev_action = self.history[-1]
        player = self.get_active_player()

        if prev_action == 'f':
            return self.pot - player.bet_amount

        opponent = self.players[(self.active_player+1)%2]
        player_rank = rank(player.card + self.community_card)
        opponent_rank = rank(opponent.card + self.community_card)
        if player_rank > opponent_rank:
            return self.pot - player.bet_amount
        else:
            return -(self.pot - opponent.bet_amount)

    def get_actions(self):
        prev_action = self.history[-1]
        if prev_action in ['','ch']:
            return ['ch', 'r']
        elif prev_action=='r':
            return ['f', 'c', 'rr']
        elif prev_action=='rr':
            return ['f', 'c']

    def handle_action(self, player, action):
        next_state = copy.deepcopy(self)
        next_state.history.append(action)
        next_state.active_player = (next_state.active_player + 1) % self.num_players

        if action in ['r','rr','c']:
            next_state.pot += 2 * (self.street + 1)
            player.bet_amount += 2 * (self.street + 1)
        if action == 'c' and self.street == 0:
            next_state.newround()

        return next_state

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


def display_results(ev, node_map):
    print('\nplayer 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))
    print('\nplayer 1 strategies:')
    sorted_items = sorted(node_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print('\nplayer 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 20000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = MCCFRTrainer()
    trainer.train(Leduc, n_iterations=iterations)
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(sys.getsizeof(trainer)))

    display_results(trainer.expected_game_value, trainer.nodeMap)

    if len(sys.argv) > 2:
        filename = str(sys.argv[2]).lower()
        exportJson(trainer.get_final_strategy(), filename)
        print('Exported trained strategy as {}.json '.format(filename))
