"""
 *  Copyright (c) 2019-2023 Sinricinricinricinricinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class PowerController:

    async def power_state(self, jsn, power_state_callback):
        return power_state_callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get("value").get("state"))
