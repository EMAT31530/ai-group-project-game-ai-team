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

test = open('rawdata/'+'abs NLH handhq_1-OBFUSCATED.txt', 'r')
lines=test.readlines()
print(lines[0])

totalgames=0

print(lines[0])
print(len(lines))
if 'stage' in lines[0].lower():
    print('hi')
for i in range(len(lines)):
    if 'stage' in lines[i].lower():
        totalgames+=1
