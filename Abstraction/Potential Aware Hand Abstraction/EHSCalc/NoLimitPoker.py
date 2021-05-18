import ranking as rank
import random

def build_deck():  # To build a deck, can be used to rebuild also
    cards = []
    for suit in range(4):
        for i in range(10, 15):
            cards.append(str(i)+'♥♦♣♠'[suit])
    random.shuffle(cards)
    return cards
deck = build_deck()
print(len(deck))

class NoLimit(Gamestate):
    def __init__(self):
        self.private_states = 1326
        self.history = [' ']
        self.street = 'p' #p,f,t,r
        self.board = []
        #self.blind = 2 #w/e
        self.active_player = 0

        #intial implem
        self.hands = []
        self.hands_sorting = []
        self.current_bets = [0, 0]
        self.deck = build_deck()

    def is_terminal(self): #btec for now
        history_str = ''.join(self.history)
        fold = history_str.endswith('f')
        if self.street != 'r':
            return fold
        else:
            check = history_str.endswith('ch'*2)
            call = history_str.endswith('c')
            allin = history_str.contains('Arc') #contains is placeholder
            return fold or check or call or allin

    def is_chance(self):
        if len(self.history) == 1:
            return 'C' #C private chance nodes

        call = action == 'c'
        check = self.history[-1] == 'ch' and action == 'ch'
        allin = ['Ar', 'c'] in self.history #needs to change ofc
        if call or check or allin:
            return 'P' #P Public chance node

        return 'N'


#winnings is (pot)/2 and something to do with blinds in there
#apart from when one player folds, then remove last bet from pot first

#rn this function is a H2H function in effect
    def get_rewards(self):
        player = self.get_active_player_index()
        opponent = 1 - player

        if self.history[-1] == 'f':
            return self.current_bets[opponent]

        player_rank = rank.ranking('player.hand', self.board)
        opponent_rank = rank.ranking('opponent.hand', self.board)
        if player_rank < opponent_rank:
            return self.current_bets[opponent]
        elif player_rank > opponent_rank:
            return -self.current_bets[player]
        else:
            return 0

    def get_actions(self):
        prev_action = self.history[-1]
        raises = ARNOLD.getraises()

        fullraise = ''.join([x[0] for x in self.history]).endswith('r'*4)
        if prev_action in [' ','ch']:
            return ['ch'] + raises
        elif prev_action[0]=='r':
            return ['f', 'c'] if fullraise else ['f', 'c'] + raises
        elif prev_action == 'Ar': #all in
            return ['f', 'c']

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        next_state.history.append(action)

        player = next_state.get_active_player_index()
        next_state.active_player = (next_state.active_player + 1) % 2

        if action[0] == 'r': #raise
            next_state.current_bets[player] += int(action[0:])
        elif action == 'Ai': #all in
            next_state.current_bets[player] = 20000
        if action == 'c': #call
            next_state.current_bets[player] = next_state.current_bets[(player+1)%2]
        return next_state

    def sample_public_chance(self):
        next_state = copy.deepcopy(self)

        if self.street == 'p':
            next_state.street = 'f'
            next_state.board.append(next_state.deck.pop(-1))
            next_state.board.append(next_state.deck.pop(-1))
        elif self.street == 'f':
            next_state.street = 't'
        elif self.street == 't':
            next_state.street = 'r'
            #following final public chance event, hand sorting can be computed and stored!


        next_state.board.append(next_state.deck.pop(-1))
        next_state.active_player = 0
        next_state.history.append(' ') #dummy action
        return next_state

    def handle_private_chance(self):
        next_state = copy.deepcopy(self)
        two_card_perms = itertools.combinations(next_state.deck, 2)
        next_state.hands = two_card_perms * 2
        next_state.history.append(' ') #dummy action
        return next_state

    def get_active_player_index(self):
        return self.active_player

    def get_player(self, index):
        return self.players[index]

    def get_representation(self):
        pass


lookuptable = {'2♥': 0, '3♥': 1, '4♥': 2, '5♥': 3, '6♥': 4, '7♥': 5, '8♥': 6, '9♥': 7, '10♥': 8,
 '11♥': 9, '12♥': 10, '13♥': 11, '14♥': 12, '2♦': 13, '3♦': 14, '4♦': 15, '5♦': 16,
  '6♦': 17, '7♦': 18, '8♦': 19, '9♦': 20, '10♦': 21, '11♦': 22, '12♦': 23, '13♦': 24,
   '14♦': 25, '2♣': 26, '3♣': 27, '4♣': 28, '5♣': 29, '6♣': 30, '7♣': 31, '8♣': 32,
    '9♣': 33, '10♣': 34, '11♣': 35, '12♣': 36, '13♣': 37, '14♣': 38, '2♠': 39, '3♠': 40,
     '4♠': 41, '5♠': 42, '6♠': 43, '7♠': 44, '8♠': 45, '9♠': 46, '10♠': 47, '11♠': 48, '12♠': 49,
      '13♠': 50, '14♠': 51}
