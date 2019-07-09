from sinric._jsoncommands import JSON_COMMANDS


class ColorController:
    def __init__(self, x):
        pass

    async def setColor(self, jsn, set_color_callback):
        return set_color_callback(jsn[JSON_COMMANDS['DEVICEID']],
                                  jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLOR']][JSON_COMMANDS['COLOR_R']],
                                  jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLOR']][JSON_COMMANDS['COLOR_G']],
                                  jsn[JSON_COMMANDS['VALUE']][JSON_COMMANDS['COLOR']][JSON_COMMANDS['COLOR_B']])
