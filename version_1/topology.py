from mininet.topo import Topo
from mininet.util import irange
from mininet.cli  import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.log import setLogLevel, info

# info( "*** Creating (reference) controllers\n" )
# c1 = net.addController( 'c1', port=6633 )
# c2 = net.addController( 'c2', port=6634 )

def parseFile():
    line_number = 1
    with open('connection_data_100.csv') as f:
        for each_line in f:
            if(line_number == 1):
#                 print(line_number)
                global list_node
                list_node = each_line.split()
                line_number += 1
#                 print(each_line)
            else:
#                 print(line_number)
                each_link = each_line.split()
                list_link.append(each_link)
                line_number += 1
#                 print(each_line)
#     print(list_node)          
#     print(list_link)

class custom_topo(Topo):
    "Configurable Datacenter Topology"
    
    def build(self):
        global host_node_list
        global switch_node_list
        global list_link

        flag = True
        for i in list_node:
            for j in i:
                if(j == 'h'):
                    host_node_list.append(i)
                    print(i)
                    flag = False
                    break
            if(flag == True):
                switch_node_list.append(i)
#                 print(i)
        print(host_node_list)
        print(switch_node_list)
        
        for i in host_node_list:
#             info( "*** Creating switches\n" )
            self.addHost(i)
        for i in switch_node_list:
#             info( "*** Creating hosts\n" )
            self.addSwitch(i)
        for x in list_link:
#             info( "*** Adding links\n" )
            self.addLink(x[0], x[1])
            print(x)

def runNet():
    "Create and run the network"
    info( "*** Starting network\n" )
    topo = custom_topo()
    net = Mininet( topo = topo, controller=Controller, switch=OVSSwitch, )
    net.start()
    CLI(net)
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    list_node = []
    list_link = []
    host_node_list = []
    switch_node_list = []
    
    parseFile()
#     print(list_node)          
#     print(list_link)
    runNet()