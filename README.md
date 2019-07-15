#  Python3 SDK for Sinric Pro
[![](https://img.shields.io/pypi/format/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/pypi/v/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/github/repo-size/sinricpro/Python-Examples.svg)](https://github.com/sinricpro/Python-Examples) [![](https://img.shields.io/badge/author-Dhanush-orange.svg)](https://github.com/imdhanush)

### Python-2.7 not supported
### Get your credentials from [sinric-pro-website](https://sinric.pro)

### Install
        python3 -m pip install sinricpro --user
   
### Upgarde
        python3 -m pip install sinricpro --upgrade --user

### Pro Switch [Demo](https://github.com/sinricpro/Python-Examples/tree/master/pro_switch_example):
```python
from sinric import SinricPro
from sinric import SinricProUdp
from credentials import apiKey, deviceId


def power_state(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state['state'])
    return True, state['state']


callbacks = {
'powerState': power_state
}

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, callbacks, enable_trace=False)
    udp_client = SinricProUdp(callbacks)
    udp_client.enableUdpPrint(False)  # Set it to True to start printing request UDP JSON
    client.handle_all(udp_client)
```

### Pro Dim Switch [Demo](https://github.com/sinricpro/Python-Examples/tree/master/pro_dim_switch_example):
```python
from sinric import SinricPro
from sinric import SinricProUdp
from credentials import apiKey, deviceId


def power_state(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state['state'])
    return True, state['state']


def set_power_level(did, state):
    # Alexa, set power level of device to 50%
    print(did, 'PowerLevel : ', state)
    return True, state


def adjust_power_level(did, state):
    # Alexa increase/decrease power level by 30
    print(did, 'PowerLevelDelta : ', state)
    return True, state


callbacks = {
    'powerState': power_state,
    'setPowerLevel': set_power_level,
    'adjustPowerLevel': adjust_power_level
}

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, callbacks, enable_trace=False)
    udp_client = SinricProUdp(callbacks)
    udp_client.enableUdpPrint(False)  # Set it to True to start printing request UDP JSON
    client.handle_all(udp_client)
```

### Pro Light [Demo](https://github.com/sinricpro/Python-Examples/tree/master/pro_light_example):
```python
from sinric import SinricPro
from credentials import apiKey, deviceId
from sinric import SinricProUdp


def power_state(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state['state'])
    return True, state['state']


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


def increase_color_temperature(deviceId, value):
    return True, value


def decrease_color_temperature(deviceId, value):
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
    client = SinricPro(apiKey, deviceId, callbacks, enable_trace=False)
    udp_client = SinricProUdp(callbacks)
    udp_client.enableUdpPrint(False)  # Set it to True to start printing request UDP JSON
    client.handle_all(udp_client)
```