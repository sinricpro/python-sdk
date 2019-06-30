from sinric.sinricpro import SinricPro
from credential import apiKey, deviceId

def powerState(did, state):
    print(did, state)
    return True


def powerLevel(did, state):
    print(did, state['value'])
    return True


callbacks = {
    'powerState': powerState,
    'powerLevel': powerLevel,
}

if __name__ == '__main__':
    client = SinricPro(apiKey, deviceId, callbacks)
    client.handle()
