from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
DOORBELL_ID = ''

'''
DON'T FORGET TO TURN ON 'Doorbell Press' IN ALEXA APP
'''


async def events():
    while True:
        # client.event_handler.raise_event(DOORBELL_ID, SinricProConstants.DOORBELLPRESS)
        # await sleep(60) # Server will trottle / block IPs sending events too often.
        pass

callbacks = {}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [DOORBELL_ID], callbacks, event_callbacks=events,
                       enable_log=True, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

    # client.event_handler.raise_event(DOORBELL_ID, SinricProConstants.DOORBELLPRESS)
