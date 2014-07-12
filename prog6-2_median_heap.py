# Heap algorithm for median maintenance problem

import time
from pylab import *

def add_to_heap_max(heap,num):
    # heap with the minimum at the root
    heap.append(num)
    k = len(heap) # the current node
    kp = k/2 # the parent node
    while (k > 1) & (heap[k-1] > heap[kp-1]):
        heap[k-1], heap[kp-1] = heap[kp-1], heap[k-1]
        k = kp 
        kp = k/2

def add_to_heap_min(heap,num):
    # heap with the maximum at the root
    heap.append(num)
    k = len(heap) # the current node
    kp = k/2 # the parent node
    while (k > 1) & (heap[k-1] < heap[kp-1]):
        heap[k-1], heap[kp-1] = heap[kp-1], heap[k-1]
        k = kp 
        kp = k/2

def extract_max(heap):
    # Remove the maximum value, which is at the root, and reorganize the heap
    heap[0] = heap[len(heap)-1]
    heap.pop(len(heap)-1)
    k = 1
    lc = k * 2 # left child
    rc = k * 2 + 1 # right child
    while lc <= len(heap):
        if rc <= len(heap):
            n = lc if heap[lc-1] > heap[rc-1] else rc
        else:
            n = lc
        
        # bubble down
        if heap[k-1] < heap[n-1]:
            heap[k-1], heap[n-1] = heap[n-1], heap[k-1]
        else:
            break
        
        k = n
        lc = k * 2
        rc = k * 2 +1
    
    return

def extract_min(heap):
    # Remove the minimun value, which is at the root, and reorganize the heap
    heap[0] = heap[len(heap)-1]
    heap.pop(len(heap)-1)
    k = 1
    lc = k * 2 # left child
    rc = k * 2 + 1 # right child
    while lc <= len(heap):
        if rc <= len(heap):
            n = lc if heap[lc-1] < heap[rc-1] else rc
        else:
            n = lc
        
        # bubble down
        if heap[k-1] > heap[n-1]:
            heap[k-1], heap[n-1] = heap[n-1], heap[k-1]
        else:
            break
        
        k = n
        lc = k * 2
        rc = k * 2 + 1
    
    return    

def add_to_heaps(lheap,hheap,num):
    if len(lheap) == 0:
        lheap.append(num)
    else:
        if num < lheap[0]:
            add_to_heap_max(lheap, num)
        else:
            add_to_heap_min(hheap, num)
        
        
        if len(lheap) == (len(hheap) + 2):
            add_to_heap_min(hheap,lheap[0])
            extract_max(lheap)
        elif len(hheap) == (len(lheap) + 2):
            add_to_heap_max(lheap,hheap[0])
            extract_min(hheap)
    
    if len(lheap) >= len(hheap):
        return lheap[0]
    else:
        return hheap[0]


def solve_it(input_data):
    lines = input_data.split('\n')

    if '' in lines:
        lines.remove('')
    
    ncount = len(lines) 
    numlist = []
    
    heap_low = [] # heap of the lowest half 
    heap_high = [] # heap of the highest half
    
    sum_median = 0
    for line in lines:
        line = int(line)
        median = add_to_heaps(heap_low,heap_high,line)
        sum_median += median

    return sum_median % 10000
    
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        start = time.time()
        print "m_1 + m_2 + ... + m_n =", solve_it(input_data)
        end = time.time()
        print "Elasped time: ", end-start
    else:
        print 'This test requires an input file.  Please select one from the directory.'

