portList = []
portList.append(21)
portList.append(80)
portList.append(443)
portList.append(25)
print(portList)

##

portList.sort()
print portList

##

pos = portList.index(80)
print '[+] There are ' + str(pos) + ' ports to scan before 80.'

##

portList.remove(443)
print portList

cnt = len(portList)
print '[+] Scanning ' + str(cnt) + ' ports.'
