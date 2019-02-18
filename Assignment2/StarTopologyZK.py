"""
This is the file for star topology
"""

from mininet.topo import Topo


class StarTopology(Topo):
    # Star topology example.

    def __init__(self, _pubNum=None, _subNum=None, _brokerNum=None):
        """Create start topology"""

        # Initialize topology
        Topo.__init__( self )

        if _pubNum is None:
            _pubNum = 1

        if _subNum is None:
            _subNum = 1

        if _brokerNum is None:
            _brokerNum = 1

        self.pubNum = _pubNum
        self.subNum = _subNum
        self.brokerNum = _brokerNum

        # Initialize topology
        Topo.__init__(self)

        hostList = list()
        switchList = list()

        # track the name of host and switch.

        hostNum = _pubNum + _subNum + _brokerNum     # a broker at the center

        # Add one broker at the center
        hostList.append(self.addHost("broker1"))

        # The rest brokers are set
        index = 2

        for num in range(1, _pubNum):
            brokerName = "brokers" + str(index)
            hostList.append(self.addHost(brokerName))
            index += 1


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

        # Add local switches to brokers
        index = 1

        for num in range(0, _brokerNum):
            brkSName = "bs" + str(index)
            switchList.append(self.addSwitch(brkSName))
            index += 1

        # Add local switches to the publisher
        index = 1
        for num in range(0, _pubNum):
            pubSName = "ps" + str(index)
            switchList.append(self.addSwitch(pubSName))
            index += 1

        # Add local switches to the publisher
        index = 1
        for num in range(0, _subNum):
            subSName = "ss" + str(index)
            switchList.append(self.addSwitch(subSName))
            index += 1

        # Form the star topology, let the first host -- the broker1 and put it at the center

        # self.addLink(leftHost, leftSwitch)
        # connect the broker with switch
        self.addLink(hostList[0], switchList[0])

        # connect other hosts with own their switches
        for num in range(1, hostNum):
            self.addLink(hostList[num], switchList[num])

        # connect each host's own switches to the broker's switch
        for num in range(1, hostNum):
            self.addLink(switchList[0], switchList[num])


topos = { 'startopoZK': ( lambda: StarTopology(3, 3, 3) ) }
