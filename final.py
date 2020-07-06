#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    
    self.addLink(s1, s4, port1=1, port2=1)#Linking s1 to s4 (the core switch), and then s1 to h1. 
    self.addLink(s1, h1, port1=2, port2=0)

    self.addLink(s2, s4, port1=1, port2=2)#Linking s2 to s4 (the core switch), and then s2 to h2.
    self.addLink(s2, h2, port1=2, port2=0)

    self.addLink(s3, s4, port1=1, port2=3)#Linking s3 to s4 (the core switch), and then s3 to h3
    self.addLink(s3, h3, port1=2, port2=0)
    
    self.addLink(h4, s4, port1=0, port2=4)#Linking the untrusted host to the core switch
    
    self.addLink(s4, s5, port1=5, port2=1)#Linking the data center switch to the core switch
  
    self.addLink(s5, h5, port1=2, port2=0)#Linking Data Center switch to Data Center server


def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
