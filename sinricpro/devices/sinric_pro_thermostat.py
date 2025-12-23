"""SinricProThermostat Device"""
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor
from sinricpro.capabilities.thermostat_controller import ThermostatController
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import (
    ACTION_SET_POWER_STATE,
    ACTION_SET_SETTING,
    ACTION_SET_THERMOSTAT_MODE,
    ACTION_TARGET_TEMPERATURE,
)

class SinricProThermostat(SinricProDevice, PowerStateController, ThermostatController, TemperatureSensor, SettingController, PushNotification):
    """Thermostat device - temperature control with modes."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="THERMOSTAT")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_POWER_STATE:
            state_str = request.request_value.get("state", "Off")
            state = state_str.lower() == "on"
            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_SET_THERMOSTAT_MODE:
            mode = request.request_value.get("thermostatMode", "AUTO")
            success, response_value = await self.handle_thermostat_mode_request(mode, self)
            request.response_value = response_value
            return success
        elif request.action == ACTION_TARGET_TEMPERATURE:
            temperature = request.request_value.get("temperature", 20.0)
            success, response_value = await self.handle_target_temperature_request(temperature, self)
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
