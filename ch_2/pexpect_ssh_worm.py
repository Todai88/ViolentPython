import pexpect

PROMPT = ['#', '>>>', '>', '\$']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT) 
    print(child.before + " " + child.buffer)

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    strcon = 'ssh ' + user + '@' + host
    child = pexpect.spawn(strcon)

    ret = child.expect([pexpect.TIMEOUT, ssh_newkey,\
                        '[P|p]assword:'])

    if ret == 0:
        print('[-] Error connecting')
        return

    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT,\
                            '[P|p]assword:'])
        if ret == 0:
            print('[-] Error Connecting...')
            return
        child.sendline(password)
        child.expect(PROMPT)
        return child

    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = 'localhost'
    user = 'root'
    password = 'hexa3dec1'
    child = connect(user, host, password)
    send_command(child, 'grep root /etc/shadow')

if __name__ == '__main__':
    main()