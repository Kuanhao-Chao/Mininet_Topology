import markov_clustering as mc
import networkx as nx
import csv
from cmty import buildG
import sys
import matplotlib.pyplot as plt

# Cluster_rate determine how big the cluster are. Recommend value: 1.1 ~ 1.9
# 
def graph_clustering(graph,cluster_rate = 1.5, draw = False):
    AS_Num = 0
    n_Matrix = nx.to_scipy_sparse_matrix(graph)
    result = mc.run_mcl(n_Matrix,inflation = cluster_rate)
    clusters = mc.get_clusters(result)
    #print("Number of clusters: " + str(len(clusters)))
    graph.graph['Total_AS'] = len(clusters)
    for c in clusters:
        for n_id in c:
            graph.add_node(n_id,AS_N = AS_Num)
        AS_Num += 1
    if(draw):
        mc.draw_graph(n_Matrix, clusters,
        node_size=10, with_labels=False, edge_color="black",width=0.2)
        plt.show()


