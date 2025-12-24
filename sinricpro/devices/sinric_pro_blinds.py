"""SinricProBlinds Device"""
from sinricpro.capabilities.open_close_controller import OpenCloseController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.actions import ACTION_SET_POWER_STATE, ACTION_SET_RANGE_VALUE, ACTION_SET_SETTING
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest

class SinricProBlinds(SinricProDevice, PowerStateController, OpenCloseController, SettingController, PushNotification):
    """Blinds device - power control and open/close position control (0=closed, 100=open)."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="BLINDS")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_POWER_STATE:
            state_str = request.request_value.get("state", "Off")
            state = state_str.lower() == "on"
            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_SET_RANGE_VALUE:
            position = request.request_value.get("rangeValue", 0)
            success, response_value = await self.handle_open_close_request(position, self)
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
