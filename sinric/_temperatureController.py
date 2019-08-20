from ._jsoncommands import JSON_COMMANDS
from ._dataTracker import DataTracker

class TemperatureController:
    def __init__(self, k):
        self.temperature = 0
        self.temperature = DataTracker.readData('temperature')
        pass

    async def targetTemperature(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS['DEVICEID']), jsn.get(JSON_COMMANDS.get('VALUE')).get('temperature'),
                        jsn.get(JSON_COMMANDS.get('VALUE')).get('schedule').get('duration'))

    async def adjustTemperature(self, jsn, callback):
        self.temperature+=jsn.get(JSON_COMMANDS.get('VALUE')).get('temperature')
        if self.temperature < 0:
            self.temperature=0
        elif self.temperature > 100:
            self.temperature=100
        return callback(jsn.get(JSON_COMMANDS['DEVICEID']),self.temperature )
