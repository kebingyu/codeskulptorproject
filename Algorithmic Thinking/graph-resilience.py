"""
constant
"""
EX_GRAPH0 = {
    0 : set([1, 2]),
    1 : set([]),
    2 : set([])
    }
EX_GRAPH1 = {
    0 : set([1, 4, 5]),
    1 : set([2, 6]),
    2 : set([3]),
    3 : set([0]),
    4 : set([1]),
    5 : set([2]),
    6 : set([])
    }
EX_GRAPH2 = {
    0 : set([1, 4, 5]),
    1 : set([2, 6]),
    2 : set([3, 7]),
    3 : set([7]),
    4 : set([1]),
    5 : set([2]),
    6 : set([]),
    7 : set([3]),
    8 : set([1, 2]),
    9 : set([0, 3, 4, 5, 6, 7])
    }

import random

def bfs_visited(ugraph, start_node):
    """
    Breadth-first search
    """
    my_queue = [start_node]
    visited = [start_node]
    while my_queue:
        curr_node = my_queue.pop(0)
        for neighbor in ugraph[curr_node]:
            if neighbor not in visited:
                visited.append(neighbor)
                my_queue.append(neighbor)
    return set(visited)

def cc_visited(ugraph):
    """
    Connected components
    """
    remain_nodes = ugraph.keys()
    return_cc = []
    while remain_nodes:
        rand_node = random.choice(remain_nodes)
        visited = bfs_visited(ugraph, rand_node)
        return_cc.append(visited)
        remain_nodes = [n for n in remain_nodes if n not in visited]
    return return_cc

def largest_cc_size(ugraph):
    """
    returns the size (an integer) of the largest connected component
    """
    visited = cc_visited(ugraph)
    max_size = 0
    for cc_set in visited:
        if len(cc_set) > max_size:
            max_size = len(cc_set)
    return max_size

def compute_resilience(ugraph, attack_order):
    """
    Graph resilience
    """
    resilience = [largest_cc_size(ugraph)]
    for idx in range(1, len(attack_order) + 1):
        copy_graph = ugraph
        for key, value in copy_graph.items():
            if key in attack_order[:idx]:
                copy_graph.pop(key, None)
            else:
                copy_graph[key] = set([n for n in value if n not in attack_order[:idx]])
        resilience.append(largest_cc_size(copy_graph))
    return resilience

