from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
SWITCH_ID_1 = ''
SWITCH_ID_2 = ''


def power_state(device_id, state):
    if device_id == SWITCH_ID_1:
        print('device_id: {} state: {}'.format(device_id, state))
    elif device_id == SWITCH_ID_2:
        print('device_id: {} state: {}'.format(device_id, state))
    else:
        print("device_id not found!")

    return True, state


callbacks = {
    SinricProConstants.SET_POWER_STATE: power_state
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [SWITCH_ID_1, SWITCH_ID_2], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

    # To update the power state on server.
    # client.event_handler.raise_event(SWITCH_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_ON })
    # client.event_handler.raise_event(SWITCH_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_OFF })
