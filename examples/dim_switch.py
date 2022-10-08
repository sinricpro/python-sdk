from sinric import SinricPro 
import asyncio
 
APP_KEY = ''
APP_SECRET = ''
DIM_SWITCH_ID = ''


def power_state(device_id, state):
    print(device_id, state)
    return True, state
 
def power_level(device_id, powerLevel):
    print(device_id, powerLevel)
    return True, powerLevel

callbacks = {
    'powerState': power_state,
    'setPowerLevel' : power_level
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [DIM_SWITCH_ID], callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

 # client.event_handler.raiseEvent(deviceId1, 'setPowerState',data={'state': 'On'})