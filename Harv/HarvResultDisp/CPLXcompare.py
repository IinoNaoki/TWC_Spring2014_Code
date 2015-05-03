'''
Created on 27 Apr, 2014

@author: yzhang28
'''

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def CPLX(G,L,W,A, t):
    if A==1:
        print "error CPLX(G,L,W,A)"
        exit()
    if t=='thresh':
        _tmp_sum = 0.0
        for k in range(1,A):
            _tmp_sum = _tmp_sum + nCr(G,k)*nCr(A,k+1)
        return pow(A+_tmp_sum, L*W)
    elif t=='non-thresh':

        return pow(A*1.0, G*L*W)

A = 2
L = 2
W = 2

A = 2
L = 1
W = 1

#test

# G = 10

# print CPLX(G,L,W,A, 'thresh')
# print CPLX(G,L,W,A, 'non-thresh')

x_axis = []
y_axis_thresh = []
y_axis_nonthresh = []
 
# for g in range(10,51):
for g in range(1,10):
#     G = 10*(g+1)
    G = g
    x_axis.append(G)
    y_axis_thresh.append(CPLX(G,L,W,A, 'thresh'))
    y_axis_nonthresh.append(CPLX(G,L,W,A, 'non-thresh'))



plt.figure(figsize=(7.0,4.2))
# grid(True, which="both")
plot(x_axis,y_axis_thresh,color='red',lw=2,label='Threshold policy')
plot(x_axis,y_axis_nonthresh,color='black', lw=2, ls='--',label='Non-threshold policy')

xlabel('Total number of energy states $|\mathbb{G}|$',fontsize=16)
ylabel('Complexity (possible policies)',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc='best', ncol=1,fancybox=True,shadow=True)
locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
yscale('log')
# xlim([2,31])
# ylim([2,0.9])

show()
print "TERMINATED."