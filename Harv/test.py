'''
Created on 1 May, 2014

@author: yzhang28
'''



import pickle

import sys
sys.path.append("..")
from HarvCore.func import *

DISCOUNT_FACTOR = 0.90
DELTA = 0.1
RANDOM_COUNT = 1

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
E = 10 # energy state numbered: 0, 1, ..., L. L+1 states
L = 10
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

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

for ind, cur in enumerate(lam_list):
    Wmat_cur = [[TruncatedPoisson(k,cur,A) for k in range(0, A+1)] for _ in range(0,A+1)]
    print Wmat_cur[0]
    _sum = 0.0
    for c in Wmat_cur[0]:
        _sum = _sum + c