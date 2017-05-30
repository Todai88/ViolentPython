import zipfile
import optparse
from threading import Thread



def extract_file(file, password):

    try:
        file.extractall(pwd=password)
        print("[+] Found password '" + password + "'")
    except:
        pass


def main():

    parser = optparse.OptionParser("usage%prog" +\
                                   "-f <zipfile> -d <dictionaryfile>")
    parser.add_option('-f', dest='zname', type='string',
                      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', \
                      help='specify dictionary file')
    (options, args) = parser.parse_args()

    if (options.zname == None) | (options.dname == None):
        print parser.usage
        raise SystemExit
    else:
        zname = options.zname
        dname = options.dname
    zFile = zipfile.ZipFile(zname)

    with open(dname) as file:
        for line in file:
            password = line.strip('\n')
            t = Thread(target=extract_file, args=(zFile, password))
            t.start()

if __name__ == '__main__':
    main()
