from sinric import SinricPro 
import asyncio
 
APP_KEY = '40f5fb6c-2cf7-4877-a788-f9c6a3be59ba'
APP_SECRET = 'a841dc8b-e5d8-4148-9ac6-c3c918cf7f44-11bd4d83-daaa-489e-b271-5bec3f994cd7'
SWITCH_ID = '6340be8cf695e6bcd84a9f2d'

def power_state(device_id, state):
    print(device_id, state)
    return True, state
 
callbacks = {
    'powerState': power_state
}
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [SWITCH_ID], callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the power state on server. 
# client.event_handler.raiseEvent(tvId, 'setPowerState',data={'state': 'On'})
