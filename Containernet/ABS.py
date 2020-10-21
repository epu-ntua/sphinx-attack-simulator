#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Containernet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')


    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Adding Docker\n')
    d1 = net.addDocker('d1', dimage="behaviourattacksimulator_node1", dcmd="./sender-receiver.sh")
    d2 = net.addDocker('d2', dimage="behaviourattacksimulator_node2", dcmd="./sender-receiver.sh")
    super = net.addDocker('super', dimage="registry.sphinx-repo.intracom-telecom.com/sphinx-project/attack-and-behaviour-simulators/behaviour-attack-simulator:supervisor_0.2",
                        volumes=["/var/run/docker.sock:/var/run/docker.sock"],
                        port_bindings={5002:5002}, dcmd="./flask.sh")


    info( '*** Add links\n')
    net.addLink(d1, s1)
    net.addLink(s1, d2)
    net.addLink(s1, super)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
