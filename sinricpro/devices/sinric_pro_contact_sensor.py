"""SinricProContactSensor Device"""
from sinricpro.capabilities.contact_sensor import ContactSensor
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import ACTION_SET_SETTING

class SinricProContactSensor(SinricProDevice, ContactSensor, SettingController, PushNotification):
    """Contact sensor device - detects open/closed state."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="CONTACT_SENSOR")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_SETTING:
            setting_id = request.request_value.get("id", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting_id, value, self)
            request.response_value = response_value
            return success
        request.error_message = f"Missing callback function: {request.action}"
        return False
