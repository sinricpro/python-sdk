from sinric.sinricpro import SinricPro
from credential import apiKey, deviceId
from sinric.communication.sinricproudp import SinricProUdp
from threading import Thread

tempStates = {
    'powerLevel': 0,
    'brightnessLevel': 0
}


def powerState(did, state):
    print(did, state['state'])
    return True, state['state']


def setPowerLevel(did, state):
    print(did, 'PowerLevel : ', state)
    tempStates['powerLevel'] = state
    return True, tempStates['powerLevel']


def adjustPowerLevel(did, state):
    print(did, 'PowerLevelDelta : ', state)

    tempStates['powerLevel'] += state

    if tempStates['powerLevel'] > 100:
        tempStates['powerLevel'] = 100
    elif tempStates['powerLevel'] < 0:
        tempStates['powerLevel'] = 0
    return True, tempStates['powerLevel']


def setBrightness(did, state):
    print(did, 'BrightnessLevel : ', state)
    tempStates['brightnessLevel'] = state
    return True, tempStates['brightnessLevel']


def adjustBrightness(did, state):
    print(did, 'AdjustBrightnessLevel : ', state)

    tempStates['brightnessLevel'] += state
    if tempStates['brightnessLevel'] > 100:
        tempStates['brightnessLevel'] = 100
    elif tempStates['brightnessLevel'] < 0:
        tempStates['brightnessLevel'] = 0

    return True, tempStates['brightnessLevel']


def setColor(did, r, g, b):
    print(did, 'Red: ', r, 'Green: ', g, 'Blue : ', b)

    return True


def setColorTemperature(did, value):
    print(did, value)
    return True


callbacks = {
    'powerState': powerState,
    'setPowerLevel': setPowerLevel,
    'adjustPowerLevel': adjustPowerLevel,
    'setBrightness': setBrightness,
    'adjustBrightness': adjustBrightness,
    'setColor': setColor,
    'setColorTemperature': setColorTemperature
}

if __name__ == '__main__':
    wsClient = SinricPro(apiKey, deviceId, callbacks)
    udpClient = SinricProUdp(callbacks)
    t2 = Thread(target=udpClient.listen)
    t2.setDaemon(True)
    t2.start()
    while True:
        wsClient.handle()
        pass