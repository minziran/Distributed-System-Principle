import time
import threading

from BusTopology import BusTopology
from StarTopology import StarTopology
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections


def create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker):

    net = Mininet(topo=topo, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()

    # Set up the hX as pub or sub or broker

    # for host in net.hosts:
    #
    #     if 'pub' in host.name:
    #         pub_list.append(host)
    #         print(len(host))
    #     elif 'sub' in host.name:
    #         sub_list.append(host)
    #     elif 'broker' in host.name:
    #         broker = host

    # TEST: let h7 be the broker; h1, h2, h3 be the publishers; h4, h5, h6 be the subscribers
    broker = net.hosts[6]

    for num in range(0, 3):
        pub_list.append(net.hosts[num])

    for num in range(3, 6):
        sub_list.append(net.hosts[num])

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
    pub_command_list =[]
    sub_command_list = []

    pub_list, sub_list = [], []
    # broker = None
    broker = 'h7'

    # Testing echo hello
    for num in range(3):
        pub_command_list.append("echo hello" + str(num))
        sub_command_list.append("echo world" + str(num))

    if topo_type == 'bus':
        topo = BusTopology(pub_num,sub_num)
        create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
    elif topo_type == 'star':
        topo = StarTopology(pub_num,sub_num)
        create_net(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
    else:
        exit("Could not find mached topology. 'bus' and 'star' are provided")

if __name__ == '__main__':
    main()