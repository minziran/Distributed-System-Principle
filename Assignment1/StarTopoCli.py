#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def StarNet(_pubNum=None, _subNum=None):

    if _pubNum is None:
        _pubNum = 1

    if _subNum is None:
        _subNum = 1

    net = Mininet(controller=Controller)

    # info( '*** Adding controller\n' )
    net.addController('c0')

    hostList = list()
    switchList = list()

    # track the name of host and switch.
    index = 1
    hostNum = _pubNum + _subNum + 1  # a broker at the center

    # Add hosts

    for num in range(0, hostNum):
        hName = "h" + str(index)
        hostList.append(net.addHost(hName))
        index += 1

    # Add switches
    for num in range(0, hostNum):
        sName = "s" + str(index)
        switchList.append(net.addSwitch(sName))
        index += 1

    # Form the star topology, let the first host "h1" the broker and put it at the center

    # self.addLink(leftHost, leftSwitch)
    # connect the broker with switch

    net.addLink(hostList[0], switchList[0])

    # connect other hosts with own their switches
    for num in range(1, hostNum):
        info("*** adding links host {} to switch {}".format(num, num))
        net.addLink(hostList[num], switchList[num])

    # connect each host's own switches to the broker's switch
    for num in range(1, hostNum):
        info("*** adding links host 0 to switch {}".format(num))
        net.addLink(switchList[0], switchList[num])

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    StarNet(2, 3)
