
import random

def generateFile(num_vertices):
    edges = set()
    f = open(str(num_vertices) + ".in", "a")
    f.write(str(num_vertices) + "\n")

    for vertex in range(num_vertices - 1):
        edges.add((vertex, vertex + 1))

    for vertex in range(num_vertices):
        num_incoming_edges = random.randint(1, num_vertices // 10)
        num_outgoing_edges = random.randint(1, num_vertices // 10)

        curr_incoming_edges = 0
        while curr_incoming_edges < num_incoming_edges:
            in_vertex = random.randint(0, num_vertices - 1)
            if in_vertex != vertex:
                edge = (in_vertex, vertex)
                if edge not in edges:
                    edges.add(edge)
                    curr_incoming_edges += 1

        curr_outgoing_edges = 0
        while curr_outgoing_edges < num_outgoing_edges:
            out_vertex = random.randint(0, num_vertices - 1)
            if out_vertex != vertex:
                edge = (vertex, out_vertex)
                if edge not in edges:
                    edges.add(edge)
                    curr_outgoing_edges += 1

    for edge in edges:
        weight = round(random.uniform(1, 100), 3)
        f.write(str(edge[0]) + " " + str(edge[1]) + " " + str(weight) + "\n")


generateFile(25)
generateFile(45)
generateFile(95)
