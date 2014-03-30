'''
Created on 20 Feb, 2014

@author: yzhang28
'''
import random
import scipy as sp
import numpy as np
import math
import matplotlib.pyplot as plt
import pickle

from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox



# from _func import *

from scipy.optimize import curve_fit

A_CONST = 4
L_CONST = 5
B_CONST = 5
E_CONST = 10
DISCOUNT_FACTOR = 0.8
TEST_PARAM_CONST = {'A':A_CONST, 'A_inf':A_CONST+1, \
              'L':L_CONST, 'E':E_CONST, \
              'B':B_CONST, 'B_inf':B_CONST+1, \
              'GAM':DISCOUNT_FACTOR,\
              'DELTA': 0.1, \
              'LMAT': None, \
              'WMAT': None, \
              'SIG': None}


from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

xpos = [1,2,3,4,5, 1,2,3,4,5, 1,2,3,4,5, 1,2,3,4,5, 1,2,3,4,5]
ypos = [1,1,1,1,1, 2,2,2,2,2, 3,3,3,3,3, 4,4,4,4,4, 5,5,5,5,5]
zpos = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]

dx = np.ones(25)*0.8
dy = np.ones(25)*0.8
dz = np.ones(25)

ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color='red')
plt.show()

    