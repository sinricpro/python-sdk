"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from websockets import client
from websockets.exceptions import ConnectionClosed
import json
from ._queues import queue
from ._callback_handler import CallBackHandler
from ._signature import Signature
from time import time
import asyncio
import pkg_resources


class SinricProSocket(Signature):

    def __init__(self, app_key, device_id, callbacks, enable_trace=False, logger=None, restore_states=False,
                 secret_key="", loop_delay=0.5):
        self.app_key = app_key
        self.secret_key = secret_key
        self.restore_states = restore_states
        self.logger = logger
        self.device_ids = device_id
        self.connection = None
        self.callbacks = callbacks
        self.loop_delay = loop_delay

        self.callbackHandler = CallBackHandler(self.callbacks, enable_trace, self.logger, self.restore_states,
                                               secret_key=self.secret_key)
        self.enableTrace = enable_trace
        Signature.__init__(self, self.secret_key)

    async def connect(self):  # Producer
        sdk_version = pkg_resources.require("sinricpro")[0].version
        self.connection = await client.connect('wss://ws.sinric.pro',
                                               extra_headers={'appkey': self.app_key,
                                                              'deviceids': ';'.join(self.device_ids),
                                                              'platform': 'python',
                                                              'sdkversion': sdk_version,
                                                              'restoredevicestates': (
                                                                  'true' if self.restore_states else 'false')},
                                               ping_interval=30000, ping_timeout=10000)
        if self.connection.open:
            self.logger.success("Connected :)")
            timestamp = await self.connection.recv()
            if (int(time()) - json.loads(timestamp).get('timestamp') > 60000):
                self.logger.warning('Timestamp is not in sync. Please check your system time.')
            return self.connection

    async def receive_message(self, connection):
        while True:
            try:
                message = await connection.recv()
                if self.enableTrace:
                    self.logger.info(f"Request : {message}")
                request = json.loads(message)
                queue.put([request, 'socket_response', 'request_response'])
                await asyncio.sleep(self.loop_delay)
            except ConnectionClosed as e:
                self.logger.info('Connection with server closed')
                raise e

    async def handle_queue(self):
        while True:
            await asyncio.sleep(self.loop_delay)

            while queue.qsize() > 0:
                await self.callbackHandler.handle_callbacks(queue.get(), self.connection, None)
