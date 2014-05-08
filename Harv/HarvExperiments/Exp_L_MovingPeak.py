'''
Created on 25 Feb, 2014

@author: yzhang28
'''
import pickle

import sys
sys.path.append("..")
from HarvCore.func import *

# READ_TRANSMAT_FROM_FILE = True

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
E = 10 # energy state numbered: 0, 1, ..., L. L+1 states
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

L = 10

DISCOUNT_FACTOR = 0.90
DELTA = 0.1
RANDOM_COUNT = 5

# x_axis_list = [i for i in range(L+1)]
x_axis_list = [5, 10]

expnum = len(x_axis_list)
ParamsSet = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_zero = [None for _ in range(expnum)]
RESset_one = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]

PEAK = 0.8

# Matline = [[] for _ in range(len(x_axis_list))]
# for line_index, itemline in enumerate(Matline):
#     for elem_index in x_axis_list:
#         if elem_index == line_index:
#             Matline[line_index].append(PEAK)
#         else:
#             Matline[line_index].append((1.0-PEAK)/(len(x_axis_list)-1.0))

Matline = [[] for _ in range(len(x_axis_list))]
for line_index, itemline in enumerate(Matline):
    for elem_index in range(L+1):
        if elem_index == x_axis_list[line_index]:
            Matline[line_index].append(PEAK)
        else:
            Matline[line_index].append((1.0-PEAK)/(L-1.0))


for ind, l_cur in enumerate(x_axis_list):
#     LMAT = [Matline[l_cur] for _ in range(0,L+1)]
    LMAT = [Matline[ind] for _ in range(0,L+1)]
    ParamsSet[ind] = {'A':A, \
                'L':L, 'E':E, \
                'B':B, \
                'GAM':DISCOUNT_FACTOR,\
                'DELTA': DELTA, \
                'LMAT': LMAT, \
                'WMAT': None, \
                'SIG': None}

# Build transition matrix in a parallel manner
# if READ_TRANSMAT_FROM_FILE == False:
for ind, e_cur in enumerate(x_axis_list):
    TransProbSet[ind] = BuildTransMatrix(ParamsSet[ind])
#         pickle.dump(TransProbSet[ind], open("../transmatrix/L_MovingPeak/transmat"+str(ind+1),"w"))
#     print "Forming transition matrices. DONE"
# else:
#     print "Loading transition matrices..."
#     for ind, e_cur in enumerate(x_axis_list):
#         TransProbSet[ind] = pickle.load(open("../transmatrix/L_MovingPeak/transmat"+str(ind+1),"r"))
#     
print "START COMPUTING..."
for ind, e_cur in enumerate(x_axis_list):
    print "---- ROUND:", ind+1,
    print "out of", expnum

    # Bellman
    V_bell, A_bell = BellmanSolver(TransProbSet[ind], ParamsSet[ind])
    RESset_bell[ind] = GetOptResultList(V_bell,A_bell, TransProbSet[ind], ParamsSet[ind])

    # Myopic
    V_myo, A_myo = NaiveSolver_Myopic(TransProbSet[ind], ParamsSet[ind])
    RESset_myo[ind] = GetOptResultList(V_myo,A_myo, TransProbSet[ind], ParamsSet[ind])

    # All 0
    V_zero, A_zero = NaiveSolver_AllSame(TransProbSet[ind], 0,ParamsSet[ind])
    RESset_zero[ind] = GetOptResultList(V_zero,A_zero, TransProbSet[ind], ParamsSet[ind])

    # All 1
    V_one, A_one = NaiveSolver_AllSame(TransProbSet[ind], 1,ParamsSet[ind])
    RESset_one[ind] = GetOptResultList(V_one,A_one, TransProbSet[ind], ParamsSet[ind])

    # Random - a special algorithm case
    # we don't care about Values and Actions
    rangeE, rangeL, rangeW = range(ParamsSet[ind]['E']+1), range(ParamsSet[ind]['L']+1), range(ParamsSet[ind]['A']+1)
    RE = []
    for rcount in range(RANDOM_COUNT):
        print "RANDOM: %d/%d running..." % (rcount,RANDOM_COUNT-1)
        V_rnd, A_rnd = NaiveSolver_Rnd(TransProbSet[ind], ParamsSet[ind])
        RE_rnd = GetOptResultList(V_rnd,A_rnd, TransProbSet[ind], ParamsSet[ind])
        if rcount == 0:
            RE = [0.0 for _ in range(len(RE_rnd))]
        for i in range(len(RE_rnd)):
            RE[i] = RE[i] + RE_rnd[i]
    for i in range(len(RE)):
        RE[i] = RE[i]*1.0/(1.0*RANDOM_COUNT)
    RESset_rnd[ind] = RE

print "Dumping...",
pickle.dump(expnum, open("../results/L_MovingPeak/expnum","w"))
pickle.dump(ParamsSet, open("../results/L_MovingPeak/Paramsset","w"))
pickle.dump(x_axis_list, open("../results/L_MovingPeak/xaxis","w"))
pickle.dump(RESset_bell, open("../results/L_MovingPeak/bell","w"))
pickle.dump(RESset_myo, open("../results/L_MovingPeak/myo","w"))
pickle.dump(RESset_zero, open("../results/L_MovingPeak/zero","w"))
pickle.dump(RESset_one, open("../results/L_MovingPeak/one","w"))
pickle.dump(RESset_rnd, open("../results/L_MovingPeak/rnd","w"))
print "Finished"

