import numpy
import random
import time
import datetime
import project_utility as ut
def generate_Connection(Data,layers):
   
   # Variables
    print("Connection generation starting...")
    # Layer 1-1
    for i in range(1,len(layers[1])):
        dis = layers[1][0].distance(layers[1][i]) 
        closest = 0
        minDis = 0
        for j in range(i - 1):
            if j == 0:
                minDis = layers[1][j].distance(layers[1][i])
            dis = layers[1][j].distance(layers[1][i]) 
            if minDis > dis:
                minDis = dis
                closest = j   

        layers[1][closest].deg += 1
        layers[1][i].deg+=1
        Data.connections['1-1,1'].append(layers[1][closest])
        Data.connections['1-1,2'].append(layers[1][i])
        for j in range(i-1):
            if (j != closest):
                pro = random.uniform(0, 1)
                if dis == 0:
                    dis = 1
                if pro < Data.con_Para['1,1']*(layers[1][j].deg**Data.deg_Para['1,1'])/(dis**Data.con_Dispara['1,1']): # This is where you need to read, see how the parameter affects the connection.
                    layers[1][i].deg += 1
                    layers[1][j].deg += 1
                    Data.connections['1-1,1'].append(layers[1][i])
                    Data.connections['1-1,2'].append(layers[1][j])
                 
    
    for layer in range(1,Data.Layer_Num):
        ### Connection between layer_i and layer_i+1
        key1 = str(layer) + ',' + str(layer + 1)
        key2 = str(layer + 1) + ',' + str(layer + 1)
        for node_i in layers[layer]:
            for node_j in layers[layer + 1]:
                dis = node_i.distance(node_j)
                pro = random.uniform(0, 1)
                if dis == 0:
                    dis = 1
                if pro < (Data.con_Para[key1]*(node_i.deg**Data.deg_Para[key1])/(dis**Data.con_Dispara[key1])):
                    node_i.deg += 1
                    node_j.deg += 1
                    node_i.target.append(node_j), node_j.target.append(node_i)
                    Data.connections[str(layer) + '-' + str(layer + 1) + ',1'].append(node_i)
                    Data.connections[str(layer) + '-' + str(layer + 1) + ',2'].append(node_j)
                    if (node_i.connected == 1):
                        node_j.connected = 1
                 
        ### Connection between layer_i+1 and layer_i+1
        for i in range(len(layers[layer + 1])):
            for j in range(i + 1,len(layers[layer + 1])):
                node_i = layers[layer + 1][i]
                node_j = layers[layer + 1][j]
                dis = node_i.distance(node_j) 
                if dis == 0:
                    dis = 1
                pro = random.uniform(0, 1)
                if (pro < Data.con_Para[key2]*(node_j.deg**Data.deg_Para[key2])/(dis**Data.con_Dispara[key2])):
                    node_j.deg += 1
                    node_i.deg += 1
                    node_i.target.append(node_j), node_j.target.append(node_i)
                    Data.connections[str(layer + 1) + '-' + str(layer + 1) + ',1'].append(node_i)
                    Data.connections[str(layer + 1) + '-' + str(layer + 1) + ',2'].append(node_j)
                    if (node_i.connected == 1 and node_j.connected == 0):
                        node_j.connected = 1
                        node_j.net()
                    if (node_j.connected == 1 and node_i.connected == 0):
                        node_i.connected = 1
                        node_i.net()

    # Removing isolated nodes
    # Delete the nodes that aren't in the graph
    n_total = []
    for layer in layers:
        n_total += layer
    ut.delete_unconnected_new_mapping(n_total)
    node_count = 0
    for node in n_total:
        if(node.ID != -10):
            node_count += 1

    # I/O, You don't need to read them.
    # Writing connection data to csv
    file = open(Data.output_Path + str(Data.graph_Name) + ".csv",'w')
    s_connect = ""

    # Links
    key = str(1) + '-' + str(1)
    for i in range(len(Data.connections[key + ',1'])):
        if (Data.connections[key + ',1'][i].ID != -10): # if the first node is in graph, the second one must be too.
            s_connect += str(Data.connections[key + ',1'][i].ID) + ',' + str(Data.connections[key + ',2'][i].ID) + '\n'
    for i in range(1,Data.Layer_Num):
        key = str(i) + '-' + str(i+1)
        for j in range(len(Data.connections[key + ',1'])):
            if (Data.connections[key + ',1'][j].ID != -10):
                s_connect += str(Data.connections[key + ',1'][j].ID) + ',' + str(Data.connections[key + ',2'][j].ID) + '\n'
                Data.connection_Num[str(i) + ',' + str(i+1)] += 1
        key = str(i+1) + '-' + str(i+1)
        for j in range(len(Data.connections[key + ',1'])):
            if (Data.connections[key + ',1'][j].ID != -10):
                s_connect += str(Data.connections[key + ',1'][j].ID) + ',' + str(Data.connections[key + ',2'][j].ID) + '\n'
                Data.connection_Num[str(i+1) + ',' + str(i+1)] += 1

    # Parameters
    count = 0
    s = "# Created at " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n'
    file.write(s)
    s = "# Connection parameters." + "\n# Layer1-1:" + str(Data.con_Para['1,1'])
    count += 1
    for layer in range(1,Data.Layer_Num):
        s += " Layer" + str(layer) + '-' + str(layer + 1) + ':'  + str(Data.con_Para[str(layer) + ',' + str(layer + 1)])
        count += 1
        if (count >= 3):
            count = 0
            s += '\n' + "#"
        s += " Layer" + str(layer + 1) + '-' + str(layer + 1) + ':'  + str(Data.con_Para[str(layer + 1) + ',' + str(layer + 1)])
        count += 1
    file.write(s)
    count = 0
    s = '\n' + "# Connection Num." + "\n# Layer1-1:" + str(len(Data.connections['1-1,1']))  
    for layer in range(1,Data.Layer_Num):
        s += (" Layer" + str(layer) + '-' + str(layer + 1) + ':' + str(Data.connection_Num[str(layer) + ',' + str(layer + 1)]))
        count += 1
        if (count >= 3):
            count = 0
            s += '\n' + "#"
        s += (" Layer" + str(layer + 1) + '-' + str(layer + 1) + ':' + str(Data.connection_Num[str(layer + 1) + ',' + str(layer + 1)]))
        count += 1
    file.write(s)
    s = '\n' + "# Lowest level starting ID, total switch number\n"
    file.write(s)
    s = str(len(layers[1])) + ',' + str(node_count) + '\n'
    file.write(s)
    s = "# NodeID, x_pos, y_pos, degree\n"
    file.write(s)

    # Node info
    for layer in layers:
        for node in layer:
            if (node.ID != -10):
                s = str(node.ID) + ',' + str(node.x_pos) + ',' + str(node.y_pos) + ',' + str(node.deg) + '\n'
                file.write(s)
            

    # Outputing links to another file for graph clustering
    file2 = open(Data.output_Path + str(Data.graph_Name) + "_links" + ".csv",'w')
    s = "# links\n"
    file.write(s)
    file2.write(str(node_count) + '\n')
    file2.write(s_connect)
    s_connect += 'c'
    file.write(s_connect)
    return n_total