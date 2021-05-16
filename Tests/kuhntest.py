import sys
import time
import numpy as np
sys.path.append('..')
import Trainer.vectorcfr as vec
import Trainer.scalarcfr as scal
from Trainer.gamestates.blankgamestate import GenericPoker
from Trainer.gamestates.gamerules import KuhnRules
from Trainer.exploitability import Exploit_Calc, Exploit_Vec_Calc
from modules.validation import exportJson


def display_results(ev, node_map):
    ranking = {'J': 1, 'Q': 2, 'K': 3}
    print('\nexpected value: {}'.format(ev))
    print('\nplayer 1 strategies:')
    #print([i for i in node_map.items()])
    sorted_items = sorted(node_map.items(), key=lambda x: ranking[x[0][0]])
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        r = [round(i , 2) for i in v]
        print('{}: {}'.format(_,r))
    print('\nplayer 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
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
if len(sys.argv) < 5:
    export = False
else:
    export = 1 == int(sys.argv[4])

if type == 1:
    gamestate = GenericPoker(KuhnRules)
    trainer = scal.VCFRTrainer(gamestate)
if type == 2:
    gamestate = GenericPoker(KuhnRules)
    trainer = scal.OutcomeSamplingCFRTrainer(gamestate)
if type == 3:
    gamestate = GenericPoker(KuhnRules)
    trainer = scal.CSCFRTrainer(gamestate)
if type == 4:
    gamestate = GenericPoker(KuhnRules, vectorised=True)
    trainer = vec.VectorAlternatingVCFR(gamestate)
if type == 5:
    gamestate = GenericPoker(KuhnRules, vectorised=True)
    trainer = vec.PublicCSCFRTrainer(gamestate)
if type == 6:
    gamestate = GenericPoker(KuhnRules, vectorised=True)
    trainer = vec.OpponentPublicCSCFRTrainer(gamestate)
if type == 7:
    gamestate = GenericPoker(KuhnRules, vectorised=True)
    trainer = vec.SelfPublicCSCFRTrainer(gamestate)
if type == 8:
    gamestate = GenericPoker(KuhnRules, vectorised=True)
    trainer = vec.CFRPlusTrainer(gamestate)

print('\nTraining kuhn poker via {}.'.format(trainer.__name__()))

if train:
    time1 = time.time()
    util = trainer.train(n_iterations=iterations)
    finalstrat = trainer.get_final_strategy()

    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes and {} node touches.'.format(len(finalstrat), trainer.nodes_touched))
    display_results(util, finalstrat)

else:
    ExplCalc = Exploit_Calc()
    ExplVecCalc = Exploit_Vec_Calc()
    timeT = time.time()
    util = 0
    exploit = []
    exploitvec = []
    timestep = [0]
    nodes_touched = []
    stepnum = 10
    steps = int(iterations/stepnum)
    time1 = time.time()
    for i in range(stepnum):
        util += trainer.train(n_iterations=steps)
        exp1, brLIN = ExplCalc.compute_exploitability(trainer)
        exp2, brVEC = ExplVecCalc.compute_exploitability(trainer)
        timestep.append(round(timestep[-1] + abs(time.time() - time1),2))
        exploit.append(round(exp1, 5))
        exploitvec.append(round(exp2, 5))
        nodes_touched.append("{:1.2e}".format(trainer.nodes_touched))
        time1 = time.time()
        
        '''boel = True
        for key in brLIN:
            if not (key in brVEC and np.array_equal(brLIN[key],brVEC[key])):
                boel = False
        for key in brVEC:
            if not (key in brLIN and np.array_equal(brLIN[key],brVEC[key])):
                boel = False    
        print(boel)'''


    finalstrat = trainer.get_final_strategy()
    print('Completed {} iterations in {} seconds.'.format(iterations, round(abs(timeT - time.time()), 2)))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)
    print('expl lin: {}'.format(exploit))
    milblinds = np.array(exploit)/0.001
    #print('milblinds lin: {}'.format(milblinds))
    print('expl vec: {}'.format(exploitvec))
    print('touching nodes: {}'.format(nodes_touched))
    print('time: {}'.format(timestep))

if export:
    exportJson(finalstrat, 'kuhn{}-{}'.format(type, iterations))