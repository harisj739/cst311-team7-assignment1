"""Legacy Network for CST311 Programming Assignment 4"""
__author__ = "Team 7 - SSS"
__credits__ = [
  "Andrew Grant",
  "Anthony Matricia",
  "Haris Jilani"
]

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.term import makeTerm
import subprocess

# Generates the server certifcates prior to starting the network.
subprocess.run(["sudo", "-E", "python3", "certificate_generation.py"])

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    # Switches are now properly initialized before the initialization of routers.
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    r5 = net.addHost('r5', cls=Node, ip='10.0.1.4/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='192.168.0.2/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='10.0.0.4/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    # Added default routes to each of the hosts, which connect the two subnets together.
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24', defaultRoute='via 10.0.0.4')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24', defaultRoute='via 10.0.0.4')
    # Modified the host's IP addresses of h3 and h4 to fit the East Coast Network's address space.
    h3 = net.addHost('h3', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.4')
    h4 = net.addHost('h4', cls=Host, ip='10.0.1.2/24', defaultRoute='via 10.0.1.4')

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    # Modified the following two addLink statement by connecting each switch to its respective routing interface. 
    net.addLink(s2, r5)
    net.addLink(s1, r3)
    # Modified the following two addLink statements by adding 2 two-host networks for each link present between the routers.
    net.addLink(r3, r4, intfName1='r3-eth1', params1={ 'ip' : '192.168.0.1/30' }, intfName2='r4-eth0', params2={ 'ip' : '192.168.0.2/30' })
    net.addLink(r4, r5, intfName1='r4-eth1', params1={ 'ip' : '192.168.1.1/30' }, intfName2='r5-eth1', params2={ 'ip' : '192.168.1.2/30' })

    info( '*** Starting network\n')
    net.build()
    
    # Added static routes to interconnect each router's interfaces to connect the two subnets.
    # Static Routes: r3
    info(net['r3'].cmd ('ip route add 192.168.1.0/30 via 192.168.0.2 dev r3-eth1'))
    info(net['r3'].cmd ('ip route add 10.0.1.0/24 via 192.168.0.2 dev r3-eth1'))
    # Static Routes: r4
    info(net['r4'].cmd ('ip route add 10.0.0.0/24 via 192.168.0.1 dev r4-eth0'))
    info(net['r4'].cmd ('ip route add 10.0.1.0/24 via 192.168.1.2 dev r4-eth1'))
    # Static Routes: r5
    info(net['r5'].cmd ('ip route add 10.0.0.0/24 via 192.168.1.1 dev r5-eth1'))
    info(net['r5'].cmd ('ip route add 192.168.0.0/30 via 192.168.1.1 dev r5-eth1'))
    
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    
    # these windows need to be created after the entire network is created -- keldin
    #using makeTerm to open individual terminal windows
    makeTerm(h1, title='Node', term='xterm', display=None, cmd='python3 PA4_Chat_Client_Team7.py; bash')
    makeTerm(h2, title='Node', term='xterm', display=None, cmd='python3 CST311/tlswebserver.py; bash')
    makeTerm(h3, title='Node', term='xterm', display=None, cmd='python3 PA4_Chat_Client_Team7.py; bash')
    makeTerm(h4, title='Node', term='xterm', display=None, cmd='python3 PA4_Chat_Server_Team7.py; bash')

    CLI(net)
    net.stop()
    # after you exit mininet, also close all the active terminal windows -- keldin
    net.stopXterms()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
