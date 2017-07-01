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

        #### Define Switches ####
        s1=self.addSwitch('s1', protocols=["OpenFlow13"] )
        s2=self.addSwitch('s2', protocols=["OpenFlow13"] )
        s3=self.addSwitch('s3', protocols=["OpenFlow13"] )
        s4=self.addSwitch('s4', protocols=["OpenFlow13"] )
        s5=self.addSwitch('s5', protocols=["OpenFlow13"] )
        s6=self.addSwitch('s6', protocols=["OpenFlow13"] )
        s7=self.addSwitch('s7', protocols=["OpenFlow13"] )

        #### Define Hosts ####
        h1=self.addHost('h1')
        h2=self.addHost('h2')
        h3=self.addHost('h3')
        h4=self.addHost('h4')
        h5=self.addHost('h5')
        h6=self.addHost('h6')
        h7=self.addHost('h7')
        h8=self.addHost('h8')

        #### Define Host Links (10 Mbit/sec) ####
        self.addLink(s1, h1, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s1, h2, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

        self.addLink(s2, h3, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s2, h4, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

        self.addLink(s6, h5, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s6, h6, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

        self.addLink(s7, h7, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s7, h8, bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

        #### Define Switch Links ####
        # Aggregation to Edge Links (20 Mbit/sec)
        self.addLink(s3, s1, bw=20, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s3, s2, bw=20, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s5, s6, bw=20, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s5, s7, bw=20, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        # Core to Aggregation Links (40 Mbit/sec)
        self.addLink(s4, s3, bw=40, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(s4, s5, bw=40, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)


def perfTest():
    "Create network and run simple performance test"
    topo = MyTopo()
    #net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=POXcontroller1)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=partial(RemoteController, ip='127.0.0.1', port=6633))
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()






    #
