#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class BusToplogy:
	"Linear topology of k switches, with one host per switch."
	def __init__(self, pub, sub, b, **opts):

	super(LinearTopo, self).__init__(**opts)
	self.pub = pub
	self.sub = sub
	self.b = b
	lastSwitch = None
	for i in irange(1, pub):
		host = self.addHost('pub%s' % i)
		switch = self.addSwitch('s%s' % i)
		self.addLink( host, switch)
		##if lastSwitch:
		##	self.addLink( switch, lastSwitch)
		##lastSwitch = switch
	for i in irange(1, sub):
		host = self.addHost('sub%s' % i)
		switch = self.addSwitch('s%s' % i)
		self.addLink( host, switch)
		##if lastSwitch:
		##	self.addLink( switch, lastSwitch)
		##lastSwitch = switch
	host = self.addhost('b%s' % len(b))
	switch = self.addSwitch('s%s' % len(b))
	self.addlink(host, switch)
	if lastSwitch:
		self.addLink( switch, lastSwitch)
	lastSwitch = switch
