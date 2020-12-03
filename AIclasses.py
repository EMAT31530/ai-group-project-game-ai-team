import random as rnd
import validation as vald
import ranking as rnk
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
        # make into big fuckoff 'if' thing for each possible ranking
        strlist = ["High card", "Pair", "Two pair", "Three of a kind", "Straight", "Flush", "Full House", "Four of a kind", "Straight Flush"]
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        return "{} {}".format(strlist[self.rank[0]-1], vals[self.rank[1][0]-2])

    def addCard(self, card):
        self.cards.append(card)

    def rankupd(self, board):
        self.rank = rnk.checker(self, board)


# ___Just some btec stuff to get an idea of what we would need to do___
class Player:  # Object to represent player
    def __init__(self, name, chair, money):
        self.name = name
        self.chair = chair
        self.hand = Hand()
        self.money = money
        self.curBid = 0
        self.state = 0  # 0: in round, 1: called, 2: folded, 3: for blinds so they act last

    def __str__(self):  # Overwrites the String fucntion
        return "{}".format(self.name)

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


class Round:
    def __init__(self, bigBlind, players):
        self.deck = Deck()
        self.pot = 0
        self.curBid = 0
        self.board = Hand()
        self.bigBlind = bigBlind
        self.histPlayers = 0
        self.start(players)

    def __str__(self):  # Overwrites the String fucntion
        return "nice"

    def strRoundState(self, player):
        print("Player {}'s turn.".format(str(player)))
        print("Currently the pot is £{}, and the highest bid is £{}.".format(self.pot, self.curBid))
        print("Your current bid is £{}, and you have £{}.".format(player.curBid, player.money))
        print("In you hand you have: {}. And on the board there is: {}.".format(player.hand, self.board))
        print("Your best hand is {}.".format(player.hand.strRank()))

    def start(self, players):
        for i in range(2):
            for player in players:
                player.hand.addCard(self.deck.draw())

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

    def bidding(self, players):
        def fold(player):
            player.state = 2

        def call(player):
            player.state = 1
            self.bid(player, self.curBid - player.curBid)

        def raize(player):
            # get a valid raise from user
            def raisecheck(amount):
                return amount >= (2*self.curBid - player.curBid) and (amount <= player.money)
            while True:
                amount = vald.checkInt("Balance: £{}, Current bid: £{}, Minimum bid: £{}. ".format(player.money, player.curBid, 2*self.curBid))
                if raisecheck(amount):
                    break
            # updates relevant info
            self.curBid += amount - (self.curBid - player.curBid)
            self.bid(player, amount)
            for playee in [i for i in players if i.state != 2]:
                playee.state = 0
            player.state = 1

        remainPlayers = [i for i in players if i.state == 0] + [i for i in players if i.state == 3]
        while any([i.state in [0, 3] for i in players]):
            for player in remainPlayers:
                self.strRoundState(player)
                choices = (["Raise", "Call", "Fold"] if player.curBid != self.curBid else ["Raise", "Check", "Fold"])
                action = vald.getChoice(choices)
                if action == "raise":
                    raize(player)
                elif action == "fold":
                    fold(player)
                else:
                    call(player)
            remainPlayers = [i for i in players if i.state == 0]  # updates remaining players
        # resets state of remaining players for next bidding
        for player in [i for i in players if i.state != 2]:
            player.state = 0


class Game:  # Object to represent entire game state
    def __init__(self, blind):
        self.players = self.buildPlayers(blind * 20)  # Creates list of players
        self.Rounds = []  # To store all ellapsed rounds
        self.blind = blind
        self.curRound = Round(blind, self.players)

    def buildPlayers(self, initmoney):
        players = vald.checkInt("How many players?\n")
        playerlist = []
        for i in range(players):
            name = vald.checkString("Player {}s name?\n".format(i+1))
            playerlist.append(Player(name, i, initmoney))
        return playerlist

    def start(self):
        while True:
            self.curRound.blinds(self.players)
            self.play()
            self.endRound()
            print("Would you like to play a new roud")
            answer = vald.getChoice(["Yes", "No", "Y", "N"])
            if answer == "y" or answer == "yes":
                self.newRound()
            else:
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
            sortedplayers = sorted(remainingPlyrs, key=cmp_to_key(Player.rankcomp))
            winplyrs = vald.howManyEqu(sortedplayers)
            n = len(winplyrs)
            for plyr in winplyrs:
                plyr.money += int(self.curRound.pot/n)
            print("Player(s) {} won £{}.".format(str([str(i) for i in winplyrs]), int(self.curRound.pot/n)))
        # add something for how much monies init

    def play(self):
        self.curRound.updRankings(self.players)
        self.curRound.bidding(self.players)
        plyrs = [i for i in self.players if i.state != 2]  # Players who have not folded
        for j in range(3):  # Implements flop/turn/river
            self.curRound.increment(burn=True)
            if j == 0:
                self.curRound.increment()
                self.curRound.increment()
            plyrs = [i for i in plyrs if i.state != 2]
            self.curRound.updRankings(plyrs)
            self.curRound.bidding(plyrs)
