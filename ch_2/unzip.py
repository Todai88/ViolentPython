import zipfile


def testPass(password, zFile):
    try:
        zFile.extractall(pwd=password)
        return password
    except Exception as e:
        return

def main():
    filename = 'evil.zip'
    zFile = zipfile.ZipFile(filename)
    with open('dictionary.txt', 'r') as file:
        for line in file:
            password = line.strip('\n')
            guess = testPass(password, zFile)
            if guess:
                print("[+] Found the password to '" + filename + "'. It was: '" + password + "'")
                return True

if __name__ == '__main__':
    if not main():
        print("[-] Could not find password for file")

