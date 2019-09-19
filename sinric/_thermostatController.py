from ._jsoncommands import JSON_COMMANDS


class ThermostateMode:

    def __init__(self, k):
        pass

    async def setThermostateMode(self, jsn, thermostat_callback):
        return thermostat_callback(
            jsn.get("payload").get("deviceId"), jsn.get("payload").get("value").get("thermostatMode"))
