from random import shuffle


class Round:
    def __init__(self, n_communitycards, raise_amount, num_raises):
        self.n_communitycards = n_communitycards #num of cards added to community pool
        self.raise_amount = raise_amount #amount each raise is worth
        self.num_raises = num_raises #max number of possible raises


class Rules:
    def __init__(self, 
            round_s, vals, suits, hand_size, blinds,
            get_representation, get_rank
        ):
        self.hand_size = hand_size
        self.blinds = blinds
        self.round_s = round_s
        self.finalround = len(self.round_s) - 1
        self.deck = self.build_deck(vals, suits)
        self.lookuptable = {}
        for ic, card in enumerate(self.deck):
            self.lookuptable[card] = ic

        self.get_representation = get_representation
        self.get_rank = get_rank

    def build_deck(self, vals, suits):
        deck = []
        for suit in suits:
            for val in vals:
                deck.append(str(val)+suit)
        shuffle(deck)
        return deck


#-------------------------------------------------------
#STANDARD KUHN POKER
def get_rank_kuhn(card):
    ranks = {'K': 3, 'Q': 2, 'J': 1}
    return ranks[card[0][0]]

def get_representation_kuhn(hand, history):
    conv = {'f': 'p', 'ch': 'p', 'c': 'b', 'r': 'b'}
    history_str = "".join([conv[i] for i in history])
    return str(hand[0][0])+history_str

KuhnRules = Rules([Round(0,1,1)], ['J','Q','K'], ['♥'], 1, 1,
    get_representation_kuhn, get_rank_kuhn)
#-------------------------------------------------------
#(https://www.cs.cmu.edu/~ggordon/ggordon.CMU-CALD-05-112.no-regret.pdf)
# is a generalization of Kuhn Poker
def get_rank_onecardpoker(card):
    return int(card[0][:-1])

def get_representation_onecardpoker(hand, history):
    conv = {'f': 'p', 'ch': 'p', 'c': 'b', 'r': 'b'}
    history_str = "".join([conv[i] for i in history])
    return str(hand[0][:-1])+history_str

OnecardpokerRules = Rules([Round(0,1,1)], range(100), ['♥'], 1, 1,
    get_representation_onecardpoker, get_rank_onecardpoker)
#-------------------------------------------------------

def get_rank_leduc(cards):
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

def get_representation_leduc(hand, history):
    repr = ''.join([x[0] for x in hand])
    history_str = ".".join(history)
    return '{}-{}'.format(repr, history_str)

LeducRules = Rules([Round(1,2,2), Round(0,4,2)],
    ['J','Q','K'], ['♥','♦'], 1, 1,
    get_representation_leduc, get_rank_leduc)
#-------------------------------------------------------

def get_rank_royal():
    pass

def get_representation_royal():
    pass

RoyalRules = Rules([Round(1,2,2), Round(1,4,2), Round(0,4,2)],
    ['J','Q','K','A'], ['♥','♦'], 1, 1,
    get_representation_royal, get_rank_royal)




