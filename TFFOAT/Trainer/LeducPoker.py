from cfr import *


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
    return ranks[cards]


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
        self.bet_amounts = [1, 1]
        self.active_player = 0
        self.cards = [0,0]
        self.deck = build_deck()

    def is_terminal(self):
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street == 0:
            return fold
        check =  history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return fold or check or call

    def is_chance(self):
        if self.history[-1] == ' ' or self.history[-2] == ' ' and self.history[-1] == 'd':
            return 'pr' #Private chance node

        call = self.history[-1] == 'c'
        check = self.history[-1] == 'ch' and self.history[-2] == 'ch'
        if call or check:
            return 'pu' #Public chance node
        else:
            return False #Not

    def get_actions(self):
        prev_action = self.history[-1]
        if prev_action in ['d',' ','ch']:
            return ['ch', 'r']
        elif prev_action=='r':
            return ['f', 'c', 'rr']
        elif prev_action=='rr':
            return ['f', 'c']

    def get_public_chanceoutcomes(self):
        return self.deck

    def get_private_chanceoutcomes(self):
        return self.deck

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        player = next_state.get_active_player_index()
        if action in ['r','rr','c']:
            next_state.bet_amounts[player] += 2 * (next_state.street + 1)
        next_state.history.append(action)
        next_state.active_player = (1 - player)
        return next_state

    def handle_private_chance(self, chance_outcome):
        next_state = copy.deepcopy(self)  
        player = next_state.get_active_player_index()
        next_state.active_player = (1 - player)
        next_state.history.append('d') #d for dummy action

        next_state.deck.remove(chance_outcome)
        next_state.cards[player] = chance_outcome
        return next_state

    def handle_public_chance(self, chance_outcome):
        next_state = copy.deepcopy(self)
        next_state.street = 1
        next_state.active_player = 0
        next_state.community_card = chance_outcome
        next_state.history.append(' ') #dummy action
        return next_state


    def get_active_player_index(self):
        return self.active_player

    def get_representation(self):
        player = self.get_active_player_index()
        hand_rank = rank(self.cards[player][0])
        community_rank = '' if self.street == 0 else rank(self.community_card[0])
        history_str = "/".join(self.history[3:])
        return '{}|{}-{}'.format(hand_rank, community_rank, history_str)

    def get_rewards(self):
        player = self.get_active_player_index()
        opponent = 1 - player

        if self.history[-1] == 'f':
            return self.bet_amounts[opponent]

        player_rank = rank(self.cards[player][0]+self.community_card[0])
        opponent_rank = rank(self.cards[opponent][0]+self.community_card[0])
        if player_rank > opponent_rank:
            return self.bet_amounts[opponent]
        elif player_rank < opponent_rank:
            return -self.bet_amounts[player]
        else:
            return 0

def display_results(ev, node_map):
    print('\nplayer 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))
    print('\nplayer 1 strategies:')
    #print([i for i in node_map.items()])
    sorted_items = sorted(node_map.items(), key=lambda x: ranking[x[0][0]])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))
    print('\nplayer 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 20000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = VCFRTrainer()


    util = trainer.train(Leduc, n_iterations=iterations)
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(trainer.nodeMap)))


    display_results(util, trainer.get_final_strategy())
