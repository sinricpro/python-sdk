from sinric.controller.powerController import PowerController
from sinric.controller.brightnessController import BrightnessController
from sinric.command.jsoncommands import JSON_COMMANDS
from sinric.controller.powerLevelController import PowerLevel
from sinric.controller.colorController import ColorController
from sinric.controller.colorTemperature import ColorTemperatureController


# TODO Time Stamp Calculation
# TODO increaseColorTemperature
# TODO decreaseColorTemperature

class CallBackHandler(PowerController, BrightnessController, PowerLevel, ColorController, ColorTemperatureController):
    def __init__(self, callbacks):
        super().__init__()
        self.callbacks = callbacks

    async def handleCallBacks(self, jsn, connection):
        if jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETPOWERSTATE']:
            resp, state = await self.powerState(jsn, self.callbacks['powerState'])
            response = {
                "payloadVersion": 1,
                "success": True,
                "message": "OK",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
                "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                "type": "response",
                "action": "setPowerState",
                "value": {
                    "state": state
                }
            }
            if resp:
                await connection.send(response)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETPOWERLEVEL']:
            resp, value = self.setPowerLevel(jsn[JSON_COMMANDS['DEVICEID']],
                                             self.callbacks['setPowerLevel'])
            response = {
                "payloadVersion": 1,
                "success": resp,
                "message": "OK",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
                "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                "type": "response",
                "action": "setPowerLevel",
                "value": {
                    "powerLevel": value
                }
            }
            if resp:
                connection.send(response)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['ADJUSTPOWERLEVEL']:
            resp, value = self.setPowerLevel(jsn[JSON_COMMANDS['DEVICEID']],
                                             self.callbacks['adjustPowerLevel'])
            response = {
                "payloadVersion": 1,
                "success": resp,
                "message": "OK",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
                "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                "type": "response",
                "action": "adjustPowerLevel",
                "value": {
                    "powerLevel": value
                }
            }
            if resp:
                connection.send(response)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETBRIGHTNESS']:
            resp, value = await self.setBrightness(jsn, self.callbacks['setBrightness'])
            response = {
                "payloadVersion": 1,
                "clientId": "alexa-skill",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
                "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                "deviceAttributes": "",
                "type": "request",
                "action": "setBrightness",
                "value": {
                    "brightness": value
                }
            }
            if resp:
                await connection.send(response)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['ADJUSTBRIGHTNESS']:
            resp, value = await self.adjustBrightness(jsn, self.callbacks['adjustBrightness'])
            response = {
                "payloadVersion": 1,
                "clientId": "alexa-skill",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
                "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                "deviceAttributes": "",
                "type": "request",
                "action": "adjustBrightness",
                "value": {
                    "brightness": value
                }
            }
            if resp:
                await connection.send(response)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETCOLOR']:
            resp = await self.setColor(jsn, self.callbacks['setColor'])
            response = {
                "payloadVersion": 1,
                "success": resp,
                "message": "OK",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
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
                await connection.send(response)

        elif jsn[JSON_COMMANDS['ACTION']] == JSON_COMMANDS['SETCOLORTEMPERATURE']:
            resp = await self.setColorTemperature(jsn, self.callbacks['setColorTemperature'])
            response = {
                "payloadVersion": 1,
                "success": resp,
                "message": "OK",
                "createdAt": jsn[JSON_COMMANDS['TIMESTAMP']],
                "deviceId": jsn[JSON_COMMANDS['DEVICEID']],
                "type": "response",
                "action": "setColorTemperature",
                "value": {
                    "colorTemperature": jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLORTEMPERATURE']]
                }
            }
            if resp:
                connection.send(response)
