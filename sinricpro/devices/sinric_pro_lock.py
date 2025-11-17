"""SinricProLock Device"""
from sinricpro.capabilities.lock_controller import LockController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import ACTION_SET_LOCK_STATE, ACTION_SET_SETTING

class SinricProLock(SinricProDevice, LockController, SettingController, PushNotification):
    """Smart lock device - lock/unlock control."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="SMARTLOCK")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_LOCK_STATE:
            state_str = request.request_value.get("state", "lock")
            lock = state_str == "lock"
            success, response_value = await self.handle_lock_state_request(lock, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_SET_SETTING:
            setting = request.request_value.get("setting", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting, value, self)
            request.response_value = response_value
            return success
        request.error_message = f"Missing callback function: {request.action}"
        return False
