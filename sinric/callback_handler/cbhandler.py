class CallBackHandler:
    def __init__(self, callbacks):
        self.callbacks = callbacks

    def handleCallBacks(self, jsn, connection):
        if jsn['actions'][0]['name'] == 'setOn':
            powerState = self.callbacks['powerState']
            resp = powerState(jsn['did'], jsn['actions'][0]['name'])
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
                connection.send(response)

        elif jsn['actions'][0]['name'] == 'setOff':
            powerState = self.callbacks['powerState']
            resp = powerState(jsn['did'], jsn['actions'][0]['name'])
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
                connection.send(response)

        elif jsn['actions'][0]['name'] == 'setPowerLevel':
            powerState = self.callbacks['powerLevel']
            powerState(jsn['did'], jsn['actions'][0]['parameters'])
