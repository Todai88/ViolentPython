import dpkt, socket, pygeoip, argparse

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def print_record(target):
    try:
        rec = gi.record_by_name(target)
        city = rec['city']
        country = rec['country_code3']

        if city != '':
            geolocation = '[+] City: ' + city +\
                     ', Country: ' + country
        else:
            geolocation = '[+] City: Unregistered, Country: ' + country
        return geolocation
    except:
        return 'Unregistered!'
def print_pcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print("\n[ ==================== ]\n")
            print("[+] Src: " + src + " --> Dst: " + dst)
            print("[+] Src: " + print_record(src) + "--> Dst: " +\
                  print_record(dst))
        except Exception as e:
            print(e)
            pass

def main():
    import os

    parser = argparse.ArgumentParser(
    description=u'A script that show the ip and location of captured packages'
    )

    parser.add_argument(
        u'-p',
        dest='pcap_file',
        required=True,
        help=u'The PATH to the .pcap file you wish to analyse!'
    )

    arguments = parser.parse_args()

    if not os.path.isfile(arguments.pcap_file):
        parser.print_usage()
        raise SystemExit

    with open(arguments.pcap_file) as file:
        pcap = dpkt.pcap.Reader(file)
        print_pcap(pcap)

if __name__ == '__main__':
    main()