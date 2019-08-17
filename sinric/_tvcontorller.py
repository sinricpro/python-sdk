from ._jsoncommands import JSON_COMMANDS
import json


class TvController:
    def __init__(self, x):
        self.volume = x
        with open('localdata.json','r') as f:
            self.data = json.load(f)
            self.volume = self.data.get('volume')
            f.close()

    def dumpData(self, inp, val):
        with open('localdata.json','w') as f:
            self.data.update({inp: val})
            json.dump(self.data, f)
            f.close()

    async def setVolume(self, jsn, callback):
        self.volume = jsn.get(JSON_COMMANDS.get('VALUE')).get('volume')
        self.dumpData("volume", self.volume)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.volume)

    async def adjustVolume(self, jsn, callback):
        self.volume += jsn.get(JSON_COMMANDS.get('VALUE')).get('volume')
        if self.volume > 100:
            self.volume = 100
        elif self.volume < 0:
            self.volume = 0
        self.dumpData("volume", self.volume)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.volume)

    async def setMute(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), )

    async def mediaControl(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get(JSON_COMMANDS.get('VALUE')).get('control'))

    async def selectInput(self, jsn, callback):
        inp = jsn.get(JSON_COMMANDS.get('VALUE')).get('input')
        self.dumpData("input", inp)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), inp)

    async def changeChannel(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get('value').get('channel').get('name'))

    async def skipChannels(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get(JSON_COMMANDS.get('VALUE')).get('channelCount'))
