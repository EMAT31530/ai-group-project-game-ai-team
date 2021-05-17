import matplotlib.pyplot as plt

#Placeholderfunc for now
def graphing(metricdict):
    x=list(metricdict.items())
    for i in range(0, len(x[0][1])):
        plt.plot([y for y in range(0, len(x))], [x[k][1][i] for k in range(0,len(x))])
        plt.xlabel('Another Metric')
        plt.ylabel('Metric')
        plt.show()