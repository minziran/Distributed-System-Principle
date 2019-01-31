
from mininet.topo import Topo


class BusTopology(Topo):
    # Star topology example.

    def __init__(self, _pubNum=None, _subNum=None):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )
        self.hostList = list()
        self.localSwitchList = list()
        self.busSwitchList = list()

        # track the name of host and switch.
        index = 1
        hostNum = _pubNum + _subNum + 1  # a broker at the center

        # Add hosts

        for num in range(0, hostNum):
            hName = "h" + str(index)
            self.hostList.append(self.addHost(hName))
            index += 1

        # Add local switches
        index = 1

        for num in range(0, hostNum):
            sName = "s" + str(index)
            self.localSwitchList.append(self.addSwitch(sName))
            index += 1

        # Add bus switches
        index = 1
        numBusSwitch = (hostNum - 1)//2 + 1

        for num in range(numBusSwitch):
            sName = "bs" + str(index)
            self.busSwitchList.append(self.addSwitch(sName))
            index += 1

        # Build Local Links
        for num in range(hostNum):
            self.addLink(self.hostList[num], self.localSwitchList[num])

        # Link the bus switches together
        for num in range(0, numBusSwitch-1):
            self.addLink(self.busSwitchList[num], self.busSwitchList[num + 1])

        # Build Links between local switches and bus switches
        for num in range(hostNum):
            self.addLink(self.localSwitchList[num], self.busSwitchList[num//2])


topos = { 'bustopo': ( lambda: BusTopology(2, 3) ) }
