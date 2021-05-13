from playgame import *
from games import PlayKuhn, Rules

kuhnrules = Rules({"J": {"diamonds": 1}, "Q": {"diamonds": 2}, "K": {"diamonds": 3}}, 
    {'check': 'p', 'fold': 'p', 'bet': 'b', 'call': 'b'}, 
    10 )

newgame = Game(PlayKuhn, kuhnrules, 'AI1')

newgame.play()