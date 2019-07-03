import asyncio
from sinric.communication.sinricprosocket import SinricProSocket


class SinricPro:
    def __init__(self, api, deviceid, callbacks):
        self.apiKey = api
        self.deviceid = deviceid
        self.callbacks = callbacks
        self.socket = SinricProSocket(self.apiKey, self.deviceid, self.callbacks)
        self.connection = asyncio.get_event_loop().run_until_complete(self.socket.connect())

    def get_ws_connection(self):
        return self.connection

    def handle(self):
        tasks = [
            # asyncio.ensure_future(self.socket.handle()),
            asyncio.ensure_future(self.socket.receiveMessage(self.connection)),
        ]

        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
