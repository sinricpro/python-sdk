from time import sleep


class PiActions:
    def __init__(self, action, deviceId):
        self.action = action
        self.deviceId = deviceId

    def printData(self):
        print(self.action, '    ', self.deviceId)

    def pinActions(self):
        return