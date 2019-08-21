#  Python3 SDK for Sinric Pro
[![](https://img.shields.io/pypi/format/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/pypi/v/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/github/repo-size/sinricpro/Python-SDK.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/badge/author-Dhanush-orange.svg)](https://github.com/imdhanush)

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


def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)
    return True, state


callbacks = {
'powerState': onPowerState
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


def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)
    return True, state


def onSetPowerLevel(did, state):
    # Alexa, set power level of device to 50%
    print(did, 'PowerLevel : ', state)
    return True, state


def onAdjustPowerLevel(did, state):
    # Alexa increase/decrease power level by 30
    print(did, 'PowerLevelDelta : ', state)
    return True, state


callbacks = {
    'powerState': onPowerState,
    'setPowerLevel': onSetPowerLevel,
    'adjustPowerLevel': onAdjustPowerLevel
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


def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)
    return True, state


def onSetBrightness(did, state):
    # Alexa set device brightness to 40%
    print(did, 'BrightnessLevel : ', state)
    return True, state


def onAdjustBrightness(did, state):
    # Alexa increase/decrease device brightness by 44
    print(did, 'AdjustBrightnessLevel : ', state)

    return True, state


def onSetColor(did, r, g, b):
    # Alexa set device color to Red/Green
    print(did, 'Red: ', r, 'Green: ', g, 'Blue : ', b)

    return True


def onSetColor_temperature(did, value):
    print(did, value)
    return True


def onIncreaseColorTemperature(deviceId, value):
    return True, value


def onDecreaseColorTemperature(deviceId, value):
    return True, value


callbacks = {
    'powerState': onPowerState,
    'setBrightness': onSetBrightness,
    'adjustBrightness': onAdjustBrightness,
    'setColor': onSetColor,
    'setColorTemperature': onSetColor_temperature,
    'increaseColorTemperature': onIncreaseColorTemperature,
    'decreaseColorTemperature': onDecreaseColorTemperature
}

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, callbacks, enable_trace=False)
    udp_client = SinricProUdp(callbacks)
    udp_client.enableUdpPrint(False)  # Set it to True to start printing request UDP JSON
    client.handle_all(udp_client)
```

### Pro DoorBell [Demo](https://github.com/sinricpro/Python-Examples/tree/master/pro_doorbell_example):
```python
from sinric import SinricPro
from credentials import apiKey, deviceId, doorBellId
from sinric import SinricProUdp
from sinric import eventNames
from time import sleep

'''
DON'T FORGET TO TURN ON 'Doorbell Press' IN ALEXA APP
'''


def door_bell_event():
    # while True:
    client.event_handler.raiseEvent(doorBellId, eventNames['door_bell_event'])
    sleep(1)


request_callbacks = {}

event_callbacks = {
    'door_bell_event': door_bell_event
}
if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, request_callbacks, event_callbacks, enable_trace=True)
    udp_client = SinricProUdp(request_callbacks)
    udp_client.enableUdpPrint(False)  # Set it to True to start printing request UDP JSON
    client.handle_all(udp_client)
```
