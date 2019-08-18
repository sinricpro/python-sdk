from ._jsoncommands import JSON_COMMANDS
import json

class RangeValueController:
    def __init__(self, k):
        self.rangeValue = 0
        with open('localdata.json','r') as  f:
            self.rangeDat = json.load(f)
            self.rangeValue = self.rangeDat.get('rangeValue',0)
            f.close()

    def dumpData(self,key,val):
        self.rangeDat.update({key,val})
        with open('localdata.json','w') as f:
            json.dump(self.rangeDat,f)
            f.close()

    async def setRangeValue(self, jsn, range_callback):
        self.rangeValue= jsn.get(JSON_COMMANDS['VALUE']).get('rangeValue')
        return range_callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.rangeValue)

    async def adjustRangeValue(self, jsn, callback):
        self.rangeValue += jsn.get(JSON_COMMANDS['VALUE']).get('rangeValue')
        if self.rangeValue > 100:
            self.rangeValue = 100
        elif self.rangeValue < 0:
            self.rangeValue = 0
        self.dumpData('rangeValue', self.rangeValue)
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.rangeValue)
