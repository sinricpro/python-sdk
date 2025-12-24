"""SinricProDoorbell Device"""
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import EVENT_LIMIT_STATE, SinricProRequest
from sinricpro.core.actions import ACTION_SET_SETTING

class SinricProDoorbell(SinricProDevice, SettingController, PushNotification):
    """Doorbell device - sends doorbell press events."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="DOORBELL")
        self._doorbell_limiter = EventLimiter(EVENT_LIMIT_STATE)
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_SETTING:
            setting_id = request.request_value.get("id", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting_id, value, self)
            request.response_value = response_value
            return success
        request.error_message = f"Missing callback function: {request.action}"
        return False
    async def send_doorbell_event(self, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send doorbell press event."""
        if not self._doorbell_limiter.can_send_event():
            return False
        success = await self.send_event(action="DoorbellPress", value={"state": "pressed"}, cause=cause)
        if success:
            self._doorbell_limiter.event_sent()
        return success
