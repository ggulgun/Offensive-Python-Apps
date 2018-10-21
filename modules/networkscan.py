# -.- coding: utf-8 -.-

import nmap
import scapy
from scapy.config import conf  
conf.ipv6_enabled = False
from scapy.all import *
import Queue

results = Queue.Queue()

def getDefaultInterface(returnNet=False):
    def long2net(arg):
        if (arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("illegal netmask value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))
    def to_CIDR_notation(bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = long2net(bytes_netmask)
        net = "%s/%s" % (network, netmask)
        if netmask < 16:
            return None
        return net

    iface_routes = [route for route in scapy.config.conf.route.routes if route[3] == scapy.config.conf.iface and route[1] != 0xFFFFFFFF]
    network, netmask, _, interface, address,abc = max(iface_routes, key=lambda item:item[1])

    net = to_CIDR_notation(network, netmask)
    if net:
        if returnNet:
            return net
        else:
            return interface

def run(network):
    returnlist = []
    nm = nmap.PortScanner()
    print network
    a = nm.scan(hosts=network, arguments='-sn')
    for k, v in a['scan'].items():
        if str(v['status']['state']) == 'up':
            try:
                results.put(str(v['addresses']['ipv4']))                
            except:
                pass
    return results



hostsList = run(getDefaultInterface(True))

