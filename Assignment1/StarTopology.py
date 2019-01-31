"""
This is the file for star topology
"""

from mininet.topo import Topo


class StarTopology(Topo):
    # Star topology example.

    def __init__(self, _pubNum=None, _subNum=None):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        if _pubNum is None:
            _pubNum = 1

        if _subNum is None:
            _subNum = 1

        self.pubNum = _pubNum
        self.subNum = _subNum

        # Initialize topology
        Topo.__init__(self)

        self.hostList = list()
        self.switchList = list()

        # track the name of host and switch.
        index = 1
        hostNum = _pubNum + _subNum + 1     # a broker at the center

        # Add hosts

        for num in range(0, hostNum):
            hName = "h"+str(index)
            self.hostList.append(self.addHost(hName))
            index += 1

        # Add switches
        index = 1
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


topos = { 'startopo': ( lambda: StarTopology(2, 3) ) }
