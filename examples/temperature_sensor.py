from sinric import SinricPro
from time import sleep
import asyncio

APP_KEY = ''
APP_SECRET = ''
TEMPERATURE_SENSOR_ID = ''

def power_state(did, state):
    print(did, state)
    return True, state
 
def events():
    while True:
        client.event_handler.raiseEvent(TEMPERATURE_SENSOR_ID, 'temperatureHumidityEvent', data={'humidity': 75.3, 'temperature': 24})
        sleep(60) # Server will trottle / block IPs sending events too often.
        pass

events_callbacks = {
    "Events": events
}

callbacks = {
    'powerState': power_state
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [TEMPERATURE_SENSOR_ID], callbacks, event_callbacks=events_callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the temperature on server. 
#client.event_handler.raiseEvent(temperatureSensorDeviceId, 'temperatureHumidityEvent', data={'humidity': 75.3, 'temperature': 24})