'''
Created on 25 Feb, 2014

@author: yzhang28
'''

import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox

import multiprocessing

import sys
sys.path.append("..")
from HarvCore.func import *

READ_TRANSMAT_FROM_FILE = False

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
L = 10 # locations numbered: 0, 1, ..., L. L+1 states
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.3
DELTA = 0.1
RANDOM_COUNT = 1

# E_list = [6,7,8,9,10,11,12,13,14,15]
E_list = [6,7,8,9]

expnum = len(E_list)
Paramsset  = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_zero = [None for _ in range(expnum)]
RESset_one = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]


for e_cur,ind in enumerate(E_list):
    Paramsset[ind] = {'A':A, \
                      'L':L, 'E':e_cur, \
                      'B':B, \
                      'GAM':DISCOUNT_FACTOR,\
                      'DELTA': DELTA, \
                      'LMAT': None, \
                      'WMAT': None, \
                      'SIG': None}

# Build transition matrix in a parallel manner
if READ_TRANSMAT_FROM_FILE==False:
    if __name__=="__main__":
        pool_transmat= multiprocessing.Pool(processes=10)
        result = []
        for e_cur,ind in enumerate(E_list):
            pool_transmat.apply_async(BuildTransMatrix,(Paramsset[ind],))
        pool_transmat.close()
        pool_transmat.join()
        print "Forming transition matrices. DONE"
# else:
#     for e_cur,ind in enumerate(E_list):
#         TransProbSet[ind] = pickle.load(open("../transmatrix/E_charging/transmat"+str(E_list.index(e_cur)+1),"r"))
#  
# for e_cur in E_list:
#     params = {'A':A, \
#                 'L':L, 'E':e_cur, \
#                 'B':B, \
#                 'GAM':DISCOUNT_FACTOR,\
#                 'DELTA': DELTA, \
#                 'LMAT': None, \
#                 'WMAT': None, \
#                 'SIG': None}
#     ind = E_list.index(e_cur)
#     
#     if READ_TRANSMAT_FROM_FILE==False:
#         TransProb = BuildTransMatrix(params)
#         pickle.dump(TransProb, open("../transmatrix/E_charging/transmat"+str(E_list.index(e_cur)+1),"w"))
#     else:
#         TransProb = pickle.load(open("../transmatrix/E_charging/transmat"+str(E_list.index(e_cur)+1),"r"))
#      
#         print "---- ROUND:", E_list.index(e_cur)+1,
#         print "out of", len(E_list)
#            
#         Paramsset[ind] = params
#     
#         def func(num):
#             if num==1:
#                 # Bellman
#                 V_bell, A_bell = BellmanSolver(TransProb, params)
#                 RESset_bell[ind] = GetOptResultList(V_bell,A_bell, params)
#             if num==2:    
#                 # Myopic
#                 V_myo, A_myo = NaiveSolver_Myopic(TransProb, params)
#                 RESset_myo[ind] = GetOptResultList(V_myo,A_myo, params)
#             if num==3:
#                 # All 0
#                 V_zero, A_zero = NaiveSolver_AllSame(TransProb, 0,params)
#                 RESset_zero[ind] = GetOptResultList(V_zero,A_zero, params)
#             if num==4:
#                 # All 1
#                 V_one, A_one = NaiveSolver_AllSame(TransProb, 1,params)
#                 RESset_one[ind] = GetOptResultList(V_one,A_one, params)
#             if num==5:
#                 # Random - a special algorithm case
#                 # we don't care about Values and Actions
#                 rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
#                 V_rnd_total = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
#                 A_rnd_total = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
#                 RE = []
#                 for rcount in range(RANDOM_COUNT):
#                     print "RANDOM: %d/%d running..." % (rcount,RANDOM_COUNT-1)
#                     V_rnd, A_rnd = NaiveSolver_Rnd(TransProb, params)
#                     RE_rnd = GetOptResultList(V_rnd,A_rnd, params)
#                     if rcount == 0:
#                         RE = [0.0 for _ in range(len(RE_rnd))]
#                     for i in range(len(RE_rnd)):
#                         RE[i] = RE[i] + RE_rnd[i]
#                 for i in range(len(RE)):
#                     RE[i] = RE[i]*1.0/(1.0*RANDOM_COUNT)
#                 RESset_rnd[ind] = RE
#         
#         if __name__=="__main__":
#             pool = multiprocessing.Pool(processes=10)
#             result = []
#             for i in [1,2,3,4,5]:
#                 result.append(pool.apply_async(func,(i,)))
#             pool.close()
#             pool.join()
#             print "Sub-proc done!"
#             
# 
# if READ_TRANSMAT_FROM_FILE == True:
#     print "Dumping...",
#     pickle.dump(expnum, open("../results/E_changing/expnum","w"))
#     pickle.dump(Paramsset, open("../results/E_changing/paramsset","w"))
#     pickle.dump(E_list, open("../results/E_changing/xaxis","w"))
#     pickle.dump(RESset_bell, open("../results/E_changing/bell","w"))
#     pickle.dump(RESset_myo, open("../results/E_changing/myo","w"))
#     pickle.dump(RESset_zero, open("../results/E_changing/zero","w"))
#     pickle.dump(RESset_one, open("../results/E_changing/one","w"))
#     pickle.dump(RESset_rnd, open("../results/E_changing/rnd","w"))
#     print "Finished"

