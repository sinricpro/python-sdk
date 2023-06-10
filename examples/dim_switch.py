from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
DIM_SWITCH_ID = ''


def power_state(device_id, state):
    print('device_id: {} state: {}'.format(device_id, state))
    return True, state


def power_level(device_id, power_level):
    print('device_id: {} power level: {}'.format(device_id, power_level))
    return True, power_level


callbacks = {
    SinricProConstants.SET_POWER_STATE: power_state,
    SinricProConstants.SET_POWER_LEVEL: power_level
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [DIM_SWITCH_ID], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

    # client.event_handler.raise_event(DIM_SWITCH_ID, SinricProConstants.SET_POWER_LEVEL, data = {SinricProConstants.POWER_LEVEL: 50 })
    # client.event_handler.raise_event(DIM_SWITCH_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_ON })
    # client.event_handler.raise_event(DIM_SWITCH_ID, SinricProConstants.SET_POWER_STATE, data = {SinricProConstants.STATE: SinricProConstants.POWER_STATE_OFF })
