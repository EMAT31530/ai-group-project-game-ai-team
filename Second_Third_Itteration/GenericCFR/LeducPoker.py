from generic import *


def rank(cards):
    ranks = {
        'KK': 9,
        'QQ': 8,
        'JJ': 7,
        'KQ': 6, 'QK': 6,
        'KJ': 5, 'JK': 5,
        'QJ': 4, 'JQ': 4,
        'K': 3, 'Q': 2, 'J': 1
    }
    repr = ''.join([x[0] for x in cards])
    return ranks[repr]


def build_deck():  # To build a deck, can be used to rebuild also
    cards = []
    vals = ['J', 'Q', 'K']
    for suit in range(2):
        for i in range(0, 3):
            cards.append(vals[i]+'♥♦'[suit])
    random.shuffle(cards)
    return cards


class Leduc(GameState):
    def __init__(self):
        self.history = [' ']
        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.current_bets = [1, 1]
        self.active_player = 0
        self.hands = []
        self.deck = []

    def initiate_round(self): #only priv node is drawing inital hands
        self.deck = build_deck()
        self.hands = [self.deck.pop(-1), self.deck.pop(-1)]
        
    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street == 0:
            return fold
        check =  history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return fold or check or call

    def is_chance(self):
        call = self.history[-1] == 'c'
        check = self.history[-1] == 'ch' and self.history[-2] == 'ch'
        if call or check:
            return 'P' #P Public chance node
        else:
            return 'N' #Not

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
        player = next_state.get_active_player_index()
        if action in ['r','rr','c']:
            next_state.bet_amounts[player] += 2 * (next_state.street + 1)
        next_state.history.append(action)
        next_state.active_player = (1 - player)
        return next_state

    def sample_public_chance(self): #only public chance node is the flop
        next_state = copy.deepcopy(self)
        next_state.street = 1
        next_state.active_player = 0
        next_state.community_card = next_state.deck.pop(-1)
        next_state.history.append(' ') #dummy action

        #following final public chance event, hand sorting can be computed and stored!
        return next_state


    def get_active_player_index(self):
        return self.active_player

    def get_representation(self, player):
        hand_rank = rank(self.hands[player])
        community_rank = '' if self.street == 0 else rank(self.community_card)
        history_str = "/".join(self.history)
        return '{}|{}-{}'.format(hand_rank, community_rank, history_str)

    def get_rewards(self):
        player = self.get_active_player_index()
        opponent = 1 - player

        if self.history[-1] == 'f':
            return self.current_bets[opponent]

        player_rank = rank([self.hands[player], self.community_card])
        opponent_rank = rank([self.hands[opponent], self.community_card])
        if player_rank > opponent_rank:
            return self.current_bets[opponent]
        elif player_rank < opponent_rank:
            return -self.current_bets[player]
        else:
            return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 20000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = PCSCFRPlusTrainer()


    util = trainer.train(Leduc, n_iterations=iterations)
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(trainer.nodeMap)))


    display_results(util, trainer.get_final_strategy())
