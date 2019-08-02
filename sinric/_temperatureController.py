from sinric._jsoncommands import JSON_COMMANDS


class TemperatureController:
    def __init__(self, k):
        pass

    async def targetTemperature(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS['DEVICEID']), jsn.get(JSON_COMMANDS.get('VALUE')).get('temperature'),
                        jsn.get(JSON_COMMANDS.get('VALUE')).get('schedule').get('duration'))

    async def adjustTemperature(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS['DEVICEID']), jsn.get(JSON_COMMANDS.get('VALUE')).get('temperature'))
