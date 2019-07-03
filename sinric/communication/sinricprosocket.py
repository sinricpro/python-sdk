import websockets
import json
from sinric.command.mainqueue import queue
from sinric.callback_handler.cbhandler import CallBackHandler
from time import sleep
import asyncore


class SinricProSocket(asyncore.dispatcher):

    def __init__(self, apiKey, deviceId, callbacks):
        asyncore.dispatcher.__init__(self)
        self.apiKey = apiKey
        self.deviceIds = deviceId
        self.connection = None
        self.callbacks = callbacks
        self.callbackHandler = CallBackHandler(self.callbacks)

    async def connect(self):  # Producer
        self.connection = await websockets.client.connect('ws://23.95.122.232:3001',
                                                          extra_headers={'Authorization': self.apiKey,
                                                                         'deviceids': self.deviceIds},
                                                          ping_interval=30000, ping_timeout=10000)
        if self.connection.open:
            print('Client Connected')
            return self.connection

    async def sendMessage(self, message):
        await self.connection.send(message)

    async def receiveMessage(self, connection):
        try:
            message = await connection.recv()
            queue.put(json.loads(message))
        except websockets.exceptions.ConnectionClosed:
            print('Connection with server closed')

    async def handle(self):
        # sleep(6)
        while queue.qsize() > 0:
            await self.callbackHandler.handleCallBacks(queue.get(), self.connection)
        return
