"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

import asyncio
import socket
from socket import AF_INET, SOCK_DGRAM
from ._queues import queue
import json
from asyncio import sleep
import struct


class EchoServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, enablePrint, deviceIdArr=[]) -> None:
        super().__init__()
        self.enablePrint = enablePrint
        self.deviceIdArr = deviceIdArr

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        jsonData = json.loads(data.decode('ascii'))
        if jsonData.get('payload', None).get('deviceId', None) in self.deviceIdArr:
            queue.put([jsonData, 'udp_response', addr])
        else:
            print('Invalid Device id')
        if self.enablePrint:
            print(data)
            print('UDP senderID : ', addr)


class SinricProUdp:
    def __init__(self, callbacks_udp, deviceIdArr, enable_trace=False, loop_delay=0.5, loopInstance=None):
        self.callbacks = callbacks_udp
        self.deviceIdArr = deviceIdArr
        self.enablePrint = enable_trace
        self.loopInstance = loopInstance
        self.loop_delay = loop_delay if loop_delay > 0 else 0.5
        self.udp_ip = '224.9.9.9'
        self.udp_port = 3333
        self.address = ('', self.udp_port)
        self.sockServ = socket.socket(AF_INET, SOCK_DGRAM)
        self.sockServ.bind(self.address)
        self.sockServ.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                 struct.pack("4sl", socket.inet_aton(self.udp_ip), socket.INADDR_ANY))

    def sendResponse(self, data, sender):
        self.sockServ.sendto(data, sender)

    async def listen(self):
        await self.loopInstance.create_datagram_endpoint(
            lambda: EchoServerProtocol(
                enablePrint=self.enablePrint, deviceIdArr=self.deviceIdArr),
            local_addr=None, remote_addr=None, sock=self.sockServ)
        while True:
            await asyncio.sleep(self.loop_delay)
