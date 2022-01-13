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
    c3=net.addController(name='c3',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6636)

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

    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h13 = net.addHost('h13', cls=Host, ip='10.1.4.1', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.1.3.4', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.1.1.1', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.1.2.4', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.1.3.2', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.1.1.4', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.1.1.3', defaultRoute=None)
    h14 = net.addHost('h14', cls=Host, ip='10.1.4.2', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.1.2.3', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.1.2.2', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.1.4.3', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.1.4.4', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.1.3.1', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.1.3.3', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.1.2.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.1.1.2', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s4, h9)
    net.addLink(s3, s1)
    net.addLink(s3, s2)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s2, h5)
    net.addLink(s2, h6)
    net.addLink(s3, s4)
    net.addLink(s1, h4)
    net.addLink(h7, s2)
    net.addLink(s2, h8)
    net.addLink(s4, h10)
    net.addLink(s4, h11)
    net.addLink(s4, h12)
    net.addLink(s5, h13)
    net.addLink(s5, h14)
    net.addLink(s5, h15)
    net.addLink(s5, h16)
    net.addLink(s5, s3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s5').start([c3])
    net.get('s3').start([])
    net.get('s1').start([c0])
    net.get('s4').start([c2])
    net.get('s2').start([c1])

    info( '*** Post configure switches and hosts\n')
    s3.cmd('ifconfig s3 10.1.0.0')
    s1.cmd('ifconfig s1 10.1.1.0')
    s4.cmd('ifconfig s4 10.1.3.0')
    s2.cmd('ifconfig s2 10.1.2.0')

    info('*** Waiting for controllers to connect\n')
    time.sleep(8)
    info('*** sleep over\n')

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
    
    time.sleep(5)
    info('*** Servers set\n##### Running tests from h4 h8 h12 ####\n\n')

    info('#### FILE SIZE TEST (file size 100mb) ####\n\n')
    h4.cmd('ab -n 100 -c 10 -g test_rand11.csv http://10.1.0.0/test_100kb.txt >> test_rand.txt &')
    h8.cmd('ab -n 100 -c 10 -g test_round11.csv http://10.1.0.0/test_100kb.txt >> test_round.txt &')
    h12.cmd('ab -n 100 -c 10 -g test_least11.csv http://10.1.0.0/test_100kb.txt >> test_least.txt &')
    h16.cmd('ab -n 100 -c 10 -g test_wrr11.csv http://10.1.0.0/test_100kb.txt >> test_wrr.txt &')
    time.sleep(30)

    info('#### FILE SIZE TEST (file size 500kb) ####\n\n')
    h4.cmd('ab -n 100 -c 10 -g test_rand12.csv http://10.1.0.0/test_500kb.txt >> test_rand.txt &')
    h8.cmd('ab -n 100 -c 10 -g test_round12.csv http://10.1.0.0/test_500kb.txt >> test_round.txt &')
    h12.cmd('ab -n 100 -c 10 -g test_least12.csv http://10.1.0.0/test_500kb.txt >> test_least.txt &')
    h16.cmd('ab -n 100 -c 10 -g test_wrr12.csv http://10.1.0.0/test_500kb.txt >> test_wrr.txt &')
    time.sleep(30)

    info('#### FILE SIZE TEST (file size 100mb) ####\n\n')
    h4.cmd('ab -n 100 -c 10 -g test_rand13.csv http://10.1.0.0/test_100mb.txt >> test_rand.txt &')
    h8.cmd('ab -n 100 -c 10 -g test_round13.csv http://10.1.0.0/test_100mb.txt >> test_round.txt &')
    h12.cmd('ab -n 100 -c 10 -g test_least13.csv http://10.1.0.0/test_100mb.txt >> test_least.txt &')
    h16.cmd('ab -n 100 -c 10 -g test_wrr13.csv http://10.1.0.0/test_100mb.txt >> test_wrr.txt &')
    time.sleep(30)

    info('#### COMPLETED TESTS ####\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

