import sys
import time
import numpy as np
from copy import deepcopy
sys.path.append('..')
import Trainer.vectorcfr as vec
import Trainer.scalarcfr as scal
from Trainer.gamestates.blankgamestate import GenericPoker
from Trainer.gamestates.gamerules import KuhnRules, OnecardpokerRules, LeducRules, RoyalRules
from Trainer.exploitability import Exploit_Calc, Exploit_Vec_Calc
from modules.validation import exportJson


def display_results(ev, node_map):
    print('\nexpected value: {}'.format(ev))
    print('\nplayer 1 strategies:')
    for j, v in enumerate(node_map.items()):
        if j < 5 or j > len(node_map.items()) - 5:
            r = [round(i , 2) for i in v[1]]
            print('{}: {}'.format(v[0],r))

if len(sys.argv) < 2:
    game_on = 'k'
else:
    game_on = str(sys.argv[1])
if len(sys.argv) < 3:
    method_used = 1
else:
    method_used = int(sys.argv[2])
if len(sys.argv) < 4:
    steps = 100
else:
    steps = int(sys.argv[3])
if len(sys.argv) < 5:
    stepnum = 0
else:
    stepnum = int(sys.argv[4])
if len(sys.argv) < 6:
    export = False
else:
    export = 1 == int(sys.argv[5])

if game_on == 'k':
    rules = KuhnRules
elif game_on == 'l':
    rules = LeducRules
elif game_on == 'r':
    rules = RoyalRules
elif game_on[0] == 'n':
    rules = OnecardpokerRules

def get_trainer(method_used):
    if method_used < 4:
        gamestate = GenericPoker(rules)
    elif method_used > 3:
        gamestate = GenericPoker(rules, vectorised=True)

    if method_used == 1:
        trainer = scal.VCFRTrainer(gamestate)
    if method_used == 2:
        trainer = scal.OutcomeSamplingCFRTrainer(gamestate)
    if method_used == 3:
        trainer = scal.CSCFRTrainer(gamestate)
    if method_used == 4:
        trainer = vec.VectorAlternatingVCFR(gamestate)
    if method_used == 5:
        trainer = vec.PublicCSCFRTrainer(gamestate)
    if method_used == 6:
        trainer = vec.OpponentPublicCSCFRTrainer(gamestate)
    if method_used == 7:
        trainer = vec.SelfPublicCSCFRTrainer(gamestate)
    if method_used == 8:
       trainer = vec.CFRPlusTrainer(gamestate)
    return trainer

trainer = get_trainer(method_used)
print('\nTraining {} poker via {}.'.format(rules.__name__,trainer.__name__()))

if stepnum < 1:
    time1 = time.time()
    util = trainer.train(n_iterations=steps*100)
    finalstrat = trainer.get_final_strategy()

    print('Completed {} iterations in {} seconds.'.format(steps*100, abs(time1 - time.time())))
    print('With {} nodes and {} node touches.'.format(len(finalstrat), trainer.nodes_touched))
    display_results(util, finalstrat)

else:
    ExplCalc = Exploit_Calc()
    timeT = time.time()
    util = 0
    exploit = []
    timestep = [0]
    iter_list = []
    nodes_touched = []
    time1 = time.time()
    exp1 = 1
    for i in range(stepnum):
        util += trainer.train(n_iterations=steps)
        timestep.append(round(timestep[-1] + abs(time.time() - time1),2))
        exp1 = ExplCalc.compute_exploitability(trainer)[0]
        exploit.append(round(exp1, 5))
        nodes_touched.append("{:1.2e}".format(trainer.nodes_touched))
        iter_list.append(steps * (i+1))
        time1 = time.time()

    exploit = np.array(exploit)
    for i in range(2):
        newtrainer = get_trainer(method_used)
        for j in range(len(exploit)):
            newtrainer.train(n_iterations=steps)
            explo = ExplCalc.compute_exploitability(newtrainer)[0]
            exploit[j] += round(explo, 5)
    exploit=exploit/3
    expl_list = [round(i, 4) for i in exploit]
    finalstrat = trainer.get_final_strategy()
    print('Completed {} iterations in {} seconds (really {}).'.format(iter_list[-1], round(abs(timeT - time.time()), 2), timestep[-1]))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)
    print('expl lin: {}'.format(expl_list))
    #milblinds = list(np.array(exploit)/0.001)
    #print('milblinds lin: {}'.format(milblinds))
    #print('touching nodes: {}'.format(nodes_touched))
    #print('time: {}'.format(timestep))

if export:
    #to export: finalstrat, iterations, exploit, milblinds, nodes_touched, timestep
    timestep.remove(0)
    
    fat_list = [iter_list, timestep, nodes_touched, expl_list]


    exportJson(fat_list, '{}VIA{}-{}avg'.format(rules.__name__,method_used, iter_list[-1]))