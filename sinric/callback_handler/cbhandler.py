class CallBackHandler:
    def __init__(self, callbacks):
        self.callbacks = callbacks

    def handleCallBacks(self, jsn):
        if jsn['actions'][0]['name'] == 'setOn':
            powerState = self.callbacks['powerState']
            powerState(jsn['did'], jsn['actions'][0]['name'])

        elif jsn['actions'][0]['name'] == 'setOff':
            powerState = self.callbacks['powerState']
            powerState(jsn['did'], jsn['actions'][0]['name'])

        elif jsn['actions'][0]['name'] == 'setPowerLevel':
            powerState = self.callbacks['powerLevel']
            powerState(jsn['did'], jsn['actions'][0]['parameters'])

