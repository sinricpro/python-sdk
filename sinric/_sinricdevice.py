import json


class SinricDevice:
    def __init__(self):
        self.deviceId = ""
        self.name = ""
        self.devicesTypes = ""
        self.product = ""
        self.room = ""
        self.home = ""
        self.powerState = False
        self.actions = {}
        self.features = {}

    def toJson(self):
        return json.dumps("")

    def fromJson(self, jsonData):
        return
