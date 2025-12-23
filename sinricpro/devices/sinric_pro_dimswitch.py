"""SinricProDimSwitch Device"""
from sinricpro.capabilities.power_level_controller import PowerLevelController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import (
    ACTION_ADJUST_POWER_LEVEL,
    ACTION_SET_POWER_LEVEL,
    ACTION_SET_POWER_STATE,
    ACTION_SET_SETTING,
)

class SinricProDimSwitch(SinricProDevice, PowerStateController, PowerLevelController, SettingController, PushNotification):
    """Dimmable switch device - on/off with power level control (0-100)."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="DIMMABLE_SWITCH")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_POWER_STATE:
            state_str = request.request_value.get("state", "Off")
            state = state_str.lower() == "on"
            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_SET_POWER_LEVEL:
            power_level = request.request_value.get("powerLevel", 0)
            success, response_value = await self.handle_power_level_request(power_level, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_ADJUST_POWER_LEVEL:
            power_level_delta = request.request_value.get("powerLevelDelta", 0)
            success, response_value = await self.handle_adjust_power_level_request(power_level_delta, self)
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
