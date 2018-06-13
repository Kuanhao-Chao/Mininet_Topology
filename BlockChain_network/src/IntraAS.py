import networkx as nx
import matplotlib.pyplot as plt

def IntraAS(G, ASnumber, nodesinthisAS, DictGWs):
	# Input: 
	# G is the input graph 
	# ASnumber is the ASnumber for this AS to find the gateway in this AS
	# nodeinthisAS is a list object containing the node id of all nodes in this AS
	# DictGWs is a dict object like {ASnumber: corrosponding gateways id}
	# Output: 
	# G, a graph object in networkx
	# The nongatwway nodes in G have attribute 'AS number', 'InterTable', and 'DefaultGateway'
	# 'InterTable' and 'DefaultGateway' will be created later
	# The gateway nodes in G have attribute 'AS number', 'InterTable', and 'IntraTable'
	# 'InterTable' will be created later
	# 'IntraTable' will be created by another function InterAS

	gateway = DictGWs[ASnumber]

	for i in nodesinthisAS:
		# Compute the shortest path for node i to the other nodes
		p = {}
		for j in nodesinthisAS:
			if j != i:
				p[j] = nx.shortest_path(G, source = i, target = j)
		
		lengthtogateway = []
		corrosgatewayid = []
		flag = (i in gateway)
		for j in p:
			# Check if node[i] is nongateway
			if flag == False:
				# Record the length of path of nongateway node[i] to each gateway
				if j in gateway:
					lengthtogateway.append(len(p[j])) 
					corrosgatewayid.append(j)

			# Construct the forwarding table for each node in the same AS
			# The type of the 'IntraTable' is dictionary {dest: next node id}
			if len(p[j]) != 1:
				p[j] = p[j][1]
			else:
				p[j] = p[j][0]
		G.add_node(i, IntraTable = p)
		# 'DefaultGateway' is the cloest (shortest path length) gateway for the node[i]
		if flag == False:
			index = lengthtogateway.index(min(lengthtogateway))
			G.add_node(i, DefaultGateway = corrosgatewayid[index])

'''test
node = [1,2,3,4,5,6,7,8,9,10]
edge = [(1,2),(1,3),(1,4),(3,5),(5,6),(6,9),(8,10),(2,3),(4,6),(3,7),(7,10),(6,10)]
G = nx.Graph()
G.add_nodes_from(node)
G.add_edges_from(edge)
DictGWs = {1: [2,8]}
IntraAS(G, 1, [2,3,5,8,10], DictGWs)
print(G.nodes[2], G.nodes[5], G.nodes[7])
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()'''