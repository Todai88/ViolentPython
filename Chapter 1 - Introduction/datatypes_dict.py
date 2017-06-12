services = {'ftp' : 21, 'ssh' : 22, 'smtp' : 25, 'http' : 80}
services.keys()

##

services.items()

##

services.has_key('ftp')

##

services['ftp']

##

print "[+] Found vuln with FTP on port " + str(services['ftp'])
