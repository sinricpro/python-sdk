import socket


class SinricProUdp:
    def __init__(self):
        self.udp_ip = "127.0.0.1"
        self.udp_port = 5005
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockServ.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockServ.bind((self.udp_ip, self.udp_port))

    def connect(self):
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockServ.bind((self.udp_ip, self.udp_port))
        return self.sockServ

    def handle(self):
        while True:
            data, addr = self.sockServ.recvfrom(1024)
            print("Message: ", data)
