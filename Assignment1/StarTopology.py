#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.node import CPULimitedHost


class StarTopology(Topo):
    """
    A class for star topology
    """
    def __init__(self, _pubNum: int =None, _subNum: int=None):
        # Create star topology. At least there is 1 pub and 1 sub
        if _pubNum is None:
            _pubNum = 1

        if _subNum is None:
            _subNum = 1

        self.pubNum = _pubNum
        self.subNum = _subNum

        # Initialize topology
        Topo.__init__(self)

        self.hostList: List[str] = list()
        self.switchList: List[str] = list()

        # track the name of host and switch.
        index: int = 1
        hostNum = _pubNum + _subNum + 1     # a broker at the center

        # Add hosts

        for num in range(0, hostNum):
            hName = "h"+str(index)
            self.hostList.append(self.addHost(hName))
            index += 1

        # Add switches
        for num in range(0, hostNum):
            sName = "s" + str(index)
            self.switchList.append(self.addSwitch(sName))
            index += 1

        # Form the star topology, let the first host "h1" the broker and put it at the center

        # self.addLink(leftHost, leftSwitch)
        # connect the broker with switch
        self.addLink(self.hostList[0], self.switchList[0])

        # connect other hosts with own their switches
        for num in range(1, hostNum):
            self.addLink(self.hostList[num], self.switchList[num])

        # connect each host's own switches to the broker's switch
        for num in range(1, hostNum):
            self.addLink(self.switchList[0], self.switchList[num])
	


topos = {'mytopo': (lambda: StarTopology(2, 3))}

def main():
    topo = StarTopology(2, 3)
    net = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
