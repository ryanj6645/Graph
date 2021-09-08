import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


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

    for i in range(19000):
        nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')
        if i % 10 == 0:
            print(i)

    # bfMin = []
    # for i in range(c):
    #     for n in list(GPrime.nodes):
    #         if n == s or n == t:
    #             continue
    #         copyG.remove_node(n)
    #         if nx.is_connected(copyG):
    #             bfMin.append((n, nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
    #         copyG = GPrime.copy()
    #     if bfMin != []:
    #         rNode = max(bfMin, key=lambda x: x[1])
    #         removedC.append(rNode[0])
    #         GPrime.remove_node(rNode[0])
    #         copyG = GPrime.copy()
    #         bfMin = []
    #     else:
    #         break
    #
    # copyG = GPrime.copy()
    # can_continue = True
    # num_eliminated_edges = 0
    # while can_continue:
    #     spEdge = minEdgeList(GPrime, s, t)
    #     flag = True
    #     if spEdge == []:
    #         flag = False
    #         can_continue = False
    #     while flag:
    #         minEdge = min(spEdge, key=lambda x: x[2])
    #         copyG.remove_edge(minEdge[0], minEdge[1])
    #         if nx.is_connected(copyG):
    #             GPrime.remove_edge(minEdge[0], minEdge[1])
    #             removedK.append((minEdge[0], minEdge[1]))
    #             num_eliminated_edges += 1
    #             flag = False
    #         else:
    #             spEdge.remove(minEdge)
    #             copyG = GPrime.copy()
    #         if spEdge == []:
    #             flag = False
    #             can_continue = False
    #         if num_eliminated_edges >= k:
    #             flag = False
    #             can_continue = False
    return (removedC, removedK)


def minEdgeList(G, s, t):
    path = nx.shortest_path(G, source=s, target=t, weight='weight', method='dijkstra')
    pathTup = []
    for i in range(len(path) - 1):
        pathTup.append((path[i], path[i+1], G[path[i]][path[i+1]]["weight"]))
    return pathTup

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
