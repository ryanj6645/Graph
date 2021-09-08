import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import time # EXTRA IMPORT
import random # EXTRA IMPORT

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    best_delta = 0
    num_nodes = G.order()
    removed_c = []
    removed_k = []
    start_time = time.time()
    if num_nodes <= 30 and num_nodes >= 20:
        k = 15
        c = 1
    elif num_nodes <= 50 and num_nodes >= 31:
        k = 50
        c = 3
    elif num_nodes <= 100 and num_nodes >= 51:
        k = 100
        c = 5
    while time.time() - start_time < 48:
        H = G.copy()
        random_nodes = random.sample(range(1, G.order() - 1), c)
        H.remove_nodes_from(random_nodes)
        random_edges = random.choices(list(H.edges()), k=k)
        H.remove_edges_from(random_edges)
        delta = calculate_quick_score(G, H, random_nodes, random_edges)
        if delta > best_delta:
            removed_c = random_nodes
            removed_k = random_edges
            best_delta = delta

    return (removed_c, removed_k)

def calculate_quick_score(G, H, c, k):
    """
    Calculates the difference between the original shortest path and the new shortest path.
    Args:
        G: networkx.Graph
        c: list of cities to remove
        k: list of edges to remove
    Returns:
        float: total score
    """
    node_count = len(G.nodes)
    original_min_dist = nx.dijkstra_path_length(G, 0, node_count-1)
    final_min_dist = nx.dijkstra_path_length(H, 0, node_count-1)
    difference = final_min_dist - original_min_dist
    return difference

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
