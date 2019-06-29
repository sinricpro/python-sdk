from sinric.sinricpro import SinricPro
from credential import apiKey, deviceId


def powerState(did, state):
    print(did, state)
    return


def powerLevel(did, state):
    print(did, state['value'])
    return


callbacks = {
    'powerState': powerState,
    'powerLevel': powerLevel,
}

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, callbacks)
    client.handle()
