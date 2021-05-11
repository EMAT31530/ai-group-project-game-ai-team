from genericPlay import *

def rank(cards):
    ranks = {
        'K': 2,
        'Q': 1,
        'J': 0
    }
    return str(ranks[cards])


class Player:
    def __init__(self, name, money):
        self.name = name
        self.card = 0
        self.money = money

    def get_action(self, gamestate):
        possible_actions = gamestate.get_actions()
        print("What be yere action?")
        action = vald.getChoice(possible_actions)
        return action

    def __str__(self):
        return "It is your turn, you hold {} and have £{}.".format(self.card, self.money)


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

    def __str__(self):
        return "It is {}'s turn, they have £{}.".format(self.name, self.money)

class Kuhn(GameState):
    def __init__(self, opp_strategy):
        self.num_players = 2
        self.history = ''
        self.active_player = 0
        self.deck = ['J', 'Q', 'K']

        strat_map = vald.importJson(opp_strategy)

        self.players = []
        plyr_name = input("what be yere name? ")
        self.players.append(AiPlayer(opp_strategy, 10, strat_map))
        self.players.append(Player(plyr_name, 10))


    def new_round(self):
        self.history = ''
        self.active_player = 0
        cards =  random.sample(self.deck, self.num_players)
        for i in range(len(self.players)):
            self.players[i].card = cards[i]
        self.players.reverse()

    def is_terminal(self):
        terminal_strings = ['pp', 'bb', 'bp']
        return self.history[-2:] in terminal_strings

    def get_rewards(self):
        plyr = self.active_player
        opp = (self.active_player+1)%2
        player_card = rank(self.players[plyr].card)
        opponent_card = rank(self.players[opp].card)

        if self.history[-1] == 'p':
            rwds = [-1,-1]
            if self.history[-2:] == 'pp': #double pass
                winr = plyr if player_card > opponent_card else opp
            else: #bet followed by fold
                winr = plyr
        else: #double bet
            rwds = [-2,-2]
            winr = plyr if player_card > opponent_card else opp

        rwds[winr] *= -1
        return rwds, winr

    def get_actions(self):
        if self.history in ['','p']:
            return ['Check', 'Bet']
        elif self.history[-1] == 'b':
            return ['Fold', 'Call']

    def handle_action(self, action):
        player = self.get_active_player()
        print("{} has chosen to {}.\n".format(player.name, action))
        act = 'p' if action.lower() in ['fold', 'check'] else 'b'
        self.history += act
        self.active_player = (self.active_player + 1) % self.num_players

    def get_active_player(self):
        return self.players[self.active_player]

    def get_representation(self):
        card = rank(self.get_active_player().card)
        key = card + ' ' + self.history
        return key

    def display_round_str(self):
        print(str(self.get_active_player()))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        strategy = 'AI1'
    else:
        strategy = str(sys.argv[1])


    game = Game()
    game.play(Kuhn, strategy)
