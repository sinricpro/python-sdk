from sinric import SinricPro 
import asyncio
 
APP_KEY = ''
APP_SECRET = ''
GARAGEDOOR_ID = ''
 
def power_state(did, state):
    print(did, state)
    return True, did

def set_mode(did, state):
    print(did, state)
    return True, state

callbacks = {
    'setMode': set_mode,
    'onPowerState': power_state
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [GARAGEDOOR_ID], callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())
