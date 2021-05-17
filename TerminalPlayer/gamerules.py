class Round:
    def __init__(self, n_communitycards, raise_amount, num_raises):
        self.n_communitycards = n_communitycards #num of cards added to community pool
        self.raise_amount = raise_amount #amount each raise is worth
        self.num_raises = num_raises #max number of possible raises

class GameRules:
    def __init__(self, 
            DECK_SPEC, round_s, 
            hand_size, blinds, start_money,
            get_representation, get_rank
        ):
        self.DECK_SPEC = DECK_SPEC
        self.hand_size = hand_size
        self.blinds = blinds
        self.start_money = start_money
        self.round_s = round_s
        self.finalround = len(self.round_s) - 1

        self.get_representation = get_representation
        self.get_rank = get_rank

#-------------------------------------------------------
#STANDARD KUHN POKER
def get_rank_kuhn(card):
    ranks = {'K': 3, 'Q': 2, 'J': 1}
    return ranks[card[0][0]]

def get_representation_kuhn(hand, history):
    conv = {'fold': 'p', 'check': 'p', 'call': 'b', 'raise': 'b'}
    history_str = "".join([conv[i.lower()] for i in history])
    return str(hand[0][0])+history_str

kuhnrules = GameRules(
    {"J": {"diamonds": 1}, "Q": {"diamonds": 2}, "K": {"diamonds": 3}},
    [Round(0,1,1)], 1, 1, 10, 
    get_representation_kuhn, get_rank_kuhn
    )
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
    repr = ''.join([x.face for x in cards])
    return ranks[repr]

def get_representation_leduc(hand, history):
    conv = {'check': 'ch', 'fold': 'f', 'call': 'c', 'raise': 'r'}, 
    repr = ''.join([x.face for x in hand])
    history_str = ".".join([conv[i.lower()] for i in history])
    return '{}-{}'.format(repr, history_str)
    
leducrules = GameRules(
    {"J": {"diamonds": 1, "hearts": 1}, "Q": {"diamonds": 2, "hearts": 2}, 
    "K": {"diamonds": 3, "hearts": 3}}, [Round(1,2,2), Round(0,4,2)],
    1, 1, 25,
    get_representation_leduc, get_rank_leduc
    )
#-------------------------------------------------------
