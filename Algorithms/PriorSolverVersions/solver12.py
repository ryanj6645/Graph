import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from collections import defaultdict

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    # print(maxDegList(G))
    numNodes = G.order()
    GPrime = G.copy()
    copyG = G.copy()
    c = 0
    k = 0
    s = 0
    removedC = []
    removedK = []
    t = numNodes - 1
    if numNodes <= 30 and numNodes >= 20:
        k = 15
        c = 1
    elif numNodes <= 50 and numNodes >= 31:
        k = 50
        c = 3
    elif numNodes <= 100 and numNodes >= 51:
        k = 100
        c = 5

    can_continue = True
    num_eliminated_vertices = 0
    while can_continue:
        spDeg = maxDegList(GPrime, s, t)
        flag = True
        if spDeg == []:
            flag = False
            can_continue = False
        while flag:
            maxDegNode = max(spDeg, key=lambda x: x[1])
            copyG.remove_node(maxDegNode[0])
            if nx.is_connected(copyG) and maxDegNode[0] != 0 and maxDegNode[0] != G.order() - 1:
                GPrime.remove_node(maxDegNode[0])
                removedC.append(maxDegNode[0])
                num_eliminated_vertices += 1
                flag = False
            else:
                spDeg.remove(maxDegNode)
                copyG = GPrime.copy()
            if spDeg == []:
                flag = False
                can_continue = False
            if num_eliminated_vertices >= c:
                flag = False
                can_continue = False
    # If there is nothing on the shortest path that can be deleted, then we could
    # delete nodeds not on the shortest path, might want to remove edges on shortest_path
    # path first.
    copyG = GPrime.copy()
    can_continue = True
    num_eliminated_edges = 0
    while can_continue:
        spEdge = bestEdgeList(GPrime, s, t)
        flag = True
        if spEdge == []:
            flag = False
            can_continue = False
        while flag:
            minEdge = max(spEdge, key=lambda x: x[1])
            copyG.remove_edge(*minEdge[0])
            if nx.is_connected(copyG):
                GPrime.remove_edge(*minEdge[0])
                removedK.append(minEdge[0])
                num_eliminated_edges += 1
                flag = False
            else:
                spEdge.remove(minEdge)
                copyG = GPrime.copy()
            if spEdge == []:
                flag = False
                can_continue = False
            if num_eliminated_edges >= k:
                flag = False
                can_continue = False
    return (removedC, removedK)

def maxDegList(G, s, t):
    node_centrality = nx.betweenness_centrality_subset(G, sources=[s], targets=[t], weight="weight")
    return list(node_centrality.items())

def bestEdgeList(G, s, t):
    edge_centrality = nx.edge_betweenness_centrality_subset(G, sources=[s], targets=[t], weight="weight")
    return list(edge_centrality.items())

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/foo.out')

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
