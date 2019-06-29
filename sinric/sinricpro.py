import asyncio
from sinric.communication.sinricprosocket import SinricProSocket


class SinricPro:
    def __init__(self, api, deviceid, callbacks):
        self.apiKey = api
        self.deviceid = deviceid
        self.callbacks = callbacks
        self.socket = SinricProSocket(self.apiKey, self.deviceid, self.callbacks)
        self.loop = asyncio.get_event_loop()
        self.connection = self.loop.run_until_complete(self.socket.connect())

    def handle(self):
        tasks = [
            asyncio.ensure_future(self.socket.handle()),
            asyncio.ensure_future(self.socket.receiveMessage(self.connection)),
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))