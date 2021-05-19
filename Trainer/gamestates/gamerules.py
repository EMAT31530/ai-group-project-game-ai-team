from random import shuffle
from Trainer.gamestates.TexasModules.ranking import get_ranking

class Round:
    def __init__(self, n_communitycards, raise_amount, num_raises):
        self.n_communitycards = n_communitycards #num of cards added to community pool
        self.raise_amount = raise_amount #amount each raise is worth
        self.num_raises = num_raises #max number of possible raises


class Rules:
    def __init__(self, 
            round_s, vals, suits, hand_size, blinds,
            get_representation, get_rank, name, pRecall=False
        ):
        self.__name__ = name
        self.hand_size = hand_size
        self.blinds = blinds
        self.round_s = round_s
        self.finalround = len(self.round_s) - 1
        self.deck = self.build_deck(vals, suits)
        self.lookuptable = {}
        for ic, card in enumerate(self.deck):
            self.lookuptable[card] = ic

        self.get_representation = get_representation
        self.pRecall = pRecall
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

def get_representation_kuhn(hand, _, history):
    conv = {'f': 'p', 'ch': 'p', 'c': 'b', 'r': 'b'}
    history_str = "".join([conv[i] for i in history])
    return str(hand[0][0])+history_str

KuhnRules = Rules([Round(0,1,1)], ['J','Q','K'], ['♥'], 1, 1,
    get_representation_kuhn, get_rank_kuhn, 'Kuhn')
#-------------------------------------------------------
#(https://www.cs.cmu.edu/~ggordon/ggordon.CMU-CALD-05-112.no-regret.pdf)
# is a generalization of Kuhn Poker
def get_rank_onecardpoker(card):
    return int(card[0][:-1])

def get_representation_onecardpoker(hand, _, history):
    conv = {'f': 'p', 'ch': 'p', 'c': 'b', 'r': 'b'}
    history_str = "".join([conv[i] for i in history])
    return str(hand[0][:-1])+history_str

OnecardpokerRules = Rules([Round(0,1,1)], range(3), ['♥'], 1, 1,
    get_representation_onecardpoker, get_rank_onecardpoker, 'One Card')
#-------------------------------------------------------

def get_rank_leduc(hand):
    ranks = {
    'KK': 9,
    'QQ': 8,
    'JJ': 7,
    'KQ': 6, 'QK': 6,
    'KJ': 5, 'JK': 5,
    'QJ': 4, 'JQ': 4,
    'K': 3, 'Q': 2, 'J': 1
    }
    repr = ''.join([x[0] for x in hand])
    return ranks[repr]

def get_representation_leduc(hand, board, history):
    cards = hand + board
    repr = ''.join([x[0] for x in cards])
    history_str = "".join([(i if i!='d' else ' ') for i in history])
    return '{}|{}'.format(repr, history_str)

LeducRules = Rules([Round(1,2,2), Round(0,4,2)],
    ['J','Q','K'], ['♥','♦'], 1, 1,
    get_representation_leduc, get_rank_leduc, 'Leduc')
#-------------------------------------------------------

#We assumeimperfect recall. With imperfect recall previous action or chance nodes are for-gotten, and as a consequence several information sets are grouped together. For example, in ourwork we only take into account the current bucket assignment in information sets, and forget pre-vious ones. This way we reduce the game complexity tremendously, which reduces both memoryrequirements and convergence time. In the case of imperfect recall the CFR algorithm loses its con-vergence guarantees to the NE, but even though we lose theoretical guarantees, this application ofimperfect recall has been shown to be practical, specifically in Poker (Waugh, Zinkevich, Johanson,Kan, Schnizlein, & Bowling, 2009) [https://arxiv.org/pdf/1401.4591.pdf]

def get_rank_royal(hand):
    return get_ranking(hand)

def get_representation_royal(hand, board, history, round):
    history_str = ''.join(history)
    if 'd' in history:
        history_str = history_str.split('d')[round]
        
    repr = closest_cluster(hand, board)
    return '{}|{}-{}'.format(repr, round, history_str)

RoyalRules = Rules([Round(1,2,2), Round(1,4,2), Round(0,4,2)],
    range(10,15), ['♥','♦','♣','♠'], 2, 1,
    get_representation_royal, get_rank_royal, 'Royal', pRecall=True)




#---------------------------------------------------------
#Heads up Limit Holdem
def get_rank_HULH(hand):
    return get_ranking(hand)

def get_representation_HULH(hand, history, round):
    #with imperfect recall
    history_str = ('d'.split(''.join(history)))[round]

    pass

HULHRules = Rules([Round(3,2,4),Round(1,2,4),Round(1,2,4),Round(0,2,4)],
    range(2,15), ['♥','♦','♣','♠'], 1, 1,
    get_representation_HULH, get_rank_HULH, 'HULH',pRecall=True)
