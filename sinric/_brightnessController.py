from sinric._jsoncommands import JSON_COMMANDS


class BrightnessController:
    def __init__(self):
        pass

    async def setBrightness(self, jsn, brightness_callback):
        return brightness_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                   jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['BRIGHTNESS']])

    async def adjustBrightness(self, jsn, brightness_callback):
        return brightness_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                   jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['BRIGHTNESSDELTA']])
