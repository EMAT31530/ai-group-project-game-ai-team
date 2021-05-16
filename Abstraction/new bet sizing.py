"""
method:
Parse data of poker players and poker games

Take the pot size, preflop pot, river pot, turn pot.

Take the bet size of every player at given pot sizes, find the proportion of
the bet size to the pot size.

Take 5 percentiles of the most common bet sizes? Ie 25th %tile,
50th %percentile 75th %tile

end result is, for each point in the game, ie flop, river, turn
we will have the most common bet sizes as parsed from several thousands
of real poker players
"""

# archived code for removing the blank lines at the end of each file
'''
for j in range(1,150):
    with open('rawdata/'+'abs NLH handhq_'+str(j)+'-OBFUSCATED.txt', "r") as f:
        lines = f.readlines()
    #pop out -1 -2 -3
    lines.pop()
    lines.pop()
    lines.pop()
    with open('rawdata/'+'abs NLH handhq_'+str(j)+'-OBFUSCATED.txt', "w") as f:
        for line in lines:
            f.write(line)

'''
import re


test = open('rawdata/'+'abs NLH handhq_25-OBFUSCATED.txt', 'r')
lines = test.readlines()
i = 0
game = 0
splitgames = []
endoffile = False
end = False
blankline = False
# splits each game into a separate list element for analysis
while endoffile is False:
    if i == len(lines):
        endoffile = True
    else:
        if len(splitgames) == 0:
            splitgames.append([])
            blankline = False
            end = False
        else:
            game = game + 1
            splitgames.append([])
            blankline = False
            end = False
    while end is False and i != len(lines):
        if len(lines[i].strip()) == 0:
            # skips through the blank lines until the next game begins
            while blankline is False:
                if len(lines[i].strip()) == 0:
                    i = i+1
                else:
                    blankline = True
            end = True
        else:
            # adds each line to the game item

            splitgames[game].append(lines[i])
            i = i+1


# have to deal with ante, raise, call
potstorage=[]
ante = ''

# counts through each game
for j in range(0,1):
    # checks each line of the game
    # let's start with count total pot first
    pot = 0
    smallblind = ''
    bigblind = ''
    currentbet = ''
    call = ''
    raised = ''
    antetotal = 0
    for i in range(len(splitgames[j])):
        ante = ''
        print(splitgames[j][i])
        if 'ante' in splitgames[j][i].lower():
            pointer = splitgames[j][i].find('ante')-1
            print(splitgames[j][i][pointer])
            while splitgames[j][i][pointer] != '$':
                print(splitgames[j][i][pointer])
                if splitgames[j][i][pointer].isnumeric() is True:
                    ante = str(ante) + str(splitgames[j][i][pointer])
                    pointer -= 1
                else:
                    pointer -= 1
            ante = int(ante[::-1])
            print(ante)
            pot += ante

'''
elif 'small blind' in splitgames[j][i].lower():
    pointer = splitgames[j][i].find('small blind')-1
    while splitgames[j][i][pointer] != '$':
        if splitgames[j][i][pointer].isnumeric() is True:
            smallblind = str(smallblind) + str(splitgames[j][i][pointer])
            pointer -= 1
        else:
            pointer -= 1
'''



print(pot)
