'''
Created on 1 May, 2014

@author: yzhang28
'''

from multiprocessing import Pool
import numpy

import multiprocessing

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return

def ParaProcess(i):
    if i==1:
        print "aaa" + str(i)
    else:
        print "bbb"
    return

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=ParaProcess, args=(i,))
        p.start()