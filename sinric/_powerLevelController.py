from sinric._jsoncommands import JSON_COMMANDS
import json


class PowerLevel:
    def __init__(self, x):
        self.power_level = x
        with open('localdata.json', 'r') as f:
            self.data2 = json.load(f)
            self.power_level = self.data2.get('powerLevel', 0)
            f.close()

    def dumpData(self, key, val):
        with open('localdata.json', 'w') as f:
            self.data2.update({key: val})
            json.dump(self.data2, f)
            f.close()

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
        self.dumpData('powerLevel', self.power_level)
        return adjust_power_level_cb(jsn[JSON_COMMANDS['DEVICEID']],
                                     self.power_level)
