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
'''
test = open('rawdata/'+'abs NLH handhq_1-OBFUSCATED.txt', 'r')'''
test = open('testtestdata.txt', 'r')
lines=test.readlines()
print(lines[0])

totalgames=0


print(lines[28])
if len(lines[29].strip()) == 0:
    print('hi')

i = 0
game = 0
splitgames = []
endoffile = False
end = False
while endoffile is False:
    if i == len(lines):
        endoffile = True
    else:
        if game == 0:
            splitgames.append([])
            end = False
        else:
            splitgames.append([])
            game = game + 1
            end = False
    while end is False:
        print('end false')
        if len(lines[i].strip()) == 0:
            print('blank line')
            i = i+1
            end = True
        else:
            print('not blank')
            print(splitgames)
            print(game)
            splitgames[game].append(lines[i])
            i = i+1

print(splitgames[0])
