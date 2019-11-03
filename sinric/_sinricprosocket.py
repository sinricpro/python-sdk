"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

import websockets
import json
from ._mainqueue import queue
from ._cbhandler import CallBackHandler
from ._signature import Signature


class SinricProSocket(Signature):

    def __init__(self, appKey, deviceId, callbacks, enable_trace=False, logger=None, enable_track=False, secretKey=""):
        self.appKey = appKey
        self.secretKey = secretKey
        self.enable_track = enable_track
        self.logger = logger
        self.deviceIds = deviceId
        self.connection = None
        self.callbacks = callbacks
        self.callbackHandler = CallBackHandler(self.callbacks, enable_trace, self.logger, self.enable_track,
                                               secretKey=self.secretKey)
        self.enableTrace = enable_trace
        Signature.__init__(self, self.secretKey)

    async def connect(self):  # Producer
        self.connection = await websockets.client.connect('ws://ws.sinric.pro',
                                                          extra_headers={'appkey': self.appKey,
                                                                         'deviceids': ';'.join(self.deviceIds),
                                                                         'platform': 'python'},
                                                          ping_interval=30000, ping_timeout=10000)
        if self.connection.open:
            self.logger.info(f"{'Client Connected'}")
            return self.connection

    async def receiveMessage(self, connection):
        while True:
            try:
                message = await connection.recv()
                if self.enableTrace:
                    self.logger.info(f"Request : {message}")
                requestJson = json.loads(message)
                queue.put([requestJson, 'socket_response'])
            except websockets.exceptions.ConnectionClosed as e:
                self.logger.info('Connection with server closed')
                self.logger.exception(e)
                break

    async def handle(self, udp_client):
        while True:
            while queue.qsize() > 0:
                await self.callbackHandler.handleCallBacks(queue.get(), self.connection, udp_client)
