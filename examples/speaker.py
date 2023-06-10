from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
SPEAKER_ID = ''


def power_state(device_id, state):
    print('device_id: {} lock state: {}'.format(device_id, state))
    return True, state


def set_bands(device_id, name, level):
    print('device_id: {}, name: {}, name: {}'.format(device_id, name, level))
    return True, {'name': name, 'level': level}


def adjust_bands(device_id, name, level, direction):
    print('device_id: {}, name: {}, name: {}, direction: {}'.format(
        device_id, name, level, direction))
    return True, {'name': name, 'level': level}


def reset_bands(device_id, band1, band2, band3):
    print('device_id: {}, band1: {}, band2: {}, band3: {}'.format(
        device_id, band1, band2, band3))
    return True


def set_mode(device_id, mode):
    print('device_id: {} mode: {}'.format(device_id, mode))
    return True, mode


def set_mute(device_id, mute):
    print('device_id: {} mute: {}'.format(device_id, mute))
    return True, mute


def set_volume(device_id, volume):
    print('device_id: {} volume: {}'.format(device_id, volume))
    return True, volume


callbacks = {
    SinricProConstants.SET_POWER_STATE: power_state,
    SinricProConstants.SET_BANDS: set_bands,
    SinricProConstants.SET_MODE: set_mode,
    SinricProConstants.ADJUST_BANDS: adjust_bands,
    SinricProConstants.RESET_BANDS: reset_bands,
    SinricProConstants.SET_MUTE: set_mute,
    SinricProConstants.SET_VOLUME: set_volume
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [SPEAKER_ID], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the speaker state on server.
# client.event_handler.raise_event(speakerId, SinricProConstants.SET_BANDS, data = {'name': '','level': 0})
