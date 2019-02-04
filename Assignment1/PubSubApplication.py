
import os, sys

import time
import threading

from BusTopology import BusTopology
from StarTopology import StarTopology
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import OVSController

def create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker):

    net = Mininet(topo=topo, link=TCLink, controller = OVSController)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()

    for host in net.hosts:
        if 'pub' in host.name:
            pub_list.append(host)
        elif 'sub' in host.name:
            sub_list.append(host)
        elif 'broker' in host.name:
            broker = host

    broker_IP = broker.IP()

    def call_broker():
        print("in call broker")
        broker.cmd('xterm -e python3 ZMQ_broker.py 5556 5557')
    def call_publisher(pub_command):
        print("in call broker")
        pub.cmd('xterm -e python ZMQ_publisher.py  ' + str(broker_IP) + str(pub_command))
    def call_subscriber(sub_command):
        print("in call subscriber")
        sub.cmd('xterm -e python ZMQ_subscriber.py  ' + str(broker_IP) + str(sub_command))

    threading.Thread(target=call_broker, args=()).start()
    time.sleep(3)
    for k, pub in enumerate(pub_list):
        threading.Thread(target=call_publisher(pub_command_list[k]), args=()).start()
        time.sleep(5)
    for k, sub in enumerate(sub_list):
        threading.Thread(target=call_subscriber(sub_command_list[k]), args=()).start()
        time.sleep(5)

    try :
        while True:
            pass
    except Exception as e:
        print(e)

    net.stop()

def get_input(file):

    file = open('./InputeFile/'+sys.argv[1])

    for line in file:
        if 'pub_num' in line:
            pub_num = int(line.split(':')[1])
        elif 'sub_num' in line:
            sub_num = int(line.split(':')[1])
        elif 'pub_command'in line:
            pub_command_list.append(str(line.split(':')[1].replace('\n','')))
        elif 'sub_command'in line:
            sub_command_list.append(str(line.split(':')[1].replace('\n','')))
        elif 'topo_type' in line:
            topo_type = str(line.split(':')[1].replace('\n','').replace(' ',''))

    # print(pub_num)
    # print(sub_num)
    # print(pub_command_list)
    # print(sub_command_list)
    # print(topo_type)

def main():
    get_input(sys.argv[1])
    if topo_type == 'bus':
        topo = BusTopology(pub_num,sub_num)
        create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
    elif topo_type == 'star':
        topo = StarTopology(pub_num,sub_num)
        create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
    else:
        exit("Could not find mached topology. 'bus' and 'star' are provided")

if __name__ == '__main__':
    pub_num = 3
    sub_num = 4
    topo_type = 'bus'
    pub_command_list = []
    sub_command_list = []
    pub_list, sub_list = [], []
    broker = None

    main()