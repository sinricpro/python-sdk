"""SinricProFan Device"""
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import (
    ACTION_ADJUST_RANGE_VALUE,
    ACTION_SET_POWER_STATE,
    ACTION_SET_RANGE_VALUE,
    ACTION_SET_SETTING,
)

class SinricProFan(SinricProDevice, PowerStateController, RangeController, SettingController, PushNotification):
    """Fan device - on/off control with fan speed range control."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="FAN")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_POWER_STATE:
            state_str = request.request_value.get("state", "Off")
            state = state_str.lower() == "on"
            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_SET_RANGE_VALUE:
            range_value = request.request_value.get("rangeValue", 0)
            success, response_value = await self.handle_range_value_request(range_value, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_ADJUST_RANGE_VALUE:
            range_value_delta = request.request_value.get("rangeValueDelta", 0)
            success, response_value = await self.handle_adjust_range_value_request(range_value_delta, self)
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
