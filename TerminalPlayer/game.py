from terminal_playing_cards import Deck
from TerminalPlayer.players import Player, AiPlayer
from TerminalPlayer.gamerules import kuhnrules, leducrules
from TerminalPlayer.blankplaytypes import PlayGeneric 
import os
import sys
import platform
sys.path.append('..')
from modules.validation import checkInt, checkString, importJson


class Game:
    def __init__(self, gamestatetype, gamestaterules, opp_strategy):
        deck = Deck(specifications=gamestaterules.DECK_SPEC)
        strat_map = importJson(opp_strategy)
        player_name = checkString("What be yere name? ")
        players = [
            Player(player_name, gamestaterules.start_money), 
            AiPlayer(opp_strategy, gamestaterules.start_money, strat_map) ]

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
            gamestate.handle_action(action)

        os.system('cls') if platform.system() == 'Windows' else os.system('clear')
        gamestate.display_round_str(round, terminal=True)

        

        _ = input('\nPress enter to contine...')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        gamtype = 'k'
        ai = 'AIKuhn'
    else:
        gamtype = str(sys.argv[1])
        ai = 'AILeduc'
    if len(sys.argv) > 2:
        ai = str(sys.argv[2])

    
    if gamtype == 'k':
        game = Game(PlayGeneric, kuhnrules, ai)
    elif gamtype == 'l':
        game = Game(PlayGeneric, leducrules, ai)

    game.play()
