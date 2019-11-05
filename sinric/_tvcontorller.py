"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._jsoncommands import JSON_COMMANDS


class TvController:
    def __init__(self, x):
        self.volume = x


    async def setVolume(self, jsn, callback):
        self.volume = jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('volume')
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), self.volume)

    async def adjustVolume(self, jsn, callback):
        self.volume += jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('volume')
        if self.volume > 100:
            self.volume = 100
        elif self.volume < 0:
            self.volume = 0
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), self.volume)

    async def setMute(self, jsn, callback):
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), jsn.get("payload").get('value').get('mute'))

    async def mediaControl(self, jsn, callback):
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('control'))

    async def selectInput(self, jsn, callback):
        inp = jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('input')
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), inp)

    async def changeChannel(self, jsn, callback):
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), jsn.get("payload").get('value').get('channel').get('name'))

    async def skipChannels(self, jsn, callback):
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), jsn.get("payload").get(JSON_COMMANDS.get('VALUE')).get('channelCount'))
