import sys
import time
import numpy as np
sys.path.append('..')
import Trainer.vectorcfr as vec
import Trainer.scalarcfr as scal
from Trainer.gamestates.blankgamestate import GenericPoker
from Trainer.gamestates.gamerules import LeducRules
from Trainer.exploitability import Exploit_Calc, Exploit_Vec_Calc
from modules.validation import exportJson

ranks = {
        'KK': 9,
        'QQ': 8,
        'JJ': 7,
        'KQ': 6, 'QK': 6,
        'KJ': 5, 'JK': 5,
        'QJ': 4, 'JQ': 4,
        'K-': 3, 'Q-': 2, 'J-': 1
        }

def display_results(ev, node_map):
    print('\nexpected value: {}'.format(ev))
    print('\nplayer 1 strategies:')
    sorted_items = sorted(node_map.items(), key=lambda x: ranks[x[0][:2]])
    for j, v in enumerate(sorted_items):
        if j < 50 or j > len(sorted_items) - 10:
            r = [round(i , 2) for i in v[1]]
            print('{}: {}'.format(v[0],r))

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
    gamestate = GenericPoker(LeducRules)
    trainer = scal.VCFRTrainer(gamestate)
if type == 2:
    gamestate = GenericPoker(LeducRules)
    trainer = scal.OutcomeSamplingCFRTrainer(gamestate)
if type == 3:
    gamestate = GenericPoker(LeducRules)
    trainer = scal.CSCFRTrainer(gamestate)
if type == 4:
    gamestate = GenericPoker(LeducRules, vectorised=True)
    trainer = vec.VectorAlternatingVCFR(gamestate)
if type == 5:
    gamestate = GenericPoker(LeducRules, vectorised=True)
    trainer = vec.PublicCSCFRTrainer(gamestate)
if type == 6:
    gamestate = GenericPoker(LeducRules, vectorised=True)
    trainer = vec.OpponentPublicCSCFRTrainer(gamestate)
if type == 7:
    gamestate = GenericPoker(LeducRules, vectorised=True)
    trainer = vec.SelfPublicCSCFRTrainer(gamestate)
if type == 8:
    gamestate = GenericPoker(LeducRules, vectorised=True)
    trainer = vec.CFRPlusTrainer(gamestate)

print('\nTraining leduc poker via {}.'.format(trainer.__name__()))

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
    nodes_touched = []
    timestep = [0]
    stepnum = 10
    steps = int(iterations/stepnum)
    time1 = time.time()
    for i in range(stepnum):
        util += trainer.train(n_iterations=steps)
        timestep.append(round(timestep[-1] + abs(time.time() - time1),2))
        exp1 = ExplCalc.compute_exploitability(trainer)[0]
        exp2 = ExplVecCalc.compute_exploitability(trainer)[0]
        exploit.append(round(exp1, 5))
        exploitvec.append(round(exp2, 5))
        nodes_touched.append("{:1.2e}".format(trainer.nodes_touched))
        time1 = time.time()


    util = util/stepnum
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
    exportJson(finalstrat, 'leduc{}-{}'.format(type, iterations))