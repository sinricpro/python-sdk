from ._dataTracker import DataTracker


class LockStateController:
    def __init__(self):
        self.lockState = DataTracker.readData("lockState")
        pass

    async def setLockState(self, jsn, callback):
        return callback(jsn.get("deviceId"), jsn.get("payload").get('value', False).get('state', "UNLOCKED"))
