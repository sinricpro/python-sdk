from time import time
from math import floor
from ._mainqueue import queue
import uuid

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
                "messageId": str(uuid.uuid4()),
                "deviceId": deviceId,
                "type": "event",
                "action": "DoorbellPress",
                "value": {
                    "state": "pressed"
                },
                "cause": {
                    "type": "PHYSICAL_INTERACTION"

                }}, 'event_response'])
