class PowerController:
    def __init__(self):
        pass

    async def powerState(self, jsn, power_state_callback):
        return power_state_callback(jsn['did'], jsn['actions'][0]['name'])
