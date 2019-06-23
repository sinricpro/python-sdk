from sinric._sinricpro import Produce, Consume
import asyncio
import urllib.request as urllib
from queue import Queue
import socket


def if_network_available():
    try:
        urllib.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.URLError as err:
        return False


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

apiKey = 'Api Key'.encode('ascii')

if __name__ == '__main__':
    myq = Queue()
    while True:
        try:

            if if_network_available():
                asyncio.get_event_loop().run_until_complete(Produce(apiKey, myq))
                asyncio.get_event_loop().run_until_complete(Consume(myq))
            else:
                print('Listening on UDP')
                data, addr = sock.recvfrom(1024)
                print(data)
        except:
            print('Error')
