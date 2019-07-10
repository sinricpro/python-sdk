from sinric._jsoncommands import JSON_COMMANDS


class ColorTemperatureController:
    def __init__(self, x, arr):
        self.temperatures_index = x
        self.temperatures_array = arr
        pass

    async def setColorTemperature(self, jsn, set_callback):
        return set_callback(jsn[JSON_COMMANDS['DEVICEID']],
                            jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLORTEMPERATURE']])

    async def increaseColorTemperature(self, jsn, increase_callback):
        return increase_callback(jsn[JSON_COMMANDS['DEVICEID']], jsn[JSON_COMMANDS['VALUE']])

    async def decreaseColorTemperature(self, jsn, decrease_callback):
        return decrease_callback(jsn[JSON_COMMANDS['DEVICEID']], jsn[JSON_COMMANDS['VALUE']])
