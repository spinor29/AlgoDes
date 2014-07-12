# Given a list of adjacent nodes and distances between adjacents nodes,find the shortest path from a source node to any other nodes.

import copy
import numpy as np
import time

class Node:
    def __init__(self, idn, prev, dpath):
        self.id = idn # index of the current node
        self.prev = prev # the previous node on the shortest path from source
        self.dpath = dpath # the distance of the shortes path from source

def dijkstra(alist, source):
    # alist is a list of list of [j,d] for each node, where for [j,d] in alist[i], j is one of the adjacent node of node i, and d is the distance between node j and node i.

    node_count = len(alist)
    shortest = [ Node(i, None, None) for i in range(node_count)]
    shortest[source].idn = source
    shortest[source].dpath = 0
    
    counted = [ source ] # counted is a list of node that has been considered
    # Use the simple comparison to get minimum every iteration (i.e. O(mn) for the whole algorithm)
    
    dsum_min = [0] * node_count # distance of shortest path from source node
    dsum_temp = 0
    to_be_counted = [] # list of nodes outside of set X (which contains all nodes that have been considered) but having edges connected with those in X. These nodes are the ones to be considered.
    
    jmin = source
    while (len(counted) < node_count):
        i = jmin
        n_adj = len(alist[i])
        dpath_prev = shortest[i].dpath # distance of shortest path to
        #print "Considering newly added node ", i+1
        for j in range(n_adj):
            idn = alist[i][j][0]
            d = alist[i][j][1]
            dsum = dpath_prev + d # distance of shortest path from source to node j through node i
            
            if idn not in counted[:]:
                if shortest[idn].prev == None:
                # Assign values for first time
                    shortest[idn].prev = i
                    shortest[idn].dpath = dsum
                    to_be_counted.append(idn)
                elif shortest[idn].dpath > dsum:
                    # Update shortest path from source to node j
                    shortest[idn].dpath = dsum
                    shortest[idn].prev = i
                
    
        dmin = 100000000
        jmin = 0
        for j in to_be_counted[:]:
            dsum2 = shortest[j].dpath
            if dmin > dsum2:
                dmin = dsum2
                jmin = j
        counted.append(jmin)
        to_be_counted.remove(jmin)
        
    return shortest
        

def solve_it(input_data):
    lines = input_data.split('\n')
    
    if "" in lines:
        lines.remove("")
    
    node_count = len(lines)
    adj_list = [] # list of adjacent nodes
    for i in range(node_count):
        adj_list.append([])

    
    for line in lines:
        fields = line.rstrip('\r').split('\t')
        #fields = line.split(' ')
        #print fields
        
        if '' in fields:
            fields.remove('')
        
        node0 = int(fields[0])
        
        for i in range(1,len(fields)):
            x = fields[i].split(',')
            # Shift down the node index from input file by one, index 0 represent node 1
            adj_list[node0-1].append([(int(x[0])-1),int(x[1])])

    source_node = 0
    shortest_dist = dijkstra(adj_list, source_node)
    
    output = ','.join(str(shortest_dist[k-1].dpath) for k in range(node_count))
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

