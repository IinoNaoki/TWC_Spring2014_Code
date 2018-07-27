'''
Created on 20 Mar, 2014

@author: yzhang28
'''

import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox

import sys
sys.path.append("..")
#from HarvCore.func import *

expnum = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/expnum","rb"))
x_axis_list = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/xaxis","rb"))

RESset_bell = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/bell","rb"))
RESset_myo = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/myo","rb"))
RESset_zero = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/zero","rb"))
RESset_one = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/one","rb"))
RESset_rnd = pickle.load(open("C:/Users/YZHAN/Documents/GitHub/TWC_Spring2014_Code/Harv/results/L_changing/rnd","rb"))


# def GetOptResultList(V,A, params):
#     return [MATOP_GetValueAvg(V, params), MATOP_GetValueSteadyAvg(V,A, params), \
#             MATOP_GetActionAvg(A, params), MATOP_GetActionSteadyAvg(A, params), \
#             MATOP_GetBlockingProb(A, params), MATOP_GetEnergySteadyAvg(A, params) ]

y_v_avg_bell = [RESset_bell[i][0] for i in range(expnum)]
y_v_steady_bell = [RESset_bell[i][1] for i in range(expnum)]
y_a_avg_bell = [RESset_bell[i][2] for i in range(expnum)]
y_a_steady_bell = [RESset_bell[i][3] for i in range(expnum)]
y_blocking_bell = [RESset_bell[i][4] for i in range(expnum)]
y_e_steady_bell = [RESset_bell[i][5] for i in range(expnum)]

y_v_avg_myo = [RESset_myo[i][0] for i in range(expnum)]
y_v_steady_myo = [RESset_myo[i][1] for i in range(expnum)]
y_a_avg_myo = [RESset_myo[i][2] for i in range(expnum)]
y_a_steady_myo = [RESset_myo[i][3] for i in range(expnum)]
y_blocking_myo = [RESset_myo[i][4] for i in range(expnum)]
y_e_steady_myo = [RESset_myo[i][5] for i in range(expnum)]

y_v_avg_zero = [RESset_zero[i][0] for i in range(expnum)]
y_v_steady_zero = [RESset_zero[i][1] for i in range(expnum)]
y_a_avg_zero = [RESset_zero[i][2] for i in range(expnum)]
y_a_steady_zero = [RESset_zero[i][3] for i in range(expnum)]
y_blocking_zero = [RESset_zero[i][4] for i in range(expnum)]
y_e_steady_zero = [RESset_zero[i][5] for i in range(expnum)]

y_v_avg_one = [RESset_one[i][0] for i in range(expnum)]
y_v_steady_one = [RESset_one[i][1] for i in range(expnum)]
y_a_avg_one = [RESset_one[i][2] for i in range(expnum)]
y_a_steady_one = [RESset_one[i][3] for i in range(expnum)]
y_blocking_one = [RESset_one[i][4] for i in range(expnum)]
y_e_steady_one = [RESset_one[i][5] for i in range(expnum)]

y_v_avg_rnd = [RESset_rnd[i][0] for i in range(expnum)]
y_v_steady_rnd = [RESset_rnd[i][1] for i in range(expnum)]
y_a_avg_rnd = [RESset_rnd[i][2] for i in range(expnum)]
y_a_steady_rnd = [RESset_rnd[i][3] for i in range(expnum)]
y_blocking_rnd = [RESset_rnd[i][4] for i in range(expnum)]
y_e_steady_rnd = [RESset_rnd[i][5] for i in range(expnum)]

# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_v_avg_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_v_avg_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
plot(x_axis_list,y_v_avg_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
plot(x_axis_list,y_v_avg_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
plot(x_axis_list,y_v_avg_rnd,color='grey',linestyle='--',fillstyle='none',marker='v',label='RND')
xlabel('$L$',fontsize=16)
ylabel('Expected utility',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc='best', fontsize=12, ncol=1,fancybox=True,shadow=True)
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
# xlim([2,31])
# ylim([-0.5,2.10])
     
# plt.figure(figsize=(4.5,5.0))
# # grid(True, which="both")
# plot(x_axis_list,y_v_steady_bell,color='red',marker='o',label='MDP')
# plot(x_axis_list,y_v_steady_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
# plot(x_axis_list,y_v_steady_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
# plot(x_axis_list,y_v_steady_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
# plot(x_axis_list,y_v_steady_rnd,color='grey',linestyle='--',fillstyle='none',marker='v',label='RND')
# xlabel('Maximum energy capacity $E$',fontsize=16)
# ylabel('Steady state avg. utility',fontsize=16)
# subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.40,0.05), fontsize=12, ncol=2,fancybox=True,shadow=True)
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
# # xlim([2,31])
# # ylim([65,165])


# # SHOW ACTIONS
# plt.figure(figsize=(4.5,5.0))
# # grid(True, which="both")
# plot(x_axis_list,y_a_avg_bell,color='red',marker='o',label='MDP')
# plot(x_axis_list,y_a_avg_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
# plot(x_axis_list,y_a_avg_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
# plot(x_axis_list,y_a_avg_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
# plot(x_axis_list,y_a_avg_rnd,color='grey',linestyle='--',fillstyle='none',marker='v',label='RND')
# xlabel('Maximum energy capacity $E$',fontsize=16)
# ylabel('Charging rate',fontsize=16)
# subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.40,0.65), fontsize=12, ncol=2,fancybox=True,shadow=True)
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
# # xlim([2,31])
# # ylim([0.6,0.9])
  
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_a_steady_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_a_steady_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
plot(x_axis_list,y_a_steady_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
plot(x_axis_list,y_a_steady_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
plot(x_axis_list,y_a_steady_rnd,color='grey',linestyle='--',fillstyle='none',marker='v',label='RND')
xlabel('$L$',fontsize=16)
ylabel('Charging rate',fontsize=16) # steady state
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc=(0.05, 0.13), fontsize=12, ncol=1,fancybox=True,shadow=True)
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
# xlim([2,31])
# ylim([0.6,0.9])
#END SHOW ACTIONS


# BLOCKING PROBABILITY
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_blocking_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_blocking_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
plot(x_axis_list,y_blocking_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
plot(x_axis_list,y_blocking_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
plot(x_axis_list,y_blocking_rnd,color='grey',linestyle='--',fillstyle='none',marker='v',label='RND')
xlabel('$L$',fontsize=16)
ylabel('Insufficient energy prob.',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc=(0.42, 0.50), fontsize=12, ncol=2, fancybox=True,shadow=True)
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
# xlim([2,31])
ylim([0.2,0.82])


# Steady state energy storage
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_e_steady_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_e_steady_zero,color='black',linestyle='--',fillstyle='none',marker='s',label='$\mathcal{A}=0$')
plot(x_axis_list,y_e_steady_one,color='blue',linestyle='--',fillstyle='none',marker='x',label='$\mathcal{A}=1$')
plot(x_axis_list,y_e_steady_myo,color='green',linestyle='--',fillstyle='none',marker='^',label='MYO')
plot(x_axis_list,y_e_steady_rnd,color='grey',linestyle='--',fillstyle='none',marker='v',label='RND')
xlabel('$L$',fontsize=16)
ylabel('Energy storage level',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.05,0.78), fontsize=12, ncol=2,fancybox=True,shadow=True)
legend(loc='best', fontsize=12, ncol=1,fancybox=True,shadow=True)
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
# xlim([2,31])
# ylim([0.6,0.9])

show()