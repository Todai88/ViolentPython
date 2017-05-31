from pexpect import pxssh

def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before + " " + s.buffer)

def connect(host, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except:
        print('[-] Error connecting...')
        raise SystemExit

s = connect('127.0.0.1', 'root', 'hexa3dec1')
send_command(s, 'grep root /etc/shadow')
