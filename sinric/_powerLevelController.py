from sinric._jsoncommands import JSON_COMMANDS


class PowerLevel:
    def __init__(self):
        pass

    async def setPowerLevel(self, jsn, power_level_callback):
        return power_level_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                    jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['POWERLEVEL']])

    async def adjustPowerLevel(self, jsn, adjust_power_level_cb):
        return adjust_power_level_cb(jsn[JSON_COMMANDS['DEVICEID']],
                                     jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['POWERLEVELDELTA']])
