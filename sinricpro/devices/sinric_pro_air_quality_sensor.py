"""SinricProAirQualitySensor Device"""
from sinricpro.capabilities.air_quality_sensor import AirQualitySensor
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest
from sinricpro.core.actions import ACTION_SET_SETTING

class SinricProAirQualitySensor(SinricProDevice, AirQualitySensor, TemperatureSensor, SettingController, PushNotification):
    """Air quality sensor device - measures PM1.0, PM2.5, PM10, and temperature."""
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id, product_type="AIR_QUALITY_SENSOR")
    async def handle_request(self, request: SinricProRequest) -> bool:
        if request.action == ACTION_SET_SETTING:
            setting = request.request_value.get("setting", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting, value, self)
            request.response_value = response_value
            return success
        request.error_message = f"Missing callback function: {request.action}"
        return False
