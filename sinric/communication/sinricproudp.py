import socket
from sinric.command.mainqueue import queue
from sinric.callback_handler.cbhandler import CallBackHandler
import json
import struct


class SinricProUdp:
    def __init__(self, callbacks1):
        self.callbacks = callbacks1
        self.udp_ip = '224.9.9.9'
        self.udp_port = 3333
        self.address = (self.udp_ip, 3333)
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockServ.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockServ.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                 struct.pack("4sl", socket.inet_aton(self.udp_ip), socket.INADDR_ANY))
        self.sockServ.bind(self.address)
        self.callbackHandler = CallBackHandler(self.callbacks)

    def listen(self):
        while True:
            data, addr = self.sockServ.recvfrom(1024)
            print(data)
            queue.put(json.loads(data.decode('utf-8')))
