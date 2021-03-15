# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 08:44:58 2020

@author: TAC
"""
import random

def check_fold(player, game_round): #function that selects check/fold for player
    boolean = (player.curBid == game_round.curBid)
    if boolean:
        return "check"
    else:
        return "fold"
    
def check_call(player, game_round): #similar, for passive but loose players
    boolean = (player.curBid == game_round.curBid)
    if boolean:
        return "check"
    else:
        return "call"
        
def bet_raise(amount, player, game_round): #similar for aggro players
    boolean = (player.curBid == game_round.curBid)
    if boolean and not player.chair == 1:
        return "bet", amount
    else:
        return "raise", amount
    #currently breaks when a player goes all in
    
#strategies below
def calling_station(player, game_round): #always calls/checks
    if player.curBid != game_round.curBid:
        return "call"
    else:
        return "check"
    
def fold_fish(player, game_round): #always folds
    return "fold"

def check_fish(player, game_round): #slight upgrade of the above since they always check/fold
    return check_fold(player, game_round)

def aggrofish(player, game_round): #always goes all-in instantly
    return bet_raise(player.money, player, game_round)
    #may need to be changed once all-in functionality added since the player is still being asked for actions on later streets when this shouldn't be an option
    
def loose_cannon(player, game_round): #chooses one of each option w.p. 1/3 and chooses raise amount uniformly from possible options if they choose to raise/bet
    x = random.randint(1, 3)
    lower = game_round.lower()
    upper = player.money
    if x == 3:
        if upper > lower: #otherwise player is going all in and must bet their entire stack 
            amount = random.uniform(lower, upper) 
        else:
            amount = player.money
        return bet_raise(amount, player, game_round)
    elif x == 2:
        return check_call(player, game_round)
    else:
        return "fold"
        

def sophisticated_ai(player, game_round): #a somewhat sophisticated (but still deterministic) strategy
    rank = player.hand.rank    
    if game_round.street == 1: #preflop
        if rank[0] == 2 or rank[1][1] >= 10: #pair or both cards greater than or equal to 10 (strong hands)
            if 5*game_round.bigBlind >= game_round.lower(): #bet 5bb if legal
                return bet_raise(5*game_round.bigBlind, player, game_round)
            else:
                return check_call(player, game_round)
        elif rank[1][0] < 7: #check/fold if not pair and both cards less than seven
            return check_fold(player, game_round)
        else:
            return check_call(player, game_round)
    else: #postflop
        if rank[0] >= 7:
            return bet_raise(player.money, player, game_round)
        elif rank[0] >= 4:
            if game_round.curBid >= 2*game_round.pot:
                return check_fold(player, game_round)
            elif game_round.curBid >= game_round.pot:
                return check_call(player, game_round)
            else:
                if game_round.pot >= game_round.lower():
                    return bet_raise(game_round.pot, player, game_round)
                else:
                    return check_call(player, game_round)
        elif rank[0] >= 2:
            if game_round.curBid >= game_round.pot:
                return check_fold(player, game_round)
            else:
                if 0.5*game_round.pot >= game_round.lower():
                    return bet_raise(0.5*game_round.pot, player, game_round)
                else:
                    return check_call(player, game_round)
        else:
            return check_fold(player, game_round)
             

def hist_dependent_ai(player, game_round): #less sophisticated than one above but will have challenge of acting based on actions on previous streets
    #e.g. always calls except if opponent raises two streets in a row, in which case they fold
    pass
    
functions = [calling_station, fold_fish, check_fish, aggrofish, loose_cannon, sophisticated_ai]