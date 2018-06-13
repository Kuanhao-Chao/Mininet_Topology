import TableSetup2 as tbl
import networkx as nx 

G = nx.Graph()
tbl.TableSetup(G, '2018-5-30-302nodes_links.csv')
print("****** Creating all route for every router")
print(tbl.pathfinding(2,256,G))
print(list(G.nodes))
print(list(G.edges))
print(G.nodes[1])