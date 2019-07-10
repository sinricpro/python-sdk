from sinric._jsoncommands import JSON_COMMANDS


class BrightnessController:
    def __init__(self, x):
        self.brightness_level = x

    async def setBrightness(self, jsn, brightness_callback):
        self.brightness_level = jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['BRIGHTNESS']]
        return brightness_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                   self.brightness_level)

    async def adjustBrightness(self, jsn, brightness_callback):
        self.brightness_level += jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['BRIGHTNESSDELTA']]

        if self.brightness_level > 100:
            self.brightness_level = 100
        elif self.brightness_level < 0:
            self.brightness_level = 0

        return brightness_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                   self.brightness_level)
