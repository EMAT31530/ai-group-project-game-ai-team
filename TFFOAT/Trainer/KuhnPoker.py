from cfr import *
from exploitability import *

class Kuhn(GameState):
    def __init__(self):
        self.num_players = 2
        self.history = ''
        self.active_player = 0
        self.deck = ['J', 'Q', 'K']
        self.cards =  [0] * 2

    def is_terminal(self):
        terminal_strings = ['pp', 'bb', 'bp']
        return self.history[-2:] in terminal_strings

    def is_chance(self):
        if self.history == '' or self.history == 'd':
            return 'pr'
        else:
            return False

    def get_rewards(self):
        player = self.get_active_player_index()
        player_rank = ranking[self.cards[player]]
        opponent_rank = ranking[self.cards[1-player]]

        if self.history[-1] == 'p':
            if self.history[-2:] == 'pp': #double pass
                return 1 if player_rank > opponent_rank else -1
            else: #bet followed by fold
                return 1
        else: #double bet
            return 2 if player_rank > opponent_rank else -2

    def get_actions(self):
        return ['p', 'b']

    def handle_action(self, action):
        next_state = copy.deepcopy(self)
        next_state.history += action
        player = next_state.get_active_player_index()
        next_state.active_player = (1 - player)
        return next_state

    def handle_public_chance(self, chance_outcome):
        pass #no public chance nodes in kuhn

    def get_public_chanceoutcomes(self):
        pass #no public chance nodes in kuhn

    def get_private_chanceoutcomes(self):
        return self.deck

    def handle_private_chance(self, chance_outcome):
        next_state = copy.deepcopy(self)  
        player = next_state.get_active_player_index()
        next_state.active_player = (1 - player)
        next_state.history += 'd' #d for dummy action

        next_state.deck.remove(chance_outcome)
        next_state.cards[player] = chance_outcome
        return next_state

    def get_active_player_index(self):
        return self.active_player

    def get_representation(self):
        player = self.get_active_player_index()
        card = str(self.cards[player])
        key = card + ' ' + self.history[2:] #removes the dummy actions
        return key



ranking = {'J': 1, 'Q': 2, 'K': 3}

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
        iterations = 2
    else:
        iterations = int(sys.argv[1])
    
    train = False

    if train:
        time1 = time.time()
        trainer = VCFRTrainer(Kuhn)

        util = trainer.train(n_iterations=iterations)
        print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
        print('With {} nodes.'.format(sys.getsizeof(trainer)))

        display_results(util, trainer.get_final_strategy())
    else:
        time1 = time.time()
        trainer = VCFRTrainer(Kuhn)
        ExplCalc = Exploit_Calc()
        util = 0
        exploit = []
        timestep = []
        stepsize = 10
        steps = int(iterations/stepsize)
        for i in range(stepsize):
            util += trainer.train(n_iterations=steps)
            exploit.append(round(ExplCalc.compute_exploitability(trainer)[0] , 3))
            timestep.append(steps * (i+1))


        print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
        print('With {} nodes.'.format(sys.getsizeof(trainer)))
        display_results(util, trainer.get_final_strategy())
        print(exploit)