from time import time
from math import floor
from ._mainqueue import queue
import uuid

eventNames = {
    'door_bell_event': 'doorBellEvent',
    'th_event': 'temperatureHumidityEvent'
}


# noinspection PyBroadException
class Events:
    def __init__(self, connection, logger=None):
        self.connection = connection
        self.logger = logger

    # noinspection PyBroadException
    def raiseEvent(self, deviceId, event_name, data={}):
        try:
            if event_name == 'doorBellEvent':
                self.logger.info('Door Bell Event Raised')
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

                    }}, 'doorbell_event_response'])

            elif event_name == 'temperatureHumidityEvent':
                self.logger.info('Raised TH event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "temperature",
                    "value": {
                        "temperature": data.get('temperature'),
                        "humidity": data.get('humidity')
                    },
                    "cause": {
                        "type": "PERIODIC_POLL"
                    }

                }, 'temp_hum_event_response'])
        except Exception:
            self.logger.exception('Error Occurred')
