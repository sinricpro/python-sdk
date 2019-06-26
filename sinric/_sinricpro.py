import websockets as ws
from time import sleep
import json


async def Request(apiKey, deviceId, queue):  # Producer
    async with ws.connect(
            'ws://23.95.122.232:3001',
            extra_headers={'Authorization': apiKey, 'deviceids': deviceId}) as websocket:
        greeting = await websocket.recv()
        queue.put(greeting)
        # print('Command Received')


async def Process(queue):  # Consumer
    if queue.qsize() > 0:
        command = queue.get()
        jsonobj = json.loads(command)
        actions = jsonobj['actions']
        actionname = actions[0]['name']
        deviceid = jsonobj['did']
        print('Action : ', actionname, '  DeviceId : ', deviceid)

    else:
        print('Queue Empty')
        return
