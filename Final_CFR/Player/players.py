import sys
sys.path.append('../modules')
from validation import getChoice
import numpy as np

class Player:
    def __init__(self, name, money):
        self.name = name
        self.cards = []
        self.money = money

    def get_action(self, gamestate):
        possible_actions = gamestate.get_actions()
        action = getChoice(possible_actions)
        return action


class AiPlayer(Player):
    def __init__(self, name, money, strategyMap = {}):
        Player.__init__(self, name, money)
        self.strategyMap = dict(strategyMap)

    def get_action(self, gamestate):
        possible_actions = gamestate.get_actions()
        key = gamestate.get_representation(self.cards)
        strategy = self.strategyMap[key]
        action = np.random.choice(possible_actions, p=strategy)
        return action
