import socket
from sinric.command.mainqueue import queue
from sinric.callback_handler.cbhandler import CallBackHandler


class SinricProUdp:
    def __init__(self, callbacks1):
        self.callbacks = callbacks1
        self.udp_ip = "127.0.0.1"
        self.udp_port = 3333
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockServ.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockServ.bind((self.udp_ip, self.udp_port))
        self.callbackHandler = CallBackHandler(self.callbacks)

    def connect(self):
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockServ.bind((self.udp_ip, self.udp_port))
        return self.sockServ

    def listen(self):
        while True:
            data, addr = self.sockServ.recvfrom(1024)
            # queue.put(data.decode('ascii'))
            print("Message: ", data)