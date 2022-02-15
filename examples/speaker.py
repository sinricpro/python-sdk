from sinric import SinricPro
import asyncio

APP_KEY = ''
APP_SECRET = ''
SPEAKER_ID = ''

def power_state(device_id, state):
    # Do Something
    print(device_id, state)
    return True, state

def set_bands(device_id, name, level):
    print(name, level)
    # Do Somethign
    return True, {'name': name, 'level': level}

def adjust_bands(device_id, name, level, direction):
    # Do something with level
    return True, {'name': name, 'level': level}

def reset_bands(device_id, band1, band2, band3):
    # Do something with reset
    return True

def set_mode(device_id, mode):
    # Do something with mode
    return True, mode

def set_mute(device_id, mute):
    # Muted : True, Not muted : False
    return True, mute

callbacks = {
    'powerState': power_state,
    'setBands': set_bands,
    'setMode': set_mode,
    'adjustBands': adjust_bands,
    'resetBands': reset_bands,
    'setMute': set_mute
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [SPEAKER_ID], callbacks, enable_log=True, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the speaker state on server. 
# client.event_handler.raiseEvent(speakerId, 'setBands',data={'name': '','level': 0})
# client.event_handler.raiseEvent(speakerId, 'setMode',data={'mode': ''})
