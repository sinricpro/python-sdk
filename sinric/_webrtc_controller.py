"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants

class WebRTCController:

    async def webrtc_offer(self, jsn, webrtc_offer_callback):
        self.format = jsn.get("payload").get("value").get("format")
        self.offer = jsn.get("payload").get("value").get("value")

        return webrtc_offer_callback(jsn.get("payload").get(SinricProConstants.DEVICEID),
                                     self.format, self.offer)
