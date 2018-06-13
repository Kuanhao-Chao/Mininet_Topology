import networkx as nx 
import matplotlib.pyplot as plt
import csv
import project_utility as pu 

G = nx.Graph()
node = [1, 2 ,3]
edge = [(1,2), (2,3)]
G.add_nodes_from(node)
G.add_edges_from(edge)
G.edges[1,2]['test'] = 'yes'
print(G.edges[1,2])

G1 = nx.Graph()
G1.add_edge(1,2)
G1.edges[1,2] = G.edges[1,2]
print(G1.edges[1,2])