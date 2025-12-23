"""SinricProGarageDoor Device"""
from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import ACTION_SET_MODE, ACTION_SET_SETTING

class SinricProGarageDoor(SinricProDevice, ModeController, SettingController, PushNotification):
    """Garage door device - open/close control."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="GARAGE_DOOR")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_MODE:
            state = request.request_value.get("mode", "Close")
            instance_id = request.instance
            success, response_value = await self.handle_mode_request(state, instance_id, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_SET_SETTING:
            setting_id = request.request_value.get("id", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting_id, value, self)
            request.response_value = response_value
            return success
        request.error_message = f"Missing callback function: {request.action}"
        return False
