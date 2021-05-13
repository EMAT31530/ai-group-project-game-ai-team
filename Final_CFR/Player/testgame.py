from playgame import *
from games import PlayKuhn, PlayLeduc, Rules
#LOOK DOWN!!!!!!!!!!!!!
kuhnrules = Rules({"J": {"diamonds": 1}, "Q": {"diamonds": 2}, "K": {"diamonds": 3}}, 
    {'check': 'p', 'fold': 'p', 'bet': 'b', 'call': 'b'}, 
    10 )
leducrules = Rules({"J": {"diamonds": 1, "hearts": 1}, 
    "Q": {"diamonds": 2, "hearts": 2}, "K": {"diamonds": 3, "hearts": 3}}, 
    {'check': 'ch', 'fold': 'f', 'call': 'c', 'raise': 'r', 'reraise': 'rr'}, 
    20 )
newgame = Game(PlayLeduc, leducrules, 'AILeduc')

newgame.play()

#https://github.com/pwildenhain/terminal_playing_cards
#LOOK BELOW!!!!!!!!!!!!!

#run me pip install terminal-playing-cards