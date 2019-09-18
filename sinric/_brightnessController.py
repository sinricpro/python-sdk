from ._jsoncommands import JSON_COMMANDS
from ._dataTracker import DataTracker

class BrightnessController:
    def __init__(self, x):
        self.brightness_level = DataTracker.readData('brightness')

    async def setBrightness(self, jsn, brightness_callback):
        self.brightness_level = jsn.get("payload").get("value").get("brightness")
        return brightness_callback(jsn.get("payload").get("deviceId"),
                                   self.brightness_level)

    async def adjustBrightness(self, jsn, brightness_callback):
        self.brightness_level += jsn.get("payload").get("value").get("brightnessDelta")
        if self.brightness_level > 100:
            self.brightness_level = 100
        elif self.brightness_level < 0:
            self.brightness_level = 0

        return brightness_callback(jsn.get("payload").get("deviceId"),
                                   self.brightness_level)
