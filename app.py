from sinric.communication.sinricprosocket import SinricProSocket
from sinric.sinricpro import SinricPro
import asyncio

apiKey = 'c963892e-1116-47bb-be34-14ff95c4ce00'
deviceId1 = '5d126916eb7e894a699e0ae0'
deviceId2 = '5d13927d5d37dc4a5b9c74e5'
deviceId = ';'.join([deviceId1, deviceId2])

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId)
    client.add()
    client.handle()
