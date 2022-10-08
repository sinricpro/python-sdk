from sinric import SinricPro
import asyncio

APP_KEY = ''
APP_SECRET = ''
LIGHT_ID = ''

def power_state(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)
    return True, state


def set_brightness(did, state):
    # Alexa set device brightness to 40%
    print(did, 'BrightnessLevel : ', state)
    return True, state


def adjust_brightness(did, state):
    # Alexa increase/decrease device brightness by 44
    print(did, 'AdjustBrightnessLevel : ', state)

    return True, state


def set_color(did, r, g, b):
    # Alexa set device color to Red/Green
    print(did, 'Red: ', r, 'Green: ', g, 'Blue : ', b)

    return True


def set_color_temperature(did, value):
    print(did, value)
    return True


def increase_color_temperature(device_id, value):
    return True, value


def decrease_color_temperature(device_id, value):
    return True, value


callbacks = {
    'powerState': power_state,
    'setBrightness': set_brightness,
    'adjustBrightness': adjust_brightness,
    'setColor': set_color,
    'setColorTemperature': set_color_temperature,
    'increaseColorTemperature': increase_color_temperature,
    'decreaseColorTemperature': decrease_color_temperature
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [LIGHT_ID], callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the light state on server. 
# client.event_handler.raiseEvent(lightId, 'setPowerState',data={'state': 'On'})
# client.event_handler.raiseEvent(device_id1, 'setColor',data={'r': 0,'g': 0,'b': 0})
# client.event_handler.raiseEvent(device_id1, 'setColorTemperature',data={'colorTemperature': 2400})
