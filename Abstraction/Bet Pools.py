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

from pprint import pprint
import json



with open('hands_valid.json') as f:
    tweets = []
    for line in open('hands_valid.json', 'r'):
        tweets.append(json.loads(line))


try:
    with open('hands_valid.json', 'r') as f:
        print('#' * 60)
        line = f.readline()
        while line:
            hand = json.loads(line)
            pots = []
            for stage in ['f', 't', 'r', 's']:
                p = [h for h in hand['pots'] if h['stage'] == stage][0]
                pots.append((p['num_players'], p['size']))

            print("pots")
            print(pots[0])
            print(pots[1])
            print(pots[2])
            print(pots[3])
            print(pots)
            hand['players'] = {player['pos']: player for player in hand['players']}
            for pos in range(1, hand['num_players'] + 1):
                description = hand['players'][pos].copy()
                user = description['user']
                del description['user'], description['pos']
                pprint(description)
                print(('· ' if pos < hand['num_players'] else '##') * 30)
            line = f.readline()
    print('Finished.')
except KeyboardInterrupt:
    print('Interrupted.')

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(tweets[0])
