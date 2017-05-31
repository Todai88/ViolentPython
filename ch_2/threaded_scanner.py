import optparse
from socket import *
from threading import *

screen_lock = Semaphore(value=1)
def conn_scan(host, port):
    try:
        conn_socket = socket(AF_INET, SOCK_STREAM)
        conn_socket.connect((host, port))
        conn_socket.send('ViolentPython\r\n')
        results = conn_socket.recv(100)
        screen_lock.acquire()
        print("[+] {}/tcp open".format(port))
        print("[+] {}".format(str(results)))
    except Exception as e:
        screen_lock.acquire()
        print("[-]{}/tcp closed".format(port))
    finally:
        screen_lock.release()
        conn_socket.close()


def port_scan(host, ports):

    try:
        target_ip = gethostbyname(host)
    except:
        print('[-] Cannot resolve ip for "{}": Unkown Host'.format(host))
        return

    try:
        target_name = gethostbyaddr(target_ip)
        print("[+] Scan Results for: " + target_name[0])
    except:
        print("[+] Scan Results for: " + target_ip)
    setdefaulttimeout(1)

    for port in ports:
        t = Thread(target=conn_scan, args=(host, int(port)))
        t.start()

def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def main():

    parser = optparse.OptionParser("usage %prog -H"\
                                   " <target host> -p <target port>")

    parser.add_option('-H', dest='target_host', type='string', \
                      help='specify target host')

    parser.add_option('-p', dest='target_port', type='string',\
                      help='specify target port',\
                      action='callback',\
                      callback=get_comma_separated_args)

    (options, args) = parser.parse_args()

    target_host = options.target_host
    target_port = options.target_port
    print(target_port)
    if (target_host == None) | (target_port == None):
        print(parser.usage)
        raise SystemExit

    port_scan(target_host, target_port)

if __name__ == "__main__":
    main()
