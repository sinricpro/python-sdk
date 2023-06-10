"""
 *  Copyright (c) 2019-2023 Sinricinricinricinricinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class ModeController:
    def __init__(self):
        self.instance_id = ''

    async def set_mode(self, jsn, callback):
        self.instance_id = jsn.get("payload").get(SinricProConstants.INSTANCE_ID, '')
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get('value').get('mode'), self.instance_id)
