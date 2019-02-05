"""
This is the file for star topology
"""

from mininet.topo import Topo


class StarTopology(Topo):
    # Star topology example.

    def __init__(self, _pubNum=None, _subNum=None):
        """Create start topology"""

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

        hostList = list()
        switchList = list()

        # track the name of host and switch.

        hostNum = _pubNum + _subNum     # a broker at the center


        # Add publishers
        index = 1

        for num in range(0, _pubNum):
            pubName = "pub"+str(index)
            hostList.append(self.addHost(pubName))
            index += 1

        # Add subscribers
        index = 1

        for num in range(0, _subNum):
            subName = "sub"+str(index)
            hostList.append(self.addHost(subName))
            index += 1

        # Add switches

        # Add local switches to the publisher
        index = 1
        for num in range(0, _pubNum):
            pubName = "ps" + str(index)
            switchList.append(self.addSwitch(pubName))
            index += 1

        # Add local switches to the publisher
        index = 1
        for num in range(0, _subNum):
            subName = "ss" + str(index)
            switchList.append(self.addSwitch(subName))
            index += 1

        # connect other hosts with own their switches
        for num in range(0, hostNum):
            self.addLink(hostList[num], switchList[num])

        # connect each host's own switches to the first host's switch
        for num in range(1, hostNum):
            self.addLink(switchList[0], switchList[num])


topos = { 'startopo': ( lambda: StarTopology(3, 3) ) }
