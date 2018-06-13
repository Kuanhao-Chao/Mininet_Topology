import random
import numpy as np
import csv

# Node represents a connected device in the internet, ex: router
class Node:
    
    def __init__(self,ID_Num,x_pos = 0,y_pos = 0):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.deg = 0
        self.target = []   # Node connected to this node 
        self.connected = 0 # If 1 means this node is in the graph, else it is out of the graph.
        self.ID = ID_Num
    
    # Calculate Distance between two nodes
    def distance(self,other_Node):
        delta_x = abs(self.x_pos - other_Node.x_pos)
        # Earth is round, y cordinate is not considered, since it goes across the polar area.
        if (delta_x > 18000):
            delta_x = 36000 - delta_x
        return ((delta_x)**2 + (self.y_pos - other_Node.y_pos)**2)**0.5
    
    # Set the target node's connected flag to true, recursively called.
    # A node being connected means that it is directly or indirectly connected to 
    # the layer_1 nodes.
    def net(self):
        for node in self.target:
            if node.connected == 0:
                node.connected = 1
                node.net()
# The class for storing configurations.
# Set with some default values
class Data:
    def __init__(self):
        self.Layer_Num = 2
        self.output_Path = "./"
        self.graph_Name = "testing_v3"
        self.con_Para = {}
        self.con_Para['1,1'] = 75
        self.con_Para['1,2'] = 6
        self.con_Para['2,2'] = 10
        self.deg_Para = {}
        for i in range(1,self.Layer_Num + 1):
            self.deg_Para[str(i) + ',' + str(i)] = 1
            if (i != self.Layer_Num):
                self.deg_Para[str(i) + ',' + str(i + 1)] = 1
        self.con_Dispara = {}
        for i in range(1,self.Layer_Num + 1):
            self.con_Dispara[str(i) + ',' + str(i)] = 1
            if (i != self.Layer_Num):
                self.con_Dispara[str(i) + ',' + str(i + 1)] = 1
        self.gen_Dispara = {}
        for i in range(2,self.Layer_Num + 1):
            self.gen_Dispara[str(i)] = 1.5
        self.node_Gen_Para = 100
        self.layer_Node_Num = [-1] * (self.Layer_Num + 1)
        for i in range(1,self.Layer_Num + 1):
            self.layer_Node_Num[i] = 20*(5*i - 4)
        self.connections = {}
        self.connection_Num = {}
        for i in range(1,self.Layer_Num + 1):
            self.connection_Num[str(i) + ',' + str(i)] = 0
            if (i != self.Layer_Num):
                self.connection_Num[str(i) + ',' + str(i + 1)] = 0
        for i in range(1,self.Layer_Num + 1):
            self.connections[str(i) + '-' + str(i) + ',1'] = []
            self.connections[str(i) + '-' + str(i) + ',2'] = []
            if (i != self.Layer_Num):
                self.connections[str(i) + '-' + str(i + 1) + ',1'] = []
                self.connections[str(i) + '-' + str(i + 1) + ',2'] = []
             

# Just a class for the function map_Cordinate_Generator(continent_List)
class Region:
    def __init__(self,y1_pos,x1_pos,y2_pos,x2_pos):
        self.x1 = x1_pos
        self.y1 = y1_pos
        self.x2 = x2_pos
        self.y2 = y2_pos
        self.area = abs(x1_pos - x2_pos) * abs(y1_pos - y2_pos)
    Regions = [] # Static, can be seen as a global variable within the class.
    sum = 0 # Static

def map_Cordinate_Generator(continent_List):
    if (len(Region.Regions) == 0): # Read the continent_List if it haven't yet.
        for list in continent_List:
            region = Region(int(list[0]),int(list[1]),int(list[2]),int(list[3]))
            Region.Regions.append(region)
        
        for region in Region.Regions:
            Region.sum += region.area # Sum up the Region area

    pro = random.randrange(0,Region.sum)
    sum_buf = 0
    # the probability is directly proportional to the continent's area
    for region in Region.Regions:
        if (sum_buf <= pro < sum_buf + region.area):
            x = random.randrange(region.x1,region.x2)
            y = random.randrange(region.y2,region.y1)
            return (x,y)
        sum_buf += region.area

# Just changes the ID mapping, not important, You can ask Pohan for the concept.
def delete_unconnected_new_mapping( node_array ): # Input is an array of nodes
    node_mapping = []
    length = len(node_array)
    for j in range(length):
        node_mapping.append(j)
    for i in range(length):
        if node_array[i].connected == 0:
            node_mapping[i] = -10 # Set the iD to -10 if the node is not in the graph.
                                  # -10 doesn't have any special meaning
            for j in range(i+1,length):
                node_mapping[j] = node_mapping[j] -1
    for i in range(length):
        node_array[i].ID = node_mapping[i]

def dimension_calculation(image, image_size,unit, initial_box_size, number_of_linear_regression, scale):
    # image would be a list of object(node)
    # suggest setting initial_box_soze to be 1/100 of image_size, unit = 1
    # unit is the unit for transforming the image from point format to pixel format
    b = initial_box_size
    q = number_of_linear_regression
    (m,n) = image_size
    
    # Build successive box sizes, 1/10 smaller
    sizes = b/(scale**np.arange(0,q,1))
    
    # Extract the positions of image
    image_pos = []
    for i in image:
        image_pos.append([i.x_pos/10 + 1800,i.y_pos/10 + 900])
    
    # Transform the point graph to pxiel image where 1 means existing point
    (px,py) = (int(m/unit), int(n/unit))
    pixel_image = np.zeros((px+1,py+1))
    for i in image_pos:
        bx = int(i[0]/unit)
        by = int(i[1]/unit)
        pixel_image[(bx,by)] = 1
    # The positions of pixels at where points exist
    points = np.transpose(np.nonzero(pixel_image))*unit
    
    # Count the number of boxes
    def box_count(image,k): # z is the image and k is the box size
        (nx,ny) = (int(m/k), int(n/k))
        boxcount = np.zeros((nx+1,ny+1))
        for i in points:
            ppx = int(i[0]/k)
            ppy = int(i[1]/k)
            boxcount[(ppx,ppy)] = 1
        return np.count_nonzero(boxcount)

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(box_count(image_pos, size))
    # Calculate the dimension with linear regression
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]

#construct the weighted version of the contact graph from the input file
#First line in the file must be the number of nodes in the graph
#Other lines are the links
#link format: node_id1,node_id2,weight or node_id1,node_id2 (weight = 1)
def buildG(G, file_name, delimiter_=','):   
    reader = csv.reader(open(file_name), delimiter=delimiter_)
    for line in reader:
        if len(line) > 2:
            if float(line[2]) != 0.0:
                #line format: u,v,w
                G.add_edge(int(line[0]),int(line[1]),weight=float(line[2]))
        elif len(line) == 2:
            #line format: u,v
            G.add_edge(int(line[0]),int(line[1]),weight=1.0)
        else:
            for i in range(int(line[0])):
                G.add_node(i)
### gets the gateway router in different AS, must run mcl.graph_clustering first.
def get_gateway(G):
    G.graph['gateWayList'] = {}
    for i in range(G.graph['Total_AS']):
        G.graph['gateWayList'][str(i)] = set()
    for e in G.edges():
        if(G.node[e[0]]['AS_N'] != G.node[e[1]]['AS_N']):
            G.add_node(e[0],isGateway = True)
            G.add_node(e[1],isGateway = True)
            G.graph['gateWayList'][str(G.node[e[0]]['AS_N'])].add(e[0])
            G.graph['gateWayList'][str(G.node[e[1]]['AS_N'])].add(e[1])
        else:
            if((G.node[e[0]].get('isGateway')) == None):
                G.add_node(e[0],isGateway = False)
            if((G.node[e[1]].get('isGateway')) == None):
                G.add_node(e[1],isGateway = False)