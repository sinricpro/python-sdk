"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class TvController:
    def __init__(self, x):
        self.volume = x

    async def set_volume(self, jsn, callback):
        self.volume = jsn.get("payload").get(
            SinricProConstants.VALUE).get('volume')
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), self.volume)

    async def adjust_volume(self, jsn, callback):
        self.volume += jsn.get("payload").get(
            SinricProConstants.VALUE).get('volume')
        if self.volume > 100:
            self.volume = 100
        elif self.volume < 0:
            self.volume = 0
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), self.volume)

    async def set_mute(self, jsn, callback):
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get(SinricProConstants.VALUE).get('mute'))

    async def media_control(self, jsn, callback):
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get(SinricProConstants.VALUE).get('control'))

    async def select_input(self, jsn, callback):
        inp = jsn.get("payload").get(SinricProConstants.VALUE).get('input')
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), inp)

    async def change_channel(self, jsn, callback):
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get(SinricProConstants.VALUE).get('channel').get('name'))

    async def skip_channels(self, jsn, callback):
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), jsn.get("payload").get(SinricProConstants.VALUE).get('channelCount'))
