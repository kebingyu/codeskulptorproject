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

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary
    corresponding to a complete directed graph with the 
    specified number of nodes.
    """
    if num_nodes <= 0:
        return {}
    ret = {}
    for idx_i in range(num_nodes):
        curr_set = []
        for idx_j in range(num_nodes):
            if idx_i != idx_j:
                curr_set.append(idx_j)
        ret[idx_i] = set(curr_set)
    return ret

def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph.
    """
    ret = {}
    for key in digraph:
        ret[key] = 0
    for key in digraph:
        for _ in digraph[key]:
            ret[_] += 1
    return ret

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution of the in-degrees
    of the graph.
    """
    in_degree_dict = compute_in_degrees(digraph)
    ret = {}
    for key in in_degree_dict:
        if ret.has_key(in_degree_dict[key]):
            ret[in_degree_dict[key]] += 1
        else:
            ret[in_degree_dict[key]] = 1
    return ret

