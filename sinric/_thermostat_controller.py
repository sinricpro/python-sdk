"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class ThermostateMode:

    async def set_thermostate_mode(self, jsn, thermostat_callback):
        return thermostat_callback(
            jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get("value").get(SinricProConstants.THERMOSTATMODE))
