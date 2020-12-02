# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:04:25 2020

@author: TAC
"""
import AIclasses as ai

#build a few preliminary functions which will be used for the hand ranking function

def sort_by_key(dictionary, backwards = False): #function to sort a dictionary by key whilst preserving the dictionary
    dict_2 = {}
    for key in sorted(dictionary, reverse=backwards):
        dict_2[key] = dictionary[key]
    return dict_2


def sort_by_value(dictionary, backwards=False):  # ditto for values
    array = sorted(dictionary.items(), key=lambda item: item[1])
    if backwards:
        array.reverse()
    dict_2 = {}
    for i in range(len(array)):
        dict_2[array[i][0]] = array[i][1]
    return dict_2


def num_same(hand):  # returns a dictionary with keys as the card numbers and values as the number of cards of that type
    card_nums = {}
    for card in hand:
        if card.val in card_nums:
            card_nums[card.val] += 1
        else:
            card_nums[card.val] = 1
    return sort_by_value(card_nums, True)


def num_suit(hand):  # same as above but with keys as card suits and values as number of cards of that suit
    card_suits = {}
    for card in hand:
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


def high_card(card_nums, num = 5, sub = True): #card_nums is a dictionary here but this could be changed
    #assuming here that the hand inputted will not have any pairs or anything
    if len(card_nums) == 0:
        return 0 #convention
    card_nums = sort_by_key(card_nums, True)
    cards = list(card_nums.keys())
    if len(cards) < num:
        if sub: #being called as a sub function we don't want to return the hand ranking (9)
            return cards #output here is a list; in previous functions the output is a tuple - not sure of an easy way to adapt this
        else:
            return 1, cards
    else:
        if sub:
            return cards[:num]
        else:
            return 1, cards[:num]


def straight_flush(card_suits, consec_cards, hand): #all the following functions check to see if you have the following hand
    #am wondering if the first 3 functions should be class methods so we don't have to constantly call them
    if consec_cards == False or list(card_suits.values())[0] < 5:
        return False
    else:
        suit_hand = ai.Hand() #create a pseudo hand of all the cards of the main suit and then call the straight fu
        suit = list(card_suits.keys())[0]
        for i in hand:
            if i.suit == suit:
                suit_hand.addCard(i)
        return 9, consecutive(suit_hand) #return top card for easier comparison
        #also removed suit in return since it is unhelpful in the comparison but can be added back in if wanted


def four_of_a_kind(card_nums):
    if list(card_nums.values())[0] != 4:
        return False
    else:
        main_card = list(card_nums.keys())[0]
        if len(list(card_nums.keys())) == 1:
            return 8, [list(card_nums.keys())[0]] #if the hand is only four cards (not technically possible in a poker game but anyway) then by default return the four of a kind and zero
        else:
            card_nums.pop(main_card)
            other_card = high_card(card_nums, 1)
            return 8, [main_card, other_card]


def full_house(card_nums, keys, vals):
    if vals[0] != 3 or len(vals) == 1: #require a three of a kind and a pair as well
        return False
    elif vals[1] == 1:
        return False
    else:
        if vals[1] == 3: #if we have two three of a kinds (rare but possible) then we choose the higher ranking as our three of a kind and the lower as our pair
            return 7, [max(keys[0], keys[1]), min(keys[0], keys[1])]
        elif len(vals) > 2 and vals[2] == 2: #if we have a three of a kind and two pairs then we must choose the higher ranking of the two pairs
            #also the and statement will evaluate to see if the length is long enough for vals[2] to exist before referencing it
            return 7, [keys[0], max(keys[1], keys[2])]
        else:
            return 7, [keys[0], keys[1]]


def flush(card_suits, hand):
    if list(card_suits.values())[0] < 5:
        return False
    else:
        suit_hand = ai.Hand() #code mostly copied from straight flush function
        suit = list(card_suits.keys())[0]
        for i in hand:
            if i.suit == suit:
                suit_hand.addCard(i)
        return 6, high_card(num_same(suit_hand))
    #removed suit as in straight flush


def straight(consec):
    if not consec:
        return consec #returns false
    else:
        return 5, consec



def trips(card_nums, keys, vals): #three of a kind
    if not vals[0] == 3:
        return False
    elif len(vals) > 1 and vals[1] != 1: #otherwise we have a full house
        return False
    else:
        card_nums.pop(keys[0])
        order = high_card(card_nums, 2)
        if len(vals) == 1:
            return 4, [keys[0]]
        if len(vals) == 2:
            return 4, [keys[0]] + order[:1]
        else:
            return 4, [keys[0]] + order[:2]


def two_pair(card_nums, keys, vals):
    if len(vals) == 1 or not(vals[0] == 2 and vals[1] == 2):
        return False
    else:
        if len(vals) >= 3 and vals[2] == 2: #possibility of the legendary three pair
            pairs = keys[:3] #we choose the top two of the three pairs
            pairs.sort(reverse = True)
            card_nums.pop(pairs[0])
            card_nums.pop(pairs[1])
            if card_nums == {}:
                return 3, [pairs[0], pairs[1]]
            else:
                return 3, [pairs[0], pairs[1]] + high_card(card_nums, 1)
        else:
            if len(vals) == 2: #return top two pairs
                keys.sort()
                return 3, keys[0], keys[1]
            else:
                pairs = keys[:2]
                pairs.sort(reverse=True)
                card_nums.pop(pairs[0])
                card_nums.pop(pairs[1])
                return 3, [pairs[0], pairs[1]] + high_card(card_nums, 1)


def pair(card_nums, keys, vals):
    if not vals[0] == 2:
        return False
    else:
        if len(vals) != 1 and vals[1] != 1:  #otherwise our hand is better than a pair
            return False
        else:
            card_nums.pop(keys[0])
            return 2, [keys[0]] + high_card(card_nums, 3)


def checker(self, board):
    hand = self.cards if board == [] else self.cards + board
    card_suits = num_suit(hand)
    consec_cards = consecutive(hand)
    card_nums = num_same(hand)
    keys = list(card_nums.keys())
    vals = list(card_nums.values())

    x = straight_flush(card_suits, consec_cards, hand)
    if x != False:
        return x
    x = four_of_a_kind(card_nums)
    if x != False:
        return x
    x = full_house(card_nums, keys, vals)
    if x != False:
        return x
    x = flush(card_suits, hand)
    if x != False:
        return x
    x = straight(consec_cards)
    if x != False:
        return x
    x = trips(card_nums, keys, vals)
    if x != False:
        return x
    x = two_pair(card_nums, keys, vals)
    if x != False:
        return x
    x = pair(card_nums, keys, vals)
    if x != False:
        return x

    return high_card(card_nums, sub=False)
