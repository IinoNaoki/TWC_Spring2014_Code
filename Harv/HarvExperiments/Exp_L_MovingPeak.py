'''
Created on 25 Feb, 2014

@author: yzhang28
'''
import pickle
from HarvCore.func import *

A = 5 # operation status state: 0, 1, 2, ..., A, +\infty. A+2 states 
E = 10 # energy state numbered: 0, 1, ..., L. L+1 states
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B = 5 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

L = 10

DISCOUNT_FACTOR = 0.8
DELTA = 0.1
RANDOM_COUNT = 5

x_axis_list = [0,1,2,3,4,5,6,7,8,9]

expnum = len(x_axis_list)

Paramsset = [None for _ in range(expnum)]

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

PEAK = 0.5
Matline = [[] for _ in range(len(x_axis_list))]
for line,itemline in enumerate(Matline):
    for elem_index in range(L+1):
        peak_line = int(L*(line+1.0)*1.0/(1.0*len(x_axis_list)))
        if peak_line==elem_index:
            Matline[line].append(PEAK)
        else:
            Matline[line].append((1.0-PEAK)/(len(x_axis_list)-1.0))
# Matline[0]  = [0.6, 0.2, 0.1, 0.015, 0.015, 0.015, 0.015, 0.01, 0.01, 0.01, 0.01]
# Matline[1]  = [0.015, 0.015, 0.1, 0.6, 0.2, 0.015, 0.015, 0.01, 0.01, 0.01, 0.01]
# Matline[2]  = list(reversed(Matline[1]))
# Matline[3]  = list(reversed(Matline[0]))
 

for l_cur in x_axis_list:
    LMAT = [Matline[l_cur] for _ in range(0,L+1)]
    params = {'A':A, 'A_inf':A+1, \
                'L':L, 'E':E, \
                'B':B, 'B_inf':B+1, \
                'GAM':DISCOUNT_FACTOR,\
                'DELTA': DELTA, \
                'LMAT': LMAT, \
                'WMAT': None, \
                'SIG': None}
    ind = x_axis_list.index(l_cur)
       
    print "---- ROUND:", x_axis_list.index(l_cur)+1,
    print "out of", len(x_axis_list)
    
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
pickle.dump(expnum, open("./results/L_MovingPeak/expnum","w"))
pickle.dump(Paramsset, open("./results/L_MovingPeak/paramsset","w"))
pickle.dump(x_axis_list, open("./results/L_MovingPeak/xaxis","w"))
pickle.dump([Vset_bell, Aset_bell, RESset_bell], open("./results/L_MovingPeak/bell","w"))
pickle.dump([Vset_myo, Aset_myo, RESset_myo], open("./results/L_MovingPeak/myo","w"))
pickle.dump([Vset_zero, Aset_zero, RESset_zero], open("./results/L_MovingPeak/zero","w"))
pickle.dump([Vset_one, Aset_one, RESset_one], open("./results/L_MovingPeak/one","w"))
pickle.dump([Vset_rnd, Aset_rnd, RESset_rnd], open("./results/L_MovingPeak/rnd","w"))
print "Finished"







# figa = plt.figure(figsize=(4.5,5.0))
# # grid(True, which="both")
# plot(test_list,act_rate_list_L_bell,color='red',marker='o', label='MDP')
# plot(test_list,act_rate_list_L_myo,color='green', linestyle='--',fillstyle='none',marker='^', label='MYO')
# # plot(test_list,act_rate_list_L_rnd,color='0.75', linestyle='--', fillstyle='none',marker='v',label='RND')
# xlabel('$L$',fontsize=16)
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
# # figc = plt.figure(figsize=(4.5,5.0))
# # # grid(True, which="both")
# # plot(test_list,vavg_list_L_bell,color='red',marker='o',label='MDP')
# # plot(test_list,vavg_list_L_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
# # plot(test_list,vavg_list_L_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
# # plot(test_list,vavg_list_L_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
# # # plot(test_list,vavg_list_L_rnd,color='0.75', linestyle='--', fillstyle='none',marker='v',label='RND')
# # xlabel('$L$',fontsize=16)
# # ylabel('Agent\'s avg. profit',fontsize=16)
# # subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# # legend(loc='best', fontsize=12)
# # locs, labels = plt.yticks()
# # plt.setp(labels, rotation=90)
# # # xlim([2,31])
# # # ylim([65,165])
# 
# figd = plt.figure()
# bar(np.asarray(test_list)-0.3+1, vavg_list_L_bell, width=0.2, color='red',align='center')
# bar(np.asarray(test_list)-0.1+1, vavg_list_L_myo, width=0.2, color='blue',align='center')
# bar(np.asarray(test_list)+0.1+1, v_list_L_steady_bell, width=0.2, color='grey',align='center')
# bar(np.asarray(test_list)+0.3+1, v_list_L_steady_myo, width=0.2, color='black',align='center')
# # bar(np.asarray(test_list)-0.1+1, vavg_list_L_myo, width=0.2, color='green',align='center')
# # bar(np.asarray(test_list)+0.1+1, vavg_list_L_one, width=0.2, color='blue',align='center')
# # bar(np.asarray(test_list)+0.3+1, vavg_list_L_zero, width=0.2, color='black',align='center')
# 
# show()
# print "TERMINATED."