from ._jsoncommands import JSON_COMMANDS

class RangeValueController:
    def __init__(self,k):
        pass

    async def rangeValueControl(self,jsn,range_callback):
        return range_callback(jsn.get(JSON_COMMANDS.get('DEVICEID')),jsn[JSON_COMMANDS['VALUE']]['rangeValue'])