"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from numbers import Real
from typing import Any, Callable
from ._sinricpro_constants import SinricProConstants


class PowerLevelController:
    def __init__(self, power_level: Real) -> None:
        self.power_level: Real = power_level

    async def set_power_level(self, jsn: Any, power_level_callback: Callable[[str, Real], tuple[bool, Real]]) -> tuple[bool, Real]:
        self.power_level = jsn.get("payload").get(
            SinricProConstants.VALUE).get(SinricProConstants.POWER_LEVEL)
        return power_level_callback(jsn.get("payload").get(SinricProConstants.DEVICEID),
                                    self.power_level)

    async def adjust_power_level(self, jsn: Any, adjust_power_level_cb: Callable[[str, Real], Any]) -> Any:
        # TODO: no examples for adjust_power_level_cb can't infer return type
        self.power_level += jsn.get(SinricProConstants.VALUE).get(
            SinricProConstants.POWER_LEVEL_DELTA)
        if self.power_level > 100:
            self.power_level = 100
        elif self.power_level < 0:
            self.power_level = 0
        return adjust_power_level_cb(jsn.get(SinricProConstants.DEVICEID),
                                     self.power_level)
