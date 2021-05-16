from abc import ABC, abstractmethod

class GameState(ABC):
    #To check if the current gamestate is a terminal state
    @abstractmethod
    def is_terminal(self):
        pass

    @abstractmethod
    def is_fold(self):
        pass

    #To check if the current gamestate is a chance state (i.e card draw)
    @abstractmethod
    def is_chance(self):
        pass

    #To get the payoff from a terminal state
    @abstractmethod
    def get_payoff(self, chance_outcome):
        pass 

    #To get the possible actions of said player from the current gamestate
    @abstractmethod
    def get_actions(self, player):
        pass
    
    #To get the possible chance outcomes of the current gamestate
    @abstractmethod
    def get_public_chanceoutcomes(self):
        pass 
    
    #To get the possible chance outcomes of the current gamestate
    @abstractmethod
    def get_private_chanceoutcomes(self):
        pass 

    #To translate from the current state to a new state via the given action
    @abstractmethod
    def handle_action(self, action):
        pass

    #To translate from the current state to a new state via the given chance outcome
    @abstractmethod
    def handle_public_chance(self, chance_outcome):
        pass

    #To translate from the current state to a new state via the given chance outcome
    @abstractmethod
    def handle_private_chance(self):
        pass 
    
    #To get the active player from the current state
    @abstractmethod
    def get_active_player_index(self):
        pass

    #To get the representative key of a given state
    @abstractmethod
    def get_representation(self):
        pass