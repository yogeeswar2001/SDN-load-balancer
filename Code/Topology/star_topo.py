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

    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6634)

    c2=net.addController(name='c2',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6635)

    info( '*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h9 = net.addHost('h9', cls=Host, ip='10.1.3.3', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.1.3.1', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.1.1.1', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.1.2.2', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.1.2.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.1.1.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.1.1.3', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.1.2.3', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.1.3.2', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s2, h5)
    net.addLink(s2, h6)
    net.addLink(s3, s4)
    net.addLink(s4, h7)
    net.addLink(s4, h8)
    net.addLink(s4, h9)
    net.addLink(s3, s1)
    net.addLink(s3, s2)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s2, h4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c1])
    net.get('s3').start([])
    net.get('s1').start([c0])
    net.get('s4').start([c2])

    info( '*** Post configure switches and hosts\n')
    s2.cmd('ifconfig s2 10.1.2.0')
    s3.cmd('ifconfig s3 10.1.0.0')
    s1.cmd('ifconfig s1 10.1.1.0')
    s4.cmd('ifconfig s4 10.1.3.0')

    info('*** Running tests\n')
    info('*** Setting servers h1 h2 h4 h5 h7 h8\n')
    h1.cmd('python -m SimpleHTTPServer 80 &')
    h2.cmd('python -m SimpleHTTPServer 80 &')
    h3.cmd('python -m SimpleHTTPServer 80 &')
    h5.cmd('python -m SimpleHTTPServer 80 &')
    h6.cmd('python -m SimpleHTTPServer 80 &')
    h7.cmd('python -m SimpleHTTPServer 80 &')
    h9.cmd('python -m SimpleHTTPServer 80 &')
    h10.cmd('python -m SimpleHTTPServer 80 &')
    h11.cmd('python -m SimpleHTTPServer 80 &')
    h13.cmd('python -m SimpleHTTPServer 80 &')
    h14.cmd('python -m SimpleHTTPServer 80 &')
    h15.cmd('python -m SimpleHTTPServer 80 &')
    info('*** Servers set\n##### Running tests from h4 h8 h12 ####')

    h4.cmd('ab -n 100 -c 10 -g test_rand.csv http://10.0.1.1/ >> test_rand.txt')
    h8.cmd('ab -n 100 -c 10 -g test_round.csv http://10.0.1.1/ >> test_round.txt')
    h12.cmd('ab -n 100 -c 10 -g test_least.csv http://10.0.1.1/ >> test_least.txt')
    h16.cmd('ab -n 100 -c 10 -g test_wrr.csv http://10.0.1.1/ >> test_wrr.txt')

    info('#### COMPLETED TESTS ####')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

