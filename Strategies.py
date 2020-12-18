# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 08:44:58 2020

@author: TAC
"""

def calling_station(player, game_round): #always calls/checks
    if player.curBid != game_round.curBid:
        return "call"
    else:
        return "check"
    
def fold_fish(player, game_round): #always folds
    return "fold"

def aggrotard(player, game_round): #always goes all-in instantly
    if player.curBid != game_round.curBid:
        return "raise", player.money
    else:
        return "bet", player.money
    #may need to be changed once all-in functionality added since the player is still being asked for actions on later streets when this shouldn't be an option
    
def loose_cannon(player, game_round): #chooses one of each option w.p. 1/3 and chooses raise amount uniformly from possible options if they choose to raise/bet
    pass

def sophisticated_ai(player, game_round): #a somewhat sophisticated (but still deterministic) strategy if we can be bothered to implement it
    pass

def hist_dependent_ai(player, game_round): #less sophisticated than one above but will have challenge of acting based on actions on previous streets
    #e.g. always calls except if opponent raises two streets in a row, in which case they fold
    pass
    
functions = [calling_station, fold_fish, aggrotard]