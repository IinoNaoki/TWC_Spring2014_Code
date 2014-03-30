'''
Created on 26 Feb, 2014

@author: yzhang28
'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox

from HarvCore.func import *

A_CONST = 1
E_CONST = 5
L_CONST = 4
#### WE ASSUME E_CONST>A_CONST and E_CONST>B_CONST
B_CONST = 1 # NOT A STATE, chargeable energy unit: \sigma_0, \sigma_1, ..., \sigma_B, \sigma_{+\infty}
#B_INFTY = B_CONST + 1

DISCOUNT_FACTOR = 0.8
DELTA = 0.01
SIG = [0.5, 0.5, 0.0]


# w_line = [[0.60, 0.10, 0.10, 0.10, 0.10, 0.00],
#           [0.10, 0.10, 0.10, 0.10, 0.60, 0.00]]
w_line = [[0.90, 0.10, 0.00],
          [0.10, 0.90, 0.00]]
wmat = [None for _ in range(len(w_line))]
for i in range(len(w_line)):
    wmat[i] = [w_line[i] for _ in range(A_CONST+1+1)]

for WMAT in wmat:
    params_e = {'A':A_CONST, 'A_inf':A_CONST+1, \
                'L':L_CONST, 'E':E_CONST, \
                'B':B_CONST, 'B_inf':B_CONST+1, \
                'GAM':DISCOUNT_FACTOR,\
                'DELTA': DELTA, \
                'LMAT': None, \
                'WMAT': WMAT, \
                'SIG': SIG}
      
    V, A = BellmanSolver(params_e, parabola_flag=1)
    ShowMatrix(A, mode='a', fixdim='w', fixnum=1, params=params_e)
    # ShowMatrix(A, mode='a', fixdim='w', fixnum=2, params=params_e)
    # ShowMatrix(A, mode='a', fixdim='w', fixnum=3, params=params_e)
    ShowMatrix(A, mode='a', fixdim='l', fixnum=1, params=params_e)
#     ShowMatrix(V, mode='v', fixdim='l', fixnum=1, params=params_e)
    ShowMatrix(A, mode='a', fixdim='l', fixnum=2, params=params_e)
#     ShowMatrix(V, mode='v', fixdim='l', fixnum=2, params=params_e)
    ShowMatrix(A, mode='a', fixdim='l', fixnum=3, params=params_e)
#     ShowMatrix(V, mode='v', fixdim='l', fixnum=3, params=params_e)
    print '-------------------------------------------------------------'
    print '-------------------------------------------------------------'
    print '-------------------------------------------------------------'
    print '-------------------------------------------------------------'
    

    
    
# first result, when proft_e is concave
# BUILDING PROB MATRIX
# Delta= 1.14915638653
# Delta= 0.495563315636
# Delta= 0.353328102346
# Delta= 0.24786051562
# Delta= 0.170364505285
# Delta= 0.116002975188
# Delta= 0.0785100379132
# Delta= 0.0528944107324
# Delta= 0.035510303836
# Delta= 0.0237738797865
# Delta= 0.0158829494949
# Delta= 0.0105946062436
# Delta= 0.0070592256064
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     0     0     0    
# 1     1     0     0     0    
# 1     1     0     0     0    
# 1     1     0     0     0    
# 1     0     0     0     0    
# 0     0     0     0     0    
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 0     0     0    
# 0     0     0    
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# BUILDING PROB MATRIX
# Delta= 1.68251660254
# Delta= 0.694538569756
# Delta= 0.269065661918
# Delta= 0.168282009468
# Delta= 0.116035455628
# Delta= 0.0797433825193
# Delta= 0.0547673322724
# Delta= 0.0376102305748
# Delta= 0.0258275262278
# Delta= 0.0177360491942
# Delta= 0.0121795031017
# Delta= 0.0083637603647
# ---ACTION MATRIX---
# Line: e
# Col: l
# 1     1     1     0     0    
# 1     1     1     0     0    
# 1     1     1     0     0    
# 1     1     1     0     0    
# 1     1     1     0     0    
# 0     0     0     0     0    
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 0     0     0    
# ---ACTION MATRIX---
# Line: e
# Col: w
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 1     1     1    
# 0     0     0    
# ---ACTION MATRIX---
# Line: e
# Col: w
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# 0     0     0    
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

