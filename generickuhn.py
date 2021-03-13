import numpy as np
import random as rnd
import validation as vald
#taken from https://github.com/IanSullivan/PokerCFR under MIT license

class AiKuhn:
    def __init__(self, action_dict={0: 'p', 1: 'b'}):
        self.nodeMap = {} #Contains all possible nodes
        self.action_dict = action_dict
        self.n_actions = 2 #number of possible actions (pass, bet)
        self.expected_game_value = 0
        self.winrate = {} #winrate throughout learning (iteration: [, ,])

        self.current_player = 0
        self.deck = np.array([0, 1, 2]) #Three card kuhn poker deck

    def get_node(self, card, history, Nodetype):
        key = str(card) + " " + history
        if key not in self.nodeMap:
            newnode = Nodetype(key, self.action_dict)
            self.nodeMap[key] = newnode
            return newnode
        return self.nodeMap[key]

    def get_aistrategy(self):
        finalstrat = {}
        for x in self.nodeMap:
            finalstrat[x] = self.nodeMap[x].get_average_strategy()
        return finalstrat

    def play_vs_dummy(self, ai_strat, dummyfilename, test_iterations = 1000):
        dummy_strat = vald.importJson(dummyfilename)
        wins = 0
        deck = np.array([0,1,2])
        for j in range(test_iterations):
            actions = ''
            player = j % 2
            rnd.shuffle(deck)
            ai_card = deck[0] if player==0 else deck[1]
            dummy_card = deck[1] if player==0 else deck[0]

            while not is_terminal(actions):
                card = ai_card if player==0 else dummy_card
                strat = ai_strat if player==0 else dummy_strat
                action = ai_get_nodestrategy(strat, card, actions)
                actions += action
                player = (player+1)%2

            won = roundWinnings(actions, ai_card, dummy_card, train=False, player = j % 2)
            won = 1 if won > 0 else 0
            wins += won
        win_average = wins/test_iterations
        return win_average

class Node:
    def __init__(self, key, action_dict, n_actions=2):
        self.key = key #the label of  the node in the form: [cards previous actions]
        self.n_actions = n_actions #the number of possible actions taken from said node
        self.possible_actions = np.arange(self.n_actions) #an indicies list for the possible actions
        self.action_dict = action_dict #dictionary to label each action

        self.regret_sum = np.zeros(self.n_actions) #the sum of the regret at each iteration (for each action)
        self.strategy_sum = np.zeros(self.n_actions) # the sum of the strategy at each iteration (for each action)

        #the strategy(probability of choosing each action) from each node, updated for each iteration
        self.strategy = np.repeat(1/self.n_actions, self.n_actions) #initially, equal probability of each action occuring

        self.reach_pr = 0 #probablity of reaching said node (based on the strategy of previous nodes) for an individual iteration
        self.reach_pr_sum = 0 #the sum over all iterations

    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy #adds the strategy for this iteration
        self.reach_pr_sum += self.reach_pr #adds the reach pr for this iteration
        self.strategy = self.get_strategy() #updates the strategy for the next iteration
        self.reach_pr = 0 #resets the reach probablity for the next iteration

    def get_strategy(self):
        self.regret_sum[self.regret_sum < 0] = 0 #negative regrets are removed
        normalising_sum = sum(self.regret_sum) #the total regret
        if normalising_sum > 0:
            return self.regret_sum / normalising_sum
        else: #if regrets are zero, returns an even probability distribution for each action
            return np.repeat(1/self.n_actions, self.n_actions)

    #to get the final strategy over previous iterations
    def get_average_strategy(self):
        if self.reach_pr_sum != 0:
            strategy = self.strategy_sum / self.reach_pr_sum
        else:
            strategy = self.strategy_sum
        #renormalise
        normalising_sum = sum(strategy)
        if normalising_sum > 0:
            strategy = strategy / normalising_sum
        else:
            strategy = np.repeat(1 / self.n_actions, self.n_actions)
        return list(strategy)

    #it's a str representation init
    def __str__(self):
            strategies = ['{:03.2f}'.format(x)
                          for x in self.get_average_strategy()]
            return '{} {}'.format(self.key.ljust(6), strategies)

#some funcs idk where to put teeb used in multiple places

def ai_get_nodestrategy(strategy, card, history):
    key = str(card) + " " + history
    ai_p = strategy[key]
    aichoice = np.random.choice(np.array(['p','b']),p=ai_p)
    return aichoice

def roundWinnings(actions, card1, card2, train=True, player=2):
    if actions[-1] == 'p': #the last action was a pass
        if actions[-2:] == 'pp': #both players passed
            return 1 if card1 > card2 else -1
        else:
            if train:
                return 1
            if (len(actions) % 2 == 0 and player==0) or (len(actions) % 2 == 1 and player==1):
                return 1
            else:
                return -1
    elif actions[-2:] == "bb": #both players bet
        return 2 if card1 > card2 else -2

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
    def __init__(self, aistrategymap = {}):
        self.players = self.buildPlayers(10, aistrategymap)
        self.deck = np.array([0,1,2]) #ze kuhn poker deck
        self.actions = '' #string of actions in a given round
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
        player = 1 if self.players[0].cpu else 0
        self.moneyAdj(roundWinnings(self.actions, self.players[0].card, self.players[1].card), train=False, player=player)

    def moneyAdj(self, money):
        if money > 0:
            print("{} wins £{}.".format(self.players[0].name,money))
        else:
            print("{} wins £{}.".format(self.players[1].name,-money))
        self.players[0].money += money
        self.players[1].money -= money
