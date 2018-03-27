from mininet.topo import Topo
from mininet.util import irange
from mininet.cli  import CLI
from mininet.net import Mininet
from mininet.net import Node
from mininet.node import IVSSwitch
from mininet.node import OVSKernelSwitch, Controller, RemoteController, Host
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import csv

with open('topology_data/try_20.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        print ', '.join(row)

# def parse_file():
line_list = []
with open('topology_data/try_20.csv') as f:
    for each_line in f:
        if each_line[0] == '#':
            print(each_line)
            continue
        elif each_line == 'c\n':
            break
        else:
            a = each_line.split(",")
            line_list.append(a)
            print(a)
bottom_start_id = int(line_list[0][0])
switch_num = int(line_list[0][1])
bandwidth = int(line_list[0][2])
print(line_list)

def runNet():
    "Create and run the network"
    info( "*** Starting network\n" )
    # topo = custom_topo()
    net = Mininet( topo = None, build=False, ipBase='10.0.0.0/16' )
#     c1 = Controller( 'c0', port=6633 )
#     net.addController( controller = c1)
    info( '*** Adding controller\n' )
    c0 = net.addController(name = 'c0', controller = Controller, protocol='tcp', port = 6633)

    info( '*** Add switches\n')
    for i in line_list[1:switch_num+1]:
#             info( "*** Creating hosts\n" )
        s = net.addSwitch("s"+i[0], cls=OVSKernelSwitch)
        switch_node_list.append(s)
        print("s"+i[0])
#         step = 0
        if(int(i[0]) >= bottom_start_id):
            info( '*** Add hosts\n')
            h = net.addHost("h"+i[0]+str(1), cls=Host, defaultRoute=None, ip='10.0.0.'+i[0])
            host_node_list.append(h)
            print("h"+i[0]+str(1))
    print('Length of switch_node_list', len(switch_node_list))
#    print('Length of host_node_list', len(host_node_list))

#     host_node_list = [[0 for i in range(3)] for j in range(bottom_start_id, switch_num+1)]
#     for i in line_list[bottom_start_id:switch_num+1]:
#         for index_outer, element_outer in enumerate(host_node_list):
#             for index_inner, element_inner in enumerate(element):
#                 h = net.addHost("h"+i[0]+str(index_inner+1), cls=Host, defaultRoute=None)
#                 element_inner = h

    info( '*** Add links\n')
    for i in line_list[switch_num+1:]:
#             info( "*** Adding links\n" )
#             print(i[0])
        net.addLink(switch_node_list[int(i[0])], switch_node_list[int(i[1])])
        print("s"+str(int(i[0])), "s"+str(int(i[1])))

    for i, element in enumerate(line_list[bottom_start_id+1:switch_num+1]):
        net.addLink(switch_node_list[int(element[0])], host_node_list[i])
        print("s"+element[0], "h"+ str(i+20))

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    for x in range(40):
        input_switch = 's' + str(x)
        net.get(input_switch).start([c0])
        print(input_switch, '  Starting')

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    list_node = []
    list_link = []
    host_node_list = []
#     test = [[0 for i in range(m)] for j in range(n)]
#     host_node_list.append([])
#     host_node_list.append([])
    switch_node_list = []
    runNet()
