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
            self.connection = asyncio.get_event_loop().run_until_complete(self.socket.connect())
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

    def handle(self):
        tasks = [
            asyncio.ensure_future(self.socket.receiveMessage(self.connection)),
        ]

        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

    def handle_clients(self, handle, udp_client, sleep=0):
        asyncio.new_event_loop().run_until_complete(handle(udp_client,sleep))

    def handle_all(self, udp_client=None, sleep=0):
        try:
            t1 = Thread(target=self.handle_clients, args=(self.socket.handle, udp_client, sleep))
            t1.setDaemon(True)
            t1.start()
            if udp_client != None:
                print('Yes udp')
                t2 = Thread(target=udp_client.listen)
                t2.setDaemon(True)
                t2.start()
            if self.event_callbacks != None:
                t3 = Thread(target=self.event_callbacks['Events'])
                t3.setDaemon(True)
                t3.start()
            self.handle()
        except KeyboardInterrupt:
            self.logger.error("Keyboard Interrupt")
            sys.exit(1)
        except Exception as e:
            self.logger.error(str(e))
