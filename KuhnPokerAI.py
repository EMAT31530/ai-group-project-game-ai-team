import numpy as np
import random as rnd
import time
import sys
import validation as vald
import matplotlib.pyplot as plt
#taken from https://github.com/IanSullivan/PokerCFR under MIT license

class Node:
    def __init__(self, key, action_dict, n_actions=2):
        self.key = key #the label of  the node in the form: [cards previous actions]
        self.n_actions = n_actions #the number of possible actions taken from said node
        self.regret_sum = np.zeros(self.n_actions) #the sum of the regret at each iteration (for each action)
        self.strategy_sum = np.zeros(self.n_actions) # the sum of the strategy at each iteration (for each action)
        self.action_dict = action_dict #dictionary to label each action
        #the strategy(probability of choosing each action) from each node
        self.strategy = np.repeat(1/self.n_actions, self.n_actions) #initially, equal probability of each action occuring
        self.reach_pr = 0 #probablity of reaching said node (based on the strategy of previous nodes) for an individual iteration
        self.reach_pr_sum = 0 #the sum over all iterations

    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy #adds the strategy for this iteration
        self.reach_pr_sum += self.reach_pr #adds the reach pr for this iteration
        self.strategy = self.get_strategy() #updates the strategy for the next iteration
        self.reach_pr = 0 #resets the reach probablity for the next iteration

    #Returns the strategy for the current regrets, i.e for regrets [50, 50, 100], returns [1/4,1/4,1/2]
    def get_strategy(self):
        regrets = self.regret_sum
        regrets[regrets < 0] = 0 #negative regrets are ignored
        normalising_sum = sum(regrets) #the total regret
        if normalising_sum > 0:
            return regrets / normalising_sum
        else: #if regrets are negative, returns an even probability distribution for each action
            return np.repeat(1/self.n_actions, self.n_actions)

    #to get the final strategy over all iterations
    def get_average_strategy(self):
        strategy = self.strategy_sum / self.reach_pr_sum
        #renormalise
        total = sum(strategy)
        strategy /= total
        return list(strategy)

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
        self.winrate = {} #winrate throughout learning (iteration: [, ,])
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

    def trainWcomparison(self, dummyai, n_iterations=50000, n_intervals=1000):
        for _ in range(n_iterations):
            if _ % n_intervals == 0:
                cur_aistrat = self.get_aistrategy()
                if _ == 0:
                    cur_aistrat = vald.importJson('defaultkuhn')

                cur_winrate = list(np.zeros(len(dummyai)))

                for j in range(len(dummyai)):
                    winstatistics = self.play_vs_dummy(cur_aistrat, dummyai[j])
                    cur_winrate[j] = winstatistics
                self.winrate[_] = cur_winrate

            rnd.shuffle(self.deck)
            self.cfr('', 1, 1)
            for _, v in self.nodeMap.items():
                v.update_strategy()
        vald.exportJson(self.winrate, 'winr8_{}_3'.format(n_iterations))
        
    def graphing(self, winratedict):
        x=list(winratedict.items())
        for i in range(0, len(x[0][1])):
            """
            currwinrate = []
            for k in range(0, len(x)):
                currwinrate.append(x[k][1][i])
                print(currwinrate)"""
            plt.plot([y for y in range(0, len(x))], [x[k][1][i] for k in range(0,len(x))])
            plt.xlabel('Number of games played')
            plt.ylabel('Win Rate')
            plt.show()


    #The Counterfactual Regret Minimisation function
    def cfr(self, history, pr_1, pr_2):
        n = len(history)
        is_player_1 = n % 2 == 0
        player_card = self.deck[0] if is_player_1 else self.deck[1]

        if is_terminal(history):
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

    def play_vs_dummy(self, ai_strat, dummyfilename, test_iterations = 1000):
        dummy_strat = vald.importJson(dummyfilename)
        wins = 0
        deck = np.array([0,1,2])
        for j in range(test_iterations):
            actions = ''
            is_player_1 = j % 2 == 0
            rnd.shuffle(deck)
            ai_card = deck[0] if is_player_1 else deck[1]
            dummy_card = deck[1] if is_player_1 else deck[0]

            while not is_terminal(actions):
                card = ai_card if is_player_1 else dummy_card
                strat = ai_strat if is_player_1 else dummy_strat
                action = ai_get_nodestrategy(strat, card, actions)
                actions += action
                is_player_1 = False if is_player_1 else True

            won = roundWinnings(actions, ai_card, dummy_card)
            won = 1 if won > 0 else 0
            wins += won
        win_average = wins/test_iterations
        return win_average

    #Finds the node within the Ai's NodeMap
    def get_node(self, card, history):
        key = str(card) + " " + history
        if key not in self.nodeMap:
            action_dict = {0: 'p', 1: 'b'}
            info_set = Node(key, action_dict)
            self.nodeMap[key] = info_set
            return info_set
        return self.nodeMap[key]

    def get_aistrategy(self):
        finalstrat = {}
        for x in self.nodeMap:
            finalstrat[x] = self.nodeMap[x].get_average_strategy()
        return finalstrat

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
            self.strategyMap = dict(strategyMap)

    def ai_get_strategy(self, actions):
        key = str(self.card) + " " + actions
        return self.strategyMap[key]

class Game:  # Object to represent game
    def __init__(self, aistrategymap = {}, training = False):
        self.players = self.buildPlayers(10, aistrategymap)
        self.deck = np.array([0,1,2]) #ze kuhn poker deck
        self.actions = '' #string of actions in a given round
        self.training = training
        self.start()

    def buildPlayers(self, initmoney, aistrategymap):
        playerlist = []
        name = vald.checkString("What is your name?\n")
        if aistrategymap == {}:
            aistrategymap = self.chooseai()
        playerlist.append(Player("AIBOT", initmoney, True, aistrategymap))
        playerlist.append(Player(name, initmoney))
        return playerlist

    def chooseai(self):
        message = "Please input the filename of your chosen AI to compete against. "
        filename = vald.checkJson(input(message))
        strategy = vald.importJson(filename)
        return strategy

    def start(self):
        roundcount = 10
        while not roundcount < 1:
            for i in range(roundcount):
                self.startnewRound()
            roundcount = vald.checkInt("How many more rounds would you like to play? ")

    # Updates round and appends old round to round list
    def startnewRound(self):
        print('\n')
        self.actions = '' #resets actions!
        self.players.reverse() #swaps the player order for the new round!
        rnd.shuffle(self.deck) #shuffles the deck
        for i in range(2):
            self.players[i].card = self.deck[i]
        i = 0
        while not is_terminal(self.actions):
            if self.players[i].cpu == True:
                strat = self.players[i].strategyMap
                card = self.players[i].card
                aichoice = ai_get_nodestrategy(strat, card, self.actions)
                self.actions += aichoice
                pasbet =  'pass' if aichoice == 'p' else 'bet'
                print("The AIBOT has £{}, and has chosen to {}!!!!".format(self.players[i].money, pasbet))
            else:
                print("You have £{}, and in your hand you have {}.".format(self.players[i].money,self.players[i].card))
                print("Would you like to pass or bet?")
                choice = vald.getChoice(['pass','bet'])
                self.actions += 'p' if choice == 'pass' else 'b'
            i = (i +1) % 2
        self.moneyAdj(roundWinnings(self.actions, self.players[0].card, self.players[1].card))

    def moneyAdj(self, money):
        if money > 0:
            print("{} wins £{}.".format(self.players[0].name,money))
        else:
            print("{} wins £{}.".format(self.players[1].name,-money))
        self.players[0].money += money
        self.players[1].money -= money


def roundWinnings(actions, card1, card2):
    if actions[-1] == 'p': #the last action was a pass
        if actions[-2:] == 'pp': #both players passed
            return 1 if card1 > card2 else -1
        else:
            return 1 if len(actions) % 2 == 0 else -1
    elif actions[-2:] == "bb": #both players bet
        return 2 if card1 > card2 else -2

def ai_get_nodestrategy(strategy, card, history):
    key = str(card) + " " + history
    ai_p = strategy[key]
    aichoice = np.random.choice(np.array(['p','b']),p=ai_p)
    return aichoice

def is_terminal(history):
    if history[-2:] == 'pp' or history[-2:] == "bb" or history[-2:] == 'bp':
        return True

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
trainer=AiKuhnBotTrainer()
dict={"0":[0.25,0.5,0.75],"1":[0.5,0.6,0.8],"3":[0.25,0.5,0.75],"4":[0.5,0.6,0.8],"5":[0.25,0.5,0.75],"6":[0.5,0.6,0.8]}

trainer.graphing(dict)
