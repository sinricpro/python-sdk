from sinric import SinricPro 
import asyncio
 
APP_KEY = ''
APP_SECRET = ''
DOORBELL_ID = ''

'''
DON'T FORGET TO TURN ON 'Doorbell Press' IN ALEXA APP
'''

def Events():
    while True:
        # client.event_handler.raiseEvent(doorBellId, eventNames['door_bell_event'])
        pass

callbacks = {}

eventsCallbacks = {
    'Events': Events
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [DOORBELL_ID], callbacks, event_callbacks=eventsCallbacks, enable_log=True, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect()) 