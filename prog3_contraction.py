# Random contraction algorithm for calculating minimum cuts

import random

import copy

def contraction(edges, neigh_list, num_edges, tot_edges):
    n_edges = len(edges) # number of total distinct edges
    while n_edges > 1:
        if n_edges == 1:
            return num_edges[tuple(edges[0])]
        else:
            p = random.randrange(0, tot_edges) # randomly choose an edge
            q = 0
            temp = p
            while temp > 0:
                temp -= num_edges[tuple(edges[q])]
                q += 1
            # merging node1 into node0
            node0 = edges[q-1][0] 
            node1 = edges[q-1][1]
        
            #print "node0, node1 = ", node0, node1
            for neighbor in neigh_list[node1]:
                # node_pair is a tuple
                if neighbor != node0:
                    # sort node0 and neighbor
                    node_pair0 = (node0, neighbor) if node0 < neighbor else (neighbor, node0)
                    # sort node1 and neighbor
                    node_pair1 = (node1, neighbor) if node1 < neighbor else (neighbor, node1)
                    if neighbor in neigh_list[node0]:
                        num_edges[node_pair0] += num_edges[node_pair1]
                    else:
                        neigh_list[node0].append(neighbor)
                        neigh_list[neighbor].append(node0)
                        edges.append(list(node_pair0))
                        num_edges[node_pair0] = num_edges[node_pair1]
                    neigh_list[neighbor].remove(node1)
                    edges.remove(list(node_pair1))
                    num_edges.pop(node_pair1, None)
                else:
                    edges.remove([node0, node1])
                    tot_edges -= num_edges[(node0, node1)] # update total number of edges
                    neigh_list[node0].remove(node1)
                    num_edges.pop((node0, node1), None)
                    
            neigh_list.pop(node1, None)
            n_edges = len(edges)
    return num_edges[tuple(edges[0])]

def solve_it(input_data):
    #random.seed(seed)
    lines = input_data.split('\n')
    lines.remove("")
    num_nodes = len(lines)
    edges = []
    neighbors_list = {}
    num_edges = {} # number of edges between two nodes, edges[0] and edges[1]
    id_edges = [[]] * num_nodes # index of edges in which a node index is present
    
    # parse input data into edges and neighbors_list
    tot_edges = 0
    for line in lines:
        fields = line.rstrip('\r').split('\t')
        if '' in fields:
            fields.remove('')
        #print fields
        fields = [ int(s) for s in fields ]
        node = fields[0]
        neighbors_list[node] = fields[1:len(fields)]
        n_adjacent = len(fields)-1 # number of adjacent nodes of node fields[0]
        for i in range(1, n_adjacent+1):
            if node < fields[i]:
                edges.append([node, fields[i]]) # list of nodes pair
                num_edges[(node, fields[i])] = 1
                tot_edges += 1
        
    min_cut = 1000000
    for i in range(100000):
        neighbors_list_copy = copy.deepcopy(neighbors_list)
        edges_copy = copy.deepcopy(edges)
        num_edges_copy = copy.deepcopy(num_edges)
        cut = contraction(edges_copy, neighbors_list_copy, num_edges_copy, tot_edges)
        if min_cut > cut:
            min_cut = cut
            print "min_cut = ", min_cut
    
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        solve_it(input_data)
    else:
        print 'This test requires an input file. Please select one from the directory.'


