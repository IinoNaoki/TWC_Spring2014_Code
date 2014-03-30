'''
Created on 25 Feb, 2014

@author: yzhang28
'''

import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox

from HarvCore.func import *

# A = 4 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
# E = 5 # energy state numbered: 0, 1, ..., L. L+1 states
# L = 5
# #### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
# B = 4 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
# #B_INFTY = B_CONST + 1

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
E = 10 # energy state numbered: 0, 1, ..., L. L+1 states
L = 10
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.8
DELTA = 0.01
RANDOM_COUNT = 5

############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
#   problem
#   problem
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################

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

def AccumdPoisson(k,lam, A_max):
    if NMaxFunc(lam)<=A_max+1:
        return np.exp(-1.0*lam)*pow(lam,k)/math.factorial(k)
    else:
        if k<A_max+1:
            return np.exp(-1.0*lam)*pow(lam,k)/math.factorial(k)
        elif k==A_max+1:
            prb = 0.0
            for c in range(k,NMaxFunc(lam)+1):
                prb = prb + np.exp(-1.0*lam)*pow(lam,c)/math.factorial(c)
            return prb
        else:
            return 0.0
        

# x_axis_list = [0,1,2,3]
lam_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
# lam_list = [1.0, 2.0, 3.0, 4.0, 5.0]
test_list = [i for i in range(len(lam_list))]

# Matline = [
#            [0.5, 0.1, 0.1, 0.1, 0,1, 0.1],
#            [0.1, 0.5, 0.1, 0.1, 0.1, 0.1],
#            [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],
#            [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],
#            [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],
#            [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
#            ]
# test_list = [0,1,2,3,4,5]

expnum = len(test_list)

Paramsset  = [None for _ in range(expnum)]

Vset_bell = [None for _ in range(expnum)]
Aset_bell = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]

Vset_myo = [None for _ in range(expnum)]
Aset_myo = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]

Vset_zero = [None for _ in range(expnum)]
Aset_zero = [None for _ in range(expnum)]
RESset_zero = [None for _ in range(expnum)]

Vset_one = [None for _ in range(expnum)]
Aset_one = [None for _ in range(expnum)]
RESset_one = [None for _ in range(expnum)]

Vset_rnd = [None for _ in range(expnum)]
Aset_rnd = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]


for cur in test_list:
    Wmat_cur = [[AccumdPoisson(k,lam_list[cur],A) for k in range(0, A+1+1)] for _ in range(0,A+1+1)]
#     Wmat_cur = [Matline[cur] for _ in range(0,A+1+1)]
    params = {'A':A, 'A_inf':A+1, \
                'L':L, 'E':E, \
                'B':B, 'B_inf':B+1, \
                'GAM':DISCOUNT_FACTOR, \
                'DELTA': DELTA, \
                'LMAT': None, \
                'WMAT': Wmat_cur, \
                'SIG': None}
    ind = test_list.index(cur)
     
    print "---- ROUND:", test_list.index(cur)+1,
    print "out of", len(test_list)
    
    Paramsset[ind] = params
    
    # Bellman
    V_bell, A_bell = BellmanSolver(params)
    Vset_bell[ind] = V_bell
    Aset_bell[ind] = A_bell
    RESset_bell[ind] = GetOptResultList(V_bell,A_bell, params)

       
    # Myopic
    V_myo, A_myo = NaiveSolver_Myopic(params)
    Vset_myo[ind] = V_myo
    Aset_myo[ind] = A_myo
    RESset_myo[ind] = GetOptResultList(V_myo,A_myo, params)
     
     
    # All 0
    V_zero, A_zero = NaiveSolver_AllSame(0,params)
    Vset_zero[ind] = V_zero
    Aset_zero[ind] = A_zero
    RESset_zero[ind] = GetOptResultList(V_zero,A_zero, params)
               
    # All 1
    V_one, A_one = NaiveSolver_AllSame(1,params)
    Vset_one[ind] = V_one
    Aset_one[ind] = A_one
    RESset_one[ind] = GetOptResultList(V_one,A_one, params)

    # Random - a special algorithm case
    # we don't care about Values and Actions
    rangeE, rangeL, rangeW = range(params['E']+1), range(params['L']+1), range(params['A_inf']+1)
    V_rnd_total = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    A_rnd_total = [[[0.0 for _ in rangeW] for _ in rangeL] for _ in rangeE]
    RE = []
    for rcount in range(RANDOM_COUNT):
        print "RANDOM: %d/%d running..." % (rcount,RANDOM_COUNT-1)
        V_rnd, A_rnd = NaiveSolver_Rnd(params)
        for e1 in rangeE:
            for l1 in rangeL:
                for w1 in rangeW:
                    V_rnd_total[e1][l1][w1] = V_rnd_total[e1][l1][w1] + V_rnd[e1][l1][w1]
                    A_rnd_total[e1][l1][w1] = A_rnd_total[e1][l1][w1] + A_rnd[e1][l1][w1]
        RE_rnd = GetOptResultList(V_rnd,A_rnd, params)
        if rcount == 0:
            RE = [0.0 for _ in range(len(RE_rnd))]
        for i in range(len(RE_rnd)):
            RE[i] = RE[i] + RE_rnd[i]
    for e1 in rangeE:
        for l1 in rangeL:
            for w1 in rangeW:
                V_rnd_total[e1][l1][w1] = V_rnd_total[e1][l1][w1]*1.0 / (1.0*RANDOM_COUNT)
                A_rnd_total[e1][l1][w1] = A_rnd_total[e1][l1][w1]*1.0 / (1.0*RANDOM_COUNT)
    for i in range(len(RE)):
        RE[i] = RE[i]*1.0/(1.0*RANDOM_COUNT)
    Vset_rnd[ind] = V_rnd_total
    Aset_rnd[ind] = A_rnd_total
    RESset_rnd[ind] = RE

print "Dumping...",
pickle.dump(expnum, open("./results/A_Poisson/expnum","w"))
pickle.dump(Paramsset, open("./results/A_Poisson/paramsset","w"))
pickle.dump(lam_list, open("./results/A_Poisson/xaxis","w"))
pickle.dump([Vset_bell, Aset_bell, RESset_bell], open("./results/A_Poisson/bell","w"))
pickle.dump([Vset_myo, Aset_myo, RESset_myo], open("./results/A_Poisson/myo","w"))
pickle.dump([Vset_zero, Aset_zero, RESset_zero], open("./results/A_Poisson/zero","w"))
pickle.dump([Vset_one, Aset_one, RESset_one], open("./results/A_Poisson/one","w"))
pickle.dump([Vset_rnd, Aset_rnd, RESset_rnd], open("./results/A_Poisson/rnd","w"))
print "Finished"



# figa = plt.figure(figsize=(4.5,5.0))
# # grid(True, which="both")
# plot(lam_list,act_rate_list_A_bell,color='red',marker='o', label='MDP')
# plot(lam_list,act_rate_list_A_myo,color='green', linestyle='--',fillstyle='none',marker='^', label='MYO')
# # plot(lam_list,act_rate_list_A_rnd,color='0.75', linestyle='--', fillstyle='none',marker='v',label='RND')
# xlabel('$A$',fontsize=16)
# ylabel('Charging rate',fontsize=16)
# subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best')
# # xlim([2,31])
# # ylim([-0.02,1.0])
# ####################################ylim([0.30,0.75])
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
#    
#    
# figc = plt.figure(figsize=(4.5,5.0))
# # grid(True, which="both")
# plot(lam_list,vavg_list_A_bell,color='red',marker='o',label='MDP')
# # plot(lam_list,vavg_list_A_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
# # plot(lam_list,vavg_list_A_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
# plot(lam_list,vavg_list_A_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
# # plot(lam_list,vavg_list_A_rnd,color='0.75', linestyle='--', fillstyle='none',marker='v',label='RND')
# xlabel('$A$',fontsize=16)
# ylabel('Agent\'s avg. profit',fontsize=16)
# subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best')
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
# # xlim([2,31])
# # ylim([65,165])
#    
# show()
# print "TERMINATED."