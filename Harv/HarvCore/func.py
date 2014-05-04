'''
Created on 19 Feb, 2014

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
import time

from HarvCore.header import *    

###################################################################################
###################################################################################
###################################################################################
###################################################################################

def pro_l_new(l1, act, params):
    # Get price using log-norminal distribution
    def PriceDistroInv(y,mu,sigm):
        def PriceDistro(x,mu,sigm):
            return 0.5 + 0.5*math.erf((math.log(x)-mu)/(2.0*math.sqrt(sigm*sigm)))
        x, step = 0.01, 0.01
        if y==0:
            return 0
        if y>=1:
            return PriceDistroInv(0.999,mu,sigm)  # PROBLEM!
        while 1:
            if PriceDistro(x,mu,sigm)<=y and PriceDistro(x+step,mu,sigm)>=y:
                return x
            else:
                x = x + step
    # Profit l
    _budget = 0.0
    _p_mu = 0.0
    _p_sigm = 0.5
    price = PriceDistroInv(l1*1.0/(params['L']),_p_mu,_p_sigm)
    max_price = PriceDistroInv(0.999,_p_mu,_p_sigm)
    profit_loc = (_budget - act * price) / max_price        #L5    
    return profit_loc

def pro_w_new(e1, w1, params):
    if e1 < w1:
        return -1.0 * (w1-e1) / (params['A'] * 1.0)
    else:
        return  math.sqrt(w1*1.0)/math.sqrt(params['A']*1.0)

def ImmediateProfit(e1,l1,w1,act, params):
    weight1 = 0.7
    weight2 = 0.3
    p_l = pro_l_new(l1, act, params)
    p_w = pro_w_new(e1, w1, params)
    return weight1*p_l + weight2*p_w

###################################################################################
###################################################################################
###################################################################################
###################################################################################


def BellmanSolver(TransProb, params):
    print "MDP"
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    V_op = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A_op = [[[  0 for _ in rangeW] for _ in rangeL] for _ in rangeE]

    while 1:
        delta = 0.0
        for e1 in rangeE:
            for l1 in rangeL:
                for w1 in rangeW:
                    _v_old = V_op[e1][l1][w1]
                    _v_temp = [None, None]
                    for act in [0,1]:
                        _s_tmp = 0.0
                        for e2 in rangeE:
                            for l2 in rangeL:
                                for w2 in rangeW:
                                    _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2][act] * V_op[e2][l2][w2]
                        _v_temp[act] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    if _v_temp[0] > _v_temp[1] or e1==params['E']:
                        V_op[e1][l1][w1] = _v_temp[0]
                        A_op[e1][l1][w1] = 0
                    elif _v_temp[0] <= _v_temp[1]:
                        V_op[e1][l1][w1] = _v_temp[1]
                        A_op[e1][l1][w1] = 1
#                     elif _v_temp[0] == _v_temp[1]:
# #                         V_up[e1][l1][w1] = _v_temp[1]
# #                         V[e1][l1][w1] = _v_temp[1]
# #                         A[e1][l1][w1] = 2
#                         if e1==0:
#                             A_op[e1][l1][w1] = 1
#                             V_op[e1][l1][w1] = _v_temp[1]
#                         else:
#                             A_op[e1][l1][w1] = A_op[e1-1][l1][w1]
#                             V_op[e1][l1][w1] = _v_temp[A_op[e1][l1][w1]]
                    else:
                        print "ERROR IN BellmanSolver(params)"
                        exit(0)
                    delta = delta if delta>np.fabs(V_op[e1][l1][w1]-_v_old) else np.fabs(V_op[e1][l1][w1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op

def NaiveSolver_Myopic(TransProb, params):
    print "Myopic."
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)

    V = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A = [[[0 for _ in rangeW] for _ in rangeL] for _ in rangeE]

    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                A[e1][l1][w1] = 1 if ImmediateProfit(e1,l1,w1,1, params)>=ImmediateProfit(e1,l1,w1,0, params) else 0
                if e1==params['E']:
                    A[e1][l1][w1] = 0

    while 1:
        delta = 0.0
        for e1 in rangeE:
            for l1 in rangeL:
                for w1 in rangeW:
                    act = A[e1][l1][w1]
                    _v_old = V[e1][l1][w1]
                    _s_tmp = 0.0
                    for e2 in rangeE:
                        for l2 in rangeL:
                            for w2 in rangeW:
                                _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2][act] * V[e2][l2][w2]
                    V[e1][l1][w1] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    delta = delta if delta>np.fabs(V[e1][l1][w1] -_v_old) else np.fabs(V[e1][l1][w1] -_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            break

    return V, A

def NaiveSolver_Rnd(TransProb, params):
    print "Random"
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)
    V = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A = [[[0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                V[e1][l1][w1] = 0.0
                A[e1][l1][w1] = random.randint(0,1)
                if e1==params['E']:
                    A[e1][l1][w1] = 0

    while 1:
        delta=0.0
        for e1 in rangeE:
            for l1 in rangeL:
                for w1 in rangeW:
                    act = A[e1][l1][w1]
                    _v_old = V[e1][l1][w1]
                    _s_tmp = 0.0
                    for e2 in rangeE:
                        for l2 in rangeL:
                            for w2 in rangeW:
                                _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2][act] * V[e2][l2][w2]
                    V[e1][l1][w1] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    delta = delta if delta>np.fabs(V[e1][l1][w1] -_v_old) else np.fabs(V[e1][l1][w1] -_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            break
    return V, A

def NaiveSolver_AllSame(TransProb, act_input, params):
    if act_input not in [0,1]:
        print "ERROR NaiveSolver_AllSame(act_input=0)"
        exit(0)
    print "All " + str(act_input) + " Scheme, running."
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A']+1)

    V = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A = [[[act_input for _ in rangeW] for _ in rangeL] for _ in rangeE]
    
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                if e1==params['E']:
                    A[e1][l1][w1] = 0  # always not charge if the battery is full
                if e1==0:
                    A[e1][l1][w1] = 1 # always charge if the battery is empty
                            
    while 1:
        delta = 0.0
        for e1 in rangeE:
            for l1 in rangeL:
                for w1 in rangeW:
                    act = A[e1][l1][w1]
                    _v_old = V[e1][l1][w1]
                    _s_tmp = 0.0
                    for e2 in rangeE:
                        for l2 in rangeL:
                            for w2 in rangeW:
                                _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2][act] * V[e2][l2][w2]
                    V[e1][l1][w1] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    delta = delta if delta>np.fabs(V[e1][l1][w1] -_v_old) else np.fabs(V[e1][l1][w1] -_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            break
    return V, A
