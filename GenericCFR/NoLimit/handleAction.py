def perform_flop(self):
    self.street = 'f'
    self.active_player = 0
    for i in range(3):
        self.board.append(self.deck.draw())
    self.history.append(' ')

def perform_turn(self):
    self.street = 't'
    self.active_player = 0
    self.board.append(self.deck.draw())
    self.history.append(' ')

def perform_river(self):
    self.street = 'r'
    self.active_player = 0
    self.board.append(self.deck.draw())
    self.history.append(' ')

#Does not account for all ins, can be added l8er init
def handleAction(self, player, action):
    next_state = copy.deepcopy(self)
    next_state.history.append(action)

    active_player = next_state.get_active_player()
    next_state.active_player = (next_state.active_player + 1) % self.num_players
    opp_player = next_state.get_active_player() #cheeky

    call = action == 'c'
    check = self.history[-1] == 'ch' and action == 'ch'

    if action[0] == 'r': #will need to change depending upon previous raises maybe
        amount = int(action[0:])
        next_state.pot += amount
        active_player.bet_amount += amount
    if call: #might need to change this too, will see once we have bet groupings
        amount = int(self.history[-1][0:])
        next_state.pot += amount
        active_player.bet_amount += amount

    if self.street == 'p':
        if check or call:
            next_state.perform_flop()
    elif self.street == 'f':
        if check or call:
            next_state.perform_turn()
    elif self.street  == 't':
        if check or call:
            next_state.perform_river()
    return next_state
