"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""


class ColorTemperatureController:
    def __init__(self, temperatures_index, temperatures_array):
        self.temperatures_index = temperatures_index
        self.temperatures_array = temperatures_array

    async def set_color_temperature(self, jsn, set_callback):
        return set_callback(jsn.get("payload").get("deviceId"),
                            jsn.get("payload").get("value").get("colorTemperature"))

    async def increase_color_temperature(self, jsn, increase_callback):
        return increase_callback(jsn.get("payload").get("deviceId"), jsn.get("payload").get("value"))

    async def decrease_color_temperature(self, jsn, decrease_callback):
        return decrease_callback(jsn.get("payload").get("deviceId"), jsn.get("payload").get("value"))
