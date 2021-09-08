import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from collections import defaultdict
import cvxpy as cvx

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    x = cvx.Variable(G.number_of_edges(), integer=True)
    weight_multiplier = cvx.Variable(G.number_of_edges(), integer=True)
    objective = cvx.Maximize(cvx.Minimize("""TODO"""))
    constraints = [0 <= x <= 1]


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
