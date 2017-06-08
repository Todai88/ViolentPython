import dpkt, socket, pygeoip, argparse, os

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def ret_klm(ip):
    rec = gi.record_by_name(ip)

    try:
        long = rec['longitude']
        lat  = rec['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<Point>\n'
            '<coordinates>%6f, %6f</coordinates>\n'
            '</Point>\n'
            '</Placemark>\n'
            )%(ip, long, lat)
        return kml
    except:
        return ''


def plotIPs(pcap):
    kml_points = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip  = eth.data
            src = socket.inet_ntoa(ip.src)
            src_kml = ret_klm(src)
            dst = socket.inet_ntoa(ip.dst)
            dst_kml = ret_klm(dst)
            kml_points = kml_points + src_kml + dst_kml
        except:
            pass

    return kml_points

def main():

    parser = argparse.ArgumentParser(
        description=u'GeoLocator to parse IP addresses to their '
                    u'long, lat in KML for Google Maps.'
    )

    parser.add_argument(
        u'-p',
        help=u'Pcap file for parsing',
        required=True,
        dest=u'pcap_file'
    )
    arguments = parser.parse_args()

    if not os.path.isfile(arguments.pcap_file):
        parser.print_usage()
        raise SystemExit

    with open(arguments.pcap_file) as file:
        pcap = dpkt.pcap.Reader(file)
        kmlheader = '<?xml version="1.0" encoding="UTF-8"?>'+\
            '\n<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        kmlfooter = '</kml>\n'
        kmldoc = kmlheader + plotIPs(pcap) + kmlfooter
        print(kmldoc)

if __name__ == '__main__':
    main()