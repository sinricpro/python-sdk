"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._jsoncommands import JSON_COMMANDS


class PowerController:
    def __init__(self, x):
        pass

    async def powerState(self, jsn, power_state_callback):
        return power_state_callback(jsn.get("payload").get("deviceId"), jsn.get("payload").get("value").get("state"))
