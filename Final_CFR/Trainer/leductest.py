import sys
import time
import vectorcfr as vec
import scalarcfr as scal
from LeducPoker import Leduc, LeducRules
#sys.path.append('../modules')
#import validation as vald


def display_results(ev, node_map):
    print('\nexpected value: {}'.format(ev))
    print('\nplayer 1 strategies:')
    sorted_items = sorted(node_map.items(), key=lambda x: x[0][0])
    for _, v in sorted_items:
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
    trainer = scal.VCFRTrainer(Leduc, LeducRules)
if type == 2:
    trainer = scal.PruningCFRTrainer(Leduc, LeducRules)
if type == 3:
    trainer = scal.OutcomeSamplingCFRTrainer(Leduc, LeducRules)
if type == 4:
    trainer = scal.CSCFRTrainer(Leduc, LeducRules)
if type == 5:
    trainer = vec.VectorAlternatingVCFR(Leduc, LeducRules)
if type == 6:
    trainer = vec.PublicCSCFRTrainer(Leduc, LeducRules)
if type == 7:
    trainer = vec.OpponentPublicCSCFRTrainer(Leduc, LeducRules)
if type == 8:
    trainer = vec.SelfPublicCSCFRTrainer(Leduc, LeducRules)
if type == 9:
    trainer = vec.CFRPlusTrainer(Leduc, LeducRules)


if train:
    time1 = time.time()
    
    util = trainer.train(n_iterations=iterations)
    finalstrat = trainer.get_final_strategy()

    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)
'''
else:
    time1 = time.time()
    trainer = VectorAlternatingVCFR(gamestatestype, gamerulestype)
    ExplCalc = Exploit_Calc()
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