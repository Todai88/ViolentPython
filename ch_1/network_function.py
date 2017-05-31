import socket

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)

        return banner
    except:
        return

def checkVulns(banner):

    if "FreeFloat Ftp Server (Version 1.00)" in banner:
        print "[+] FreeFloat FTP Server is vulnerable."
    elif "3Com 3CDaemon FTP Server Version 2.0" in banner:
        print "[+] 3CDaemon FTP Server is vulnerable."
    elif "Ability Server 2.34" in banner:
        print "[+] Ability FTP Server is vulnerable."
    elif "Sami FTP Server 2.0.2" in banner:
        print "[+] Sami FTP Server is vulnerable."
    else:
        print "[-] FTP Server not vulnerable."
    return

def main():

    ip1 = "192.168.95.148"
    ip2 = "192.168.95.149"
    ip3 = "192.168.95.150"
    port = 21
    
    banner1 = retBanner(ip1, port)
    banner2 = retBanner(ip2, port)
    banner3 = retBanner(ip3, port)

    if banner1:
        print "[+] " + ip1 + ": " + banner1.strip("\n")
        checkVulns(banner1)
    else:
        print "[-] " + ip1 + ": Gave us nothing."
    if banner2:
        print "[+] " + ip2 + ": " + banner2.strip("\n")
        checkVulns(banner2)
    else:
        print "[-] " + ip2 + ": Gave us nothing."
    if banner3:
        print "[+] " + ip3 + ": " + banner3.strip("\n")
        checkVulns(banner3)
    else:
        print "[-] " + ip3 + ": Gave us nothing."

if __name__=='__main__':
    main()
