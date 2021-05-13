import sys
import time
import vectorcfr as vec
import scalarcfr as scal
from KuhnPoker import Kuhn, KuhnRules
from exploitability import Exploit_Calc, Exploit_Vec_Calc
sys.path.append('../modules')
from validation import exportJson


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
if len(sys.argv) < 5:
    export = False
else:
    export = 1 == int(sys.argv[4])

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

print('\nTraining kuhn poker via {}.'.format(trainer.__name__()))

if train:
    time1 = time.time()
    util = trainer.train(n_iterations=iterations)
    finalstrat = trainer.get_final_strategy()

    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)

else:
    ExplCalc = Exploit_Calc()
    ExplVecCalc = Exploit_Vec_Calc()
    time1 = time.time()
    util = 0
    exploit = []
    exploitvec = []
    timestep = []
    stepnum = 100
    steps = int(iterations/stepnum)
    for i in range(stepnum):
        util += trainer.train(n_iterations=steps)
        exp1 = ExplCalc.compute_exploitability(trainer)[0]
        #exp2 = ExplVecCalc.compute_exploitability(trainer)[0]
        exploit.append(round(exp1, 5))
        #exploitvec.append(round(exp2, 3))
        #timestep.append(steps * (i+1))

    finalstrat = trainer.get_final_strategy()
    print('Completed {} iterations in {} seconds.'.format(iterations, abs(time1 - time.time())))
    print('With {} nodes.'.format(len(finalstrat)))
    display_results(util, finalstrat)
    print('expl lin: {}'.format(exploit))
    print('expl vec: {}'.format(exploitvec))

if export:
    exportJson(finalstrat, 'kuhn{}-{}'.format(type, iterations))