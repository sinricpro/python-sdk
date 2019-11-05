"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._jsoncommands import JSON_COMMANDS

class RangeValueController:
    def __init__(self, k):
        self.rangeValue = 0

    async def setRangeValue(self, jsn, range_callback):
        self.rangeValue= jsn.get("payload").get(JSON_COMMANDS['VALUE']).get('rangeValue')
        return range_callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.rangeValue)

    async def adjustRangeValue(self, jsn, callback):
        self.rangeValue += jsn.get("payload").get(JSON_COMMANDS['VALUE']).get('rangeValue')
        if self.rangeValue > 100:
            self.rangeValue = 100
        elif self.rangeValue < 0:
            self.rangeValue = 0
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.rangeValue)
