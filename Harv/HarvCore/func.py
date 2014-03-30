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

%test
    

def pro_e(e1, params, parabola_flag=0):
    if parabola_flag==0:
        profit_e = math.sqrt(e1*1.0)/math.sqrt(params['E']) # inc func, concave        #E3
    else:
        profit_e = (-1.0*pow(e1*1.0,2.0) + 40.0)/40.0 #dec func, concave            #E4
    return profit_e

def pro_l(l1,act, params, parabola_flag=0):
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
    _budget = 1.0
    if act==0:
        if parabola_flag==0:
            return _budget
        else:
            return 0.0
    else:
        _p_mu = 0.0
        _p_sigm = 0.5
        price = PriceDistroInv(l1*1.0/(params['L']),_p_mu,_p_sigm)
        profit_loc = (_budget - price*act)/1.0        #L5    
        return profit_loc

def pro_w(w1,e1, params):
    profit_w = 0.0
    if w1>e1:
        profit_w = -1.0 * w1 / (params['A_inf']*1.0)
    else:
        profit_w = math.sqrt(w1*1.0)/math.sqrt(params['A_inf']*1.0)     #W3
    return profit_w

def ImmediateProfit(e1,l1,w1,act, params, parabola_flag=0):
    p_e = pro_e(e1, params, parabola_flag)
    p_l = pro_l(l1,act, params, parabola_flag)
    p_w = pro_w(w1,e1, params)
    # OVERALL PROFIT
    return (p_w + p_l + p_e)/3.0

def BellmanSolver(params, parabola_flag=0): # the parabola_flag is only used in ThreshCalc module
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A_inf']+1)
    rangeA = range(2) # 0 and 1
    V_op = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
#     V_up = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A_op = [[[  0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
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
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            for act in rangeA:
                                TransProb[e1][l1][w1][e2][l2][w2][act] = OverallTransProb(e1,l1,w1, e2,l2,w2, act, params)
    while 1:
        delta = 0.0
        for e1 in rangeE:
            for l1 in rangeL:
#                 _timestamp_01 = int(round(time.time() * 1000))
                for w1 in rangeW:
                    _v_old = V_op[e1][l1][w1]
                    _v_temp = [None, None]
                    for act in [0,1]:
                        _s_tmp = 0.0
                        for e2 in rangeE:
                            for l2 in rangeL:
                                for w2 in rangeW:
                                    _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2][act] * V_op[e2][l2][w2]
#                                     _s_tmp = _s_tmp + OverallTransProb(e1,l1,w1, e2,l2,w2, act, params) * V[e2][l2][w2]
                        _v_temp[act] = ImmediateProfit(e1,l1,w1,act, params, parabola_flag) + params['GAM'] * _s_tmp
                    if _v_temp[0] > _v_temp[1] or e1==params['E']:
#                         V_up[e1][l1][w1] = _v_temp[0]
                        V_op[e1][l1][w1] = _v_temp[0]
                        A_op[e1][l1][w1] = 0
                    elif _v_temp[0] < _v_temp[1]:
#                         V_up[e1][l1][w1] = _v_temp[1]
                        V_op[e1][l1][w1] = _v_temp[1]
                        A_op[e1][l1][w1] = 1
                    elif _v_temp[0] == _v_temp[1]:
#                         V_up[e1][l1][w1] = _v_temp[1]
#                         V[e1][l1][w1] = _v_temp[1]
#                         A[e1][l1][w1] = 2
                        if e1==0:
                            A_op[e1][l1][w1] = 1
                            V_op[e1][l1][w1] = _v_temp[1]
                        else:
                            A_op[e1][l1][w1] = A_op[e1-1][l1][w1]
                            V_op[e1][l1][w1] = _v_temp[A_op[e1][l1][w1]]
                    else:
                        print "ERROR IN BellmanSolver(params)"
                        exit(0)
#                     delta = delta if delta>np.fabs(V_up[e1][l1][w1]-_v_old) else np.fabs(V_up[e1][l1][w1]-_v_old)
                    delta = delta if delta>np.fabs(V_op[e1][l1][w1]-_v_old) else np.fabs(V_op[e1][l1][w1]-_v_old)
#                 _timestamp_01_e = int(round(time.time() * 1000)) - _timestamp_01
#                 print "time spent:", _timestamp_01_e 
#         for e1 in rangeE:
#             for l1 in rangeL:
#                 for w1 in rangeW:
#                     V[e1][l1][w1] = V_up[e1][l1][w1]
#                     V_up[e1][l1][w1] = 0.0
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op

def NaiveSolver_Myopic(params):
    print "Myopic."
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A_inf']+1)

    V = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A = [[[0 for _ in rangeW] for _ in rangeL] for _ in rangeE]

    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                A[e1][l1][w1] = 1 if ImmediateProfit(e1,l1,w1,1, params)>=ImmediateProfit(e1,l1,w1,0, params) else 0
                if e1==params['E']:
                    A[e1][l1][w1] = 0

    TransProb = [
                 [
                  [
                   [
                    [
                     [ 0.0 for _ in rangeW ]
                    for _ in rangeL ]
                   for _ in rangeE ]
                  for _ in rangeW ]
                 for _ in rangeL ]
                for _ in rangeE ]
    print "BUILDING PROB MATRIX"
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            TransProb[e1][l1][w1][e2][l2][w2] = OverallTransProb(e1,l1,w1, e2,l2,w2, A[e1][l1][w1], params)

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
                                _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2] * V[e2][l2][w2]
#                                 _s_tmp = _s_tmp + OverallTransProb(e1,l1,w1, e2,l2,w2, act, params) * V[e2][l2][w2]
                    V[e1][l1][w1] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    delta = delta if delta>np.fabs(V[e1][l1][w1] -_v_old) else np.fabs(V[e1][l1][w1] -_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            break

    return V, A

def NaiveSolver_Rnd(params):
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A_inf']+1)
#     rangeA = range(2) # 0 and 1
    V = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A = [[[0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                V[e1][l1][w1] = 0.0
                A[e1][l1][w1] = random.randint(0,1)
                if e1==params['E']:
                    A[e1][l1][w1] = 0

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
    print "BUILDING PROB MATRIX"
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            TransProb[e1][l1][w1][e2][l2][w2] = OverallTransProb(e1,l1,w1, e2,l2,w2, A[e1][l1][w1], params)

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
                                _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2] * V[e2][l2][w2]
#                                 _s_tmp = _s_tmp + OverallTransProb(e1,l1,w1, e2,l2,w2, act, params) * V[e2][l2][w2]
                    V[e1][l1][w1] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    delta = delta if delta>np.fabs(V[e1][l1][w1] -_v_old) else np.fabs(V[e1][l1][w1] -_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            break

    return V, A

def NaiveSolver_AllSame(act_input, params):
    if act_input not in [0,1]:
        print "ERROR NaiveSolver_AllSame(act_input=0)"
        exit(0)
    print "All " + str(act_input) + " Scheme, running."
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A_inf']+1)
#     rangeA = range(2) # 0 and 1
    V = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A = [[[act_input for _ in rangeW] for _ in rangeL] for _ in rangeE]
    
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                if e1==params['E']:
                    A[e1][l1][w1] = 0
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
    print "BUILDING PROB MATRIX"
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                for e2 in rangeE:
                    for l2 in rangeL:
                        for w2 in rangeW:
                            TransProb[e1][l1][w1][e2][l2][w2] = OverallTransProb(e1,l1,w1, e2,l2,w2, A[e1][l1][w1], params)
                            
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
                                _s_tmp = _s_tmp + TransProb[e1][l1][w1][e2][l2][w2] * V[e2][l2][w2]
#                                 _s_tmp = _s_tmp + OverallTransProb(e1,l1,w1, e2,l2,w2, act, params) * V[e2][l2][w2]
                    V[e1][l1][w1] = ImmediateProfit(e1,l1,w1,act, params) + params['GAM'] * _s_tmp
                    delta = delta if delta>np.fabs(V[e1][l1][w1] -_v_old) else np.fabs(V[e1][l1][w1] -_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            break
     
    return V, A
