'''
Created on 1 May, 2014

@author: yzhang28
'''

from multiprocessing import Pool
import numpy

def sqrt(x):
    return numpy.sqrt(x[0])+x[1]

maplist = []
for i in range(10):
    for j in range(100):
        maplist.append((i,j))

if __name__=='__main__':
    pool = Pool()
    roots = pool.map(sqrt, maplist)
    print roots