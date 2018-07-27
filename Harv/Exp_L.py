'''
Created on 25 Feb, 2014

@author: yzhang28
'''
import pickle

import multiprocessing

import sys
#sys.path.append(".")
from HarvCore.func import *

# READ_TRANSMAT_FROM_FILE = True

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
E = 10
# L = 10 # locations numbered: 0, 1, ..., L. L+1 states
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.90
DELTA = 0.1
RANDOM_COUNT = 5

L_list = [1,3,5,7,9,11,13,15,17,19]

expnum = len(L_list)
ParamsSet  = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_zero = [None for _ in range(expnum)]
RESset_one = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]


for ind, l_cur in enumerate(L_list):
    ParamsSet[ind] = {'A':A, \
                      'L':l_cur, 'E':E, \
                      'B':B, \
                      'GAM':DISCOUNT_FACTOR,\
                      'DELTA': DELTA, \
                      'LMAT': None, \
                      'WMAT': None, \
                      'SIG': None}

# Build transition matrix in a parallel manner

for ind, l_cur in enumerate(L_list):
    TransProbSet[ind] = BuildTransMatrix(ParamsSet[ind])
#     pickle.dump(TransProbSet[ind], open("../transmatrix/E_charging/transmat"+str(ind+1),"w"))
# print "Forming transition matrices. DONE" 
# 
# print "Loading transition matrices..."
# for ind, e_cur in enumerate(E_list):
#     TransProbSet[ind] = pickle.load(open("../transmatrix/E_charging/transmat"+str(ind+1),"r"))

print("START COMPUTING...")
for ind, l_cur in enumerate(L_list):
    print("---- ROUND:%d"%(ind+1), end=" ")
    print("out of %d"%expnum)

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
        print("RANDOM: %d/%d running..." % (rcount,RANDOM_COUNT-1))
        V_rnd, A_rnd = NaiveSolver_Rnd(TransProbSet[ind], ParamsSet[ind])
        RE_rnd = GetOptResultList(V_rnd,A_rnd, TransProbSet[ind], ParamsSet[ind])
        if rcount == 0:
            RE = [0.0 for _ in range(len(RE_rnd))]
        for i in range(len(RE_rnd)):
            RE[i] = RE[i] + RE_rnd[i]
    for i in range(len(RE)):
        RE[i] = RE[i]*1.0/(1.0*RANDOM_COUNT)
    RESset_rnd[ind] = RE
            
print("Dumping...", end=" ")
pickle.dump(expnum, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/expnum","wb"))
pickle.dump(ParamsSet, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/Paramsset","wb"))
pickle.dump(L_list, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/xaxis","wb"))
pickle.dump(RESset_bell, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/bell","wb"))
pickle.dump(RESset_myo, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/myo","wb"))
pickle.dump(RESset_zero, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/zero","wb"))
pickle.dump(RESset_one, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/one","wb"))
pickle.dump(RESset_rnd, open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/rnd","wb"))
print("Finished")

