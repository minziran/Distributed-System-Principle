import os              # OS level utilities
import sys
import argparse   # for command line parsing

from signal import SIGINT
import time
import threading

from BusTopology import BusTopology
from StarTopology import StarTopology
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.util import pmonitor

def create_net(topo, test_command, pub_list, sub_list, broker):


    net = Mininet(topo=topo, link=TCLink)
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

    broker_ip = broker.IP()

    def call_broker():
       broker.cmd('xterm -e python ZMQ_broker.py 5556 5557')
    def call_publisher():
        pub.cmd('xterm -e python ZMQ_publisher.py  ' + str(broker_ip) + str(test_command))
    def call_subscriber():
        sub.cmd('xterm -e python ZMQ_subscriber.py  ' + str(broker_ip) + str(test_command))

    threading.Thread(target=call_broker, args=()).start()
    time.sleep(3)
    for pub in pub_list:
        threading.Thread(target=call_publisher, args=()).start()
        time.sleep(5)
    for sub in sub_list:
        threading.Thread(target=call_subscriber, args=()).start()
        time.sleep(5)

    try :
        while True:
            pass
    except Exception as e:
        print(e)

    net.stop()


def main():
    pub_num = 3
    sub_num = 3
    topo_type = 'bus'
    test_command = ''
    pub_list, sub_list = [], []
    broker = None
    if topo_type == 'bus':
        topo = BusTopology(pub_num,sub_num)
        create_net(topo, test_command, pub_list, sub_list, broker)
    elif topo_type == 'star':
        topo = StarTopology(pub_num,sub_num)
        create_net(topo, test_command, pub_list, sub_list, broker)
    else:
        exit("Could not find mached topology. 'bus' and 'star' are provided")

if __name__ == '__main__':
    main()