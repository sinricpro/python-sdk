from sinric import SinricPro, SinricProConstants
import asyncio
from asyncio import sleep

APP_KEY = ""
APP_SECRET = ""
THERMOSTAT_ID = ""

def power_state(device_id, state):
    print('device_id: {} state: {}'.format(device_id, state))
    return True, state

def target_temperature(device_id, temperature):
    print('device_id: {} set temperature: {}'.format(device_id, temperature))
    return True, temperature

def set_thermostate_mode(device_id, thermostat_mode):
    print('device_id: {} set thermostat mode: {}'.format(device_id, thermostat_mode))
    return True, thermostat_mode

def mode_value(device_id, mode_value):
    print(device_id, mode_value)
    return True, mode_value

async def events():
    while True:
        # client.event_handler.raise_event(THERMOSTAT_ID, SinricProConstants.SET_THERMOSTAT_MODE, data= { SinricProConstants.MODE : SinricProConstants.THERMOSTAT_MODE_COOL})
        # client.event_handler.raise_event(THERMOSTAT_ID, SinricProConstants.SET_POWER_STATE, data= {SinricProConstants.STATE: SinricProConstants.POWER_STATE_OFF})
        # client.event_handler.raise_event(THERMOSTAT_ID, SinricProConstants.CURRENT_TEMPERATURE, data={'humidity': 75.3, 'temperature': 24})
        # Server will trottle / block IPs sending events too often.
        await sleep(60)

callbacks = {
    SinricProConstants.SET_POWER_STATE: power_state,
    SinricProConstants.TARGET_TEMPERATURE: target_temperature,
    SinricProConstants.SET_THERMOSTAT_MODE: set_thermostate_mode
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [THERMOSTAT_ID], callbacks, event_callbacks=events,
                       enable_log=True, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())