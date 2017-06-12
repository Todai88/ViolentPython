import crypt
import hashlib

def testPass(cryptopass):

	salt = cryptopass[0:2]

	with open('dictionary.txt', 'r') as dictfile:
		for word in dictfile:
			word = word.strip('\n')
			cryptword = crypt.crypt(word, salt)

			if (cryptword == cryptopass or hashlib.sha512(word) == cryptword):
				print('[+] Found password: ' + word + '\n')
				return

		print('[-] Password not found\n')
		return

def main ():
	with open('password.txt') as passfile:
		for line in passfile.readlines():
			if(':' in line):
				user = line.split(':')[0]
				cryptpass = line.split(':')[1],strip(' ')
				print('[*] Cracking Password for: ' + user)
				testPass(cryptpass)

if __name__ == "__main__":
	main()
