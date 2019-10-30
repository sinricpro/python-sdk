"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""


class ThermostateMode:

    def __init__(self, k):
        pass

    async def setThermostateMode(self, jsn, thermostat_callback):
        return thermostat_callback(
            jsn.get("payload").get("deviceId"), jsn.get("payload").get("value").get("thermostatMode"))
