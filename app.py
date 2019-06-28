from sinric.communication._sinricprosocket import SinricPro
import asyncio

apiKey = 'Api Key'
deviceId1 = 'Device Id 1'
deviceId2 = 'Device Id 2'
deviceId = ';'.join([deviceId1, deviceId2])

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId)
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(client.connect())
    tasks = [
        asyncio.ensure_future(client.handle()),
        asyncio.ensure_future(client.heartbeat(connection)),
        asyncio.ensure_future(client.receiveMessage(connection)),
    ]

    loop.run_until_complete(asyncio.wait(tasks))
