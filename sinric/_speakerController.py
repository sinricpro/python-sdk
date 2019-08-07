from ._jsoncommands import JSON_COMMANDS


class SpeakerController:

    def __init__(self):
        pass

    async def setBands(self, jsn, callback):
        value = jsn.get('value')
        bands = value.get('bands')[0]
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), bands.get('level'))

    async def adjustBands(self, jsn, callback):
        value = jsn.get('value')
        bands = value.get('bands')[0]
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), bands.get('name'), bands.get('levelDelta'),
                        bands.get('levelDirection'))

    async def resetBands(self, jsn, callback):
        value = jsn.get('value')
        band1 = value.get('bands')[0]
        band2 = value.get('bands')[1]
        band3 = value.get('bands')[2]
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), band1, band2, band3)

    async def setMode(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get('value').get('mode'))
