from ._jsoncommands import JSON_COMMANDS
import json

class SpeakerController:

    def __init__(self, x):
        self.band=0
        with open('localdata.json','r') as f:
            self.data = json.load(f)
            self.band = self.data.get('bands',[])[0].get('levelDelta',0)
            self.bands = self.data.get('bands',0)
            f.close()

    def dumpData(self, inp, val):
        with open('localdata.json','w') as f:
            self.data.update({inp: val})
            json.dump(self.data, f)
            f.close()

    async def setBands(self, jsn, callback):
        value = jsn.get('value')
        bands = value.get('bands')[0]
        self.dumpData('bands',bands)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), bands.get('level'))

    async def adjustBands(self, jsn, callback):
        value = jsn.get('value')
        bands = value.get('bands')[0]
        self.band += bands.get('levelDelta')
        if(self.band < 0):
            self.band=0
        elif self.band > 100:
            self.band=100
        self.dumpData('bands',bands)
        self.dumpData('band', self.band)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), self.band,
                        bands.get('levelDirection'))

    async def resetBands(self, jsn, callback):
        value = jsn.get('value')
        band1 = value.get('bands')[0]
        band2 = value.get('bands')[1]
        band3 = value.get('bands')[2]
        self.dumpData('band',0)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), band1, band2, band3)

    async def setMode(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get('value').get('mode'))
