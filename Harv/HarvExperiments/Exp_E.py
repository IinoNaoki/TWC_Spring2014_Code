'''
Created on 25 Feb, 2014

@author: yzhang28
'''
import pickle

import multiprocessing

import sys
sys.path.append("..")
from HarvCore.func import *

READ_TRANSMAT_FROM_FILE = True

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
L = 10 # locations numbered: 0, 1, ..., L. L+1 states
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.95
DELTA = 0.1
RANDOM_COUNT = 5

E_list = [6,7,8,9,10,11,12,13,14,15]

expnum = len(E_list)
ParamsSet  = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_zero = [None for _ in range(expnum)]
RESset_one = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]


for ind, e_cur in enumerate(E_list):
    ParamsSet[ind] = {'A':A, \
                      'L':L, 'E':e_cur, \
                      'B':B, \
                      'GAM':DISCOUNT_FACTOR,\
                      'DELTA': DELTA, \
                      'LMAT': None, \
                      'WMAT': None, \
                      'SIG': None}

# Build transition matrix in a parallel manner
if READ_TRANSMAT_FROM_FILE == False:
    for ind, e_cur in enumerate(E_list):
        TransProbSet[ind] = BuildTransMatrix(ParamsSet[ind])
        pickle.dump(TransProbSet[ind], open("../transmatrix/E_charging/transmat"+str(ind+1),"w"))
    print "Forming transition matrices. DONE" 
else:
    print "Loading transition matrices..."
    for ind, e_cur in enumerate(E_list):
        TransProbSet[ind] = pickle.load(open("../transmatrix/E_charging/transmat"+str(ind+1),"r"))
    
    print "START COMPUTING..."
    for ind, e_cur in enumerate(E_list):
        print "---- ROUND:", ind+1,
        print "out of", expnum
    
        # Bellman
        V_bell, A_bell = BellmanSolver(TransProbSet[ind], ParamsSet[ind])
        RESset_bell[ind] = GetOptResultList(V_bell,A_bell, TransProbSet[ind], ParamsSet[ind])
    
        # Myopic
        V_myo, A_myo = NaiveSolver_Myopic(TransProbSet[ind], ParamsSet[ind])
        RESset_myo[ind] = GetOptResultList(V_myo,A_myo, TransProbSet[ind], ParamsSet[ind])
    
        # All 0
        V_zero, A_zero = NaiveSolver_AllSame(TransProbSet[ind], 0, ParamsSet[ind])
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
    pickle.dump(expnum, open("../results/E_changing/expnum","w"))
    pickle.dump(ParamsSet, open("../results/E_changing/Paramsset","w"))
    pickle.dump(E_list, open("../results/E_changing/xaxis","w"))
    pickle.dump(RESset_bell, open("../results/E_changing/bell","w"))
    pickle.dump(RESset_myo, open("../results/E_changing/myo","w"))
    pickle.dump(RESset_zero, open("../results/E_changing/zero","w"))
    pickle.dump(RESset_one, open("../results/E_changing/one","w"))
    pickle.dump(RESset_rnd, open("../results/E_changing/rnd","w"))
    print "Finished"

