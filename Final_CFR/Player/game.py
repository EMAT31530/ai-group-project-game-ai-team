from players import Player, AiPlayer
from terminal_playing_cards import Deck
import os
import sys
import platform
sys.path.append('../modules')
from validation import checkInt, checkString, importJson


class Game:
    def __init__(self, gamestatetype, gamestaterules, opp_strategy):
        self.rules = gamestaterules
        deck = Deck(specifications=self.rules.DECK_SPEC)

        strat_map = importJson(opp_strategy)
        player_name = checkString("What be yere name? ")
        players = [
            Player(player_name, self.rules.start_money), 
            AiPlayer(opp_strategy, self.rules.start_money, strat_map) ]

        self.gamestate = gamestatetype(deck, players, self.rules)

    def play(self, roundcount=5):
        while not roundcount < 1:
            for i in range(roundcount):
                self.round(self.gamestate, i)

            roundcount = checkInt("How many more rounds would you like to play? ")

    def round(self, gamestate, round):
        gamestate.start_round()
        while not gamestate.is_terminal():
            #imagine having a mac, can you even run python on mac?
            os.system('cls') if platform.system() == 'Windows' else os.system('clear')
            if gamestate.is_chance():
                gamestate.handle_chance()

            gamestate.display_round_str(round+1)
            player = gamestate.get_active_player()
            action = player.get_action(gamestate)

            tranlsated_action = self.rules.Action_Spec[action.lower()]
            gamestate.handle_action(tranlsated_action)

        os.system('cls') if platform.system() == 'Windows' else os.system('clear')
        gamestate.display_round_str(round, terminal=True)

        

        _ = input('\nPress enter to contine...')
