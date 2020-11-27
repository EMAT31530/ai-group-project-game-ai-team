import random as rnd


class Card:  # Object to represent individual cards
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.visible = False  # If card is visible to other players

    def __str__(self):  # Overwrites the String fucntion
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        return '{} of {}'.format(vals[self.val-2], self.suit)

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
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
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

    # i need to include high card in comparisons
    def __gt__(self, other):  # compares two hand rankings
        return self.rank > other.rank

    def __lt__(self, other):  # ditto
        return self.rank < other.rank

    def __eq__(self, other):  # ditto
        return self.rank == other.rank

    def addCard(self, card):
        self.cards.append(card)

    def rankupd(self, board):
        import ranking as rnk
        self.rank = rnk.checker(self, board)


# ___Just some btec stuff to get an idea of what we would need to do___
class Player:  # Object to represent player
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.hand = Hand()
        self.money = 0


class Round:
    def __init__(self, players, bigBlind):
        self.pot = 0
        self.board = Hand()
        self.bigBlind = bigBlind
        self.players = players

    def start(self):
        for i in range(2):
            for player in self.players:
                player.hand.addCard(self.deck.draw())

    def increment(self, burn):
        self.board.addCard(self.deck.draw(burn=burn))
        for player in self.players:
            player.rankupd(self.board)
        self.bidding()

    def bidding(self):
        return 0


class Game:  # Object to represent entire game state
    def __init__(self, players):
        self.players = players  # Pre created list of players
        self.deck = Deck()
        self.Rounds = []  # To store all ellapsed rounds
        self.curRound = Round(self.players, 100)

    # Updates round and appends old round to round list
    def newRound(self):
        self.Rounds.append(self.curRound)
        self.curRound = Round(self.players, 100)
