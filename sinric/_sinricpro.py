"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

import asyncio
from ._sinricprosocket import SinricProSocket
from threading import Thread
from ._events import Events
from loguru import logger
import re
import sys

logger.add("{}.log".format("sinricpro_logfile"), rotation="10 MB")


class SinricPro:
    def __init__(self, api, deviceid, request_callbacks, event_callbacks=None, enable_log=False, restore_states=False,
                 secretKey=""):
        try:
            assert (self.verifyDeviceIdArr(deviceid))
            self.restore_states = restore_states
            self.apiKey = api
            self.secretKey = secretKey
            self.deviceid = deviceid
            self.logger = logger
            self.request_callbacks = request_callbacks
            self.socket = SinricProSocket(self.apiKey, self.deviceid, self.request_callbacks, enable_log, self.logger,
                                          self.restore_states, self.secretKey)
            self.connection = None
            self.event_callbacks = event_callbacks
            self.event_handler = Events(self.connection, self.logger, self.secretKey)
        except AssertionError as e:
            logger.error("Device Id verification failed")
            sys.exit(0)

    def verifyDeviceIdArr(self, deviceIdArr):
        Arr = deviceIdArr
        for i in Arr:
            res = re.findall(r'^[a-fA-F0-9]{24}$', i)
            if len(res) == 0:
                return False
        return True

    async def startUdpClient(udp_client):
        if(udp_client):
          await udp_client.listen()

    async def connect(self, udp_client=None, sleep=0):
        
        try:
            self.connection = await self.socket.connect()
            receiveMessageTask = asyncio.create_task(self.socket.receiveMessage(connection=self.connection))
            handleQueueTask = asyncio.create_task(self.socket.handleQueue(udp_client=udp_client))
            handleUdpQueueTask = asyncio.create_task(self.startUdpClient())
            await receiveMessageTask
            await handleQueueTask
            await handleUdpQueueTask
        except KeyboardInterrupt:
            self.logger.error('Keyboard interrupt')
        except Exception as e:
            self.logger.error(e)
        
