import json


def checkJson(filename):
    if filename == '':
        filename = checkString("Input a  filename for the exported AI strategy").lower() + '.json'
    if filename[-5:]!='.json':
        filename += '.json'
    return filename

def exportJson(dict, filename = ''):
    filename = checkJson(filename)
    json.dump(dict, open('strategies/'+filename, 'w'))

def importJson(filename = ''):
    filename = checkJson(filename)
    dict = json.load(open('strategies/'+filename))
    return dict

def checkInt(message):
    while True:
        try:
            userInt = int(input(message))
            return userInt
        except ValueError:
            print('You must enter an integer')


def checkFloat(message):
    while True:
        try:
            userFloat = float(input(message))
            return userFloat
        except ValueError:
            print('You must enter a number')


def checkString(message):
    while True:
        try:
            userStr = str(input(message))
            return userStr
        except ValueError:
            print('You must enter an string')


def getChoice(choices):
    choice = ""
    while choice not in [i.lower() for i in choices]:
        choice = input("Choose one of [%s]: " % ", ".join(choices)).lower()
    return choice


def howManyEqu(players):
    thismany = [players[-1]]
    if len(players) == 1:
        return thismany
    for i in range(len(players) - 1):
        if players[-i-1].rankcomp(players[-i-2]) == 0: #players have equal hand rankings
            thismany.append(players[-i-2])
        else:
            return thismany

#similar to get choices to determine a player's chosen strategy
def getStrategy(funcs):
    print("Please enter a number corresponding to which strategy this player is using.")
    print("Choose one of:\n")
    for i in range(len(funcs)):
        print("{}: {}".format(str(i + 1), funcs[i].__name__))
    nums = list(range(1, len(funcs) + 1))
    nums = [str(j) for j in nums]
    return getChoice(nums) #returns a string of index one greater than element in function list e.g. if index is i then returns 'str(i+1)'
