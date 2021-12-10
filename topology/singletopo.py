#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import time

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, h6)
    net.addLink(s1, h7)
    net.addLink(s1, h8)
    net.addLink(s1, h9)
    net.addLink(s1, h10)
    net.addLink(s1, h11)
    net.addLink(s1, h12)
    net.addLink(s1, h13)
    net.addLink(s1, h14)
    net.addLink(s1, h15)
    net.addLink(s1, h16)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)
    net.addLink(s1, h5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    s1.cmd('ifconfig s1 10.0.1.1')
    
    info('*** Waiting for controllers to connect\n')
    time.sleep(8)
    info('*** sleep over\n')

    info('*** Running tests\n')
    
    info('*** Setting servers h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12\n')
    h1.cmd('python -m SimpleHTTPServer 80 &')
    h2.cmd('python -m SimpleHTTPServer 80 &')
    h3.cmd('python -m SimpleHTTPServer 80 &')
    h4.cmd('python -m SimpleHTTPServer 80 &')
    h5.cmd('python -m SimpleHTTPServer 80 &')
    h6.cmd('python -m SimpleHTTPServer 80 &')
    h7.cmd('python -m SimpleHTTPServer 80 &')
    h8.cmd('python -m SimpleHTTPServer 80 &')
    h9.cmd('python -m SimpleHTTPServer 80 &')
    h10.cmd('python -m SimpleHTTPServer 80 &')
    h11.cmd('python -m SimpleHTTPServer 80 &')
    h12.cmd('python -m SimpleHTTPServer 80 &')
    
    
    time.sleep(5)
    info('*** Servers set\n##### Running tests from h13 ####\n\n')
  
    info('#### FILE SIZE TEST (SIZE 100kb) ####\n\n')
    h13.cmd('ab -n 400 -c 10 -g test_rand1.csv http://10.0.1.1/test_100kb.txt/ >> test.txt &')
    time.sleep(40)
    
    info('#### FILE SIZE TEST (SIZE 500kb) ####\n\n')
    h13.cmd('ab -n 400 -c 10 -g test_rand2.csv http://10.0.1.1/test_500kb.txt/ >> test.txt &')
    time.sleep(40)
    
    info('#### FILE SIZE TEST (SIZE 100mb) ####\n\n')
    h13.cmd('ab -n 400 -c 10 -g test_rand3.csv http://10.0.1.1/test_100mb.txt/ >> test.txt &')
   

    info('#### COMPLETED TESTS ####\n')
    

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

