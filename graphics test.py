from graphics import *


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


    win.setBackground('green')
    win.getMouse()
    win.close()


main()
