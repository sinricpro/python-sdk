"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from ._jsoncommands import JSON_COMMANDS

class ModeController:
    def __init__(self, x): 
        self.instanceId = ''
       

    async def setMode(self, jsn, callback):
        self.instanceId= jsn.get("payload").get(JSON_COMMANDS['INSTANCE_ID'], '')
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), jsn.get("payload").get('value').get('mode'), self.instanceId)
