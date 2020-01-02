"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from time import time, sleep
from ._mainqueue import queue
from ._jsoncommands import JSON_COMMANDS
import uuid
from ._signature import Signature

eventNames = {
    'door_bell_event': 'doorBellEvent',
    'th_event': 'temperatureHumidityEvent'
}


# noinspection PyBroadException
class Events(Signature):
    def __init__(self, connection, logger=None, secretKey=""):
        self.connection = connection
        self.logger = logger
        self.secretKey = secretKey
        Signature.__init__(self, self.secretKey)

    # noinspection PyBroadException
    def raiseEvent(self, deviceId, event_name, data=None):
        if data is None:
            data = {}
        try:
            def jsnHandle(action, deviceId, value, typeI="PHYSICAL_INTERACTION") -> dict:
                header = {
                    "payloadVersion": 2,
                    "signatureVersion": 1
                }

                payload = {
                    "action": action,
                    "cause": {
                        "type": typeI
                    },
                    "createdAt": int(time()),
                    "deviceId": deviceId,
                    "replyToken": str(uuid.uuid4()),
                    "type": "event",
                    "value": value
                }
                signature = self.getSignature(payload)
                return {"header": header, "payload": payload, "signature": signature}

            if event_name == JSON_COMMANDS.get('SETPOWERSTATE'):
                queue.put([jsnHandle("setPowerState", deviceId, {"state": data.get("state", "Off")}),
                           'setpowerstate_event_response'])



            elif event_name == JSON_COMMANDS.get('SETPOWERLEVEL'):
                queue.put([jsnHandle("setPowerLevel", deviceId, {
                    "powerLevel": data.get('powerLevel')
                }), 'setPowerLevel_event_response'])


            elif event_name == JSON_COMMANDS.get('SETBRIGHTNESS'):
                queue.put([jsnHandle("setBrightness", deviceId, {
                    "powerLevel": data.get('brightness')
                }), 'setBrightness_event_response'])


            elif event_name == JSON_COMMANDS.get('SETCOLOR'):
                queue.put([jsnHandle("setColor", deviceId, {
                    "color": {
                        "r": data.get('r'),
                        "g": data.get('g'),
                        "b": data.get('b')
                    }
                }), 'setColor_event_response'])



            elif event_name == JSON_COMMANDS.get('SETCOLORTEMPERATURE'):
                queue.put([jsnHandle("setColorTemperature", deviceId, {
                    "colorTemperature": 2400
                }), 'setColorTemperature_event_response'])


            ##########################DOOR BELL EVENT####################################

            elif event_name == 'doorBellEvent':
                queue.put([jsnHandle("DoorbellPress", deviceId, {
                    "state": "pressed"
                }), 'doorbell_event_response'])


            elif event_name == 'temperatureHumidityEvent':
                queue.put([jsnHandle("currentTemperature", deviceId, {
                    "temperature": round(data.get('temperature'), 1),
                    "humidity": round(data.get('humidity'), 1),
                }, typeI="PERIODIC_POLL"), 'temp_hum_event_response'])


            elif event_name == 'setThermostatMode':
                queue.put([jsnHandle("setThermostatMode", deviceId, {
                    "thermostatMode": data.get('Mode')
                }), 'setThermostatMode_event_response'])


            elif event_name == 'setRangeValue':
                queue.put([jsnHandle("setRangeValue", deviceId, {
                    "rangeValue": data.get('rangeValue')
                }), 'setRangeValue_event_response'])


            elif event_name == 'motion':
                queue.put([jsnHandle("motion", deviceId, {
                    "state": data.get('state')
                }), 'motion_event_response'])



            elif event_name == 'setContactState':
                queue.put([jsnHandle("setContactState", deviceId, {
                    "state": data.get('state')
                }), 'contact_event_response'])



            elif event_name == 'setVolume':
                queue.put([jsnHandle("setVolume", deviceId, {
                    "volume": data.get('volume')
                }), 'set_volume_event_response'])


            elif event_name == 'selectInput':
                queue.put([jsnHandle("selectInput", deviceId, {
                    "input": data.get('input')
                }), 'select_input_event_response'])



            elif event_name == 'mediaControl':
                queue.put([jsnHandle("mediaControl", deviceId, {
                    "control": data.get('control')
                }), 'media_control_event_response'])



            elif event_name == 'changeChannel':
                queue.put([jsnHandle("changeChannel", deviceId, {
                    "channel": {
                        "name": data.get('name')
                    }
                }), 'change_channel_event_response'])


            elif event_name == 'setBands':
                queue.put([jsnHandle("setBands", deviceId, {
                    "bands": [
                        {
                            "name": data.get('name'),
                            "level": data.get('level')
                        }
                    ]
                }), 'set_bands_event_response'])


            elif event_name == 'setMode':
                queue.put([jsnHandle("setMode", deviceId, {
                    "mode": data.get('mode')
                }), 'set_mode_event_response'])


            elif event_name == 'setLockState':
                queue.put([jsnHandle("setLockState", deviceId, {
                    "state": data.get('state')
                }), 'set_lock_event_response'])


            elif event_name == 'resetBands':
                queue.put([jsnHandle("resetBands", deviceId, {
                    "bands": [
                        {
                            "name": "BASS",
                            "level": 0
                        },
                        {
                            "name": "MIDRANGE",
                            "level": 0
                        },
                        {
                            "name": "TREBLE",
                            "level": 0
                        }]
                }), 'reset_bands_event_response'])


            elif event_name == 'setMute':
                queue.put([jsnHandle("setMute", deviceId, {
                    "mute": data.get('mute', False)
                }), 'reset_bands_event_response'])


        except Exception:
            self.logger.exception('Error Occurred')
