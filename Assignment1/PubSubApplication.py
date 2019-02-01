import time
import threading
from signal import SIGINT
from BusTopology import BusTopology
from StarTopology import StarTopology

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import OVSController


def create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker):
    net = Mininet(topo=topo, link=TCLink, controller=OVSController)
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
        broker.cmd('xterm -e python ZMQ_broker.py 5556 5557')

    def call_publisher(pub_command):
        pub.cmd('xterm -e python ZMQ_publisher.py  ' + str(broker_IP) + str(pub_command))

    def call_subscriber(sub_command):
        sub.cmd('xterm -e python ZMQ_subscriber.py  ' + str(broker_IP) + str(sub_command))

    threading.Thread(target=call_broker, args=()).start()
    time.sleep(3)
    for k, pub in enumerate(pub_list):
        threading.Thread(target=call_publisher(pub_command_list[k]), args=()).start()
        time.sleep(5)
    for k, sub in enumerate(sub_list):
        threading.Thread(target=call_subscriber(sub_command_list[k]), args=()).start()
        time.sleep(5)

    try:
        while True:
            pass
    except Exception as e:
        print(e)

    net.stop()


def main():
    pub_num = 3
    sub_num = 3
    topo_type = 'star'
    pub_command_list = []
    sub_command_list = []

    pub_list, sub_list = [], []
    broker = None
    if topo_type == 'bus':
        topo = BusTopology(pub_num, sub_num)
        create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
    elif topo_type == 'star':
        topo = StarTopology(pub_num, sub_num)
        create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
    else:
        exit("Could not find mached topology. 'bus' and 'star' are provided")


if __name__ == '__main__':
    main()
