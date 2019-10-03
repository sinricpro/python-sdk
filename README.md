#  Python3 SDK for Sinric Pro
[![](https://img.shields.io/pypi/format/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/pypi/v/sinricpro.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/github/repo-size/sinricpro/Python-SDK.svg)](https://github.com/sinricpro/Python-SDK) [![](https://img.shields.io/badge/author-Dhanush-orange.svg)](https://github.com/imdhanush)

# Python-2.7 not supported

### Check the examples [here](https://github.com/sinricpro/Python-Examples)

### Install
        python3 -m pip install sinricpro --user
   
### Upgarde
        python3 -m pip install sinricpro --upgrade --user
### Virtual Env
        python3 -m pip install virtualenv --user
    
        python3 -m virtualenv sinricenv
    
        source sinricenv/bin/activate
    
        pip install sinricpro
    

### Pro Switch [Demo](https://github.com/sinricpro/Python-Examples/tree/master/pro_switch_example):
```python
from sinric import SinricPro
from sinric import SinricProUdp
from credentials import appKey, deviceId, secretKey
from time import sleep

def Events():
    while True:
        # Select as per your requirements
        # REMOVE THE COMMENTS TO USE
        # client.event_handler.raiseEvent(deviceId1, 'setPowerState',data={'state': 'On'})
        sleep(2) #Sleep for 2 seconds 

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
    client = SinricPro(appKey, deviceId, callbacks,event_callbacks=eventsCallbacks, enable_trace=False,secretKey=secretKey)
    udp_client = SinricProUdp(callbacks,deviceId)
    udp_client.enableUdpPrint(False)  # Set it to True to start logging request Offline Request/Response
    client.handle_all(udp_client)
```
