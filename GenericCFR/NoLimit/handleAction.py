
def perform_flop(self):
    self.street = 'f'
    self.active_player = 0
    for i in range(3):
        self.board.append(self.deck.draw())
    self.history.append(' ')

def perform_turn(self):
    self.street = 't'
    self.active_player = 0
    self.community_card = self.deck.draw()
    self.history.append(' ')

def perform_river(self):
    self.street = 'r'
    self.active_player = 0
    self.community_card = self.deck.draw()
    self.history.append(' ')

def handleAction(self, player, action):
    pass
