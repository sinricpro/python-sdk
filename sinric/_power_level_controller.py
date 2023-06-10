"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class PowerLevelController:
    def __init__(self, power_level) -> None:
        self.power_level = power_level

    async def set_power_level(self, jsn, power_level_callback):
        self.power_level = jsn.get("payload").get(
            SinricProConstants.VALUE).get(SinricProConstants.POWER_LEVEL)
        return power_level_callback(jsn.get("payload").get(SinricProConstants.DEVICEID),
                                    self.power_level)

    async def adjust_power_level(self, jsn, adjust_power_level_cb):
        self.power_level += jsn[SinricProConstants.VALUE][SinricProConstants.POWER_LEVEL_DELTA]
        if self.power_level > 100:
            self.power_level = 100
        elif self.power_level < 0:
            self.power_level = 0
        return adjust_power_level_cb(jsn[SinricProConstants.DEVICEID],
                                     self.power_level)
