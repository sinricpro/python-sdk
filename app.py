from sinric._sinricpro import Request, Process
import asyncio
from queue import Queue

apiKey = 'Api'
deviceId1 = 'id1'
deviceId2 = 'Id2'
deviceId = ';'.join([deviceId1, deviceId2])


async def main():
    try:
        prod = loop.create_task(Request(apiKey, deviceId, myq))
        cons = loop.create_task(Process(myq))
        await asyncio.wait([prod, cons])
        return
    except Exception as e:
        print(e)


if __name__ == '__main__':
    myq = Queue()
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        except Exception as e:
            print(e)
