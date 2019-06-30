from sinric.controller.powerController import PowerController


class CallBackHandler(PowerController):
    def __init__(self, callbacks):
        super().__init__()
        self.callbacks = callbacks

    async def handleCallBacks(self, jsn, connection):
        if jsn['actions'][0]['name'] == 'setOn':
            resp = await self.powerState(jsn, self.callbacks['powerState'])
            response = {
                "success": True,
                "results": [
                    {
                        "success": True,
                        "message": "OK",
                        "did": jsn['did'],
                        "action": "setOn",
                        "device": {
                            "powerState": "On"
                        }
                    }
                ]
            }
            if resp:
                await connection.send(response)

        elif jsn['actions'][0]['name'] == 'setOff':
            resp = await self.powerState(jsn, self.callbacks['powerState'])
            response = {
                "success": True,
                "results": [
                    {
                        "success": True,
                        "message": "OK",
                        "did": jsn['did'],
                        "action": "setOff",
                        "device": {
                            "powerState": "Off"
                        }
                    }
                ]
            }
            if resp:
                await connection.send(response)

        elif jsn['actions'][0]['name'] == 'setPowerLevel':
            powerState = self.callbacks['powerLevel']
            resp = powerState(jsn['did'], jsn['actions'][0]['parameters'])
            response = {
                "clientId": "android-app",
                "did": jsn['did'],
                "deviceAttributes": [],
                "type": "action",
                "ts": 1556844844604,
                "actions": [{
                    "name": "setPowerLevel",
                    "parameters": {
                        "value": jsn['actions'][0]['parameters']['value']
                    }
                }]
            }
            if resp:
                connection.send(response)
