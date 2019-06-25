import websockets as ws


async def Produce(apiKey, deviceId, queue):
    async with ws.connect(
            'ws://23.95.122.232:3001',
            extra_headers={'Authorization': apiKey, 'deviceids': deviceId}) as websocket:
        greeting = await websocket.recv()
        queue.put(greeting)


async def Consume(queue):
    if queue.qsize() > 0:
        print(queue.get())
    else:
        return
