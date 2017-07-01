#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller
from mininet.cli import CLI
from functools import partial
from mininet.node import RemoteController
import os

class MyTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self):
        Topo.__init__(self)
        s1=self.addSwitch('s1', protocols=["OpenFlow13"] )
        s2=self.addSwitch('s2', protocols=["OpenFlow13"] )
        h1=self.addHost('h1')
        h2=self.addHost('h2')
        h3=self.addHost('h3')

        self.addLink(s1, h1, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s1, h2, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s1, s2, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s2, h3, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

def perfTest():
    "Create network and run simple performance test"
    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    net.pingAll()
    # print "Testing bandwidth between h1 and h3"
    # h1, h3 = net.get( 'h1', 'h3' )
    # net.iperf( (h3, h5) )
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
