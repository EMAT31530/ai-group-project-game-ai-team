from TerminalPlayer.game import *
from TerminalPlayer.gametypes import PlayKuhn, PlayLeduc, Rules

if len(sys.argv) < 2:
    gamtype = 'k'
    ai = 'AIKuhn'
else:
    gamtype = str(sys.argv[1])
    ai = 'AILeduc'
if len(sys.argv) > 2:
    ai = str(sys.argv[2])

kuhnrules = Rules({"J": {"diamonds": 1}, "Q": {"diamonds": 2}, "K": {"diamonds": 3}}, 
    {'check': 'p', 'fold': 'p', 'bet': 'b', 'call': 'b'}, 
    10 )
leducrules = Rules({"J": {"diamonds": 1, "hearts": 1}, 
    "Q": {"diamonds": 2, "hearts": 2}, "K": {"diamonds": 3, "hearts": 3}}, 
    {'check': 'ch', 'fold': 'f', 'call': 'c', 'raise': 'r', 'reraise': 'R'}, 
    20 )

if gamtype == 'k':
    game = Game(PlayKuhn, kuhnrules, ai)
elif gamtype == 'l':
    game = Game(PlayLeduc, leducrules, ai)

game.play()
