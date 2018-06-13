import networkx as nx
import matplotlib.pyplot as plt

def InterAS(G, DictGWs):
	# Input: 
	# G is the graph object
	# DictGWs is a dictionary object {ASnumber: [corrosponding gateway nodes id]}
	# Output: 
	# GW, a graph object in which the gateways have attribute ['InterTable']
	# The type of 'InterTable' is dictionary, {ASnumber: path}
	# where path is the shortest path of each gateway to theAS

	# AS is a list object [ASnumber].
	AS = list(DictGWs.keys())

	# Compute the InterTable for gateways in ASi
	for i in AS:
		gatewayfori = DictGWs[i]
		# Here j is the jth gateway in ASi
		for j in gatewayfori:
			# Compute the InterTable for jth gateway in ASi
			InterTableforj = {}
			for k in AS:
				if k != i:
					gatewayfork = DictGWs[k]
					lengthtogateway = []
					corrosgatewayid = []
					# Here l is the lth gateway in ASk
					for l in gatewayfork:
						lengthtogateway.append(nx.shortest_path_length(G, source = j, target = l))	
						corrosgatewayid.append(l)
					# Find the shortest path for j to ASk
					index = lengthtogateway.index(min(lengthtogateway))
					InterTableforj[k] = nx.shortest_path(G, source = j, target = corrosgatewayid[index])
			G.add_node(j, InterTable = InterTableforj)
'''test
DictGWs = {'1': [11,12,13], '2':[21,22,23],'3':[31,32], '4':[41,42,43,44]}
AS = ['1','2','3','4']
node = [11,12,13,21,22,23,31,32,41,42,43,44]
edge = [(11,21), (12,23), (22,41),(42,32),(21,31),(13,43),(32,44)]
edgeinside = [
	(11, 12), (12, 13), (21,22), (22,23), (21, 23), (31,32), (41,42), (41,43),(43,44)
]
GW = nx.Graph()
GW.add_nodes_from(node)
GW.add_edges_from(edge)
GW.add_edges_from(edgeinside)
InterAS(GW, DictGWs)
print(GW.nodes[11])
print(GW.nodes[11]['InterTable']['4'], GW.nodes[11]['InterTable']['3'], GW.nodes[11]['InterTable']['2'])
nx.draw(GW, with_labels=True, font_weight='bold')
plt.show()'''