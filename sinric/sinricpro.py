import asyncio
from sinric.communication.sinricprosocket import SinricProSocket
from sinric.communication.sinricproudp import SinricProUdp


class SinricPro:
    def __init__(self, api, deviceid, callbacks):
        self.apiKey = api
        self.deviceid = deviceid
        self.callbacks = callbacks
        self.socket = SinricProSocket(self.apiKey, self.deviceid, self.callbacks)
        self.udp_obj = SinricProUdp()
        # self.loop = asyncio.get_event_loop()
        self.connection = asyncio.get_event_loop().run_until_complete(self.socket.connect())
        # self.udp_connection = asyncio.get_event_loop().run_until_complete(self.udp_obj.connect())
        # self.connection = None

    def handle(self):
        # self.connection =
        tasks = [
            #
            # self.socket.receiveMessage(self.connection),
            # self.socket.handle(),
            # self.udp_obj.handle()
            asyncio.ensure_future(self.socket.handle()),
            asyncio.ensure_future(self.socket.receiveMessage(self.connection)),
        ]

        # asyncio.get_event_loop().run_until_complete(self.socket.receiveMessage(self.connection))
        # asyncio.get_event_loop().run_until_complete(self.socket.handle())
        # asyncio.get_event_loop().run_until_complete(self.udp_obj.handle(self.udp_connection))
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
        # asyncio.get_event_loop().run_until_complete()
