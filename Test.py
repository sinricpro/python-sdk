import websockets as ws
import asyncio
import logging as log
from time import sleep
from threading import Thread
from queue import Queue


class Sinric:
    def __init__(self, apiKey, deviceId):
        self.apiKey = apiKey
        self.myQueue = Queue()
        self.deviceId = deviceId

    async def listen(self):
        async with ws.connect(
                'ws://23.95.122.232:3001',
                extra_headers={'Authorization:': self.apiKey, 'deviceids:': self.deviceId}) as websocket:
            greeting = await websocket.recv()
            self.myQueue.put(greeting)

    def Action(self):
        while self.myQueue.qsize() > 0:
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


apiKey = '6125c4a0-2d5b-4d0b-a0c6-70774d6c0b69'
deviceId = '5d11133035d6f2121c7dccb6'

if __name__ == '__main__':
    obj = Sinric(apiKey, deviceId)
    obj.initialize()

# from sinric._sinricpro import SinricPro, Consumer
# import multiprocessing as mp
#
# apiKey = '6125c4a0-2d5b-4d0b-a0c6-70774d6c0b69'
# deviceId = '5d11133035d6f2121c7dccb6'
# if __name__ == '__main__':
#     with mp.Pool(3) as pool:
#         m = mp.Manager()
#         data_q = m.Queue()
#         p = pool.map_async(SinricPro, (apiKey, deviceId, data_q,))
#         c = pool.map_async(Consumer, (data_q,))
