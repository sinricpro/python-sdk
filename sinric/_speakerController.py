"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._jsoncommands import JSON_COMMANDS

class SpeakerController:

    def __init__(self, x):
        self.band=0


    async def setBands(self, jsn, callback):
        value = jsn.get("payload").get('value')
        bands = value.get('bands')[0]
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), bands.get('level'))

    async def adjustBands(self, jsn, callback):
        value = jsn.get("payload").get('value')
        bands = value.get('bands')[0]
        self.band += bands.get('levelDelta',0)
        if(self.band < 0):
            self.band=0
        elif self.band > 100:
            self.band=100
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), self.band,
                        bands.get('levelDirection'))

    async def resetBands(self, jsn, callback):
        value = jsn.get("payload").get('value')
        band1 = value.get('bands')[0]
        band2 = value.get('bands')[1]
        band3 = value.get('bands')[2]
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), band1, band2, band3)

    async def setMode(self, jsn, callback):
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), jsn.get("payload").get('value').get('mode'))
