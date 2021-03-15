from KuhnModules import *
import numpy as np
import random as rnd
from .. import validation

class Player:  # Object to represent player
    def __init__(self, name, money):
        self.name = name
        self.card = 0
        self.money = money

class AiPlayer(Player):
    def __init__(self, name, money, strategyMap = {}):
        Player.__init__(self, name, money)
        self.strategyMap = dict(strategyMap)

    def ai_get_strategy(self, actions):
        key = str(self.card) + " " + actions
        return self.strategyMap[key]

class Game:  # Object to represent game
    def __init__(self, aistrategymap = {}):
        self.players = self.buildPlayers(10, aistrategymap)
        self.deck = np.array([0,1,2]) #ze kuhn poker deck
        self.actions = '' #string of actions in a given round
        self.start()

    def buildPlayers(self, initmoney, aistrategymap):
        playerlist = []
        name = validation.checkString("What is your name? ")
        if aistrategymap == {}:
            aistrategymap = self.chooseai()
        playerlist.append(AiPlayer("AIBOT", initmoney, aistrategymap))
        playerlist.append(Player(name, initmoney))
        return playerlist

    def chooseai(self):
        message = "Please input the filename of your chosen AI to compete against. "
        filename = validation.checkJson(input(message))
        strategy = validation.importJson(filename)
        return strategy

    def start(self):
        roundcount = 10
        while not roundcount < 1:
            for i in range(roundcount):
                self.startnewRound()
            roundcount = validation.checkInt("How many more rounds would you like to play? ")

    # Updates round and appends old round to round list
    def startnewRound(self):
        self.actions = '' #resets actions!
        self.players.reverse() #swaps the player order for the new round!
        rnd.shuffle(self.deck) #shuffles the deck
        for i in range(2):
            self.players[i].card = self.deck[i]
        i = 0
        while not is_terminal(self.actions):
            if type(self.players[i]) == AiPlayer:
                strat = self.players[i].strategyMap
                card = self.players[i].card
                aichoice = ai_get_nodestrategy(strat, card, self.actions)
                self.actions += aichoice
                pasbet =  'pass' if aichoice == 'p' else 'bet'
                print("The AIBOT has £{}, and has chosen to {}!!!!".format(self.players[i].money, pasbet))
            else:
                print("You have £{}, and in your hand you have {}.".format(self.players[i].money,self.players[i].card))
                print("Would you like to pass or bet?")
                choice = validation.getChoice(['pass','bet'])
                self.actions += 'p' if choice == 'pass' else 'b'
            i = (i +1) % 2
        player = 0 if type(self.players[0]) == Player else 1
        self.moneyAdj(roundWinnings(self.actions, self.players[0].card, self.players[1].card, train=False, player=player) )

    def moneyAdj(self, money):
        if money > 0:
            print("{} wins £{}.\n".format(self.players[0].name,money))
        else:
            print("{} wins £{}.\n".format(self.players[1].name,-money))
        self.players[0].money += money
        self.players[1].money -= money

if __name__ == "__main__":
    game = game()
