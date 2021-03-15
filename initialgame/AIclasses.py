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
            return onetext(strlist[n], 0)
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
        self.state = 0  # 0: in round, 1: called, 2: folded, 3: for blinds so they act last, 4: all in, 5: player has checked, 6: player is not permitted to raise

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
        self.playerMonies = {player: player.money for player in players} #used for calculating side pots
        self.prevBid = 0 #used to determine raising rules; lags one bet behind curBid
        #eventually will want to develop full hand history so that the above will be redundant anyway
        self.curBid = 0
        self.board = Hand()
        self.bigBlind = bigBlind
        self.histPlayers = []
        self.histActions = []
        self.street = 0 #street is one of preflop, flop, turn, river
        self.numPlayers = len(players) #number of players not folded
        self.playon = True #turns false if there is only one player left to bet
        self.partial = 0 #to keep track of partial raise amounts
        self.start(players)

    def __str__(self):  # Overwrites the String fucntion
        return "nice"

    def strRoundState(self, player):
        print("Player {}'s turn.".format(str(player)))
        print("Currently the pot is £{}, and the highest bid is £{}.".format(self.pot, self.curBid + self.partial))
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

    def lower(self): #minimum amount you can raise to at any given point
        if self.partial + self.curBid <= max(self.bigBlind, 2*self.curBid - self.prevBid): #cumulative partial raises have not yet amounted to a full raise
            return max(self.bigBlind, self.partial + 2*self.curBid - self.prevBid)
        else:
            return max(self.bigBlind, 2*self.partial + self.curBid)

    def bidding(self, players):
        def fold(player):
            player.state = 2
            if player.cpu:
                print("{} has decided to fold.\n".format(player.name))
            self.numPlayers -= 1

        def call(player):
            amount = self.curBid + self.partial - player.curBid
            if amount >= player.money:
                player.state = 4 #player is all-in
                if player.cpu:
                    print("{} has decided to call the bet with {}, and is now all-in.".format(player.name, player.money))
                else:
                    print("You have called the bet with £{} and are now all-in.".format(player.money))
                self.bid(player, player.money)
            else:
                self.bid(player, amount)
                if amount > 0:
                    player.state = 1
                    if player.cpu:
                        print("{} has decided to call £{}.\n".format(player.name, amount))
                else:
                    player.state = 5 #checking state
                    if player.cpu:
                        print("{} has decided to check.\n".format(player.name))


        def raize(player):
            # get a valid raise from user
            def raisecheck(amount):
                return amount >= self.lower() and (amount <= player.money + player.curBid)
            if player.money + player.curBid <= self.lower():
                print("You have now raised all-in for £{}".format(player.money))
                player.state = 4
                amount = player.money + player.curBid #add player.curBid because amount is the amount to raise to e.g. if bet 20 then raised by another player to 50, to reraise to 80 we need 80 - 10 chips
            else:
                while True:
                    amount = vald.checkFloat("Max amount: £{}, Current bid: £{}, Minimum bid: £{}. ".format(player.money + player.curBid, player.curBid, self.lower()))
                    if raisecheck(amount):
                        break
            # updates relevant info
            bet = amount - player.curBid
            self.bid(player, bet)
            if player.state != 4:
                self.prevBid = self.curBid + self.partial
                self.curBid = amount
                self.partial = 0 #partial raise counter reset after full raise
                for playee in [i for i in players if (i.state != 2 and i.state != 4)]:
                    playee.state = 0
                if player.money == 0:
                    player.state = 4
                else:
                    player.state = 1
            else: #player has gone all in
                self.partial = amount - self.curBid #once self.partial reaches min bet threshold, betting is opened again
                if amount >= max(self.bigBlind, 2*self.curBid - self.prevBid): #cumulative partial raises have become a full raise
                    for playee in [i for i in players if (i.state == 6)]:
                        playee.state = 0 #frozen players now unfrozen
                else:
                    for playee in [i for i in players if (i.state == 1)]:
                        playee.state = 6 #player has made a partial raise so other players who have bet or called are not allowed to raise yet
                for playee in [i for i in players if (i.state != 6 and i.state != 4 and i.state != 2)]: #others are set to 0
                    playee.state = 0

        """
        remember to fix this!!
        also change strategies e.g. to deal with state 6
        """
        def ai_raize(player, amount): #to be used in ai strategy functions
            #assuming here that the amount to raise is a valid amount
            self.prevBid = self.curBid
            #self.curBid += amount - (self.curBid - player.curBid)
            self.curBid = amount
            self.bid(player, amount - player.curBid)
            for playee in [i for i in players if i.state != 2]:
                playee.state = 0
            if player.money == 0:
                player.state = 4
                self.competingPlayers -= 1
            else:
                player.state = 1
            if player.state == 4:
                print("{} has decided to go all-in.")
            elif self.prevBid == 0: #unsure about this since self.curBid currently doesn't seem to reset on each street but I feel like it should?
                print("{} has decided to bet £{}.\n".format(player.name, amount))
            else:
                print("{} has decided to raise by £{}.\n".format(player.name, amount - self.prevBid))


        while any([i.state in [0, 3, 6] for i in players]) and self.numPlayers >= 2 and self.playon:
            for player in [i for i in players if i.state in [0, 3, 6]]:
                if self.numPlayers >= 2:
                    self.strRoundState(player)
                    if player.state == 6 or (player.curBid + player.money <= self.curBid + self.partial): #can't raise if frozen or don't have enough chips
                        choices = ["Call", "Fold"]
                    elif player.curBid != self.curBid + self.partial:
                        choices = ["Raise", "Call", "Fold"]
                    elif player.chair == 1 and self.street == 1:
                        choices = ["Raise", "Check", "Fold"] #should just be for BB
                    else:
                        choices = ["Bet", "Check", "Fold"]
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
        remaining_players = [i for i in players if (i.state != 2 and i.state != 4)]
        for player in remaining_players:
            player.state = 0
            player.curBid = 0
        self.prevBid = 0
        self.curBid = 0
        self.partial = 0
        if len(remaining_players) <= 1:
            self.playon = False


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
            self.players = [player for player in self.players if player.money > 0] #removes all players with no money left
            if len(self.players) >= 2:
                print("Would you like to play a new round?")
                answer = vald.getChoice(["Yes", "No", "Y", "N"])
                if answer in ["y","yes"]:
                    self.newRound()
                else:
                    print("Good night")
                    break
            else:
                print("Only one player remains. {} wins the game with £{}.".format(self.players[0], self.players[0].money))
                print("Good night")
                break

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
            coins = self.curRound.playerMonies
            winnings = {} #keys/values are players/winnings
            totalbets = {player: (coins[player] - player.money) for player in coins.keys()} #dictionary of amount that each player put in during the round
            bets_sorted = rnk.sort_by_value(totalbets)
            prevbet = 0 #initialising a variable here
            for bet in bets_sorted.values():
                compPlayers = list(filter(lambda player: totalbets[player] >= bet, remainingPlyrs)) #list of non-folded players who bet at least the amount of 'bet' in that round
                m = len(list(filter(lambda player: totalbets[player] >= bet, self.players))) #number of players (including those who folded) betting at least the amount
                sortedplayers = sorted(compPlayers, key=cmp_to_key(Player.rankcomp))
                winplyrs = vald.howManyEqu(sortedplayers)
                n = len(winplyrs)
                win = (bet - prevbet)*m/n
                for plyr in winplyrs:
                    if plyr in winnings:
                        winnings[plyr] += win
                    else:
                        winnings[plyr] = win
                prevbet = bet
            for plyr in winnings:
                if winnings[plyr] > 0:
                    print("Player {} won £{}".format(str(plyr), winnings[plyr]))
                    plyr.money += winnings[plyr]
                    #print("Player(s) {} won £{}.".format(str([str(i) for i in winplyrs]), int(self.curRound.pot/n)))
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
                self.curRound.street += 1
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
