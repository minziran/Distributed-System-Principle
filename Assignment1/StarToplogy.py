#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class BusToplogy:
	"Linear topology of k switches, with one host per switch."
	def __init__(self, j, l, **opts):

	super(LinearTopo, self).__init__(**opts)
	k = j + l
	self.k = k
	lastSwitch = None
	for i in irange(1, k):
		host = self.addHost('h%s' % i)
		switch = self.addSwitch('s%s' % i)
		self.addLink( host, switch)
		if lastSwitch:
			self.addLink( switch, lastSwitch)
		lastSwitch = switch
