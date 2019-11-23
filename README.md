#  Python3 SDK for Sinric Pro
[![](https://img.shields.io/pypi/format/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) 
[![](https://img.shields.io/pypi/v/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) 
[![Downloads](https://pepy.tech/badge/sinricpro)](https://pypi.org/project/sinricpro/)
[![](https://img.shields.io/github/repo-size/sinricpro/Python-SDK.svg)](https://github.com/sinricpro/Python-SDK) 
[![](https://img.shields.io/badge/author-Dhanush-orange.svg)](https://github.com/imdhanush)

### Check the examples [here](https://github.com/sinricpro/Python-Examples)

### Install
       pip install sinricpro --user
   
### Upgarde
       pip install sinricpro --upgrade --user
   
### Simple example
```python
from sinric import SinricPro
from sinric import SinricProUdp
from time import sleep

appKey = '' # d89f1***-****-****-****-************
secretKey = '' # f44d1d31-1c19-****-****-9bc96c34b5bb-d19f42dd-****-****-****-************
device1 = '' # 5d7e7d96069e275ea9******
device2 = '' # 5d80ac5713fa175e99******
deviceIdArr = [device1,device2]

def Events():
    while True:
        # Select as per your requirements
        # REMOVE THE COMMENTS TO USE
        # client.event_handler.raiseEvent(device1, 'setPowerState',data={'state': 'On'})
        pass
def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)
    return True, state


eventsCallbacks={
    "Events": Events
}

callbacks = {
'powerState': onPowerState
}

if __name__ == '__main__':
    client = SinricPro(appKey, deviceIdArr, callbacks,event_callbacks=eventsCallbacks, enable_trace=False,restore_states=True,secretKey=secretKey)
    udp_client = SinricProUdp(callbacks,deviceIdArr,enable_trace=False)  # Set it to True to start logging request Offline Request/Response
    client.handle_all(udp_client)

```

### Credentials file (credential.py)

```python
appKey = 'd89f1***-****-****-****-************'
secretKey = 'f44d1d31-1c19-****-****-9bc96c34b5bb-d19f42dd-****-****-****-************'
deviceId1 = '5d7e7d96069e275ea9******'
deviceId2 = ' 5j7e7d96069e275ea9******'
deviceId3 = ' 5d7e7d96069e275ea9******'
lock = ' 5d7e7d96069e275ea9******'
deviceIdArr = [deviceId1, deviceId2, deviceId3, lock]
```

### Pro Switch [Demo](https://github.com/sinricpro/Python-Examples/tree/master/pro_switch_example):
```python
from sinric import SinricPro
from sinric import SinricProUdp
from credentials import appKey, deviceIdArr, secretKey
from time import sleep

def Events():
    while True:
        # Select as per your requirements
        # REMOVE THE COMMENTS TO USE
        # client.event_handler.raiseEvent(device1, 'setPowerState',data={'state': 'On'})
        pass
def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)
    return True, state


eventsCallbacks={
    "Events": Events
}

callbacks = {
'powerState': onPowerState
}

if __name__ == '__main__':
    client = SinricPro(appKey, deviceIdArr, callbacks,event_callbacks=eventsCallbacks, restore_states=False,secretKey=secretKey)
    udp_client = SinricProUdp(callbacks,deviceIdArr,enable_trace=False)  # Set it to True to start logging request Offline Request/Response
    client.handle_all(udp_client)
```
