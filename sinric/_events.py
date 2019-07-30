from time import time
from math import floor
from ._mainqueue import queue
from ._jsoncommands import JSON_COMMANDS
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
            if event_name == JSON_COMMANDS.get('SETPOWERSTATE'):
                self.logger.info('setPowerState Event Raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setPowerState",
                    "value": {
                        "state": data.get('state')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setpowerstate_event_response'])

            elif event_name == JSON_COMMANDS.get('SETPOWERLEVEL'):
                self.logger.info('setPowerLevel event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setPowerLevel",
                    "value": {
                        "powerLevel": data.get('powerLevel')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setPowerLevel_event_response'])


            elif event_name == JSON_COMMANDS.get('SETBRIGHTNESS'):
                self.logger.info('setBrightness event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setBrightness",
                    "value": {
                        "powerLevel": data.get('brightness')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setBrightness_event_response'])


            elif event_name == JSON_COMMANDS.get('SETCOLOR'):
                self.logger.info('setColor event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setColor",
                    "value": {
                        "color": {
                            "r": data.get('r'),
                            "g": data.get('g'),
                            "b": data.get('b')
                        }
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setColor_event_response'])


            elif event_name == JSON_COMMANDS.get('SETCOLORTEMPERATURE'):
                self.logger.info('setColor event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setColorTemperature",
                    "value": {
                        "colorTemperature": 2400
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setColorTemperature_event_response'])

            ##########################DOOR BELL EVENT####################################

            elif event_name == 'doorBellEvent':
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
                    "action": "setTemperature",
                    "value": {
                        "temperature": data.get('temperature'),
                        "humidity": data.get('humidity')
                    },
                    "cause": {
                        "type": "PERIODIC_POLL"
                    }

                }, 'temp_hum_event_response'])

            elif event_name == 'setThermostatMode':
                self.logger.info('Raised Thermostat event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setThermostatMode",
                    "value": {
                        "thermostatMode": data.get('Mode')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setThermostatMode_event_response'])

            elif event_name == 'setRangeValue':
                self.logger.info('Raised Range value event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setRangeValue",
                    "value": {
                        "rangeValue": data.get('rangeValue')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'setRangeValue_event_response'])



            elif event_name == 'motion':
                self.logger.info('Raised motion event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "motion",
                    "value": {
                        "state": data.get('state')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'motion_event_response'])


            elif event_name == 'setContactState':
                self.logger.info('Raised contact event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setContactState",
                    "value": {
                        "state": data.get('state')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }

                }, 'contact_event_response'])

            elif event_name == 'setVolume':
                self.logger.info('Raised set volume event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setVolume",
                    "value": {
                        "volume": data.get('volume')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'set_volume_event_response'])


            elif event_name == 'selectInput':
                self.logger.info('Raised select input event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "selectInput",
                    "value": {
                        "input": data.get('input')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'select_input_event_response'])


            elif event_name == 'mediaControl':
                self.logger.info('Media control event')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "mediaControl",
                    "value": {
                        "control": data.get('control')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'media_control_event_response'])

            elif event_name=='changeChannel':
                self.logger.info('Change channel event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "changeChannel",
                    "value": {
                        "channel": {
                            "name": data.get('name')
                        }
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                },'change_channel_event_response'])

            elif event_name == 'setBands':
                self.logger.info('Set Bands event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setBands",
                    "value": {
                        "bands": [
                            {
                                "name": data.get('name'),
                                "level":data.get('level')
                            }
                        ]
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                },'set_bands_event_response'])


            elif event_name == 'setMode':
                self.logger.info('Set Mode event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setMode",
                    "value": {
                        "mode": data.get('mode')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                },'set_mode_event_raised'])


            elif event_name == 'setLockState':
                self.logger.info('setLockState event raised')
                queue.put([{
                    "payloadVersion": 1,
                    "createdAt": floor(time()),
                    "messageId": str(uuid.uuid4()),
                    "deviceId": deviceId,
                    "type": "event",
                    "action": "setLockState",
                    "value": {
                        "state": data.get('state')
                    },
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
                    }
                }, 'set_lock_event_raised'])

        except Exception:
            self.logger.exception('Error Occurred')
