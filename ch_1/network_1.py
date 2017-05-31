import socket

socket.setdefaulttimeout(2)
# socket connection times out in 2 seconds if not established.

##

s = socket.socket()

##

s.connect(("192.168.95.148", 21))
##connecting the socket with ip: 192.168.95.148, port: 21.

ans = s.recv(1024) # read the next 1024 bytes on attached socket.
print ans
