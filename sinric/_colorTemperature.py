"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from sinric._jsoncommands import JSON_COMMANDS


class ColorTemperatureController:
    def __init__(self, x, arr):
        self.temperatures_index = x
        self.temperatures_array = arr
        pass

    async def setColorTemperature(self, jsn, set_callback):
        return set_callback(jsn.get("payload").get("deviceId"),
                            jsn.get("payload").get("value").get("colorTemperature"))

    async def increaseColorTemperature(self, jsn, increase_callback):
        return increase_callback(jsn.get("payload").get("deviceId"), jsn.get("payload").get("value"))

    async def decreaseColorTemperature(self, jsn, decrease_callback):
        return decrease_callback(jsn.get("payload").get("deviceId"), jsn.get("payload").get("value"))
