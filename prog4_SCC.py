# Strongly connected components algorithm

class Node:
    def __init__(self, head = [], tail = [], explored=False, ft=0):
        self.head = head # a dictionary {index of head node: explored or not}
        self.tail = tail
        self.explored = explored # if the node has been explored
        self.ft = ft # finishing time

import copy
import numpy as np
import time

# Calculate finishing time for each node
# The pass direction is backward, i.e. walk from head node to tail node
def cal_ft(alist):
    node_count = len(alist)
    unfinished = [] # list of indices of nodes to handel unfinished and finished nodes. Move unfinished nodes to the top of the list.
    location = []
    for i in range(node_count):
        unfinished.append(i)
        location.append(i)

    track = [] # to store the trace of current pass
    t = 1
    len_un = len(unfinished)
    current = len_un-1

    while t <= node_count:
        len_un = len(unfinished)
        
        alist[current].explored = True
        
        if len(alist[current].tail) == 0: 
            alist[current].ft = t
            
            # Swap current with unfinished[t-1]. The swapping is tricky
            temp1 = location[current]
            temp2 = unfinished[t-1]
            unfinished[location[current]], unfinished[t-1] = unfinished[t-1], unfinished[location[current]]
            location[temp2] = temp1
            location[temp1] = t-1  
            
            #if len(unfinished) == 0:
            t += 1
            if t > node_count:
                continue

            
            # Back tracing (tail to head) or jump to new unfinished node
            n_track = len(track)
            if n_track != 0:
                # Back tracing
                prev = current
                current = track[n_track-1]
                track.pop() # remove last element from track
            else:
                # no walking backwards and back tracing available
                # jump to a new unfinished node
                current = unfinished[-1]
        else:
            for nextt in alist[current].tail:

                if alist[nextt].explored:
                    # Remove nodes in tail that have been explored
                    #alist[current].tail.pop(0)
                    alist[current].tail.remove(nextt)
                else:
                    # walk backwards along direction (advancing)
                    prev = current
                    track.append(prev)
                    current = nextt
                    # Remove node in tail that has been explored
                    alist[prev].tail.remove(nextt) 
                    break
        
        #print
        
# Calculate SCC
# The pass direction is forward, i.e. walk from tail node to head node
def cal_scc(alist):
    node_count = len(alist)
    print "node_count = ", node_count
    unfinished = []
    ftime = [] # setup a list of finishing times for obtaining maximum finishing time of unexplored nodes
    location = [] # list of index in unfinished and ftime
    scc_group = []
    vals_ex = []
    for i in range(node_count):
        unfinished.append(i)
        location.append(i) # the index in the list
        ftime.append(alist[i].ft)
        vals_ex.append(False)
    
    vals = np.array(ftime)
    vals = vals.argsort()
    print vals
    
    track = [] # to store the trace of current pass
    t = 1
    len_un = len(unfinished)
    
    #print "ftime = ", ftime
    current = ftime.index(max(ftime[:]))
    ftmax = alist[current].ft
    print "ftmax = ", ftmax
    
    scc_group.append([])
    
    while t <= node_count:
        len_un = len(unfinished)
        
        alist[current].explored = True
        vals_ex[current] = True
        
        if len(alist[current].head) == 0:
            scc_group[-1].append(current) # add current node to the current scc group
            # Swap current with unfinished[t-1]. The swapping is tricky
            temp1 = location[current]
            temp2 = unfinished[t-1]
            unfinished[location[current]], unfinished[t-1] = unfinished[t-1], unfinished[location[current]]
            ftime[location[current]], ftime[t-1] = ftime[t-1], ftime[location[current]]
            location[temp2] = temp1
            location[temp1] = t-1  
            
            t += 1
            if t > node_count:
                continue
            
            # Back tracing (tail to head) or jump to new unfinished node
            n_track = len(track)
            if n_track != 0:
                # Back tracing
                #print "back tracing..."
                prev = current
                current = track[n_track-1]
                track.pop() # remove last element from track
            else:
                # no walking forward and back tracing available
                # jump to a new unfinished node
                scc_group.append([])
                
                idx = ftmax-1
                while alist[vals[idx]].explored:
                    idx -= 1
                current = vals[idx]
                ftmax = idx+1
                nscc = 0

        else:
            for nextt in alist[current].head:      
                if alist[nextt].explored:
                    alist[current].head.remove(nextt) # Remove nodes in head that have been explored.
                    
                else:
                    # Walk backwards along direction (advancing)
                    prev = current
                    track.append(prev)
                    current = nextt
                    # Remove nodes in head that has been explored
                    alist[prev].head.remove(nextt)
                    break
        
        len_un = len(unfinished)

    return scc_group

def solve_it(input_data):
    node_count = 9
    lines = input_data.split('\n')
    #lines = input_data.split('\t')
    if "" in lines:
        lines.remove("")
    
    scc_list = [ Node([],[]) for i in range(0, node_count) ] # info of node i is in scc_list[i-1]
    for line in lines:
        fields = line.split(' ')
        #fields = line.split('\t')
        
        #if '' in fields:
        #    fields.remove('')
        
        fields[0] = int(fields[0])
        fields[1] = int(fields[1])
        #print fields
        if fields[0] != fields[1]:
            if (fields[1]-1) not in scc_list[fields[0]-1].head:
                scc_list[fields[0]-1].head.append(fields[1]-1) # fields[]
            if (fields[0]-1) not in scc_list[fields[1]-1].tail:
                scc_list[fields[1]-1].tail.append(fields[0]-1)
    
    scc_list2 = copy.deepcopy(scc_list) # copy for the second pass
    
    print "First pass: calculating finishing times:"
    cal_ft(scc_list) # calculate finishing time for each node
    
    print "Finishing times: "
    for i in range(node_count):
        print i+1, scc_list[i].ft
    
    print "Preparing for the second pass:"
    for i in range(node_count):
        scc_list2[i].ft = scc_list[i].ft
        
    print "Second pass: calculating SCC:"
    scc_group = cal_scc(scc_list2)

    n_scc = []
    for scc in scc_group:
        n_scc.append(len(scc))
    
    n_scc.sort(reverse=True)
    
    print "Number of Components: ", len(n_scc)
    
    for i in range(len(n_scc),5):
        n_scc.append(0)
           
    output = ','.join(str(scc) for scc in n_scc[:5])
    return output

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

