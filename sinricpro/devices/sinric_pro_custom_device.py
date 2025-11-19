"""
SinricProCustomDevice - Flexible device with all capabilities

A custom device type that supports all SinricPro capabilities, allowing you to
build devices with any combination of features you need.
"""

from sinricpro.capabilities.air_quality_sensor import AirQualitySensor
from sinricpro.capabilities.brightness_controller import BrightnessController
from sinricpro.capabilities.camera_controller import CameraController
from sinricpro.capabilities.color_controller import ColorController
from sinricpro.capabilities.color_temperature_controller import ColorTemperatureController
from sinricpro.capabilities.contact_sensor import ContactSensor
from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.lock_controller import LockController
from sinricpro.capabilities.motion_sensor import MotionSensor
from sinricpro.capabilities.open_close_controller import OpenCloseController
from sinricpro.capabilities.percentage_controller import PercentageController
from sinricpro.capabilities.power_level_controller import PowerLevelController
from sinricpro.capabilities.power_sensor import PowerSensor
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor
from sinricpro.capabilities.thermostat_controller import ThermostatController
from sinricpro.core.actions import (
    ACTION_ADJUST_BRIGHTNESS,
    ACTION_ADJUST_POWER_LEVEL,
    ACTION_ADJUST_RANGE_VALUE,
    ACTION_DECREASE_COLOR_TEMPERATURE,
    ACTION_GET_CAMERA_STREAM_URL,
    ACTION_GET_SNAPSHOT,
    ACTION_GET_WEBRTC_ANSWER,
    ACTION_INCREASE_COLOR_TEMPERATURE,
    ACTION_SET_BRIGHTNESS,
    ACTION_SET_COLOR,
    ACTION_SET_COLOR_TEMPERATURE,
    ACTION_SET_LOCK_STATE,
    ACTION_SET_MODE,
    ACTION_SET_PERCENTAGE,
    ACTION_SET_POWER_LEVEL,
    ACTION_SET_POWER_STATE,
    ACTION_SET_RANGE_VALUE,
    ACTION_SET_SETTING,
    ACTION_SET_THERMOSTAT_MODE,
    ACTION_TARGET_TEMPERATURE,
)
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest


class SinricProCustomDevice(
    SinricProDevice,
    # Power Control
    PowerStateController,
    # Lighting Controls
    BrightnessController,
    ColorController,
    ColorTemperatureController,
    PowerLevelController,
    # Position & Range Controls
    RangeController,
    PercentageController,
    OpenCloseController,
    # Climate Control
    ThermostatController,
    TemperatureSensor,
    # Security & Access
    LockController,
    ModeController,
    MotionSensor,
    ContactSensor,
    # Camera
    CameraController,
    # Environmental Sensors
    AirQualitySensor,
    PowerSensor,
    # Common
    SettingController,
    PushNotification,
):
    """
    Custom device supporting all SinricPro capabilities.

    This flexible device type allows you to combine any capabilities you need
    without creating a new device class. Simply register callbacks for the
    capabilities you want to use.

    Example:
        >>> from sinricpro import SinricPro, SinricProCustomDevice
        >>>
        >>> # Create a custom device that's a smart light with temperature sensor
        >>> device = SinricProCustomDevice("device-id", "LIGHT")
        >>>
        >>> # Register only the callbacks you need
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"Light: {'On' if state else 'Off'}")
        ...     return True
        >>>
        >>> async def on_brightness(brightness: int) -> bool:
        ...     print(f"Brightness: {brightness}%")
        ...     return True
        >>>
        >>> device.on_power_state(on_power_state)
        >>> device.on_brightness(on_brightness)
        >>>
        >>> # Send temperature updates
        >>> await device.send_temperature_event(23.5)

    Supported Capabilities:
        Power Control:
            - PowerStateController: on_power_state()
            - PowerLevelController: on_power_level()

        Lighting:
            - BrightnessController: on_brightness(), on_adjust_brightness()
            - ColorController: on_color()
            - ColorTemperatureController: on_color_temperature(), etc.

        Position & Range:
            - RangeController: on_range_value(), on_adjust_range_value()
            - PercentageController: on_percentage()
            - OpenCloseController: (events only)

        Climate:
            - ThermostatController: on_thermostat_mode(), on_target_temperature()
            - TemperatureSensor: send_temperature_event()

        Security:
            - LockController: on_lock_state()
            - ModeController: on_door_mode()
            - MotionSensor: send_motion_event()
            - ContactSensor: send_contact_event()

        Camera:
            - CameraController: on_snapshot(), send_snapshot(), send_motion_event()

        Sensors:
            - AirQualitySensor: send_air_quality_event()
            - PowerSensor: send_power_usage_event()

        Common:
            - SettingController: on_setting()
            - PushNotification: send_push_notification()
    """

    def __init__(self, device_id: str, product_type: str = "CUSTOM_DEVICE") -> None:
        """
        Initialize a custom device.

        Args:
            device_id: Unique device ID from SinricPro portal
            product_type: Device type name (default: "CUSTOM_DEVICE")
                         You can use any type from the SinricPro portal

        Example:
            >>> # Generic custom device
            >>> device = SinricProCustomDevice("device-id")
            >>>
            >>> # Custom device with specific type
            >>> device = SinricProCustomDevice("device-id", "SMART_LIGHT")
        """
        super().__init__(device_id=device_id, product_type=product_type)

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle incoming requests for all supported capabilities.

        Args:
            request: The incoming request object

        Returns:
            True if request was handled successfully, False otherwise
        """
        action = request.action

        # Power State Control
        if action == ACTION_SET_POWER_STATE:
            state = request.request_value.get("state", "Off").lower() == "on"
            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success

        # Brightness Control
        elif action == ACTION_SET_BRIGHTNESS:
            brightness = request.request_value.get("brightness", 0)
            success, response_value = await self.handle_brightness_request(brightness, self)
            request.response_value = response_value
            return success

        elif action == ACTION_ADJUST_BRIGHTNESS:
            brightness_delta = request.request_value.get("brightnessDelta", 0)
            success, response_value = await self.handle_adjust_brightness_request(
                brightness_delta, self
            )
            request.response_value = response_value
            return success

        # Color Control
        elif action == ACTION_SET_COLOR:
            r = request.request_value.get("color", {}).get("r", 0)
            g = request.request_value.get("color", {}).get("g", 0)
            b = request.request_value.get("color", {}).get("b", 0)
            success, response_value = await self.handle_color_request(r, g, b, self)
            request.response_value = response_value
            return success

        # Color Temperature Control
        elif action == ACTION_SET_COLOR_TEMPERATURE:
            color_temp = request.request_value.get("colorTemperature", 2700)
            success, response_value = await self.handle_color_temperature_request(
                color_temp, self
            )
            request.response_value = response_value
            return success

        elif action == ACTION_INCREASE_COLOR_TEMPERATURE:
            success, response_value = await self.handle_increase_color_temperature_request(self)
            request.response_value = response_value
            return success

        elif action == ACTION_DECREASE_COLOR_TEMPERATURE:
            success, response_value = await self.handle_decrease_color_temperature_request(self)
            request.response_value = response_value
            return success

        # Power Level Control
        elif action == ACTION_SET_POWER_LEVEL:
            power_level = request.request_value.get("powerLevel", 0)
            success, response_value = await self.handle_power_level_request(power_level, self)
            request.response_value = response_value
            return success

        elif action == ACTION_ADJUST_POWER_LEVEL:
            power_level_delta = request.request_value.get("powerLevelDelta", 0)
            success, response_value = await self.handle_adjust_power_level_request(
                power_level_delta, self
            )
            request.response_value = response_value
            return success

        # Range Control
        elif action == ACTION_SET_RANGE_VALUE:
            range_value = request.request_value.get("rangeValue", 0)
            success, response_value = await self.handle_range_value_request(range_value, self)
            request.response_value = response_value
            return success

        elif action == ACTION_ADJUST_RANGE_VALUE:
            range_value_delta = request.request_value.get("rangeValueDelta", 0)
            success, response_value = await self.handle_adjust_range_value_request(
                range_value_delta, self
            )
            request.response_value = response_value
            return success

        # Percentage Control (Legacy)
        elif action == ACTION_SET_PERCENTAGE:
            percentage = request.request_value.get("percentage", 0)
            success, response_value = await self.handle_percentage_request(percentage, self)
            request.response_value = response_value
            return success

        # Lock Control
        elif action == ACTION_SET_LOCK_STATE:
            lock_state = request.request_value.get("state", "LOCK")
            success, response_value = await self.handle_lock_state_request(lock_state, self)
            request.response_value = response_value
            return success

        # Mode Control
        elif action == ACTION_SET_MODE:
            mode = request.request_value.get("mode", "")
            success, response_value = await self.handle_mode_request(mode, self)
            request.response_value = response_value
            return success

        # Thermostat Control
        elif action == ACTION_SET_THERMOSTAT_MODE:
            thermostat_mode = request.request_value.get("thermostatMode", "AUTO")
            success, response_value = await self.handle_thermostat_mode_request(
                thermostat_mode, self
            )
            request.response_value = response_value
            return success

        elif action == ACTION_TARGET_TEMPERATURE:
            temperature = request.request_value.get("temperature", 20.0)
            success, response_value = await self.handle_target_temperature_request(
                temperature, self
            )
            request.response_value = response_value
            return success

        # Camera Control
        elif action == ACTION_GET_SNAPSHOT:
            success, response_value = await self.handle_snapshot_request(self)
            request.response_value = response_value
            return success

        elif action == ACTION_GET_WEBRTC_ANSWER:
            offer = request.request_value.get("offer", "")
            success, response_value = await self.handle_get_webrtc_answer(offer, self)
            request.response_value = response_value
            return success

        elif action == ACTION_GET_CAMERA_STREAM_URL:
            protocol = request.request_value.get("protocol", "")
            success, response_value = await self.handle_get_camera_stream_url(protocol, self)
            request.response_value = response_value
            return success

        # Settings Control
        elif action == ACTION_SET_SETTING:
            setting = request.request_value.get("setting", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting, value, self)
            request.response_value = response_value
            return success

        # Unknown action
        request.error_message = f"Missing callback function: {action}"
        return False
