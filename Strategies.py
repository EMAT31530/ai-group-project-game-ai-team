# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 08:44:58 2020

@author: TAC
"""

def calling_station(self, game_round):
    if self.curBid != game_round.curBid:
        return "call"
    else:
        return "check"
    
def folding_fish(self, game_round):
    return "fold"

def aggrotard(self, game_round):
    pass

functions = [calling_station, folding_fish, aggrotard]