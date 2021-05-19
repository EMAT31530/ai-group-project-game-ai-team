from Trainer.gamestates.blankgamestate import GenericPoker
from Trainer.gamestates.gamerules import Rules, Round
from Trainer.gamestates.TexasModules.ranking import get_ranking
from Abstraction.Arnold import get_representation_Texas
import copy 


TexasRules = Rules([Round(3,2,3),Round(1,2,3),Round(1,2,3),Round(0,2,3)], 
    range(2,15), ['♥','♦','♣','♠'], 2, 1,
    get_representation_Texas, get_ranking)


class HUNLHPoker(GenericPoker):
    def is_terminal(self): #btec for now
        history_str = ''.join(self.history)
        if history_str.contains('Arc'): #contains is placeholder
            return True
        fold = history_str.endswith('f')
        if self.street != 'r':
            return fold
        else:
            check = history_str.endswith('ch'*2)
            call = history_str.endswith('c')
            return fold or check or call

    def is_chance(self):
        history_str = ''.join(self.history)
        if history_str.contains('Arc'): #contains is placeholder
            return True
        check = history_str.endswith('ch'*2)
        call = history_str.endswith('c')
        return call or check

    def get_actions(self):
        history_str = ''.join(self.history)
        raises = ARNOLD.getraises() #if no limit
        if self.history == [] or history_str.endswith(('d','ch')):
            return ['ch'] + raises
        elif history_str.endswith('r'):
            return ['f', 'c'] + raises
        elif history_str.endswith('R') or history_str.endswith('Ar'): 
            return ['f', 'c'] #max num of raises or all in raise

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


