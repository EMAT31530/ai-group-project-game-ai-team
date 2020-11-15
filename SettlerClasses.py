
class Hex:
    def __init__(self, x, y):
        self.x = 0
        self.y = 0
        self.Point = []
        self.Verticies = []
        self.Sides = []
        self.face = ''  # Land type
        self.diceroll = 0  # The dice roll required for said hex


class Board:
    def __init__(self):
        self.Hexes = self.build()

    def build(self):
        return 0
