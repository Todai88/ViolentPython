import socket

def retBanner(ip, port):
    print "Testing " + str(ip) + " : " +  str(port)
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)

        return banner

    except:
        return

def checkVulns(banner):

    f = open("vuln_banners.txt", "r")
    print "Opening file " + str(f)
    for line in f.readlines():
        if line.strip("\n") in banner:
            print "[+] Server is vulnerable: " + banner.strip("\n")

    return

def main():

    portList = [21, 22, 25, 80, 110, 443]

    for x in range(1, 255):
        ip = "192.168.95." + str(x)
        for port in portList:
            banner = retBanner(ip, port)

            if banner:
                print "[+] " + ip + ": " + banner
                checkVulns(banner)


if __name__ == '__main__':
    main()
