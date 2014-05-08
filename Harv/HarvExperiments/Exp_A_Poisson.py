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
L = 10
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.90
DELTA = 0.1
RANDOM_COUNT = 5

def PoissonGenerator(k, lam):
    def RawPoisson(k, lam):
        return np.exp(-1.0*lam)*pow(lam,k)/math.factorial(k)
    def AppxSumToOne(k, lam):
        '''
        summation of P^{N}(0), P^{N}(1), to P^{N}(N2)
        The function is used to check if P^{N}(N2+1) should be neglected  
        '''
        if k<0:
            return 0
        else:
            return RawPoisson(k, lam) + AppxSumToOne(k-1, lam)
    _epsilon = 0.01 
    if 1.0-AppxSumToOne(k-1, lam)<_epsilon:
        return 0
    else:
        return RawPoisson(k, lam)

def NMaxFunc(lam):
    for k in range(65535):
        if PoissonGenerator(k,lam)==0:
            return k-1+1

def TruncatedPoisson(k,lam, A_upper):
    if k<A_upper:
        return np.exp(-1.0*lam)*pow(lam,k)/math.factorial(k)
    elif k==A_upper:
        _tmp_sum = 0.0
        for c in range(0,k):
            _tmp_sum = _tmp_sum + np.exp(-1.0*lam)*pow(lam,c)/math.factorial(c)
        return 1.0 - _tmp_sum 
    else:
        return 0.0
        

lam_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
# lam_list = [1.5, 3.0, 3.5, 5.0]

expnum = len(lam_list)
ParamsSet  = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_zero = [None for _ in range(expnum)]
RESset_one = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]


for ind, cur in enumerate(lam_list):
    Wmat_cur = [[TruncatedPoisson(k,cur,A) for k in range(0, A+1)] for _ in range(0,A+1)]
    ParamsSet[ind] = {'A':A, \
                      'L':L, 'E':E, \
                      'B':B, \
                      'GAM':DISCOUNT_FACTOR, \
                      'DELTA': DELTA, \
                      'LMAT': None, \
                      'WMAT': Wmat_cur, \
                      'SIG': None}

# Build transition matrix in a parallel manner
# if READ_TRANSMAT_FROM_FILE == False:
for ind, cur in enumerate(lam_list):
    TransProbSet[ind] = BuildTransMatrix(ParamsSet[ind])
#         pickle.dump(TransProbSet[ind], open("../transmatrix/A_Poisson/transmat"+str(ind+1),"w"))
#     print "Forming transition matrices. DONE" 
# 
# else:
#     print "Loading transition matrices..."
#     for ind, cur in enumerate(lam_list):
#         TransProbSet[ind] = pickle.load(open("../transmatrix/A_Poisson/transmat"+str(ind+1),"r"))
         
print "START COMPUTING..."
for ind, cur in enumerate(lam_list):
    print "---- ROUND:", ind+1,
    print "out of", len(lam_list)

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
pickle.dump(expnum, open("../results/A_Poisson/expnum","w"))
pickle.dump(ParamsSet, open("../results/A_Poisson/paramsset","w"))
pickle.dump(lam_list, open("../results/A_Poisson/xaxis","w"))
pickle.dump(RESset_bell, open("../results/A_Poisson/bell","w"))
pickle.dump(RESset_myo, open("../results/A_Poisson/myo","w"))
pickle.dump(RESset_zero, open("../results/A_Poisson/zero","w"))
pickle.dump(RESset_one, open("../results/A_Poisson/one","w"))
pickle.dump(RESset_rnd, open("../results/A_Poisson/rnd","w"))
print "Finished"


