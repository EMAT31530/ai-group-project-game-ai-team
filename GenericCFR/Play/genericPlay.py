from abc import ABC, abstractmethod

class GameState(ABC):
    #To check if the current gamestate is a terminal state
    @abstractmethod
    def is_terminal(self):
        pass

    #To get the payoff from a terminal state
    @abstractmethod
    def get_rewards(self):
        pass

    #To get the possible actions of said player from the current state
    @abstractmethod
    def get_actions(self, player):
        pass

    #To translate from the current state to a new state via the given action
    @abstractmethod
    def handle_action(self, player, action):
        pass
        #next_state = copy.deepcopy(self)

    #To get the active player from the current state
    @abstractmethod
    def get_active_player(self):
        pass

    #Initalises a new round
    @abstractmethod
    def new_round(self):
        pass

    #To get get_indexthe representative key of a given state
    @abstractmethod
    def get_representation(self):
        pass


class Game:
    def play(self, gamestatetype, opp_strategy):
        gamestate = gamestatetype(opp_strategy)

        roundcount = 10
        while not roundcount < 1:
            for i in range(roundcount):
                self.round(gamestate)
                
            roundcount = validation.checkInt("How many more rounds would you like to play? ")

    def round(self, gamestate):
        gamestate.new_round()
        while not gamestate.is_terminal():
            player = gamestate.get_active_player()
            print(player)
            action = player.get_action(gamestate)
            gamestate.handle_action(action)
    
        rewards = gamestate.get_rewards()
        for i in range(rewards):
            gamestate.players[i].money += rewards[i]
        