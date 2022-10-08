from sinric import SinricPro 
import asyncio
from asyncio import sleep
from loguru import logger

APP_KEY = ''
APP_SECRET = ''
DEVICE_ID = ''
 
async def events():
    while True:
        client.event_handler.raiseEvent(DEVICE_ID, 'pushNotification', data={'alert': "Hello there"})
        await sleep(60) # Server will trottle / block IPs sending events too often.

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [DEVICE_ID], {}, event_callbacks=events, enable_log=True, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())
