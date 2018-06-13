from graph_tool.all import*
import numpy
import csv
import os
import sys

version = sys.argv[1]
first = True
flag = False
g = Graph(directed = False)
v = []
pos = g.new_vertex_property("vector<double>")

connection_CSV = csv.reader(open('connection_100_' + str(version) + '.csv'),delimiter = ',')
count = 0
flag = False
for row in connection_CSV:
    if (row[0] == "# links"):
        break
    elif (flag):
        v1 = g.add_vertex()
        v.append(v1)
        pos[g.vertex(count)] = (int(row[1])/10,int(row[2])/10)
        count += 1
    else:
        if (row[0] == "# NodeID"):
            flag = True

for row in connection_CSV:
    if (row[0] == 'c'):
        break
    elif (flag):
        e = g.add_edge(v[int(row[0])],v[int(row[1])])
    else:
        if (row[0] == "# links"):
            flag = True

deg = g.degree_property_map("total")
deg.a = deg.a**0.6 + 10

output_name = "two-nodes_" + str(version) + ".png"
graph_draw(g,vertex_size = deg,
vertex_fill_color=deg, output_size = (3600,1800),  output = output_name)

print("docker cp 1d306a674312:/home/user/" + output_name + " /Users/apple/Desktop/project/graph")

