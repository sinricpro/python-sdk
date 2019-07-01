from sinric.sinricpro import SinricPro
from credential import apiKey, deviceId


def powerState(did, state):
    print(did, state)
    return True


def powerLevel(did, state):
    print(did, 'PowerLevel : ', state['value'])
    return True


def brightnessLevel(did, state):
    print(did, 'BrightnessLevel : ', state['brightness'])
    return True


callbacks = {
    'powerState': powerState,
    'powerLevel': powerLevel,
    'brightnessLevel': brightnessLevel
}

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, callbacks)
    while True:
        client.handle()
