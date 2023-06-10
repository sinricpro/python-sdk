from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
BLINDS_ID = ''


def set_power_state(device_id, state):
    print('device_id: {} state: {}'.format(device_id, state))
    return True, state


def set_range_value(device_id, value, instance_id):
    print('device_id: {} set to: {}'.format(device_id, value))
    return True, value, instance_id


callbacks = {
    SinricProConstants.SET_POWER_STATE: set_power_state,
    SinricProConstants.SET_RANGE_VALUE: set_range_value
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [BLINDS_ID], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

# client.event_handler.raise_event(BLINDS_ID, SinricProConstants.SET_RANGE_VALUE, data = {SinricProConstants.RANGE_VALUE: 30 })
# client.event_handler.raise_event(BLINDS_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_ON })
# client.event_handler.raise_event(BLINDS_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_OFF })
