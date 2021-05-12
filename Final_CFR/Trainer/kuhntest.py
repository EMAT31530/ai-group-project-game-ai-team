import sys
import time
import vectorcfr as vec
import scalarcfr as scal
from KuhnPoker import Kuhn, KuhnRules
#from exploitability import *
#sys.path.append('../modules')
#import validation as vald


def display_results(ev, node_map):
    ranking = {'J': 1, 'Q': 2, 'K': 3}
    print('\nexpected value: {}'.format(ev))
    print('\nplayer 1 strategies:')
    #print([i for i in node_map.items()])
    sorted_items = sorted(node_map.items(), key=lambda x: ranking[x[0][0]])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))
    print('\nplayer 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))



if len(sys.argv) < 2:
    type = 1
else:
    type = int(sys.argv[1])
if len(sys.argv) < 3:
    iterations = 10000
else:
    iterations = int(sys.argv[2])
if len(sys.argv) < 4:
    train = True
else:
    train = 0 == int(sys.argv[3])

if type == 1:
    trainer = scal.VCFRTrainer(Kuhn, KuhnRules)
if type == 2:
    trainer = scal.PruningCFRTrainer(Kuhn, KuhnRules)
if type == 3:
    trainer = scal.OutcomeSamplingCFRTrainer(Kuhn, KuhnRules)
if type == 4:
    trainer = scal.CSCFRTrainer(Kuhn, KuhnRules)
if type == 5:
    trainer = vec.VectorAlternatingVCFR(Kuhn, KuhnRules)
if type == 6:
    trainer = vec.PublicCSCFRTrainer(Kuhn, KuhnRules)
if type == 7:
    trainer = vec.OpponentPublicCSCFRTrainer(Kuhn, KuhnRules)
if type == 8:
    trainer = vec.SelfPublicCSCFRTrainer(Kuhn, KuhnRules)
if type == 9:
    trainer = vec.CFRPlusTrainer(Kuhn, KuhnRules)

if train:
    print('\nTraining kuhn poker via {}.'.format(trainer.__name__()))
    time1 = time.time()
    util = trainer.train(n_iterations=iterations)
    finalstrat = trainer.get_final_strategy()

    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)
'''
else:
    ExplCalc = Exploit_Calc()
    print('\nTraining kuhn poker via {}.'.format(trainer.__name__()))
    time1 = time.time()
    util = 0
    exploit = []
    timestep = []
    stepnum = 2
    steps = int(iterations/stepnum)
    for i in range(stepnum):
        util += trainer.train(n_iterations=steps)
        exploit.append(round(ExplCalc.compute_exploitability(trainer)[0] , 3))
        timestep.append(steps * (i+1))

    finalstrat = trainer.get_final_strategy()
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)
    print('expl : {}'.format(exploit))'''