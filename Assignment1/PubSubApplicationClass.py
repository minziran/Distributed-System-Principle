import time
import threading
from signal import SIGINT
from BusTopology import BusTopology
from StarTopology import StarTopology

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import OVSController


class MNSystem(object):
    def __init__(self, _topo=None, _pub_command_list=list(), _sub_command_list=list(),
                 _pub_list=list(),_sub_list=list(), _broker=None):
        self.net = Mininet(topo=_topo, link=TCLink, controller=OVSController)
        self.pub_list = _pub_list
        self.sub_list = _sub_list
        self.pub_command_list = _pub_command_list
        self.sub_command_list = _sub_command_list
        self.broker = _broker
        
        self.net.start()
        dumpNodeConnections(self.net.hosts)
        self.net.pingAll()

    def call_broker(self):
        self.broker.cmd('xterm -e python ZMQ_broker.py 5556 5557')

    def call_publisher(self, _pub, _pub_command):
        _pub.cmd('xterm -e python ZMQ_publisher.py  ' + str(self.broker.IP()) + str(_pub_command))

    def call_subscriber(self,_sub, _sub_command):
        _sub.cmd('xterm -e python ZMQ_subscriber.py  ' + str(self.broker.IP()) + str(_sub_command))

    def create_net(self):

        for host in self.net.hosts:
            if 'pub' in host.name:
                self.pub_list.append(host)
            elif 'sub' in host.name:
                self.sub_list.append(host)
            elif 'broker' in host.name:
                self.broker = host

        threading.Thread(target=self.call_broker, args=()).start()
        time.sleep(3)
        for k, pub in enumerate(self.pub_list):
            threading.Thread(target=self.call_publisher(pub, self.pub_command_list[k]), args=()).start()
            time.sleep(5)
        for k, sub in enumerate(self.sub_list):
            threading.Thread(target=self.call_subscriber(sub, self.sub_command_list[k]), args=()).start()
            time.sleep(5)

        try:
            while True:
                pass
        except Exception as e:
            print(e)

        self.net.stop()


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
        testNet = MNSystem(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
        testNet.create_net()

    elif topo_type == 'star':
        topo = StarTopology(pub_num, sub_num)
        testNet = MNSystem(topo, pub_command_list, sub_command_list, pub_list, sub_list, broker)
        testNet.create_net()
    else:
        exit("Could not find matched topology. 'bus' and 'star' are provided")


if __name__ == '__main__':
    main()
