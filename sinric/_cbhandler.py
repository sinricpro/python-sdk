from sinric._powerController import PowerController
from sinric._brightnessController import BrightnessController
from sinric._jsoncommands import JSON_COMMANDS
from sinric._powerLevelController import PowerLevel
from sinric._colorController import ColorController
from sinric._colorTemperature import ColorTemperatureController
import json
from time import time
from math import floor


# noinspection PyBroadException
class CallBackHandler(PowerLevel, PowerController, BrightnessController, ColorController, ColorTemperatureController):
    def __init__(self, callbacks, trace_bool):
        PowerLevel.__init__(self, 0)
        BrightnessController.__init__(self, 0)
        PowerController.__init__(self, 0)
        ColorController.__init__(self, 0)
        ColorTemperatureController.__init__(self, 0, [2200, 2700, 4000, 5500, 7000])
        self.callbacks = callbacks
        self.trace_response = trace_bool

    async def handleCallBacks(self, dataArr, connection, udp_client):
        jsn = dataArr[0]
        socketTrace = dataArr[1]
        udpTrace = dataArr[2]
        if jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETPOWERSTATE']:
            try:
                resp, state = await self.powerState(jsn, self.callbacks['powerState'])
                response = {
                    "payloadVersion": 1,
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "success": True,
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "type": "response",
                    "action": "setPowerState",
                    "value": {
                        "state": state
                    }
                }
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETPOWERLEVEL']:
            try:
                resp, value = await self.setPowerLevel(jsn, self.callbacks['setPowerLevel'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "type": "response",
                    "action": "setPowerLevel",
                    "value": {
                        "powerLevel": value
                    }
                }
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['ADJUSTPOWERLEVEL']:
            try:
                resp, value = await self.adjustPowerLevel(jsn,
                                                          self.callbacks['adjustPowerLevel'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "type": "response",
                    "action": jsn[JSON_COMMANDS['ACTION']],
                    "value": {"powerLevel": value}}
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETBRIGHTNESS']:
            try:
                resp, value = await self.setBrightness(jsn, self.callbacks['setBrightness'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "deviceAttributes": "",
                    "type": "response",
                    "action": "setBrightness",
                    "value": {"brightness": value}}
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)
        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['ADJUSTBRIGHTNESS']:
            try:
                resp, value = await self.adjustBrightness(jsn, self.callbacks['adjustBrightness'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "deviceAttributes": "",
                    "type": "response",
                    "action": "adjustBrightness",
                    "value": {
                        "brightness": value
                    }
                }
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)
        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETCOLOR']:
            try:
                resp = await self.setColor(jsn, self.callbacks['setColor'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    "message": "OK",
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
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
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETCOLORTEMPERATURE']:
            try:
                resp = await self.setColorTemperature(jsn, self.callbacks['setColorTemperature'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "type": "response",
                    "action": "setColorTemperature",
                    "value": {
                        "colorTemperature": jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLORTEMPERATURE']]
                    }
                }
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)
        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['INCREASECOLORTEMPERATURE']:
            try:
                resp, value = await self.increaseColorTemperature(jsn, self.callbacks['increaseColorTemperature'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "type": "response",
                    "action": "increaseColorTemperature",
                    "value": {
                        "colorTemperature": value
                    }
                }
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['DECREASECOLORTEMPERATURE']:
            try:
                resp, value = await self.decreaseColorTemperature(jsn, self.callbacks['decreaseColorTemperature'])
                response = {
                    "payloadVersion": 1,
                    "success": resp,
                    'clientId': jsn[JSON_COMMANDS['CLIENTID']],
                    'messageId': jsn[JSON_COMMANDS['MESSAGEID']],
                    "message": "OK",
                    "createdAt": floor(time()),
                    "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                    "type": "response",
                    "action": "decreaseColorTemperature",
                    "value": {
                        "colorTemperature": value
                    }
                }
                if resp:
                    if self.trace_response:
                        print('Response : ')
                        print(json.dumps(response))
                    if socketTrace:
                        await connection.send(json.dumps(response))
                    elif udpTrace:
                        udp_client.sendResponse(json.dumps(response).encode('ascii'), dataArr[3])
            except Exception as e:
                print('Callback not defined')
                print('Error : ', e)
