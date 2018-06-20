#!/usr/bin/python

import sys
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

#Global variables
net = Mininet(controller=Controller, link=TCLink)
s = 1

#Functions
def serial_connection(switches):
	for i in range(len(switches)-1):
		net.addLink(switches[i], switches[i+1], bw=b, delay=d, loss=l, max_queue_size=mqs)

def create_topo():
	global s
	if float(n)/s > 24:
		s += 1
		create_topo()
	else:
		switches = []
		hosts = []
		h = 1
		info('*** Creating topology.\n')		
		net.addController('c1')
		if ((float(n)/s)%2 == 0) or n <= 24:
			for i in range(s):
				switch = net.addSwitch('s'+str(i+1))
				switches.append(switch)
				for j in range(n/s):
					host = net.addHost('h'+str(h))
					hosts.append(host)
					net.addLink(host, switch, bw=b, delay=d, loss=l, max_queue_size=mqs)
					h += 1
		else:
			num_hosts = n
			for i in range(s-1):

				switch = net.addSwitch('s'+str(i+1))
				switches.append(switch)
				for j in range(n/s):
					host = net.addHost('h'+str(h))
					hosts.append(host)
					net.addLink(host, switch, bw=b, delay=d, loss=l, max_queue_size=mqs)
					num_hosts -= 1
					h += 1
			switch = net.addSwitch('s'+str(s))
			switches.append(switch)
			for i in range(num_hosts):
				host = net.addHost('h'+str(h))
				hosts.append(host)
				net.addLink(host, switch, bw=b, delay=d, loss=l, max_queue_size=mqs)
				h += 1

		serial_connection(switches)

def execute():
	create_topo()

	net.start()

	CLI(net)

	net.stop()

#Main
if __name__ == '__main__':
	n = int(sys.argv[1])
	b = 7 #Band width
	d = '3ms' #Delay
	l = 0 #Loss
	mqs = 800 #Max queue size

	setLogLevel('info')
	execute()
