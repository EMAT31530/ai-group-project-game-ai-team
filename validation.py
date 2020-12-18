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
    for i in range(len(players)):
        if players[-i-1] == players[-i-2]:
            thismany.append(players[-i-2])
        else:
            return thismany
