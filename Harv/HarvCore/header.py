'''
Created on 20 Mar, 2014

@author: yzhang28
'''
import numpy as np
import scipy as sp
from scipy.misc import factorial
from scipy.integrate import quad
import math
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from copy import deepcopy
import random

from multiprocessing import Pool

__name__=='__main__'

# A_CONST = 10
# L_CONST = 10
# B_CONST = 10
# E_CONST = 12
# A_CONST = 1
# L_CONST = 1
# B_CONST = 1
# E_CONST = 2
# DISCOUNT_FACTOR = 0.8
# TEST_PARAM_CONST = {'A':A_CONST, \
#               'L':L_CONST, 'E':E_CONST, \
#               'B':B_CONST, \
#               'GAM':DISCOUNT_FACTOR,\
#               'DELTA': 0.1, \
#               'LMAT': None, \
#               'WMAT': None, \
#               'SIG': None}

def CompareMat(m1,m2, params):
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    for e in rangeE:
        for l in rangeL:
            for w in rangeW:
                if (not m1[e][l][w]==m2[e][l][w]):
                    print "(%d,%d,%d): %d v.s.%d" %(e,l,w,m1[e][l][w],m2[e][l][w])

def ShowMatrix(Mat, mode, fixdim, fixnum, params):
    if Mat==None:
        print "ERROR INPUT ShowMatrix()"
        exit()
    
    if mode=='a':   # Show action
        print "---ACTION MATRIX---"
    elif mode=='v':    # Show value
        print "---VALUE MATRIX---"
    else:
        print "ERROR, UNKNOWN MATRIX"
        exit()
    
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    dimList = ['e','l','w']
    feasList = [rangeE, rangeL, rangeW]
    del(feasList[dimList.index(fixdim)])
    del(dimList[dimList.index(fixdim)])
    print 'Line:', dimList[0]
    print 'Col:', dimList[1] 
    for ra in feasList[0]:
        for rb in feasList[1]:
            if fixdim=='e':
                if mode=='a':
                    print "%d" % Mat[fixnum][ra][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[fixnum][ra][rb],
                else:
                    print "ERROR, POS 1"
                    exit()
                print '   ',
            elif fixdim=='l':
                if mode=='a':
                    print "%d" % Mat[ra][fixnum][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][fixnum][rb],
                else:
                    print "ERROR, POS 2"
                    exit()
                print '   ',
            elif fixdim=='w':
                if mode=='a':
                    print "%d" % Mat[ra][rb][fixnum],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][rb][fixnum],
                else:
                    print "ERROR, POS 3"
                    exit()
                print '   ',
            else:
                print "ERROR, POS 4"
                exit()
        print

def L_mat(l1, l2, params):
    if params['LMAT']==None:
        mat_mu = [[1.0/(params['L']+1.0) for _ in range(params['L']+1)] for _ in range(params['L']+1)]
    else:
        mat_mu = params['LMAT']
    if (l1 in range(params['L']+1)) and (l2 in range(params['L']+1)):
        return mat_mu[l1][l2]
    else:
        return 0.0

def W_mat(wo1, wo2, params):
    if params['WMAT']==None:
        mat_omg = [[1.0/(params['A']+1.0) for _ in range(params['A']+1)] for _ in range(params['A']+1)]
    else:
        mat_omg = params['WMAT']
    if 0<=wo1 and wo1<=params['A'] and 0<=wo2 and wo2<=params['A']:  
        return mat_omg[wo1][wo2]
    else:
        return 0.0

def W(i,wo1,wo2, params):
    if i<0 and i>params['A']:
        return 0.0
    else:
        if wo2==i:
            return W_mat(wo1,wo2, params)
        else:
            return 0.0

def sig(j, params):
    if params['SIG']==None:
        sig_set = [1.0/(params['B']+1.0) for _ in range(params['B']+1)]
    else:
        sig_set = params['SIG'] 
    
    if 0<=j and j<=params['B']:
        return sig_set[j]
    else:
        return 0.0

def E_tilde(e1,w1, e2,w2, act,j, params):
    if act == 0:
        if 0<=e1 and e1<params['A']:
            if e2 == 0:
                sum_tmp = 0.0
                for i in range(e1,params['A']+1):
                    sum_tmp = sum_tmp + W(i,w1,w2, params)
                return sum_tmp
            elif e2>0 and e1>0 and e1>=e2:
                return W(e1-e2,w1,w2, params)
            else:
                return 0.0
        elif e1>=params['A'] and e1<=params['E']:
            if e2>=e1-params['A'] and e2<=e1:
                return W(e1-e2,w1,w2, params)
            else:
                return 0.0
        else:
            return 0.0
    elif act == 1:
        if j==0:
            return E_tilde(e1,w1, e2,w2, 0, None, params)
        elif j>0 and j<=params['A']:  # 0<j<=A case
            if 0<=e1 and e1<params['A']-j:
                if e2==0:
                    sum_tmp = 0.0
                    for i in range(j+e1,params['A']+1):
                        sum_tmp = sum_tmp + W(i,w1,w2, params)
                    return sum_tmp
                elif e2>0 and e2<=j+e1:
                    return W(j+e1-e2,w1,w2, params)
                else:
                    return 0.0
            elif e1>=params['A']-j and e1<params['E']-j:
                if e2>=e1-(params['A']-j) and e2<=e1+j: ## line *1
                    return W(j+e1-e2,w1,w2, params)
                else:
                    return 0.0
            elif e1>=params['E']-j and e1<=params['E']:
                if e2>=params['E']-params['A'] and e2<=params['E']:
                    return W(params['E']-e2,w1,w2, params)
                else:
                    return 0.0
            else:
                return 0.0
        elif j>params['A']:  # A<j<E case
            if 0<=e1 and e1<params['E']-j:
                if e2>=j-params['A']+e1 and e2<=j+e1: # same as line *1
                    return W(j+e1-e2,w1,w2, params)
                else:
                    return 0.0
            elif params['E']-j<=e1 and e1<=params['E']:
                if e2>=params['E']-params['A'] and e2<=params['E']:
                    return W(params['E']-e2,w1,w2, params)
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return 0.0
    else:
        return 0.0
    
    return 0.0

def OverallTransProb(e1,l1,w1, e2,l2,w2, act, params):
    if act==0:
        return 1.0 * E_tilde(e1,w1, e2,w2, act, None, params) * L_mat(l1,l2, params)
    else:
        _tmp_sum = 0.0
        for k in range(params['B']+1):
            _tmp_sum = _tmp_sum + 1.0 * sig(k, params) * E_tilde(e1,w1, e2,w2, act,k, params)
        return 1.0 * _tmp_sum * L_mat(l1,l2, params)

def SteadyStateMatrix(optA, params):
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    total_dim = len(rangeE) * len(rangeL) * len(rangeW)
    expanded_matrix = np.matrix( [[0.0 for _ in range(total_dim)] for _ in range(total_dim)] )
    search_list = [[[-1 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    
    TransProb = [
             [
              [
               [
                [
                 [
                  0.0
                 for _ in rangeW ]
                for _ in rangeL ]
               for _ in rangeE ]
              for _ in rangeW ]
             for _ in rangeL ]
            for _ in rangeE ]
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            TransProb[e1][l1][w1][e2][l2][w2] = OverallTransProb(e1,l1,w1, e2,l2,w2, optA[e1][l1][w1], params)
    
    # most stupid loops begin!
    # EXPAND, YA!
    expd_x_ind, expd_y_ind = 0, 0 
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            expanded_matrix[expd_x_ind, expd_y_ind] = TransProb[e1][l1][w1][e2][l2][w2]
                            expd_y_ind = expd_y_ind + 1
                search_list[e1][l1][w1] = expd_x_ind
                expd_x_ind = expd_x_ind + 1
                expd_y_ind = 0
    # the expanded matrix generated
    # the search list generated
    # in to the algorithm part
    p_hat = expanded_matrix - np.diag(np.array([1.0 for _ in range(total_dim)]))
    for x in range(total_dim):
        p_hat[x,total_dim-1] = 1.0
    a_rhs = np.zeros(total_dim)
    a_rhs[total_dim-1] = 1.0
    steady_p = a_rhs * p_hat.getI()
    steady_p_transf = [[[-1 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    for e in rangeE:
        for l in rangeL:
            for w in rangeW:
                steady_p_transf[e][l][w] = steady_p[0,search_list[e][l][w]]  
    return steady_p_transf


def GetOptResultList(V,A, params):
    steady_mat = SteadyStateMatrix(A, params)
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    v_avg = 0.0
    v_steady = 0.0
    a_avg = 0.0
    a_steady = 0.0
    bp_steady = 0.0
    eg_steady = 0.0
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                # GetValueAvg
                v_avg = v_avg + V[e1][l1][w1]
                # GetValueSteadyAvg
                v_steady = v_steady + steady_mat[e1][l1][w1] * V[e1][l1][w1]
                # GetActionAvg
                a_avg = a_avg + A[e1][l1][w1]
                # GetActionSteadyAvg
                a_steady = a_steady + steady_mat[e1][l1][w1] * A[e1][l1][w1]
                # GetBlockingProb
                if w1>e1:
                    bp_steady = bp_steady + steady_mat[e1][l1][w1]
                # GetEnergySteadyAvg
                eg_steady = eg_steady + 1.0* e1 * steady_mat[e1][l1][w1]
    v_avg = v_avg*1.0 / (1.0*len(rangeE)*len(rangeL)*len(rangeW))
    a_avg = a_avg*1.0 / (1.0*len(rangeE)*len(rangeL)*len(rangeW))
    return [v_avg, v_steady, a_avg, a_steady, bp_steady, eg_steady] 

#    return [MATOP_GetValueAvg(V, params), MATOP_GetValueSteadyAvg(V,A, steady_mat, params), \
#            MATOP_GetActionAvg(A, params), MATOP_GetActionSteadyAvg(A, steady_mat, params), \
#            MATOP_GetBlockingProb(A, steady_mat, params), MATOP_GetEnergySteadyAvg(A, steady_mat, params) ]

# def BuildTransMatrix(params):    
#     rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
#     rangeA = range(2) # 0 and 1
#     TransProb = [
#                  [
#                   [
#                    [
#                     [
#                      [
#                       [ 0.0 for _ in rangeA ] 
#                      for _ in rangeW ]
#                     for _ in rangeL ]
#                    for _ in rangeE ]
#                   for _ in rangeW ]
#                  for _ in rangeL ]
#                 for _ in rangeE ]
#     print "BUILDING PROB MATRIX"
#     for e1 in rangeE:
#         for l1 in rangeL:
#             for w1 in rangeW:
#                 for e2 in rangeE:
#                     for l2 in rangeL:
#                         for w2 in rangeW:
#                             for act in rangeA:
#                                 TransProb[e1][l1][w1][e2][l2][w2][act] = OverallTransProb(e1,l1,w1, e2,l2,w2, act, params)
#     return TransProb

def BuildTransMatrix(params):
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    rangeA = range(2) # 0 and 1
    TransProb = [
                 [
                  [
                   [
                    [
                     [
                      [ 0.0 for _ in rangeA ] 
                     for _ in rangeW ]
                    for _ in rangeL ]
                   for _ in rangeE ]
                  for _ in rangeW ]
                 for _ in rangeL ]
                for _ in rangeE ]
    print "BUILDING PROB MATRIX"
    maplist = []
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            for act in rangeA:
                                maplist.append((e1,l1,w1,e2,l2,w2,act))
#                                 TransProb[e1][l1][w1][e2][l2][w2][act] = OverallTransProb(e1,l1,w1, e2,l2,w2, act, params)
    def ParaTransProb(ml):
        print ml
        TransProb[ml[1]][ml[2]][ml[3]][ml[4]][ml[5]][ml[6]] = OverallTransProb(ml[0],ml[1],ml[2], ml[3],ml[4],ml[5], ml[6], params)
#     if __name__=='__main__':
    pool = Pool()
    pool.map(ParaTransProb, maplist)
#     print TransProb
    return TransProb