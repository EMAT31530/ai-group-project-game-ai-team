from graphics import *
from AIclasses import *
import tkinter as tk

def playerinit(playernames, funds, graphwin):
    # player names
    Text(Point(75, 50), 'Player: %s' % playernames[0]).draw(graphwin).setSize(13)
    Text(Point(75, 950), 'Player: %s' % playernames[1]).draw(graphwin).setSize(13)
    # player funds
    Text(Point(75, 25), 'Funds: $%s' % funds[0]).draw(graphwin).setSize(13)
    Text(Point(75, 975), 'Funds: $%d' % funds[1]).draw(graphwin).setSize(13)


def carddraw(num, suit, point, graphwin):
    # create white rectangle
    rect = Rectangle(Point(point[0]-50, point[1]-75 ),Point(point[0]+50, point[1]+75))
    rect.setFill('white')
    rect.draw(graphwin)
    # create numbers
    Text(Point(point[0]-35, point[1]+60), num).draw(graphwin)
    Text(Point(point[0]+35, point[1]-60), num).draw(graphwin)

    # suit
    Text(Point(point[0], point[1]), suit).draw(graphwin).setSize(18)


def boardupdate(pot, currentbet, graphwin):
    Text(Point(75, 525), 'Pot: $%d' % pot).draw(graphwin).setSize(13)
    Text(Point(75, 475), 'Current bet: $%d' % currentbet).draw(graphwin).setSize(13)


def player1hand(hand1, graphwin):
    # player 1
    carddraw(hand[0], hand[1], (445, 100), graphwin)

    carddraw(hand[3], hand[4], (555, 100), graphwin)


def player2hand(hand2, graphwin):
    # player 2
    carddraw(hand[0], hand[1], (445, 900), graphwin)

    carddraw(hand[3], hand[4], (555, 900), graphwin)


def board(hand3, graphwin):
    # board
    carddraw(10, '♠', (280, 500), win)

    carddraw('J', '♦', (390, 500), win)

    carddraw('Q', '♥', (500, 500), win)

    carddraw('K', '♦', (610, 500), win)

    carddraw('A', '♠', (720, 500), win)


def main():
    win = GraphWin('Face', 1000, 1000)  # give title and dimensions
    win.setCoords(0, 0, 1000, 1000)  # make right side up coordinates!
    # player 1
    carddraw(2, '♥', (445, 100), win)

    carddraw(3, '♦', (555, 100), win)

    # player 2
    carddraw(8, '♣', (445, 900), win)

    carddraw(5, '♠', (555, 900), win)

    # board

    carddraw(10, '♠', (280, 500), win)

    carddraw('J', '♦', (390, 500), win)

    carddraw('Q', '♥', (500, 500), win)

    carddraw('K', '♦', (610, 500), win)

    carddraw('A', '♠', (720, 500), win)

    boardupdate(500, 5000, win)
    playerinit(['Arnold', 'Joe'], [500, 600], win)
    Button(win, Point(300,300), 40, 40, 'Quit')








    win.setBackground('green')
    win.getMouse()
    win.close()


#main()

window = tk.Tk()
window.geometry("1000x1000")
board= tk.Canvas(window, bg="green", height=1000, width=1000).pack()
tk.Canvas(window, bg="blue", height=50, width=50).place(x=500,y=500)
card=board.create_rectangle(500-50,500-75, 500+50,500+75, fill="white")
card.pack()

window.configure(bg='green')


window.mainloop()
