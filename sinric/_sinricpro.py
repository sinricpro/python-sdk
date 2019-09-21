import asyncio
from sinric._sinricprosocket import SinricProSocket
from threading import Thread
from sinric._events import Events
from loguru import logger

logger.add("{}.log".format("sinricpro_logfile"), rotation="10 MB")


class SinricPro:
    def __init__(self, api, deviceid, request_callbacks, event_callbacks=None, enable_trace=False, enable_track=False,secretKey = ""):
        self.enable_track = enable_track
        self.apiKey = api
        self.secretKey = secretKey
        self.deviceid = deviceid
        self.logger = logger
        self.request_callbacks = request_callbacks
        self.socket = SinricProSocket(self.apiKey, self.deviceid, self.request_callbacks, enable_trace, self.logger,
                                      self.enable_track,self.secretKey)
        self.connection = asyncio.get_event_loop().run_until_complete(self.socket.connect())
        self.event_callbacks = event_callbacks
        self.event_handler = Events(self.connection, self.logger,self.secretKey)

    def handle(self):
        tasks = [
            asyncio.ensure_future(self.socket.receiveMessage(self.connection)),
        ]

        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

    def handle_clients(self, handle, udp_client):
        asyncio.new_event_loop().run_until_complete(handle(udp_client))

    def handle_all(self, udp_client):
        t1 = Thread(target=self.handle_clients, args=(self.socket.handle, udp_client))
        t2 = Thread(target=udp_client.listen)
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()
        if self.event_callbacks != None:
            t3 = Thread(target=self.event_callbacks['Events'])
            t3.setDaemon(True)
            t3.start()
        self.handle()
