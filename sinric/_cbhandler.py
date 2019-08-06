from sinric._powerController import PowerController
from sinric._brightnessController import BrightnessController
from sinric._jsoncommands import JSON_COMMANDS
from sinric._powerLevelController import PowerLevel
from sinric._colorController import ColorController
from sinric._colorTemperature import ColorTemperatureController
from sinric._thermostatController import ThermostateMode
from sinric._rangeValueController import RangeValueController
from sinric._temperatureController import TemperatureController
from sinric._tvcontorller import TvController
import json
from time import time
from math import floor


# noinspection PyBroadException
class CallBackHandler(PowerLevel, PowerController, BrightnessController, ColorController, ColorTemperatureController,
                      ThermostateMode, RangeValueController, TemperatureController, TvController):
    def __init__(self, callbacks, trace_bool, logger):
        PowerLevel.__init__(self, 0)
        BrightnessController.__init__(self, 0)
        PowerController.__init__(self, 0)
        RangeValueController.__init__(self, 0)
        ColorController.__init__(self, 0)
        ThermostateMode.__init__(self, 0)
        TemperatureController.__init__(self, 0)
        TvController.__init__(self, 0)
        ColorTemperatureController.__init__(self, 0, [2200, 2700, 4000, 5500, 7000])
        self.callbacks = callbacks
        self.logger = logger
        self.trace_response = trace_bool

    async def handleCallBacks(self, dataArr, connection, udp_client):
        jsn = dataArr[0]
        Trace = dataArr[1]
        if jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETPOWERSTATE']:
            try:
                resp, state = await self.powerState(jsn, self.callbacks['powerState'])
                response = {
                    "payloadVersion": 1,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get(JSON_COMMANDS.get('MESSAGEID')),
                    "success": True,
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "setPowerState",
                    "value": {
                        "state": state
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                        # await connection.send(json.dumps(response2))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETPOWERLEVEL']:
            try:
                resp, value = await self.setPowerLevel(jsn, self.callbacks['setPowerLevel'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "setPowerLevel",
                    "value": {
                        "powerLevel": value
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['ADJUSTPOWERLEVEL']:
            try:
                resp, value = await self.adjustPowerLevel(jsn,
                                                          self.callbacks['adjustPowerLevel'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": jsn[JSON_COMMANDS['ACTION']],
                    "value": {"powerLevel": value}}
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETBRIGHTNESS']:
            try:
                resp, value = await self.setBrightness(jsn, self.callbacks['setBrightness'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "deviceAttributes": "",
                    "type": "response",
                    "action": "setBrightness",
                    "value": {"brightness": value}}
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['ADJUSTBRIGHTNESS']:
            try:
                resp, value = await self.adjustBrightness(jsn, self.callbacks['adjustBrightness'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "deviceAttributes": "",
                    "type": "response",
                    "action": "adjustBrightness",
                    "value": {
                        "brightness": value
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETCOLOR']:
            try:
                resp = await self.setColor(jsn, self.callbacks['setColor'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "setColor",
                    "value": {
                        "color": {
                            "r": jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLOR']][JSON_COMMANDS['COLOR_R']],
                            "g": jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLOR']][JSON_COMMANDS['COLOR_G']],
                            "b": jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLOR']][JSON_COMMANDS['COLOR_B']]
                        }
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETCOLORTEMPERATURE']:
            try:
                resp = await self.setColorTemperature(jsn, self.callbacks['setColorTemperature'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "setColorTemperature",
                    "value": {
                        "colorTemperature": jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLORTEMPERATURE']]
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['INCREASECOLORTEMPERATURE']:
            try:
                resp, value = await self.increaseColorTemperature(jsn, self.callbacks['increaseColorTemperature'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "increaseColorTemperature",
                    "value": {
                        "colorTemperature": value
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['DECREASECOLORTEMPERATURE']:
            try:
                resp, value = await self.decreaseColorTemperature(jsn, self.callbacks['decreaseColorTemperature'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "decreaseColorTemperature",
                    "value": {
                        "colorTemperature": value
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETTHERMOSTATMODE']:
            try:
                resp, value = await self.setThermostateMode(jsn, self.callbacks['setThermostatMode'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "setThermostatMode",
                    "value": {
                        "thermostatMode": value
                    }
                }
                # Value can be "HEAT", "COOL" or "AUTO"
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception("Error Occurred")

        elif jsn.get(JSON_COMMANDS.get('ACTION')) == JSON_COMMANDS.get('SETRANGEVALUE'):
            try:
                resp, value = await self.setRangeValue(jsn, self.callbacks.get('setRangeValue'))
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "setRangeValue",
                    "value": {
                        "rangeValue": value
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')



        elif jsn.get(JSON_COMMANDS.get('ACTION')) == JSON_COMMANDS.get('ADJUSTRANGEVALUE'):
            try:
                resp, value = await self.setRangeValue(jsn, self.callbacks.get('adjustRangeValue'))
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    "type": "response",
                    "action": "adjustRangeValue",
                    "value": {
                        "rangeValue": value
                    }
                }
                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')

        elif jsn.get(JSON_COMMANDS.get('ACTION')) == JSON_COMMANDS.get('TARGETTEMPERATURE'):
            try:
                resp, value = await  self.targetTemperature(jsn, self.callbacks.get('targetTemperature'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "type": "response",
                    "action": "targetTemperature",
                    "value": {
                        "temperature": value.get('temperature'),
                        "schedule": {
                            "duration": value.get('duration') | ""
                        }
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')

        elif jsn.get(JSON_COMMANDS.get('ACTION')) == JSON_COMMANDS.get('ADJUSTTEMPERATURE'):
            try:
                resp, value = await self.targetTemperature(jsn, self.callbacks.get('adjustTemperature'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "adjustTemperature",
                    "value": {
                        "temperature": value
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')


        elif jsn.get(JSON_COMMANDS.get('ACTION')) == 'setVolume':
            try:
                resp, value = await self.setVolume(jsn, self.callbacks.get('setVolume'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "setVolume",
                    "value": {
                        "volume": value
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')



        elif jsn.get(JSON_COMMANDS.get('ACTION')) == 'adjustVolume':
            try:
                resp, value = await self.adjustVolume(jsn, self.callbacks.get('adjustVolume'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "adjustVolume",
                    "value": {
                        "volume": value
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')



        elif jsn.get(JSON_COMMANDS.get('ACTION')) == 'mediaControl':
            try:
                resp, value = await self.mediaControl(jsn, self.callbacks.get('mediaControl'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "mediaControl",
                    "value": {
                        "control": value
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')

        elif jsn.get(JSON_COMMANDS.get('ACTION')) == 'selectInput':
            try:
                resp, value = await self.selectInput(jsn, self.callbacks.get('selectInput'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "selectInput",
                    "value": {
                        "input": value
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')


        elif jsn.get(JSON_COMMANDS.get('ACTION')) == 'changeChannel':
            try:
                resp, value = await self.changeChannel(jsn, self.callbacks.get('changeChannel'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "changeChannel",
                    "value": {
                        "channel": {
                            "name": value
                        }
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')


        elif jsn.get(JSON_COMMANDS.get('ACTION')) == 'skipChannels':
            try:
                resp, value = await self.skipChannels(jsn, self.callbacks.get('skipChannels'))

                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "createdAt": floor(time()),
                    "deviceId": jsn.get(JSON_COMMANDS.get('DEVICEID')),
                    'clientId': jsn.get(JSON_COMMANDS.get('CLIENTID')),
                    'messageId': jsn.get('MESSAGEID'),
                    "deviceAttributes": [],
                    "type": "response",
                    "action": "skipChannels",
                    "value": {
                        "channel": {
                            "name": value
                        }
                    }
                }

                if resp:
                    if self.trace_response:
                        self.logger.info(f"Response : {json.dumps(response)}")
                    if Trace == 'socket_response':
                        await connection.send(json.dumps(response))
                    elif Trace == 'udp_response':
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[2])
            except Exception:
                self.logger.exception('Error Occurred')

        ############################ EVENTS ###########################################################
        if Trace == 'doorbell_event_response':
            self.logger.info('Sending Doorbell Event Response')
            await connection.send(json.dumps(jsn))
        elif Trace == 'temp_hum_event_response':
            self.logger.info('Sending temperature humidity response')
            await connection.send(json.dumps(jsn))
