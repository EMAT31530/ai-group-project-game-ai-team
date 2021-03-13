import matplotlib.pyplot as plt

def graphing(winratedict):
    x=list(winratedict.items())
    for i in range(0, len(x[0][1])):
        """
        currwinrate = []
        for k in range(0, len(x)):
            currwinrate.append(x[k][1][i])
            print(currwinrate)"""
        plt.plot([y for y in range(0, len(x))], [x[k][1][i] for k in range(0,len(x))])
        plt.xlabel('Number of games played')
        plt.ylabel('Win Rate')
        plt.show()
