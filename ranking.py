# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:04:25 2020

@author: TAC
"""

#build a few preliminary functions which will be used for the hand ranking function

def sort_by_key(dictionary, backwards = False): #function to sort a dictionary by key whilst preserving the dictionary
    dict_2 = {}
    for key in sorted(dictionary, reverse = backwards):
        dict_2[key] = dictionary[key]
    return dict_2

def sort_by_value(dictionary, backwards = False): #ditto for values
    array = sorted(dictionary.items(), key=lambda item: item[1])
    if backwards:
        array.reverse()
    dict_2 = {}
    for i in range(len(array)):
        dict_2[array[i][0]] = array[i][1]
    return dict_2 #this function is a bit clapped but will do for now
        
def num_same(hand): #returns a dictionary with keys as the card numbers and values as the number of cards of that type
    card_nums = {}
    for card in hand.cards:
        if card.val in card_nums:
            card_nums[card.val] += 1
        else:
            card_nums[card.val] = 1
    return sort_by_value(card_nums, True)
    
def num_suit(hand): #same as above but with keys as card suits and values as number of cards of that suit
    card_suits = {}
    for card in hand.cards:
        if card.suit in card_suits:
            card_suits[card.suit] += 1
        else:
            card_suits[card.suit] = 1
    return sort_by_value(card_suits, True)
        
def consecutive(hand): 
    num_dict = num_same(hand)
    def straight_check(cards):
        a = cards[0]
        return cards == [a, a + 1, a + 2, a + 3, a + 4]
    n = len(num_dict) #straights are only possible for 5+ distinct cards so we check the length first
    if n < 5:
        return False #not yet 100% certain what outputs should be but will use False here for now
    else: #quite an ugly hierarchy but I think this involves the least computation
        consec_cards = sorted(num_dict) 
        if straight_check(consec_cards[-5:]): #player could have several straights, we want the highest one
            return consec_cards[-5] #straight can be defined by its bottom card
        else: 
            if n == 5:
                return False #if there were only five distinct cards then they now cannot have been a straight
            else:    
                if straight_check(consec_cards[-6:-1]):
                    return consec_cards[-6]
                else:
                    if n == 6:
                        return False
                    else:
                        if straight_check(consec_cards[-7:-2]):
                            return consec_cards[-7]
                        else:
                            return False               



#tests                        
#test = Hand()
#deck = Deck()
#deck.build()
#deck.shuffle()
#for i in range(7):
#    test.addCard(deck.draw())
#print(str(test))
#print(num_same(test))
#print(num_suit(test))
#print(consecutive(test))


