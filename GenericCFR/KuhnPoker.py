from generic import *

class Kuhn(GameState):
    def __init__(self):
        self.num_players = 2
        self.history = ''
        self.active_player = 0
        deck = [0, 1, 2]
        self.cards =  random.sample(deck, self.num_players)

    def is_terminal(self):
        terminal_strings = ['pp', 'bb', 'bp']
        return self.history[-2:] in terminal_strings

    def get_rewards(self):
        player_card = self.cards[self.active_player]
        opponent_card = self.cards[(self.active_player+1)%2]

        if self.history[-1] == 'p':
            if self.history[-2:] == 'pp': #double pass
                return 1 if player_card > opponent_card else -1
            else: #bet followed by fold
                return 1
        else: #double bet
            return 2 if player_card > opponent_card else -2

    def get_actions(self):
        return ['p', 'b']

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        next_state.history += action
        next_state.active_player = (next_state.active_player + 1) % self.num_players
        return next_state

    def get_active_player(self):
        return self.active_player

    def get_index(self, player):
        return self.active_player

    def get_representation(self):
        card = str(self.cards[self.active_player])
        key = card + ' ' + self.history
        return key






if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterations = 20000
    else:
        iterations = int(sys.argv[1])

    time1 = time.time()
    trainer = MCCFRTrainer()
    util = trainer.train(Kuhn, n_iterations=iterations)
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(sys.getsizeof(trainer)))

    display_results(util, trainer.get_final_strategy())

    if len(sys.argv) > 2:
        filename = str(sys.argv[2]).lower()
        exportJson(trainer.get_final_strategy(), filename)
        print('Exported trained strategy as {}.json '.format(filename))
