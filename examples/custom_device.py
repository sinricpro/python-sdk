from sinric import SinricPro 
import asyncio
 
APP_KEY = ''
APP_SECRET = ''
DEVICE_ID = ''
  
def power_state(device_id, state):
    print(device_id, state)
    return True, state

def range_value(device_id, range_value, instance_id):
    print(device_id, range_value, instance_id)
    return True, range_value, instance_id

def mode_value(device_id, mode_value, instance_id):
    print(device_id, mode_value, instance_id)
    return True, mode_value, instance_id
 
callbacks = {
    'powerState': power_state,
    'setRangeValue': range_value,
    'setMode': mode_value
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [DEVICE_ID], callbacks, enable_log=True, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())