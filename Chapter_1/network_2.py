import socket

try:
    socket.setdefaulttimeout(10)

    s = socket.socket()

    s.connect(("192.168.95.148", 21))

    ans = s.recv(1024)
    if ("FreeFloat Ftp Server (Version 1.00)" in ans):
        print "[+] FreeFloat Ftp Server is vulnerable."
    else:
        print "Nothing detected."

except Exception, e:
    print "[-] Error = " + str(e)
