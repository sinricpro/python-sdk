from sinric._jsoncommands import JSON_COMMANDS


class PowerLevel:
    def __init__(self, x):
        self.power_level = x

    async def setPowerLevel(self, jsn, power_level_callback):
        self.power_level = jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['POWERLEVEL']]
        return power_level_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                    self.power_level)

    async def adjustPowerLevel(self, jsn, adjust_power_level_cb):
        self.power_level += jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['POWERLEVELDELTA']]
        if self.power_level > 100:
            self.power_level = 100
        elif self.power_level < 0:
            self.power_level = 0
        return adjust_power_level_cb(jsn[JSON_COMMANDS['DEVICEID']],
                                     self.power_level)
