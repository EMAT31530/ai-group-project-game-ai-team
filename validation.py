def checkInt(message):
    while True:
        try:
            userInt = int(input(message))
            return userInt
        except ValueError:
            print('You must enter an integer')


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
