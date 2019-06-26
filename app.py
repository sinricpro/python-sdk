from sinric._sinricpro import Request, Process
import asyncio
from queue import Queue

apiKey = ''
deviceId = ''


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
