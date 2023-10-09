# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:26:29 2023

@author: xinzhan
"""

def find_bottom(node, next_nodes):
    """
    Find the "bottom" of a cluster starting from node in dictionary next_nodes

    Parameters:
        node: starting node
        next_nodes: dictionary of node connections

    Returns:
        the bottom node in the cluster
    """
    # Your code here
    while node != next_nodes[node]:
        node = next_nodes[node]
    return node



def merge_sets(node1, node2, next_nodes, set_starters):
    """
    Merges the clusters containing node1, node2 using the connections dictionary next_nodes.
    Also removes any bottom node which is no longer a "starting node" from set_starters.

    Parameters:
        node1: first node the set of which will be merged
        node2: second node the set of which will be merged
        next_nodes: dictionary of node connections
        set_starters: set of nodes that "start" a cluster

    Returns:
        does this function need to return something?
    """
    # Your code here
    bottom1 = find_bottom(node1, next_nodes)
    bottom2 = find_bottom(node2, next_nodes)
    next_nodes[bottom1] = bottom2
    if bottom1 in set_starters:
        set_starters.remove(bottom2)


def cluster_correlations(edge_list, firms, k=200):
    """
    A mystery clustering algorithm
     
    Parameters:
         edge_list - list of edges of the form (weight,source,destination)
         firms - list of firms (tickers)
         k - number of iterations of algorithm

    Returns:
         next_nodes - dictionary to store clusters as "pointers"
            - the dictionary keys are the nodes and the values are the node in the same cluster that the key node points to
         set_starters - set of nodes that no other node points to (this will be used to construct the sets below)

    Algorithm:
         1 sort edges by weight (highest correlation first)
         2 initialize next_nodes so that each node points to itself (single-node clusters)
         3 take highest correlation edge
            check if the source and destination are in the same cluster using find_bottom
            if not, merge the source and destination nodes' clusters using merge_sets
         4 if max iterations not reached, repeat 3 with next highest correlation
         (meanwhile also keep track of the "set starters" ie nodes that have nothing pointing to them for later use)
    """
    # Sort edges
    sorted_edges = sorted(edge_list, key=lambda x: x[0], reverse=True)
    print(sorted_edges)
    # Initialize dictionary of pointers
    next_nodes = {node: node for node in firms}
    # Keep track of "starting nodes", ie nodes that no other node points to in next_nodes
    set_starters = {node for node in firms}

    # Loop k times
    for i in range(k):
        # Your algorithm here
        for edge in sorted_edges:
            if find_bottom(edge[1], next_nodes) != find_bottom(edge[2], next_nodes):
                merge_sets(edge[1], edge[2], next_nodes, set_starters)
                print("working")
                break
                
        
    return set_starters, next_nodes

# Load intermediary results from a "pickle" file
# You can use these with your algorithm below
import pickle
file_name = 'cluster_correlations'
with open(file_name, "rb") as f:
    correl = pickle.load(f)
    edges = pickle.load(f)

firms = list(correl.columns)

edges = [(0.8, 'A', 'B'),
        (0.63, 'A', 'C'),
        (0.05, 'A', 'D'),
        (0.68, 'B', 'C'),
        (0.32, 'B', 'D'),
        (0.95, 'C', 'D')]
starters = {'A','B','C','D'}
cluster_correlations(edges, starters, k=3)

# set_starters, next_nodes = cluster_correlations(edges[:20], firms[:20], k=200)