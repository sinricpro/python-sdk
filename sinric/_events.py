from time import time
from math import floor
from ._mainqueue import queue

eventNames = {
    'door_bell_event': 'doorBellEvent'
}


# noinspection PyBroadException
class Events:
    def __init__(self, connection):
        self.connection = connection

    # noinspection PyBroadException
    def raiseEvent(self, deviceId, event_name):
        if event_name == 'doorBellEvent':
            print('Door bell Event Raised')
            queue.put([{
                "payloadVersion": 1,
                "createdAt": floor(time()),
                "messageId": "fca894e9-9c47-4447-9313-be4475508a8d",
                "deviceId": deviceId,
                "type": "event",
                "action": "DoorbellPress",
                "value": {
                    "state": "pressed"
                },
                "cause": {
                    "type": "PHYSICAL_INTERACTION"

                }}, 'event_response'])
