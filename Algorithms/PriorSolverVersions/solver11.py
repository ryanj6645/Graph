import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import random

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
    t = G.order() - 1
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

    (removedC, removedK, max_path) = analyze_graph(G, t, c, k)
    return (removedC, removedK)


def analyze_graph(G, t, c, k):
    s = 0
    if c == 0 and k == 0:
        return ([], [], nx.dijkstra_path_length(G, source=s, target=t, weight='weight'))
    options = []
    item_to_del = None
    path = nx.shortest_path(G, source=s, target=t, weight='weight', method='dijkstra')
    edgeTup = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    copyG = G.copy()
    if c > 0:
        for v in path[1:-1]:
            copyG.remove_node(v)
            if nx.is_connected(copyG):
                options.append((v, nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
            copyG = G.copy()

    if k > 0:
        for edge in edgeTup:
            copyG.remove_edge(*edge)
            if nx.is_connected(copyG):
                options.append((edge, nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
            copyG = G.copy()

    options = list(sorted(options, key=lambda item: item[1], reverse=True))
    if len(options) > 1:
        branching_factor = random.randrange(1, min(4, len(options)))
    elif len(options) == 1:
        branching_factor = 1
    else:
        branching_factor = 0
    new_c = []
    new_k = []
    max_path = nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')
    for _ in range(branching_factor):
        GPrime = G.copy()
        item_to_del = options.pop(0)[0]
        if type(item_to_del) is int:
            GPrime.remove_node(item_to_del)
            (new_removed_c, new_removed_k, path_length) = analyze_graph(GPrime, t, c - 1, k)
            if path_length > max_path:
                max_path = path_length
                new_c = [item_to_del] + new_removed_c
                new_k = new_removed_k
        elif type(item_to_del) is tuple:
            GPrime.remove_edge(*item_to_del)
            (new_removed_c, new_removed_k, path_length) = analyze_graph(GPrime, t, c, k - 1)
            if path_length > max_path:
                max_path = path_length
                new_c = new_removed_c
                new_k = [item_to_del] + new_removed_k

    return (new_c, new_k, max_path)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs2/foo.out')


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
