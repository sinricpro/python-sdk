import websockets as ws
from base64 import b64encode as enc


async def Produce(apiKey, queue):
    async with ws.connect(
            'ws://iot.sinric.com',
            extra_headers={'Authorization:': enc(b'apikey:' + apiKey).decode('ascii')}) as websocket:
        greeting = await websocket.recv()
        queue.put(greeting)


async def Consume(queue):
    if queue.qsize() > 0:
        print(queue.get())
    else:
        return
