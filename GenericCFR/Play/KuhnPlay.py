import * from genericPlay

def rank(cards):
    ranks = {
        'K': 3,
        'Q': 2,
        'J': 1
    }
    return ranks[cards]


class Player:
    def __init__(self, name, hand, money):
        self.name = name
        self.hand = hand
        self.money = money

    def get_action(self, gamestate):
        possible_actions = gamestate.get_actions()
        print("what be yere action")
        action = vald.getChoice(possible_actions) 
        return action

    def __str__(self):
        print("It is {} turn, they hold {} and have £{}.".format(self.name, self.hand, self.money))


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


class Kuhn(GameState):
    def __init__(self, opp_strategy):
        self.num_players = 2
        self.history = ''
        self.active_player = 0
        deck = ['J', 'Q', 'K']
        self.cards =  random.sample(deck, self.num_players)

        #strat = importstrat(opp_strategy)

        self.players = []
        plyr_name = input("what be yere name")
        players.append(Player(plyr_name, cards[0], 10))
        players.append(AiPlayer(opp_strategy, cards[1], 10, strat))
        
    def new_round():
        self.history = ''
        self.active_player = 0
        deck = ['J', 'Q', 'K']
        self.cards =  random.sample(deck, self.num_players)
        for i in range(len(self.players)):
            self.players[i].hand = cards[i] 


    def is_terminal(self):
        terminal_strings = ['pp', 'bb', 'bp']
        return self.history[-2:] in terminal_strings

    def get_rewards(self):
        plyr = self.active_player
        opp = (self.active_player+1)%2
        player_card = rank(self.cards[plyr])
        opponent_card = rank(self.cards[opp])

        if self.history[-1] == 'p':
            rwds = [-1,-1]
            if self.history[-2:] == 'pp': #double pass
                rwds[plyr if player_card > opponent_card else opp] = 1
            else: #bet followed by fold
                rwds[plyr] = 1
        else: #double bet
            rwds = [-2,-2]
            rwds[plyr if player_card > opponent_card else opp] = 2
        return rwds

    def get_actions(self):
        if self.history in ['','p']:
            return ['Check', 'Bet']
        elif self.history[-1] = 'b'
            return ['Fold', 'Call']

    def handle_action(self, action):
        player = self.get_active_player()
        print("{} has chosen to {}.".format(player.name, action))
        act = 'p' if action in ['Fold', 'Check'] else 'b'
        self.history += act
        self.active_player = (self.active_player + 1) % self.num_players


    def get_active_player(self):
        return self.players[self.active_player]

    def get_representation(self):
        card = str(self.cards[self.active_player])
        key = card + ' ' + self.history
        return key


if __name__ == "__main__":
    if len(sys.argv) < 2:
        strategy = 'defaultkuhn'
    else:
        strategy = str(sys.argv[1])


    game = Game()
    game.play(Kuhn, strategy)
    
