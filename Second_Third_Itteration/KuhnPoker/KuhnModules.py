import numpy as np
import random as rnd

def ai_get_choice(strategy, card, history):
    key = str(card) + " " + history
    ai_p = strategy[key]
    aichoice = np.random.choice(np.array(['p','b']),p=ai_p)
    return aichoice

def is_terminal(history):
    terminal_strings = ['pp', 'bb', 'bp']
    return history[-2:] in terminal_strings

def get_reward(history, player_card, opponent_card, train=True, player=2):
    if history[-1] == 'p':
        if history[-2:] == 'pp': #double pass
            return 1 if player_card > opponent_card else -1
        else: #bet followed by fold
            if train or (len(history) % 2 == 0 and player==0) or (len(history) % 2 == 1 and player==1):
                return 1
            else:
                return -1
    else: #double bet
        return 2 if player_card > opponent_card else -2

def display_results(ev, node_map):
    print('\nplayer 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))
    print('\nplayer 1 strategies:')
    sorted_items = sorted(node_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print('\nplayer 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)
