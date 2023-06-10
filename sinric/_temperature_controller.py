"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class TemperatureController:
    def __init__(self, temperature):
        self.temperature = temperature

    async def target_temperature(self, jsn, callback):
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get(SinricProConstants.VALUE).get('temperature'))

    async def adjust_temperature(self, jsn, callback):
        self.temperature += jsn.get("payload").get(SinricProConstants.VALUE).get('temperature')
        if self.temperature < 0:
            self.temperature = 0
        elif self.temperature > 100:
            self.temperature = 100
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), self.temperature)
