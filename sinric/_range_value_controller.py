"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from sinric.helpers.set_limits import set_limits
from ._sinricpro_constants import SinricProConstants


class RangeValueController:
    def __init__(self, range_value):
        self.range_value = range_value
        self.instance_id = ''

    async def set_range_value(self, jsn, range_callback):
        self.range_value = jsn.get("payload").get(
            SinricProConstants.VALUE).get(SinricProConstants.RANGE_VALUE)
        self.instance_id = jsn.get("payload").get(
            SinricProConstants.INSTANCE_ID, '')
        return range_callback(jsn.get("payload").get(SinricProConstants.DEVICEID), self.range_value, self.instance_id)

    async def adjust_range_value(self, jsn, callback):
        self.range_value += jsn.get("payload").get(
            SinricProConstants.VALUE).get(SinricProConstants.RANGE_VALUE)
        self.range_value = set_limits(self.range_value)
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), self.range_value)
