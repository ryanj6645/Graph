import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import time


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    # print(maxDegList(G))
    startTime = time.time()
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

    bfMin = []
    for i in range(c):
        for n in list(GPrime.nodes):
            if n == s or n == t:
                continue
            copyG.remove_node(n)
            if nx.is_connected(copyG):
                bfMin.append((n, nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
            copyG = GPrime.copy()
        if bfMin != []:
            rNode = max(bfMin, key=lambda x: x[1])
            removedC.append(rNode[0])
            GPrime.remove_node(rNode[0])
            copyG = GPrime.copy()
            bfMin = []
        else:
            break

    # bfMin = []
    # for i in range(k):
    #     edgeList = GPrime.edges
    #     for e in edgeList:
    #         copyG.remove_edge(e[0], e[1])
    #         if nx.is_connected(copyG):
    #             bfMin.append((e[0], e[1], nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
    #         copyG = GPrime.copy()
    #     if bfMin != []:
    #         rEdge = max(bfMin, key=lambda x: x[2])
    #         removedK.append((rEdge[0], rEdge[1]))
    #         GPrime.remove_edge(rEdge[0], rEdge[1])
    #         copyG = GPrime.copy()
    #         bfMin = []
    #     else:
    #         break
    #
    bfMin = []
    for i in range(k//3):
        for e1 in range(0, len(GPrime.edges) - 2):
            for e2 in range(e1 + 1, len(GPrime.edges) - 1):
                for e3 in range(e2 + 1, len(GPrime.edges)):
                    ae1 = list(GPrime.edges)[e1]
                    ae2 = list(GPrime.edges)[e2]
                    ae3 = list(GPrime.edges)[e3]
                    copyG.remove_edge(ae1[0], ae1[1])
                    copyG.remove_edge(ae2[0], ae2[1])
                    copyG.remove_edge(ae3[0], ae3[1])
                    if nx.is_connected(copyG):
                        bfMin.append((ae1[0], ae1[1], ae2[0], ae2[1], ae3[0], ae3[1], nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
                    copyG = GPrime.copy()
        if bfMin != []:
            rEdge = max(bfMin, key=lambda x: x[6])
            removedK.append((rEdge[0], rEdge[1]))
            removedK.append((rEdge[2], rEdge[3]))
            removedK.append((rEdge[4], rEdge[5]))
            GPrime.remove_edge(rEdge[0], rEdge[1])
            GPrime.remove_edge(rEdge[2], rEdge[3])
            GPrime.remove_edge(rEdge[4], rEdge[5])
            copyG = GPrime.copy()
            bfMin = []
        else:
            break
    print(time.time() - startTime)
    return (removedC, removedK)

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
