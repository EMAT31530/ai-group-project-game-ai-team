import numpy as np
import random as rnd
import time
import sys
import validation as vald
#taken from https://github.com/IanSullivan/PokerCFR under MIT license

class Node:
    def __init__(self, key, action_dict, n_actions=2):
        self.key = key #the label of  the node in the form: [cards, previous actions]
        self.n_actions = n_actions #the number of possible actions taken from said node
        self.regret_sum = np.zeros(self.n_actions) #the sum of the regret at each iteration (for each action)
        self.strategy_sum = np.zeros(self.n_actions) # the sum of the strategy at each iteration (for each action)
        self.action_dict = action_dict #dictionary to label each action
        #the strategy(probability of choosing each action) from each node
        self.strategy = np.repeat(1/self.n_actions, self.n_actions) #initially, equal probability of each action occuring
        self.reach_pr = 0 #probablity of reaching said node (based on the strategy of previous nodes) for an individual iteration
        self.reach_pr_sum = 0 #the sum over all itterations

    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy #adds the strategy for this itteration
        self.reach_pr_sum += self.reach_pr #adds the reach pr for this itteration
        self.strategy = self.get_strategy() #updates the strategy for the next iteration
        self.reach_pr = 0 #resets the reach probablity for the next itteration

    #Returns the strategy for the current regrets, i.e for regrets [50, 50, 100], returns [1/4,1/4,1/2]
    def get_strategy(self):
        regrets = self.regret_sum
        regrets[regrets < 0] = 0 #negative regrets are ignored
        normalizing_sum = sum(regrets) #the total regret
        if normalizing_sum > 0:
            return regrets / normalizing_sum
        else: #if regreats are negative, returns an even probability distribution for each action
            return np.repeat(1/self.n_actions, self.n_actions)

    #to get the final strategy over all iterations
    def get_average_strategy(self):
        strategy = self.strategy_sum / self.reach_pr_sum
        # Re-normalize
        total = sum(strategy)
        strategy /= total
        return strategy

    #it's a str representation init
    def __str__(self):
            strategies = ['{:03.2f}'.format(x)
                          for x in self.get_average_strategy()]
            return '{} {}'.format(self.key.ljust(6), strategies)


class AiKuhnBotTrainer:
    def __init__(self):
        self.nodeMap = {} #Contains all possible nodes
        self.expected_game_value = 0
        self.current_player = 0
        self.deck = np.array([0, 1, 2]) #Three card kuhn poker deck
        self.n_actions = 2 #number of possible actions (pass, bet)

    #Training function
    def train(self, n_iterations=50000):
        expected_game_value = 0
        for _ in range(n_iterations):
            rnd.shuffle(self.deck)
            expected_game_value += self.cfr('', 1, 1)
            for _, v in self.nodeMap.items():
                v.update_strategy()

        expected_game_value /= n_iterations
        display_results(expected_game_value, self.nodeMap)

    #The Counterfactual Regret Minimisation function
    def cfr(self, history, pr_1, pr_2):
        n = len(history)
        is_player_1 = n % 2 == 0
        player_card = self.deck[0] if is_player_1 else self.deck[1]

        if self.is_terminal(history):
            card_player = self.deck[0] if is_player_1 else self.deck[1]
            card_opponent = self.deck[1] if is_player_1 else self.deck[0]
            reward = self.get_reward(history, card_player, card_opponent)
            return reward

        node = self.get_node(player_card, history)
        strategy = node.strategy

        # Counterfactual utility per action.
        action_utils = np.zeros(self.n_actions)

        for act in range(self.n_actions):
            next_history = history + node.action_dict[act]
            if is_player_1:
                action_utils[act] = -1 * self.cfr(next_history, pr_1 * strategy[act], pr_2)
            else:
                action_utils[act] = -1 * self.cfr(next_history, pr_1, pr_2 * strategy[act])

        # Utility of information set.
        util = sum(action_utils * strategy)
        regrets = action_utils - util
        if is_player_1:
            node.reach_pr += pr_1
            node.regret_sum += pr_2 * regrets
        else:
            node.reach_pr += pr_2
            node.regret_sum += pr_1 * regrets

        return util

    #Finds the node within the Ai's NodeMap
    def get_node(self, card, history):
        key = str(card) + " " + history
        if key not in self.nodeMap:
            action_dict = {0: 'p', 1: 'b'}
            info_set = Node(key, action_dict)
            self.nodeMap[key] = info_set
            return info_set
        return self.nodeMap[key]

    def export_results(self):
        finalstrat = {}
        for x in self.nodeMap:
            finalstrat[x] = self.nodeMap[x].get_average_strategy()
        return finalstrat

    #Checks if the round has reached an end state
    @staticmethod
    def is_terminal(history):
        if history[-2:] == 'pp' or history[-2:] == "bb" or history[-2:] == 'bp':
            return True

    #Calculates the reward from a given end state
    @staticmethod
    def get_reward(history, player_card, opponent_card):
        terminal_pass = history[-1] == 'p'
        double_bet = history[-2:] == "bb"
        if terminal_pass:
            if history[-2:] == 'pp':
                return 1 if player_card > opponent_card else -1
            else:
                return 1
        elif double_bet:
            return 2 if player_card > opponent_card else -2

class Player:  # Object to represent player
    def __init__(self, name, money, cpu = False, strategyMap = {}):
        self.name = name
        self.card = 0
        self.money = money
        self.cpu = cpu
        if cpu:
            self.strategyMap = strategyMap

    def ai_get_strategy(self, actions):
        key = str(self.card) + " " + actions
        return self.strategyMap[key]

class Game:  # Object to represent game
    def __init__(self, aistrategymap):
        self.players = self.buildPlayers(10, aistrategymap)
        self.deck = np.array([0,1,2]) #ze kuhn poker deck
        self.actions = '' #string of actions in a given round
        self.start()

    def buildPlayers(self, initmoney, aistrategymap):
        playerlist = []
        name = vald.checkString("What is your name?\n")
        playerlist.append(Player("AIBOT", initmoney, True, aistrategymap))
        playerlist.append(Player(name, initmoney))
        return playerlist

    def start(self):
        while True:
            self.startnewRound()
            if len(self.players) == 1:
                print("{} wins the game with £{}.".format(self.players[0], self.players[0].money))
                print("Good night")
                break
            print("Would you like to play a new round?")
            answer = vald.getChoice(["Yes", "No", "Y", "N"])
            if answer in ["y","yes"]:
                self.startnewRound()
            else:
                print("Good night")
                break

    # Updates round and appends old round to round list
    def startnewRound(self):
        self.actions = '' #resets actions!
        self.players.reverse() #swaps the player order for the new round!
        rnd.shuffle(self.deck) #shuffles the deck
        for i in range(len(self.players)): #gives each player their card
            self.players[i].card = self.deck[0] if i==0 else self.deck[1]
        #PLAY!!!!!
        while True:
            for i in range(2):
                if self.roundTerminate():
                    self.roundWinnings()
                    return 0
                if self.players[i].cpu == True:
                    Aip = self.players[i].ai_get_strategy(self.actions[-2:])
                    Aichoice = np.random.choice(np.array(['p','b']),p=Aip)
                    if Aichoice == 'p':
                        print("The AIBOT has £{}, hand = {}, and has chosen to PASS!!!!".format(self.players[i].money, self.players[i].card))
                    else:
                        print("The AIBOT has £{}, hand = {}, and has chosen to BET!!!!".format(self.players[i].money, self.players[i].card))
                    self.actions += Aichoice
                else:
                    print("You have £{}, and in your hand you have {}.".format(self.players[i].money,self.players[i].card))
                    print("Would you like to pass or bet?")
                    choice = vald.getChoice(['pass','bet'])
                    if choice == 'pass':
                        self.actions += 'p'
                    else:
                        self.actions += 'b'

    def roundTerminate(self):
        if self.actions[-2:] == 'pp' or self.actions[-2:] == "bb" or self.actions[-2:] == 'bp':
            return True

    #divvies out the winnings
    def roundWinnings(self):
        if self.actions[-1] == 'p': #the last action was a pass
            if self.actions[-2:] == 'pp': #both players passed
                if self.players[0].card > self.players[1].card:
                    self.moneyAdj(1)
                else:
                    self.moneyAdj(-1)
            else:
                if len(self.actions) % 2 == 0:
                    self.moneyAdj(1)
                else:
                    self.moneyAdj(-1)
        elif self.actions[-2:] == "bb": #both players bet
            if self.players[0].card > self.players[1].card:
                self.moneyAdj(2)
            else:
                self.moneyAdj(-2)

    def moneyAdj(self, money):
        if money > 0:
            print("{} wins £{}.".format(self.players[0].name,money))
        else:
            print("{} wins £{}.".format(self.players[1].name,-money))
        self.players[0].money += money
        self.players[1].money -= money



def display_results(ev, i_map):
    print('player 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))

    print()
    print('player 1 strategies:')
    sorted_items = sorted(i_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print()
    print('player 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)
