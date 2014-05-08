'''
Created on 26 Feb, 2014

@author: yzhang28
'''

from HarvCore.func import *

EXECNUM = 2

A = 5
E = 10
L = 10
#### WE ASSUME E>A and E>B
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B

DISCOUNT_FACTOR = 0.90
DELTA = 0.1

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

if EXECNUM == 1:
    
    lam_list = [0.5, 3.0]
    
    expnum = len(lam_list)
    ParamsSet  = [None for _ in range(expnum)]
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
        
    for ind, cur in enumerate(lam_list):
        TransProbSet[ind] = BuildTransMatrix(ParamsSet[ind])
        
    print "START COMPUTING..."
    for ind, cur in enumerate(lam_list):
        print "---- ROUND:", ind+1,
        print "out of", len(lam_list)
        
        # e, l, w.
        V, A = BellmanSolver(TransProbSet[ind], ParamsSet[ind])
        
        ShowMatrix(A, mode='a', fixdim='w', fixnum=1, params=ParamsSet[ind])
        print "w=1"
        ShowMatrix(A, mode='a', fixdim='w', fixnum=2, params=ParamsSet[ind])
        print "w=3"
        ShowMatrix(A, mode='a', fixdim='w', fixnum=3, params=ParamsSet[ind])
        print "w=5"
        
        ShowMatrix(A, mode='a', fixdim='e', fixnum=3, params=ParamsSet[ind])
        print "e=3"
        ShowMatrix(A, mode='a', fixdim='e', fixnum=5, params=ParamsSet[ind])
        print "e=5"
        ShowMatrix(A, mode='a', fixdim='e', fixnum=8, params=ParamsSet[ind])
        print "e=8"
        
        ShowMatrix(A, mode='a', fixdim='l', fixnum=3, params=ParamsSet[ind])
        print "l=3"
        ShowMatrix(A, mode='a', fixdim='l', fixnum=5, params=ParamsSet[ind])
        print "l=5"
        ShowMatrix(A, mode='a', fixdim='l', fixnum=8, params=ParamsSet[ind])
        print "l=8"
        
        print '-------------------------------------------------------------'
        print '-------------------------------------------------------------'
        print '-------------------------------------------------------------'
        print '-------------------------------------------------------------'



# BUILDING PROB MATRIX
# BUILDING PROB MATRIX
# START COMPUTING...
# ---- ROUND: 1 out of 2
# MDP
# Delta= 0.468890972206
# Delta= 0.10326293072
# Delta= 0.077571605846
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     0     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     0     0     0     0     0    
# 1     1     1     1     1     0     0     0     0     0     0    
# 1     1     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=1
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     0     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     0     0     0     0     0    
# 1     1     1     1     1     0     0     0     0     0     0    
# 1     1     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=3
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     0     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     0     0     0     0     0    
# 1     1     1     1     1     0     0     0     0     0     0    
# 1     1     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 1     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=5
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# e=3
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# e=5
# ---ACTION MATRIX---
# Line: l
# Col: w
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# e=8
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# l=3
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# l=5
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# l=8
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# ---- ROUND: 2 out of 2
# MDP
# Delta= 0.536675903192
# Delta= 0.267624343442
# Delta= 0.215412862355
# Delta= 0.159389114344
# Delta= 0.120575019889
# Delta= 0.0923219067561
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     0     0     0     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=1
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     0     0     0     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=3
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     0     0     0     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=5
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# e=3
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# e=5
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# e=8
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# l=3
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# l=5
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0     0     0     0    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# l=8
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------



if EXECNUM == 2:
    # changing the peak
    x_axis_list = [5,10]
    
    expnum = len(x_axis_list)
    ParamsSet = [None for _ in range(expnum)]
    TransProbSet = [None for _ in range(expnum)]
    
    PEAK = 0.8
    
    Matline = [[] for _ in range(len(x_axis_list))]
    for line_index, itemline in enumerate(Matline):
        for elem_index in range(L+1):
            if elem_index == x_axis_list[line_index]:
                Matline[line_index].append(PEAK)
            else:
                Matline[line_index].append((1.0-PEAK)/(L-1.0))
    
    
    for ind, l_cur in enumerate(x_axis_list):
        LMAT = [Matline[ind] for _ in range(0,L+1)]
        ParamsSet[ind] = {'A':A, \
                    'L':L, 'E':E, \
                    'B':B, \
                    'GAM':DISCOUNT_FACTOR,\
                    'DELTA': DELTA, \
                    'LMAT': LMAT, \
                    'WMAT': None, \
                    'SIG': None}
        
    for ind, e_cur in enumerate(x_axis_list):
        TransProbSet[ind] = BuildTransMatrix(ParamsSet[ind])
    
    print "START COMPUTING..."
    for ind, cur in enumerate(x_axis_list):
        print "---- ROUND:", ind+1,
        print "out of", len(x_axis_list)
        
        # e, l, w.
        V, A = BellmanSolver(TransProbSet[ind], ParamsSet[ind])
        
        print "w=1"
        ShowMatrix(A, mode='a', fixdim='w', fixnum=1, params=ParamsSet[ind])
        print "w=3"
        ShowMatrix(A, mode='a', fixdim='w', fixnum=2, params=ParamsSet[ind])
        print "w=5"
        ShowMatrix(A, mode='a', fixdim='w', fixnum=3, params=ParamsSet[ind])
        
        print "e=3"
        ShowMatrix(A, mode='a', fixdim='e', fixnum=3, params=ParamsSet[ind])
        print "3=5"
        ShowMatrix(A, mode='a', fixdim='e', fixnum=5, params=ParamsSet[ind])
        print "3=8"
        ShowMatrix(A, mode='a', fixdim='e', fixnum=8, params=ParamsSet[ind])
        
        print "l=3"
        ShowMatrix(A, mode='a', fixdim='l', fixnum=3, params=ParamsSet[ind])
        print "l=5"
        ShowMatrix(A, mode='a', fixdim='l', fixnum=5, params=ParamsSet[ind])
        print "l=8"
        ShowMatrix(A, mode='a', fixdim='l', fixnum=8, params=ParamsSet[ind])
    
        print '-------------------------------------------------------------'
        print '-------------------------------------------------------------'
        print '-------------------------------------------------------------'
        print '-------------------------------------------------------------'
        
# BUILDING PROB MATRIX
# BUILDING PROB MATRIX
# START COMPUTING...
# ---- ROUND: 1 out of 2
# MDP
# Delta= 0.488494803384
# Delta= 0.243795558096
# Delta= 0.205682748623
# Delta= 0.176532885742
# Delta= 0.109742975018
# Delta= 0.0705086236687
# w=1
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=3
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=5
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# e=3
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 3=5
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 3=8
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# l=3
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# l=5
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# l=8
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0     0     0     0    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# ---- ROUND: 2 out of 2
# MDP
# Delta= 0.456613651989
# Delta= 0.240360488749
# Delta= 0.203887857162
# Delta= 0.182777252023
# Delta= 0.158409847154
# Delta= 0.136235481436
# Delta= 0.117062234421
# Delta= 0.100157593234
# Delta= 0.0859105993424
# w=1
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     0     0     0     0     0     0     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=3
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     0     0     0     0     0     0     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# w=5
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     0     0     0     0     0     0     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     1     0    
# 1     1     1     1     1     1     1     1     1     0     0    
# 1     1     1     1     1     1     1     1     0     0     0    
# 0     0     0     0     0     0     0     0     0     0     0    
# e=3
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 3=5
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 3=8
# ---ACTION MATRIX---
# Line: l
# Col: w
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# l=3
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0     0     0     0    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# l=5
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0     0     0     0    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# l=8
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 1     1     1     1     1     1    
# 0     0     0     0     0     0    
# 0     0     0     0     0     0    
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
