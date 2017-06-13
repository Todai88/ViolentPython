import dpkt, socket

THRESH = 10000


def setup_data(buf):
    eth   = dpkt.ethernet.Ethernet(buf)
    ip    = eth.data
    src   = socket.inet_ntoa(ip.src)
    dst   = socket.inet_ntoa(ip.dst)
    tcp   = ip.data

    return (eth, ip, src, dst, tcp)

def find_download(pcap):
    for (ts, buf) in pcap:
        try:
            (eth, ip, src, dst, tcp) = setup_data(buf)
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    print('[!] ' + src + ' Downloaded LOIC.')
        except:
            pass

def find_attack(pcap):
    pkt_count = {}
    for (ts, buf) in pcap:
        try:
            (eth, ip, src, dst, tcp) = setup_data(buf)
            dport = tcp.dport

            if dport == 80: #check portnumber
                stream = src + ':' + dst
                if pkt_count.has_key(stream):
                    pkt_count[stream] = pkt_count[stream] + 1
                else:
                    pkt_count[stream] = 1
        except:
            pass

    for stream in pkt_count:
        sent_packet = pkt_count[stream]
        if sent_packet > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print('[+] ' + src + ' attacked ' + dst +\
                  ' with ' + str(sent_packet) + ' packets.')

def find_hivemind(pcap):
    for (ts, buf) in pcap:
        try:
            (eth, ip, src, dst, tcp) = setup_data(buf)
            dport = tcp.dport
            sport = tcp.sport

            if dport == 6667:
                if '!lazor' in tcp.data.lower():
                    print('[!] DDoS Hivemind issued by: ' + src)
                    print('[+] Target CMD: ' + tcp.data)
            if sport == 6667:
                if '!lazor' in tcp.data.lower():
                    print('[!] DDoS Hivemind issued to: ' + src)
                    print('[+] Target CMD: ' + tcp.data)
        except:
            pass

def find_attack(pcap):
    packet_count = {}
    for (ts, buf) in pcap:
        try:
            (eth, ip, src, dst, tcp) = setup_data(buf)
            dport = tcp.dport
            if dport == 80:
                stream = src + ':' + dst
                if packet_count.has_key(stream):
                    packet_count[stream] = packet_count[stream] + 1
                else:
                    packet_count[stream] = 1
        except:
            pass

    for stream in packet_count:
        sent_packet = packet_count[stream]
        if sent_packet > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print('[+] ' + src + ' attacked ' + dst +\
                  ' with ' + str(sent_packet) + ' packets')

def main():
    import argparse, os
    global THRESH

    parser = argparse.ArgumentParser(
        description=u'A small program to detect the usage of LOIC on your system'
    )

    parser.add_argument(
        u'-p',
        dest=u'pcap_file',
        help=u'A file containing captured packets',
        required=True
    )

    parser.add_argument(
        u'-t',
        dest=u'threshold',
        help=u'The threshold count',
        required=False,
        default=10000
    )

    args = parser.parse_args()

    if not os.path.isfile(args.pcap_file):
        parser.print_usage()
        raise SystemExit

    THRESH = args.threshold

    with open(args.pcap_file) as file:
        pcap = dpkt.pcap.Reader(file)
        find_download(pcap)
        find_hivemind(pcap)
        find_attack(pcap)

if __name__ == '__main__':
    main()
