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
        self.eventSleepTime = 2
        self.logger = logger
        self.secretKey = secretKey
        Signature.__init__(self, self.secretKey)

    # noinspection PyBroadException
    def raiseEvent(self, deviceId, event_name, data=None):
        if data is None:
            data = {}
        try:
            def jsnHandle(action, deviceId, value) -> dict:
                header = {
                    "payloadVersion": 2,
                    "signatureVersion": 1
                }

                payload = {
                    "action": action,
                    "cause": {
                        "type": "PHYSICAL_INTERACTION"
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
                self.logger.info('setPowerState Event Raised')

                queue.put([jsnHandle("setPowerState", deviceId, {"state": data.get("state", "Off")}),
                           'setpowerstate_event_response'])
                sleep(self.eventSleepTime)


            elif event_name == JSON_COMMANDS.get('SETPOWERLEVEL'):
                self.logger.info('setPowerLevel event raised')

                queue.put([jsnHandle("setPowerLevel", deviceId, {
                    "powerLevel": data.get('powerLevel')
                }), 'setPowerLevel_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == JSON_COMMANDS.get('SETBRIGHTNESS'):
                self.logger.info('setBrightness event raised')

                queue.put([jsnHandle("setBrightness", deviceId, {
                    "powerLevel": data.get('brightness')
                }), 'setBrightness_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == JSON_COMMANDS.get('SETCOLOR'):
                self.logger.info('setColor event raised')

                queue.put([jsnHandle("setColor", deviceId, {
                    "color": {
                        "r": data.get('r'),
                        "g": data.get('g'),
                        "b": data.get('b')
                    }
                }), 'setColor_event_response'])
                sleep(self.eventSleepTime)


            elif event_name == JSON_COMMANDS.get('SETCOLORTEMPERATURE'):

                self.logger.info('setColorTemperature event raised')
                queue.put([jsnHandle("setColorTemperature", deviceId, {
                    "colorTemperature": 2400
                }), 'setColorTemperature_event_response'])
                sleep(self.eventSleepTime)

            ##########################DOOR BELL EVENT####################################

            elif event_name == 'doorBellEvent':
                self.logger.info('Door Bell Event Raised')
                queue.put([jsnHandle("DoorbellPress", deviceId, {
                    "state": "pressed"
                }), 'doorbell_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'temperatureHumidityEvent':
                self.logger.info('Raised TH event')
                queue.put([jsnHandle("currentTemperature", deviceId, {
                    "humidity": data.get('humidity'),
                    "temperature": data.get('temperature')
                }), 'temp_hum_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'setThermostatMode':
                self.logger.info("Raised Thermostat event")
                queue.put([jsnHandle("setThermostatMode", deviceId, {
                    "thermostatMode": data.get('Mode')
                }), 'setThermostatMode_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'setRangeValue':
                self.logger.info('Raised Range value event')

                queue.put([jsnHandle("setRangeValue", deviceId, {
                    "rangeValue": data.get('rangeValue')
                }), 'setRangeValue_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'motion':
                self.logger.info('Raised motion event')

                queue.put([jsnHandle("motion", deviceId, {
                    "state": data.get('state')
                }), 'motion_event_response'])
                sleep(self.eventSleepTime)


            elif event_name == 'setContactState':
                self.logger.info('Raised contact event')

                queue.put([jsnHandle("setContactState", deviceId, {
                    "state": data.get('state')
                }), 'contact_event_response'])
                sleep(self.eventSleepTime)


            elif event_name == 'setVolume':
                self.logger.info('Raised set volume event')

                queue.put([jsnHandle("setVolume", deviceId, {
                    "volume": data.get('volume')
                }), 'set_volume_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'selectInput':
                self.logger.info('Raised select input event')

                queue.put([jsnHandle("selectInput", deviceId, {
                    "input": data.get('input')
                }), 'select_input_event_response'])
                sleep(self.eventSleepTime)


            elif event_name == 'mediaControl':
                self.logger.info('Media control event')

                queue.put([jsnHandle("mediaControl", deviceId, {
                    "control": data.get('control')
                }), 'media_control_event_response'])
                sleep(self.eventSleepTime)


            elif event_name == 'changeChannel':
                self.logger.info('Change channel event raised')

                queue.put([jsnHandle("changeChannel", deviceId, {
                    "channel": {
                        "name": data.get('name')
                    }
                }), 'change_channel_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'setBands':
                self.logger.info('Set Bands event raised')
                queue.put([jsnHandle("setBands", deviceId, {
                    "bands": [
                        {
                            "name": data.get('name'),
                            "level": data.get('level')
                        }
                    ]
                }), 'set_bands_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'setMode':
                self.logger.info('Set Mode event raised')
                queue.put([jsnHandle("setMode", deviceId, {
                    "mode": data.get('mode')
                }), 'set_mode_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'setLockState':
                self.logger.info('setLockState event raised')

                queue.put([jsnHandle("setLockState", deviceId, {
                    "state": data.get('state')
                }), 'set_lock_event_response'])
                sleep(self.eventSleepTime)

            elif event_name == 'resetBands':
                self.logger.info('resetBands event raised')

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
                sleep(self.eventSleepTime)

            elif event_name == 'setMute':
                self.logger.info('setMute event raised')

                queue.put([jsnHandle("setMute", deviceId, {
                    "mute": data.get('mute', False)
                }), 'reset_bands_event_response'])
                sleep(self.eventSleepTime)

        except Exception:
            self.logger.exception('Error Occurred')
