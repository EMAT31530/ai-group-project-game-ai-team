import * from genericPlay

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

def actions(action):
    acts = {
            'Check': 'ch',
            'Fold': 'f',
            'Call': 'c',
            'Raise': 'r',
            'Reraise': 'rr'
        }
    return acts[action]


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
    def __init__(self, name, hand, money):
        self.name = name
        self.hand = hand
        self.money = money
        self.bet_amount = 1

    def get_action(self, gamestate):
        possible_actions = gamestate.get_actions()
        print("what be yere action")
        action = vald.getChoice(possible_actions) 
        return action

    def __str__(self):
        return str("It is {} turn, they hold {} and have £{}.".format(self.name, self.hand, self.money))


class AiPlayer(Player):
    def __init__(self, name, money, strategyMap = {}):
        Player.__init__(self, name, money)
        self.strategyMap = dict(strategyMap)

    def get_action(self, gamestate):
        possible_actions = gamestate.get_actions()
        key = gamestate.get_representation()
        strategy = self.strategyMap[key]
        action = np.random.choice(possible_actions, p=strategy)
        return action


class Leduc(GameState):
    def __init__(self, opp_strategy):
        self.num_players = 2
        self.history = [' ']

        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.pot = 2

        self.active_player = 0

        self.deck = Deck()
        #strat = importstrat(opp_strategy)

        self.players = []
        plyr_name = input("what be yere name")
        players.append(Player(plyr_name, self.deck.draw(), 50))
        players.append(AiPlayer(opp_strategy, self.deck.draw(), 50, strat))
        
    def new_round(self):
        self.history = [' ']

        self.street = 0 #street is one of preflop [0], postflop [1]
        self.community_card = 0
        self.pot = 2
        self.deck = Deck()
        for player in self.players:
            player.hand = self.deck.draw()
            player.bet_amount = 1
            
    
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
        if prev_action == 'f':
            rwds[opp_index] = -(opp.bet_amount)
            return rwds

        player_rank = rank(plyr.card + self.community_card)
        opponent_rank = rank(opp.card + self.community_card)

        if player_rank < opponent_rank:
            rwds[opp_index] = -(opp.bet_amount)
        else:
            rwds[index] = -(plyr.bet_amount)
        return rwds
            

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

        act = actions[action]


        if act in ['r','rr','c']:
            self.pot += 2 * (self.street + 1)
            player.bet_amount += 2 * (self.street + 1)

        check = self.history[-1] == 'ch' and action == 'ch'
        if self.street == 0 and (action == 'c' or check):
            self.perform_flop()

        self.history.append(act)
        self.active_player = (self.active_player + 1) % self.num_players


    def get_active_player(self):
        return self.players[self.active_player]

    def get_representation(self):
        player = self.get_active_player()
        hand = player.card if self.street == 0 else player.card+self.community_card
        hand_rank = rank(hand)
        history_str = "/".join(self.history)
        return '{}-{}'.format(hand_rank, history_str)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        strategy = 'defaultleduc'
    else:
        strategy = str(sys.argv[1])


    game = Game()
    game.play(Leduc, strategy)
    
