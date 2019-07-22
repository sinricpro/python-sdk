import websockets
import json
from sinric._mainqueue import queue
from sinric._cbhandler import CallBackHandler


class SinricProSocket:

    def __init__(self, apiKey, deviceId, callbacks, enable_trace=False, logger=None):
        self.apiKey = apiKey
        self.logger = logger
        self.deviceIds = deviceId
        self.connection = None
        self.callbacks = callbacks
        self.callbackHandler = CallBackHandler(self.callbacks, enable_trace, self.logger)
        self.enableTrace = enable_trace

    async def connect(self):  # Producer
        self.connection = await websockets.client.connect('ws://23.95.122.232:3001',
                                                          extra_headers={'Authorization': self.apiKey,
                                                                         'deviceids': self.deviceIds},
                                                          ping_interval=30000, ping_timeout=10000)
        if self.connection.open:
            self.logger.info(f"{'Client Connected'}")
            return self.connection

    async def receiveMessage(self, connection):
        while True:
            try:
                message = await connection.recv()
                if self.enableTrace:
                    self.logger.info(f"Request : {message}")
                requestJson = json.loads(message)
                queue.put([requestJson, 'socket_response'])
            except websockets.exceptions.ConnectionClosed as e:
                self.logger.info('Connection with server closed')
                self.logger.exception(e)
                break

    async def handle(self, udp_client):
        while True:
            while queue.qsize() > 0:
                await self.callbackHandler.handleCallBacks(queue.get(), self.connection, udp_client)
