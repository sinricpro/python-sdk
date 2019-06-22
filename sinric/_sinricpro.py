import websockets as ws
import asyncio
import logging as log
from time import sleep
from base64 import b64encode as enc
from threading import Thread
from queue import Queue
from ._sinricprocommand import SinricProCommand


class Sinric:
    def __init__(self, apiKey):
        # self.sinricPro = SinricProCommand
        self.apiKey = apiKey.encode('ascii')
        self.myQueue = Queue()

    async def listen(self):
        async with ws.connect(
                'ws://iot.sinric.com',
                extra_headers={'Authorization:': enc(b'apikey:' + self.apiKey).decode('ascii')}) as websocket:
            greeting = await websocket.recv()
            self.myQueue.put(greeting)

    def Action(self):
        sleep(6)
        print(self.myQueue.get())

    async def performAction(self):
        if self.myQueue.qsize() > 0:
            Thread(target=self.Action).start()

        else:
            return

    def initialize(self):
        while True:
            asyncio.get_event_loop().run_until_complete(self.listen())
            asyncio.get_event_loop().run_until_complete(self.performAction())
