from winreg import *

def val2addr(val):
    if val == None:
        return "[!] No MAC [!]"
    return ':'.join('{:02X}'.format(b) for b in val)
    # if val:
    #     address = ""
    #     for ch in val:
    #         if(not int(ch)):
    #             address += "%02x " % ord(ch)
    #             address = address.strip(' ').replace(' ', ':')[0: 17]
    #         else:
    #             address += str(ch)
    #     return address
    # return "[!] No MAC [!]"

def print_networks():
    net = u"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"+\
          "\\NetworkList\\Signatures\\Unmanaged"
    print(str(HKEY_LOCAL_MACHINE) + net)
    key = OpenKey(HKEY_LOCAL_MACHINE, net, 0, (KEY_WOW64_64KEY + KEY_READ))
    print('\n[*] Networks You have Joined:\n')

    for network in range(100):
        try:
            guid = EnumKey(key, network)
            netkey = OpenKey(key, str(guid))
            mac = QueryValueEx(netkey, 'DefaultGatewayMac')[0]
            mac = val2addr(mac)
            network_name = QueryValueEx(netkey, 'Description')[0]
            print("[+] Network Name: " + network_name + "[+] Mac: " + mac)
            CloseKey(netkey)
        except Exception as e:
            print(e)
            break

def main():
    print_networks()

if __name__ == '__main__':
    main()

# def val2addr(val):
#     return ':'.join('{:02X}'.format(b) for b in val)
#     # addr = ''
#     # for ch in val:
#     #     addr += '%02x '% ord(ch)
#     #     addr = addr.strip(' ').replace(' ', ':')[0:17]
#     # return addr