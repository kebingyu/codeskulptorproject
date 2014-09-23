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

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)
distribution = in_degree_distribution(citation_graph)

import math
# normalize distribution and prepare log-log
dist_sum = sum(distribution.values())
dist_log = {}
distribution.pop(0)
for key in distribution:
    dist_log[math.log(key)] = math.log(distribution[key] * 1.0 /  dist_sum)
    
import simpleplot
simpleplot.plot_lines("M1-Q1: Normalized In Degree Distribution Log-Log (base 10)", 600, 600,
                      "in-degree (log)", "counter (log)", [dist_log])

