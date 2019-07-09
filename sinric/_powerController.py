from sinric._jsoncommands import JSON_COMMANDS


class PowerController:
    def __init__(self, x):
        pass

    async def powerState(self, jsn, power_state_callback):
        return power_state_callback(jsn[JSON_COMMANDS['DEVICEID']], jsn[JSON_COMMANDS['VALUE']])
