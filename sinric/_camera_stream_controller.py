"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._sinricpro_constants import SinricProConstants

class CameraStreamController:

    async def get_webrtc_answer(self, jsn, get_webrtc_answer_callback):
        self.offer = jsn.get("payload").get("value").get("offer")

        return get_webrtc_answer_callback(jsn.get("payload").get(SinricProConstants.DEVICEID),
                                          self.offer)

    async def get_camera_stream_url(self, jsn, get_camera_stream_url_callback):
        self.protocol = jsn.get("payload").get("value").get("protocol")
        
        return get_camera_stream_url_callback(jsn.get("payload").get(SinricProConstants.DEVICEID),
                                     self.protocol)
