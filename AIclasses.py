import random as rnd
import validation as vald
import ranking as rnk
import Strategies as strat
from functools import cmp_to_key


# Will be used to represent chips and such
class Money:
    def __init__(self):
        pass


class Card:  # Object to represent individual cards
    def __init__(self, suit, val):
        self.suit = '♥♦♣♠'[suit-1]
        self.val = val
        self.visible = False  # If card is visible to other players

    def __str__(self):  # Overwrites the String fucntion
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        return '{}{}'.format(vals[self.val-2], self.suit)

    def __repr__(self):  # The Formal String representation of the object
        return '(val={}, suit={})'.format(self.val, self.suit)

    def __lt__(self, other):  # Overwrites the less than function
        return self.val < other.val

    def __gt__(self, other):  # Overwrites the greater than function
        return self.val > other.val

    def __eq__(self, other):  # Overwrites the equal function
        return self.val == other.val


class Deck:  # Object to represent deck throughout game
    def __init__(self):
        self.cards = []
        self.build()

    def __str__(self):  # Overwrites the String fucntion
        return str([str(card) for card in self.cards])

    def build(self):  # To build a deck, can be used to rebuild also
        self.cards = []
        for suit in range(4):  # ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for i in range(2, 15):
                self.cards.append(Card(suit, i))
        self.shuffle()

    def shuffle(self):
        rnd.shuffle(self.cards)

    def draw(self, burn=False):
        if burn:  # Removes the top card from the deck
            del self.cards[-1]
        return self.cards.pop(-1)  # Removes and returns the top card


class Hand:  # Object to represent player hands
    def __init__(self):
        self.cards = []
        self.rank = (0, [])  # (rank, highcards)

    def __str__(self):  # Overwrites the String fucntion
        return str([str(card) for card in self.cards])

    def strRank(self):
        def onetext(text, index):
            return "{}: {}".format(text, vals[self.rank[1][index]-2])

        def twotext(text, index):
            return "{}: {} & {}".format(text, vals[self.rank[1][index]-2], vals[self.rank[1][index+1]-2])

        n = self.rank[0]
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        strlist = ["", "Highcard", "Pair", "Two Pair", "Three of a kind", "Straight, starting on a", "Flush starting on a", "Full House (Triple & Pair)", "Four of a kind", "Straight Flush, starting on a"]
        if n in [1, 2, 4, 5, 8]:
            return onetext(strlist[n], 0),
        if n in [3, 7]:
            return twotext(strlist[n], 0)
        elif n in [6, 9]:
            return onetext(strlist[n], 0)  # change to show suit

    def addCard(self, card):
        self.cards.append(card)

    def rankupd(self, board):
        self.rank = rnk.checker(self, board)


# ___Just some btec stuff to get an idea of what we would need to do___
class Player:  # Object to represent player
    def __init__(self, name, chair, money, cpu = False):
        self.name = name
        self.chair = chair
        self.hand = Hand()
        self.money = money
        self.cpu = cpu
        if cpu:
            strategy = vald.getStrategy(strat.functions) #ask user for the ai strategy
            self.strategy = int(strategy) - 1
        self.curBid = 0
        self.state = 0  # 0: in round, 1: called, 2: folded, 3: for blinds so they act last

    def __str__(self):  # Overwrites the String fucntion
        return self.name

    def chaircomp(self, other):
        if self.chair > other.chair:
            return 1
        elif self.chair < other.chair:
            return -1
        else:
            return 0

    def rankcomp(self, other):
        if self.hand.rank > other.hand.rank:
            return 1
        elif self.hand.rank < other.hand.rank:
            return -1
        else:
            return 0

    # resets players in preperation for new round
    def reset(self, n):
        self.hand = Hand()
        self.curBid = 0
        self.state = 0
        self.chair = (self.chair + 1) % n
        
    def decide(self, game_round): #decision function for an ai player
        return strat.functions[self.strategy](self, game_round)
        
"""
#decided to just keep this as part of the player class but will leave the code here in case it's useful for later
class CPU(Player):
    def __init__(self, name, chair, money, strategy):
        super().__init__(name, chair, money)
        if not strategy in strat.functions: #could also just try indexing strategies with numbers 
            strategy = vald.getChoice(strat.functions)
        self.strategy = strategy
        self.cpu = True
        
    def decide(self, game_round):
        return strat.functions[]
"""

class Round:
    def __init__(self, bigBlind, players):
        self.deck = Deck()
        self.pot = 0
        self.prevBid = 0 #used to determine raising rules; lags one bet behind curBid
        #eventually will want to develop full hand history so that the above will be redundant anyway
        self.curBid = 0
        self.board = Hand()
        self.bigBlind = bigBlind
        self.histPlayers = []
        self.histActions = []
        self.street = 0 #street is one of preflop, flop, turn, river 
        self.numPlayers = len(players) #number of players remaining in the round
        self.start(players)

    def __str__(self):  # Overwrites the String fucntion
        return "nice"

    def strRoundState(self, player):
        print("Player {}'s turn.".format(str(player)))
        print("Currently the pot is £{}, and the highest bid is £{}.".format(self.pot, self.curBid))
        if not player.cpu: #only want to display their hand for human players
            print("Your current bet is £{}, and you have £{}.".format(player.curBid, player.money))
            print("In you hand you have: {}. And on the board there is: {}.".format(player.hand, self.board))
            print("Your best hand is {}.".format(player.hand.strRank()))
        else:
            print("{}'s current bet is £{}, and they have £{}.".format(player.name, player.curBid, player.money))

    def start(self, players):
        for i in range(2):
            for player in players:
                player.hand.addCard(self.deck.draw())
        self.street += 1

    def increment(self, burn=False):
        self.board.addCard(self.deck.draw(burn=burn))
        self.street += 1

    def updRankings(self, players):
        for player in players:
            player.hand.rankupd(self.board.cards)

    def blinds(self, players):
        for i in range(2):
            self.bid(players[i], self.bigBlind / (2-i))
            players[i].state = 3
        self.curBid = self.bigBlind

    def bid(self, player, amount):
        player.money -= amount
        self.pot += amount
        player.curBid += amount
        
    def lower(self): #minimum amount you can raise by at any given point
        return max(self.bigBlind, 2*self.curBid - self.prevBid)

    def bidding(self, players):
        def fold(player):
            player.state = 2
            if player.cpu:
                print("{} has decided to fold.\n".format(player.name))
            self.numPlayers -= 1

        def call(player):
            amount = self.curBid - player.curBid
            if amount >= player.money:
                player.state = 4 #player is all-in
                self.bid(player, player.money)
                print("{} has decided to call the bet with {}, and is now all-in.".format(player.name, player.money))
                
            player.state = 1
            self.bid(player, amount)
            if player.cpu:
                if amount > 0:
                    print("{} has decided to call £{}.\n".format(player.name, amount))
                else:
                    print("{} has decided to check.\n".format(player.name))

        def raize(player):
            # get a valid raise from user
            def raisecheck(amount):
                return amount >= self.lower() and (amount <= player.money)
            while True:
                amount = vald.checkFloat("Max amount: £{}, Current bid: £{}, Minimum bid: £{}. ".format(player.money + player.curBid, player.curBid, max(self.bigBlind, 2*self.curBid - self.prevBid)))
                if raisecheck(amount):
                    break
            # updates relevant info
            self.prevBid = self.curBid
            #self.curBid += amount - (self.curBid - player.curBid)
            self.curBid = amount #I think this is right? Raising to a certain value rather than raising by 
            self.bid(player, amount - player.curBid)
            for playee in [i for i in players if i.state != 2]:
                playee.state = 0
            player.state = 1
            
        def ai_raize(player, amount): #to be used in ai strategy functions
            #assuming here that the amount to raise is a valid amount
            self.prevBid = self.curBid
            #self.curBid += amount - (self.curBid - player.curBid)
            self.curBid = amount
            self.bid(player, amount - player.curBid)
            for playee in [i for i in players if i.state != 2]:
                playee.state = 0
            player.state = 1
            if self.prevBid == 0: #unsure about this since self.curBid currently doesn't seem to reset on each street but I feel like it should?
                print("{} has decided to bet £{}.\n".format(player.name, amount))
            else:
                print("{} has decided to raise by £{}.\n".format(player.name, amount - self.prevBid))
                

        while any([i.state in [0, 3] for i in players]) and self.numPlayers >= 2:
            for player in [i for i in players if i.state in [0, 3]]:
                if self.numPlayers >= 2:
                    self.strRoundState(player)
                    choices = (["Raise", "Call", "Fold"] if player.curBid != self.curBid else ["Bet", "Check", "Fold"])
                    if not player.cpu:
                        action = vald.getChoice(choices)
                    else:
                        action = player.decide(self)
                    self.histActions.append((action, str(player)))  # for action history
                    if not(player.cpu):
                        if action == "raise" or action == "bet":
                            raize(player)
                        elif action == "fold":
                            fold(player)
                        else:
                            call(player)
                    else:
                        if action == "fold":
                            fold(player)
                        elif action == "call" or action == "check":
                            call(player)
                        else:
                            choice, amount = action
                            ai_raize(player, amount)
        
        # resets state of remaining players for next bidding
        for player in [i for i in players if (i.state != 2 and i.state != 4)]:
            player.state = 0
            player.curBid = 0
        self.prevBid = 0
        self.curBid = 0
        


class Game:  # Object to represent entire game state
    def __init__(self, blind):
        self.players = self.buildPlayers(blind * 100)  # Creates list of players
        self.Rounds = []  # To store all ellapsed rounds
        self.blind = blind
        self.curRound = Round(blind, self.players)

    def buildPlayers(self, initmoney):
        players = vald.checkInt("How many players?\n")
        playerlist = []
        for i in range(players):
            name = vald.checkString("Player {}s name?\n".format(i+1))
            print("Is {} a human?\n".format(name))
            answer = vald.getChoice(["Yes", "No", "Y", "N"])
            cpu = False
            if answer == "n" or answer == "no":
                cpu = True
                #print("What kind of player is {}?\n".format(name))
                #strategy = vald.getChoice(["test"])
                #playerlist.append((name, i, initmoney, strategy))
            #else:
            playerlist.append(Player(name, i, initmoney, cpu))
        return playerlist

    def start(self):
        while True:
            self.curRound.blinds(self.players)
            self.play()
            for player in self.players:
                if player.money == 0:
                    self.players.remove(player)
            if len(self.players) >= 2:
                print("Would you like to play a new round?")
                answer = vald.getChoice(["Yes", "No", "Y", "N"])
                if answer == "y" or answer == "yes":
                    self.newRound()
                else:
                    print("Good night")
                    break
            else:
                print("All players except for {} have been eliminated, who finishes the game with £{}.".format(self.players[0], self.players[0].money))
                print("Good night")

    # Updates round and appends old round to round list
    def newRound(self):
        # snapshot of players  at end of the round
        self.curRound.histPlayers = self.players
        # resets the players ready for the next round
        n = len(self.players)
        for player in self.players:
            player.reset(n)
        # reorders the players for the next round
        self.players = sorted(self.players, key=cmp_to_key(Player.chaircomp))
        # adds the round to the history of rounds
        self.Rounds.append(self.curRound)
        # creates the new round
        self.curRound = Round(self.blind, self.players)
    # divvies out the winnings

    def endRound(self):
        remainingPlyrs = [i for i in self.players if i.state != 2]
        if len(remainingPlyrs) == 1:
            print("Player {} won £{}.".format(str(remainingPlyrs[0]), self.curRound.pot))
            remainingPlyrs[0].money += self.curRound.pot
        else:
            sortedplayers = sorted(remainingPlyrs, key=cmp_to_key(Player.rankcomp))
            winplyrs = vald.howManyEqu(sortedplayers)
            n = len(winplyrs)
            for plyr in winplyrs:
                plyr.money += int(self.curRound.pot/n)
            print("Player(s) {} won £{}.".format(str([str(i) for i in winplyrs]), int(self.curRound.pot/n)))
        # add something for how much monies init
        
    def plyrs_check(self):
        if self.curRound.numPlayers <= 1:
            return True
        

    def play(self):
        self.curRound.updRankings(self.players)
        plyrs = [i for i in self.players if i.state == 0] + [i for i in self.players if i.state == 3]
        self.curRound.bidding(plyrs)
        cont = True #false if the round has ended
        if self.plyrs_check():
            self.endRound()
            cont = False
        if cont:
            for j in range(3):  # Implements flop/turn/river
                self.curRound.increment(burn=True)
                if j == 0:
                    self.curRound.increment()
                    self.curRound.increment()
                plyrs = [i for i in self.players if i.state != 2]   # Players who have not folded
                self.curRound.updRankings(plyrs)
                self.curRound.bidding(plyrs)
                if self.plyrs_check():
                    self.endRound()
                    cont = False
                    break
        if cont:
            self.endRound() #if round has not yet been ended then we end it now
