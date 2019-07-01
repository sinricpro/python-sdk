from sinric.controller.powerController import PowerController
from sinric.controller.brightnessController import BrightnessController
from sinric.command.jsoncommands import JSON_COMMANDS


class CallBackHandler(PowerController, BrightnessController):
    def __init__(self, callbacks):
        super().__init__()
        self.callbacks = callbacks

    async def handleCallBacks(self, jsn, connection):
        if jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['NAME']] == JSON_COMMANDS['SETON']:
            resp = await self.powerState(jsn, self.callbacks['powerState'])
            response = {
                "success": True,
                "results": [
                    {
                        "success": True,
                        "message": "OK",
                        "did": jsn[JSON_COMMANDS['DEVICEID']],
                        "action": JSON_COMMANDS['SETON'],
                        "device": {
                            "powerState": "On"
                        }
                    }
                ]
            }
            if resp:
                await connection.send(response)

        elif jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['NAME']] == JSON_COMMANDS['SETOFF']:
            resp = await self.powerState(jsn, self.callbacks['powerState'])
            response = {
                "success": True,
                "results": [
                    {
                        "success": True,
                        "message": "OK",
                        "did": jsn[JSON_COMMANDS['DEVICEID']],
                        "action": JSON_COMMANDS['SETOFF'],
                        "device": {
                            "powerState": "Off"
                        }
                    }
                ]
            }
            if resp:
                await connection.send(response)

        elif jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['NAME']] == JSON_COMMANDS['SETPOWERLEVEL']:
            powerState = self.callbacks['powerLevel']
            resp = powerState(jsn[JSON_COMMANDS['DEVICEID']],
                              jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['PARAMETERS']])
            response = {
                "clientId": "android-app",
                "did": jsn[JSON_COMMANDS['DEVICEID']],
                "deviceAttributes": [],
                "type": "action",
                "ts": 1556844844604,
                "actions": [{
                    "name": JSON_COMMANDS['SETPOWERLEVEL'],
                    "parameters": {
                        "value": jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['PARAMETERS']][JSON_COMMANDS['VALUE']]
                    }
                }]
            }
            if resp:
                connection.send(response)

        elif jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['NAME']] == JSON_COMMANDS['SETBRIGHTNESS']:
            resp = await self.Brightness(jsn, self.callbacks['brightnessLevel'])
            response = {
                "success": True,
                "results": [
                    {
                        "success": True,
                        "message": "OK",
                        "did": jsn[JSON_COMMANDS['DEVICEID']],
                        "action": JSON_COMMANDS['SETBRIGHTNESS'],
                        "device": {
                            "brightness": jsn[JSON_COMMANDS['ACTIONS']][0][JSON_COMMANDS['PARAMETERS']][
                                JSON_COMMANDS['BRIGHTNESS']]
                        }
                    }
                ]
            }
            if resp:
                await connection.send(response)
