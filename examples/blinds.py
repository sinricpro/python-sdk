from sinric import SinricPro 
import asyncio

APP_KEY = ''
APP_SECRET = ''
BLINDS_ID = ''

def power_state(device_id, state): 
    print(device_id, state)
    return True, state

def range_value(device_id,state):
    print(device_id, state)
    return True, state

callbacks = {
    'powerState': power_state,
    'setRangeValue': range_value
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [BLINDS_ID], callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())