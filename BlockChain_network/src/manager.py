import csv
import random
import time
from decimal import Decimal
import project_utility as pu
import connection
import os
#from configuration import *

class Manager:
    #def __init__(self):
    #   self = self
    def __init__(self):
        self.data = pu.Data()
    
    def set_Configuration(self, outputPath = "", graphName = "", disPara = [], genDisPara = {},
                          nodeGenPara = -1, layerNodeNum = [], layerNum = -1, conDegPara = {}, conDisPara = {}, conPara = {}):
        if (layerNum != -1):
            if (layerNum < 2):
                raise RuntimeError("Invalid layer Number!")
                
            else:
                self.data.Layer_Num = layerNum
        
        if (nodeGenPara != -1):
            self.node_Gen_Para = nodeGenPara

        if (graphName != ""):
            self.data.graph_Name = graphName

        if (outputPath != ""):
            self.data.output_Path = outputPath
        
        if (len(genDisPara) != 0):
            self.data.gen_Dispara = dict(genDisPara)
        else:
            for i in range(2,self.data.Layer_Num + 1):
                self.data.gen_Dispara[str(i)] = 2

        if (len(conPara) != 0):
            self.data.con_Para = dict(conPara)
        
        if (len(conDegPara) != 0):
            self.data.deg_Para = dict(conDegPara)
        else:
            for i in range(1,self.data.Layer_Num + 1):
                self.data.deg_Para[str(i) + ',' + str(i)] = 1
                if (i != self.data.Layer_Num):
                    self.data.deg_Para[str(i) + ',' + str(i + 1)] = 1

        if (len(conDisPara) != 0):
            self.data.con_Dispara = dict(conDisPara)
        else:
            for i in range(1,self.data.Layer_Num + 1):
                self.data.con_Dispara[str(i) + ',' + str(i)] = 1
                if (i != self.data.Layer_Num):
                    self.data.con_Dispara[str(i) + ',' + str(i + 1)] = 1

        for i in range(1,self.data.Layer_Num + 1):
            self.data.connection_Num[str(i) + ',' + str(i)] = 0
            if (i != self.data.Layer_Num):
                self.data.connection_Num[str(i) + ',' + str(i + 1)] = 0
        for i in range(1,self.data.Layer_Num + 1):
            self.data.connections[str(i) + '-' + str(i) + ',1'] = []
            self.data.connections[str(i) + '-' + str(i) + ',2'] = []
            if (i != self.data.Layer_Num):
                self.data.connections[str(i) + '-' + str(i + 1) + ',1'] = []
                self.data.connections[str(i) + '-' + str(i + 1) + ',2'] = []
        
        if (len(layerNodeNum) != 0):

            if (len(layerNodeNum) > self.data.Layer_Num):
                raise RuntimeError("Invalid layerNodeNum, too many arugment!")
            
            

            elif(len(layerNodeNum) < self.data.Layer_Num):
                raise RuntimeError("Invalid layerNodeNum, missing arugment!")
              
            else:
                if(layerNodeNum[0] > 50):
                    raise RuntimeError("layer one can only have upto 50 nodes!")
                buflist = list(layerNodeNum)
                buflist.insert(0,-1)
                self.data.layer_Node_Num = list(buflist)
      
        
    ### TODOs
    def print_Configuration(self):
        
        print("\nConfigurations")
        print("Layer_Num",self.data.Layer_Num)
        print("output_Path",self.data.output_Path)
        print("graph_Name",self.data.graph_Name)
        print("con_Para",sorted(self.data.con_Para.items()))
        print("deg_Para",sorted(self.data.deg_Para.items()))
        print("con_Dispara",sorted(self.data.con_Dispara.items()))
        print("node_Gen_Para",self.data.node_Gen_Para)
        print("gen_Dispara",sorted(self.data.gen_Dispara.items()))
        print("layer_Node_Num",self.data.layer_Node_Num[1:])

    def Visualize_Graph_(self):
        print("Visualizing graph....") # Future version will include this function


    def generate_Graph(self):
        timeStart = time.time()
        print('Node generation starting...')
        # Variable definition
        layerNode = []
        for i in range(self.data.Layer_Num + 1):
            layerNode.append([])
        ID_count = 0

        # 1.Generate node
        ## 1-1 First Layer

        for i in range(self.data.layer_Node_Num[1]):
            node = pu.Node(ID_Num = ID_count)
            layerNode[1].append(node)
            node.connected = 1 # Layer_1 nodes will always be in the graph (check connection.py)
            ID_count += 1

        CSV = csv.reader(open('1layer.csv'),delimiter = ',')
        count = 0
        for row in CSV:
            node = layerNode[1][count]
            count += 1
            node.x_pos = int(row[1])
            node.y_pos = int(row[0])
            if (count == self.data.layer_Node_Num[1]): # Can only have up to 50 layer1_Nodes
                break

        # For debugging
        for node in layerNode[1]:
            print(node.x_pos,node.y_pos)

        ## 1-2 Generate Second Layer
        ### Read Continent info
        cont_List = []
        CSV = csv.reader(open('continent.csv'),delimiter = ',')
        for row in CSV:
            buf_list = [row[0],row[1],row[2],row[3]] #(x1,y1,x2,y2) four points, not sure if that is the order, check project_utility.py
            cont_List.append(buf_list)

        ### Generate nodes
        for layer in range(2,self.data.Layer_Num + 1):
            previous_layer = layer - 1
            while(len(layerNode[layer]) != self.data.layer_Node_Num[layer]): # Run loop until the required number of nodes is generated
                (x,y) = pu.map_Cordinate_Generator(continent_List = cont_List) # Returns a (x,y) that is in the restricted area
                node = pu.Node(ID_Num = ID_count,x_pos = x, y_pos = y)
                Sum = 0
                for node_p in layerNode[previous_layer]:
                    if(node.distance(node_p) != 0):
                        dis_r = 1/node.distance(node_p)
                    else:
                        dis_r = 1 # Just to avoid bug
                    Sum += dis_r ** self.data.gen_Dispara[str(layer)] # Use the total average distance
                pro = random.uniform(0, 1)
                if (pro < self.data.node_Gen_Para*Sum): # node_Gen_Para controls the speed of generating nodes. Don't set too large values
                    layerNode[layer].append(node)      
                    ID_count += 1
        timeEnd = time.time()
        print("Node generation time used: " + str(round(timeEnd - timeStart,2)) + " seconds")
        ### Generate Connection
        n_total = connection.generate_Connection(Data = self.data,layers = layerNode)
        print("Connection generation time used: " + str(round(time.time() - timeEnd,2)) + " seconds")
        ### Calculate dimension
        dim = pu.dimension_calculation(n_total,(3600,1800),5,360.0,5,2)
        dim = round(dim,3)
        print("Graph dimension: " + str(dim))

        timeEnd = time.time()
        print("Total time used: " + str(round(timeEnd - timeStart,2)) + " seconds")
        