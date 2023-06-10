from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
GARAGEDOOR_ID = ''


def power_state(device_id, state):
    print('device_id: {} state: {}'.format(device_id, state))
    return True, device_id


def set_mode(device_id, state, instance_id):
    print('device_id: {} mode: {}'.format(device_id, state))
    return True, state, instance_id


callbacks = {
    SinricProConstants.SET_MODE: set_mode,
    SinricProConstants.SET_POWER_STATE: power_state
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [GARAGEDOOR_ID], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

    # client.event_handler.raise_event(GARAGEDOOR_ID, SinricProConstants.SET_MODE, data = {SinricProConstants.MODE: SinricProConstants.OPEN })
    # client.event_handler.raise_event(GARAGEDOOR_ID, SinricProConstants.SET_MODE, data = {SinricProConstants.MODE: SinricProConstants.CLOSE })
