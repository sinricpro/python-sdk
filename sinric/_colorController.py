"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from sinric._jsoncommands import JSON_COMMANDS


class ColorController:
    def __init__(self, x):
        pass

    async def setColor(self, jsn, set_color_callback):
        return set_color_callback(jsn.get("payload").get("deviceId"),
                                  jsn.get("payload").get("value").get("color").get("r"),
                                  jsn.get("payload").get("value").get("color").get("g"),
                                  jsn.get("payload").get("value").get("color").get("b"))
