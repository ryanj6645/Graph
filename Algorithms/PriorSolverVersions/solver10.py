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
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0
    c = 0
    k = 0
    s = 0
    removedC = []
    removedK = []
    t = numNodes - 1
    c, k = numNodesCalc(numNodes)

    while k > 0 or c > 0:
        max_path = nx.dijkstra_path_length(GPrime, source=s, target=t, weight='weight')
        item_to_del = None
        path = nx.shortest_path(GPrime, source=s, target=t, weight='weight', method='dijkstra')
        edgeTup = [(path[i], path[i+1]) for i in range(len(path) - 1)]
        copyG = GPrime.copy()
        if c > 0:
            for v in path[1:-1]:
                copyG.remove_node(v)
                if nx.is_connected(copyG):
                    new_path_length = nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')
                    if new_path_length > max_path:
                        max_path = new_path_length
                        item_to_del = v
                copyG = GPrime.copy()

        if k > 0:
            for edge in edgeTup:
                copyG.remove_edge(*edge)
                if nx.is_connected(copyG):
                    new_path_length = nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')
                    if new_path_length > max_path:
                        max_path = new_path_length
                        item_to_del = edge
                copyG = GPrime.copy()

        if type(item_to_del) is tuple:
            GPrime.remove_edge(*item_to_del)
            removedK.append(item_to_del)
            k -= 1
        elif type(item_to_del) is int:
            GPrime.remove_node(item_to_del)
            removedC.append(item_to_del)
            c -= 1
        else:
            break

    ### 1st Alg

    c, k = numNodesCalc(numNodes)
    GDoublePrime = G.copy()
    copyG = G.copy()
    removedC2 = []
    removedK2 = []

    while c > 0:
        max_path = nx.dijkstra_path_length(GDoublePrime, source=s, target=t, weight='weight')
        item_to_del = None
        path = nx.shortest_path(GDoublePrime, source=s, target=t, weight='weight', method='dijkstra')
        for v in path[1:-1]:
            copyG.remove_node(v)
            if nx.is_connected(copyG):
                new_path_length = nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')
                if new_path_length > max_path:
                    max_path = new_path_length
                    item_to_del = v
            copyG = GDoublePrime.copy()
        if item_to_del == None:
            break
        GDoublePrime.remove_node(item_to_del)
        removedC2.append(item_to_del)
        c -= 1

    copyG = G.copy()
    while k > 0:
        max_path = nx.dijkstra_path_length(GDoublePrime, source=s, target=t, weight='weight')
        item_to_del = None
        path = nx.shortest_path(GDoublePrime, source=s, target=t, weight='weight', method='dijkstra')
        edgeTup = [(path[i], path[i+1]) for i in range(len(path) - 1)]
        copyG = GDoublePrime.copy()
        for edge in edgeTup:
            copyG.remove_edge(*edge)
            if nx.is_connected(copyG):
                new_path_length = nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')
                if new_path_length > max_path:
                    max_path = new_path_length
                    item_to_del = edge
            copyG = GDoublePrime.copy()
        if item_to_del == None:
            break
        GDoublePrime.remove_edge(*item_to_del)
        removedK2.append(item_to_del)
        k -= 1

    # 2nd Alg

    c, k = numNodesCalc(numNodes)
    removedC3 = []
    removedK3 = []
    GTriplePrime = G.copy()
    copyG = G.copy()

    if k == 50:
        bfMin = []
        for i in range(c):
            for n in list(GTriplePrime.nodes):
                if n == s or n == t:
                    continue
                copyG.remove_node(n)
                if nx.is_connected(copyG):
                    bfMin.append((n, nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
                copyG = GTriplePrime.copy()
            if bfMin != []:
                rNode = max(bfMin, key=lambda x: x[1])
                removedC3.append(rNode[0])
                GTriplePrime.remove_node(rNode[0])
                copyG = GTriplePrime.copy()
                bfMin = []
            else:
                break

        bfMin = []
        for i in range(k):
            edgeList = GTriplePrime.edges
            for e in edgeList:
                copyG.remove_edge(e[0], e[1])
                if nx.is_connected(copyG):
                    bfMin.append((e[0], e[1], nx.dijkstra_path_length(copyG, source=s, target=t, weight='weight')))
                copyG = GTriplePrime.copy()
            if bfMin != []:
                rEdge = max(bfMin, key=lambda x: x[2])
                removedK3.append((rEdge[0], rEdge[1]))
                GTriplePrime.remove_edge(rEdge[0], rEdge[1])
                copyG = GTriplePrime.copy()
                bfMin = []
            else:
                break
        p3 = nx.dijkstra_path_length(GTriplePrime, source=s, target=t, weight='weight')

    # 3rd Alg BIG CHUNGUS

    GQuadPrime = G.copy()
    copyG = G.copy()
    c, k = numNodesCalc(numNodes)
    removedC4 = []
    removedK4 = []
    can_continue = True
    num_eliminated_vertices = 0
    while can_continue:
        spDeg = maxDegList(GQuadPrime, s, t)
        flag = True
        if spDeg == []:
            flag = False
            can_continue = False
        while flag:
            maxDegNode = max(spDeg, key=lambda x: x[1])
            copyG.remove_node(maxDegNode[0])
            if nx.is_connected(copyG) and maxDegNode[0] != 0 and maxDegNode[0] != G.order() - 1:
                GQuadPrime.remove_node(maxDegNode[0])
                removedC4.append(maxDegNode[0])
                num_eliminated_vertices += 1
                flag = False
            else:
                spDeg.remove(maxDegNode)
                copyG = GQuadPrime.copy()
            if spDeg == []:
                flag = False
                can_continue = False
            if num_eliminated_vertices >= c:
                flag = False
                can_continue = False
    copyG = GQuadPrime.copy()
    can_continue = True
    num_eliminated_edges = 0
    while can_continue:
        spEdge = bestEdgeList(GQuadPrime, s, t)
        flag = True
        if spEdge == []:
            flag = False
            can_continue = False
        while flag:
            minEdge = max(spEdge, key=lambda x: x[1])
            copyG.remove_edge(*minEdge[0])
            if nx.is_connected(copyG):
                GQuadPrime.remove_edge(*minEdge[0])
                removedK4.append(minEdge[0])
                num_eliminated_edges += 1
                flag = False
            else:
                spEdge.remove(minEdge)
                copyG = GQuadPrime.copy()
            if spEdge == []:
                flag = False
                can_continue = False
            if num_eliminated_edges >= k:
                flag = False
                can_continue = False

    # 4th Alg
    max_path = 0
    removedC5 = []
    removedK5 = []
    if k == 15:
        GPentaPrime = G.copy()
        c, k = numNodesCalc(numNodes)
        (removedC5, removedK5, max_path) = analyze_graph(GPentaPrime, t, c, k)

    p1 = nx.dijkstra_path_length(GPrime, source=s, target=t, weight='weight')
    p2 = nx.dijkstra_path_length(GDoublePrime, source=s, target=t, weight='weight')
    p4 = nx.dijkstra_path_length(GQuadPrime, source=s, target=t, weight='weight')
    p5 = max_path

    if p1 == max(p1, p2, p3, p4, p5):
        return (removedC, removedK)
    elif p2 == max(p1, p2, p3, p4, p5):
        return (removedC2, removedK2)
    elif p3 == max(p1, p2, p3, p4, p5):
        return (removedC3, removedK3)
    elif p4 == max(p1, p2, p3, p4, p5):
        return (removedC4, removedK4)
    elif p5 == max(p1, p2, p3, p4, p5):
        return (removedC5, removedK5)
    return (removedC, removedK)

def numNodesCalc(numNodes):
    c = 0
    k = 0
    if numNodes <= 30 and numNodes >= 20:
        k = 15
        c = 1
    elif numNodes <= 50 and numNodes >= 31:
        k = 50
        c = 3
    elif numNodes <= 100 and numNodes >= 51:
        k = 100
        c = 5
    return (c, k)

def maxDegList(G, s, t):
    node_centrality = nx.betweenness_centrality_subset(G, sources=[s], targets=[t], weight="weight")
    return list(node_centrality.items())

def bestEdgeList(G, s, t):
    edge_centrality = nx.edge_betweenness_centrality_subset(G, sources=[s], targets=[t], weight="weight")
    return list(edge_centrality.items())

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

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs2/foo.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/*')
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
