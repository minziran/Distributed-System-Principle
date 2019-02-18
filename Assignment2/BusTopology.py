
from mininet.topo import Topo


class BusTopology(Topo):
    # Bus topology example.

    def __init__(self, _pubNum=None, _subNum=None, _brokerNum=None):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )
        self.pubNum = _pubNum
        self.subNum = _subNum
        self.brokerNum = _brokerNum

        hostList = list()
        localSwitchList = list()
        busSwitchList = list()

        # track the name of host and switch.

        hostNum = _pubNum + _subNum + _brokerNum  # a broker at the center

        # Add brokers
        index = 1
        #hostList.append(self.addHost("broker"))
        for num in range(0, _brokerNum):
            hostName = "broker" + str(index)
            hostList.append(self.addHost("hostName"))
            index += 1
            
        # Add publishers
        index = 1

        for num in range(0, _pubNum):
            pubName = "pub" + str(index)
            hostList.append(self.addHost(pubName))
            index += 1

        # Add subscribers
        index = 1

        for num in range(0, _subNum):
            subName = "sub" + str(index)
            hostList.append(self.addHost(subName))
            index += 1

        # Add local switch for brokers
        index = 1
        
        for num in range(0,_brokerNum):
            sName = "bs" + str(index)
            localSwitchList.append(self.addSwitch(sName))
            index += 1

        # Add local switches for publishers
        index = 1

        for num in range(0, _pubNum):
            sName = "ps" + str(index)
            localSwitchList.append(self.addSwitch(sName))
            index += 1

        # Add local switches for subscribers
        index = 1
        for num in range(0, _subNum):
            sName = "ss" + str(index)
            localSwitchList.append(self.addSwitch(sName))
            index += 1

        # Add bus switches
        index = 1
        numBusSwitch = (hostNum - 1)//2 + 1

        for num in range(numBusSwitch):
            sName = "bus" + str(index)
            busSwitchList.append(self.addSwitch(sName))
            index += 1

        # Build Local Links
        for num in range(hostNum):
            self.addLink(hostList[num], localSwitchList[num])

        # Link the bus switches together
        for num in range(0, numBusSwitch-1):
            self.addLink(busSwitchList[num], busSwitchList[num + 1])

        # Build Links between local switches and bus switches
        for num in range(hostNum):
            self.addLink(localSwitchList[num], busSwitchList[num//2])


topos = { 'bustopo': ( lambda: BusTopology(2, 3) ) }
