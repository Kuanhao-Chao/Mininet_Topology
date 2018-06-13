import networkx as nx
import InterAS as InterAS
import IntraAS as IntraAS
import matplotlib.pyplot as plt
import project_utility as pu
import mcl as mcl 
import time

def recursive(G,start,dest, path):
	next = G.nodes[start]['IntraTable'][dest]
	path.append(next)
	if(next != dest):
		recursive(G,next,dest, path)

def pathfinding(SourceNodeID, DestNodeID, G):
	# The source and dest are in defferent ASes
	path = [SourceNodeID]
	if G.nodes[SourceNodeID]['AS_N'] != G.nodes[DestNodeID]['AS_N']:
		# Finf the gateway level path, GWpath
		# If the source is nongateway, send the packet to the default gateway first
		if G.nodes[SourceNodeID]['isGateway'] == False:
			path.append(G.nodes[SourceNodeID]['DefaultGateway'])
			GWpath = G.nodes[G.nodes[SourceNodeID]['DefaultGateway']]['InterTable'][str(G.nodes[DestNodeID]['AS_N'])]
		else:
			GWpath = G.nodes[SourceNodeID]['InterTable'][str(G.nodes[DestNodeID]['AS_N'])]
		
		# Complete the path in the GWpath
		for i in range(len(GWpath)-1):
			# If the adjacent nodes in GWpath has different ASnumber-->InterAS, has direct link
			if G.nodes[GWpath[i]]['AS_N'] != G.nodes[GWpath[i+1]]['AS_N']:
				path.append(GWpath[i+1])
			# If the adjacent nodes in GWpath has same ASnumber-->IntraAS
			# Utilize the path stored in ['LogicalEdge'] except the first element which have stored in the path
			else:
				path.extend(G.edges[(GWpath[i], GWpath[i+1])]['LogicalEdge'][1:])
		# Complete the path from the gateway to the dest
		if GWpath[-1] != DestNodeID:
			recursive(G, GWpath[-1], DestNodeID, path)

	# The source and dest are in the same AS
	else:
		# Both the source and dest are gateways
		if (G.nodes[SourceNodeID]['isGateway'] == True) and (G.nodes[DestNodeID]['isGateway'] == True):
			path = G.edges[SourceNodeID,DestNodeID]['LogicalEdge']
		else:
			recursive(G, SourceNodeID, DestNodeID, path)
	return path

def TableSetup(G, filename):
	pu.buildG(G, filename)
	mcl.graph_clustering(G)
	pu.get_gateway(G)
	DictGWs = G.graph['gateWayList']
	AS = list(DictGWs.keys())
	# Construct the IntraTable for each AS. 
	# Here, i is str
	for i in AS:
		nodesinASi = []
		# Find the nodes in ASi
		for j in list(G.nodes):
			if str(G.nodes[j]['AS_N']) == i:
				nodesinASi.append(j)
		IntraAS.IntraAS(G, i, nodesinASi, DictGWs)
	# Construct the InterTable
	InterAS.InterAS(G, DictGWs)



'''test'''
G = nx.Graph()
timestamp1 = time.time()
TableSetup(G, '2018-5-30-69nodes_links.csv')
timestamp2 = time.time()
print ("This took %.2f seconds" % (timestamp2 - timestamp1))
# print(G.graph['gateWayList'])
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()
# gateway to gateway
# print(pathfinding(29, 22, G))
# gateway to nongateway
# print(pathfinding(29, 58, G))
# nongateway to gateway
# print(pathfinding(52, 13, G))
# nongateway to nonegateway
# print(pathfinding(52, 68, G))
print(G.nodes[4])
print(G.nodes[53])
print(pathfinding(4, 53, G))