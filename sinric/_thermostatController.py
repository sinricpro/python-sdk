from ._jsoncommands import JSON_COMMANDS


class ThermostateMode:

    def __init__(self, k):
        pass

    async def setThermostateMode(self, jsn, thermostat_callback):
        return thermostat_callback(
            jsn[JSON_COMMANDS['DEVICEID'], jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['thermostatMode']]])
