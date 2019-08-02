from ._jsoncommands import JSON_COMMANDS


class RangeValueController:
    def __init__(self, k):
        pass

    async def setRangeValue(self, jsn, range_callback):
        return range_callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn[JSON_COMMANDS['VALUE']]['rangeValue'])

    async def adjustRangeValue(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn[JSON_COMMANDS['VALUE']]['rangeValue'])
