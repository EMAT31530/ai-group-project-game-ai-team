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


def howManyEqu(players):
    thismany = [players[-1]]
    for i in range(len(players)):
        if players[-i-1] == players[-i-2]:
            thismany.append(players[-i-2])
        else:
            return thismany


def quickSort(arr, low, high):
    if len(arr) == 2:
        if arr[1] < arr[0] or arr[1] == arr[0]:
            return arr
        else:
            return arr.reverse()

    def partition(arr, low, high):
        i = (low-1)         # index of smaller element
        pivot = arr[high]     # pivot
        for j in range(low, high):
            if arr[j] <= pivot:
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return (i+1)

    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)


def bubbleSort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
