import asyncio
from sinric._sinricprosocket import SinricProSocket
from threading import Thread


class SinricPro:
    def __init__(self, api, deviceid, callbacks, enable_trace=False):
        self.apiKey = api
        self.deviceid = deviceid
        self.callbacks = callbacks
        self.socket = SinricProSocket(self.apiKey, self.deviceid, self.callbacks, enable_trace)
        self.connection = asyncio.get_event_loop().run_until_complete(self.socket.connect())

    def handle(self):
        tasks = [
            asyncio.ensure_future(self.socket.receiveMessage(self.connection)),
        ]

        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

    def handle_clients(self, handle, udp_client):
        asyncio.new_event_loop().run_until_complete(handle(udp_client))

    def handle_all(self, udp_client):
        t1 = Thread(target=self.handle_clients, args=(self.socket.handle, udp_client))
        t3 = Thread(target=udp_client.listen)
        t1.setDaemon(True)
        t3.setDaemon(True)
        t1.start()
        t3.start()
        self.handle()
