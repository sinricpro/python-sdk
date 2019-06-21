class ConfigManager:
    def __init__(self):
        self.apiKey = ""
        self.GLOBAL_CONFIG_FILENAME = ""
        self.DEVICES_CONFIG_FILENAME = ""

    # @classmethod
    def setApiKey(self, apiKey):
        self.apiKey = apiKey

    def getApiKey(self):
        return self.apiKey

    def addDevice(self):
        return True

    def begin(self):
        return

    def getDevices(self):
        return [{}]

    def getDeviceIds(self):
        return ""

    def isMyDeviceId(self, deviceId):
        return True

    def readDevicesConfig(self):
        return

    def saveGlobalConfig(self):
        return True

    def readDevicesConfig(self):
        return
