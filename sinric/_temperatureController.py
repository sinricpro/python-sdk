"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._jsoncommands import JSON_COMMANDS

class TemperatureController:
    def __init__(self, k):
        self.temperature = 0
        pass

    async def targetTemperature(self, jsn, callback):
        return callback(jsn.get("payload").get(JSON_COMMANDS['DEVICEID']), jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('temperature'))

    async def adjustTemperature(self, jsn, callback):
        self.temperature+=jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('temperature')
        if self.temperature < 0:
            self.temperature=0
        elif self.temperature > 100:
            self.temperature=100
        return callback(jsn.get("payload").get(JSON_COMMANDS['DEVICEID']),self.temperature )
