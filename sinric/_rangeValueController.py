from ._jsoncommands import JSON_COMMANDS
from ._dataTracker import DataTracker

class RangeValueController:
    def __init__(self, k):
        self.rangeValue = 0
        self.rangeValue = DataTracker.readData('rangeValue')

    async def setRangeValue(self, jsn, range_callback):
        self.rangeValue= jsn.get("payload").get(JSON_COMMANDS['VALUE']).get('rangeValue')
        return range_callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.rangeValue)

    async def adjustRangeValue(self, jsn, callback):
        self.rangeValue += jsn.get("payload").get(JSON_COMMANDS['VALUE']).get('rangeValue')
        if self.rangeValue > 100:
            self.rangeValue = 100
        elif self.rangeValue < 0:
            self.rangeValue = 0
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.rangeValue)
