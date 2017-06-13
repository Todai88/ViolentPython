import time, argparse

from scapy.all import *
from IPy import IP as IPTEST

ttl_values = {}
THRESH = 5

def check_ttl(ipsrc, ttl):
    if IPTEST(ipsrc).iptype() == 'PRIVATE':
        return

    if not ttl_values.has_key(ipsrc):
        packet = sr1(IP(dst=ipsrc) / ICMP(),\
                     retry=0, timeout=1, verbose=0)
        ttl_values[ipsrc] = packet.ttl

    if abs(int(ttl) - int(ttl_values[ipsrc])) > THRESH:
        print('\n[!] TTL: ' + ttl + ', Actual TTL: ' +\
              str(ttl_values[ipsrc]))

def test_ttl(packet):
    try:
        if packet.haslayer(IPTEST):
            ipsrc = packet.getlayer(IPTEST).src
            ttl = str(packet.ttl)
            check_ttl(ipsrc, ttl)
    except:
        pass

def main():
    global THRESH

    parser = argparse.ArgumentParser(
        u"A simple program to check for a packets TTL "
        u"and judge if it's been spoofed"
    )

    parser.add_argument(
        u'-i',
        help=u'The network interface you wish to use',
        dest=u'iface',
        default='eth0'
    )

    parser.add_argument(
        u'-t',
        help=u'The threshold count',
        dest=u'thresh',
        default=5
    )

    args = parser.parse_args()


    THRESH = parser.thresh

    sniff(prn=test_ttl, store=0)

if __name__ == '__main__':
    main()