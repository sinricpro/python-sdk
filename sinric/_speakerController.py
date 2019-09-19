from ._jsoncommands import JSON_COMMANDS
from ._dataTracker import DataTracker

class SpeakerController:

    def __init__(self, x):
        self.band=0
        self.bands = DataTracker.readData('bands')
        self.band = self.bands.get('level')


    async def setBands(self, jsn, callback):
        value = jsn.get("payload").get('value')
        bands = value.get('bands')[0]
        return callback(jsn.get("payload").get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), bands.get('level'))

    async def adjustBands(self, jsn, callback):
        value = jsn.get("payload").get('value')
        bands = value.get('bands')[0]
        self.band += bands.get('levelDelta')
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
