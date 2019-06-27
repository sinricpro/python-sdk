import websockets as ws
import json
from ._piactions import PiActions


async def Request(apiKey, deviceId, queue):  # Producer
    async with ws.connect(
            'ws://23.95.122.232:3001',
            extra_headers={'Authorization': apiKey, 'deviceids': deviceId},ping_interval=30000,
            ping_timeout=10000) as websocket:
        pp = websocket.ping(data='H')
        await pp
        greeting = await websocket.recv()
        queue.put(greeting)
        pong_waiter = await websocket.ping()
        await pong_waiter
        # print('Command Received')


async def Process(queue):  # Consumer
    if queue.qsize() > 0:
        command = queue.get()
        jsonobj = json.loads(command)
        actions = jsonobj['actions']
        actionname = actions[0]['name']
        deviceid = jsonobj['did']
        piAction = PiActions(actionname, deviceid)
        piAction.printData()
        # print('Action : ', actionname, '  DeviceId : ', deviceid)

    else:
        print('Queue Empty')
        return
