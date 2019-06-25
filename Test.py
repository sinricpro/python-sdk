from sinric._sinricpro import Produce, Consume
import asyncio
from queue import Queue

apiKey = 'Api Key'
deviceId = 'Device Id'

if __name__ == '__main__':
    myq = Queue()
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(Produce(apiKey, deviceId, myq))
            asyncio.get_event_loop().run_until_complete(Consume(myq))
        except Exception as e:
            print(e)
