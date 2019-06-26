from sinric._sinricpro import Request, Process
import asyncio
from queue import Queue

# deviceId = 'Device Id'
# apiKey = 'Api Key'

deviceId = '5d13927d5d37dc4a5b9c74e5'
apiKey = 'c963892e-1116-47bb-be34-14ff95c4ce00'


async def main():
    prod = loop.create_task(Request(apiKey, deviceId, myq))
    cons = loop.create_task(Process(myq))
    await asyncio.wait([prod, cons])
    return prod, cons


if __name__ == '__main__':
    myq = Queue()
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
