"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

import socket
from ._mainqueue import queue
import json
import struct


class SinricProUdp:
    def __init__(self, callbacks_udp, deviceIdArr,enable_trace=False):
        self.callbacks = callbacks_udp
        self.deviceIdArr = deviceIdArr
        self.enablePrint = enable_trace
        self.udp_ip = '224.9.9.9'
        self.udp_port = 3333
        self.address = ('', self.udp_port)
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockServ.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockServ.bind(self.address)
        self.sockServ.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                 struct.pack("4sl", socket.inet_aton(self.udp_ip), socket.INADDR_ANY))

    def sendResponse(self, data, sender):
        self.sockServ.sendto(data, sender)

    def listen(self):
        while True:
            data, addr = self.sockServ.recvfrom(1024)
            jsonData = json.loads(data.decode('ascii'))
            if jsonData.get('payload', None).get('deviceId', None) in self.deviceIdArr:
                queue.put([jsonData, 'udp_response', addr])
            else:
                print('Invalid Device id')
            if self.enablePrint:
                print(data)
                print('UDP senderID : ', addr)
