# 2sum problem

import time
from pylab import *

def solve_it(input_data):
    lines = input_data.split('\n')

    if '' in lines:
        lines.remove('')
    
    numlist = []
    xhash = dict()
    
    nbin = 200000 # number of bins
    sbin = int(2e11/nbin) # size of bin
    for i in range(-nbin/2, nbin/2):
        xhash[i] = []
    
    for line in lines:
        #print line
        line = int(line)
        numlist.append(line)
        key = line / sbin
        
        if key in xhash:
            if line not in xhash[key]:
                xhash[key].append(line)

    z = np.array(numlist)

    # Print first 10 numbers of the input data...
    print "First 10 numbers of the input data:"
    for i in range(10):
        print numlist[i]
    
    # Print sample values in hash table
    print "Sample values in hash table:"
    for i in range(-5,5):
        if i in xhash:
            print i, xhash[i]

    tmin = -10000
    tmax = 10000
    tarray = np.zeros(tmax-tmin+1)
    
    nt = 0 # number of target values t
    
    for x in z:
        ymin = tmin - x
        ymax = tmax - x
        keymin = ymin / sbin
        keymax = ymax / sbin
        for key in range(keymin,keymax+1):
            if len(xhash[key]) != 0:
                for y in xhash[key]:
                    if (y != x):
                        t = x + y
                        if (t >= -10000) & (t <= 10000):
                            tarray[t-tmin] = 1

    nt = int(sum(tarray))
    return nt
    
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        start = time.time()
        print solve_it(input_data)
        end = time.time()
        print "Elasped time: ", end-start
    else:
        print 'This test requires an input file.  Please select one from the directory.'

