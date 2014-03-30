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

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
L = 10 # locations numbered: 0, 1, ..., L. L+1 states
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.8
DELTA = 0.01
RANDOM_COUNT = 5

E_list = [6,7,8,9,10,11,12,13,14,15]
# E_list = [5,6,7,8]

expnum = len(E_list)

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


for e_cur in E_list:
    params = {'A':A, 'A_inf':A+1, \
                'L':L, 'E':e_cur, \
                'B':B, 'B_inf':B+1, \
                'GAM':DISCOUNT_FACTOR,\
                'DELTA': DELTA, \
                'LMAT': None, \
                'WMAT': None, \
                'SIG': None}
    ind = E_list.index(e_cur)
      
    print "---- ROUND:", E_list.index(e_cur)+1,
    print "out of", len(E_list)
      
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
pickle.dump(expnum, open("./results/E_changing/expnum","w"))
pickle.dump(Paramsset, open("./results/E_changing/paramsset","w"))
pickle.dump(E_list, open("./results/E_changing/xaxis","w"))
pickle.dump([Vset_bell, Aset_bell, RESset_bell], open("./results/E_changing/bell","w"))
pickle.dump([Vset_myo, Aset_myo, RESset_myo], open("./results/E_changing/myo","w"))
pickle.dump([Vset_zero, Aset_zero, RESset_zero], open("./results/E_changing/zero","w"))
pickle.dump([Vset_one, Aset_one, RESset_one], open("./results/E_changing/one","w"))
pickle.dump([Vset_rnd, Aset_rnd, RESset_rnd], open("./results/E_changing/rnd","w"))
print "Finished"



# figa = plt.figure(figsize=(4.5,5.0))
# # grid(True, which="both")
# plot(E_list,act_rate_list_E_bell,color='red',marker='o', label='MDP')
# plot(E_list,act_rate_list_E_myo,color='green', linestyle='--',fillstyle='none',marker='^', label='MYO')
# plot(E_list,act_rate_list_E_rnd,color='0.75', linestyle='--', fillstyle='none',marker='v',label='RND')
# xlabel('$E$',fontsize=16)
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
# plot(E_list,vavg_list_E_bell,color='red',marker='o',label='MDP')
# plot(E_list,vavg_list_E_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
# plot(E_list,vavg_list_E_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
# plot(E_list,vavg_list_E_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
# plot(E_list,vavg_list_E_rnd,color='0.75', linestyle='--', fillstyle='none',marker='v',label='RND')
# xlabel('$E$',fontsize=16)
# ylabel('Agent\'s avg. profit',fontsize=16)
# subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best')
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
# # xlim([2,31])
# # ylim([65,165])
# 
# 
# show()
# print "TERMINATED."