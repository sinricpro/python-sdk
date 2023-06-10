"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants


class SpeakerController:

    def __init__(self):
        self.band = 0

    async def set_bands(self, jsn, callback):
        value = jsn.get("payload").get(SinricProConstants.VALUE)
        bands = value.get(SinricProConstants.BANDS)[0]
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), bands.get(SinricProConstants.NAME), bands.get(SinricProConstants.LEVEL))

    async def adjust_bands(self, jsn, callback):
        value = jsn.get("payload").get(SinricProConstants.VALUE)
        bands = value.get(SinricProConstants.BANDS)[0]
        self.band += bands.get(SinricProConstants.LEVEL_DELTA, 0)
        if (self.band < 0):
            self.band = 0
        elif self.band > 100:
            self.band = 100
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), bands.get(SinricProConstants.NAME), self.band,
                        bands.get(SinricProConstants.LEVELDIRECTION))

    async def reset_bands(self, jsn, callback):
        value = jsn.get("payload").get(SinricProConstants.VALUE)
        band1 = value.get(SinricProConstants.BANDS)[0]
        band2 = value.get(SinricProConstants.BANDS)[1]
        band3 = value.get(SinricProConstants.BANDS)[2]
        return callback(jsn.get("payload").get(SinricProConstants.DEVICEID), band1, band2, band3)
