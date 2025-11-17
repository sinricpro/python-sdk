"""
SinricProLight Device

Smart light device with power, brightness, color, and color temperature control.
"""

from typing import Any

from sinricpro.capabilities.brightness_controller import BrightnessController
from sinricpro.capabilities.color_controller import ColorController
from sinricpro.capabilities.color_temperature_controller import ColorTemperatureController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.actions import (
    ACTION_ADJUST_BRIGHTNESS,
    ACTION_DECREASE_COLOR_TEMPERATURE,
    ACTION_INCREASE_COLOR_TEMPERATURE,
    ACTION_SET_BRIGHTNESS,
    ACTION_SET_COLOR,
    ACTION_SET_COLOR_TEMPERATURE,
    ACTION_SET_POWER_STATE,
    ACTION_SET_SETTING,
)
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest


class SinricProLight(
    SinricProDevice,
    PowerStateController,
    BrightnessController,
    ColorController,
    ColorTemperatureController,
    SettingController,
    PushNotification,
):
    """
    SinricPro Light device.

    A smart light with power state, brightness, color, and color temperature control.

    Example:
        >>> from sinricpro import SinricPro, SinricProLight
        >>>
        >>> # Create light
        >>> my_light = SinricProLight("5dc1564130xxxxxxxxxxxxxx")
        >>>
        >>> # Register callbacks
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"Light {'on' if state else 'off'}")
        ...     return True
        >>>
        >>> async def on_brightness(brightness: int) -> bool:
        ...     print(f"Brightness: {brightness}%")
        ...     return True
        >>>
        >>> async def on_color(r: int, g: int, b: int) -> bool:
        ...     print(f"Color: RGB({r}, {g}, {b})")
        ...     return True
        >>>
        >>> async def on_color_temperature(temp: int) -> bool:
        ...     print(f"Color temperature: {temp}K")
        ...     return True
        >>>
        >>> my_light.on_power_state(on_power_state)
        >>> my_light.on_brightness(on_brightness)
        >>> my_light.on_color(on_color)
        >>> my_light.on_color_temperature(on_color_temperature)
        >>>
        >>> # Add to SinricPro
        >>> sinric_pro = SinricPro.get_instance()
        >>> sinric_pro.add(my_light)
    """

    def __init__(self, device_id: str) -> None:
        """
        Initialize a SinricProLight.

        Args:
            device_id: Unique device ID (24 hex characters)

        Example:
            >>> my_light = SinricProLight("5dc1564130xxxxxxxxxxxxxx")
        """
        super().__init__(device_id=device_id, product_type="LIGHT")

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle incoming requests for this light.

        Args:
            request: The request to handle

        Returns:
            True if request was handled successfully, False otherwise
        """
        action = request.action

        # Handle setPowerState action
        if action == ACTION_SET_POWER_STATE:
            state_str = request.request_value.get("state", "Off")
            state = state_str.lower() == "on"

            success, response_value = await self.handle_power_state_request(state, self)
            request.response_value = response_value
            return success

        # Handle setBrightness action
        elif action == ACTION_SET_BRIGHTNESS:
            brightness = request.request_value.get("brightness", 0)

            success, response_value = await self.handle_brightness_request(brightness, self)
            request.response_value = response_value
            return success

        # Handle adjustBrightness action
        elif action == ACTION_ADJUST_BRIGHTNESS:
            brightness_delta = request.request_value.get("brightnessDelta", 0)

            success, response_value = await self.handle_adjust_brightness_request(
                brightness_delta, self
            )
            request.response_value = response_value
            return success

        # Handle setColor action
        elif action == ACTION_SET_COLOR:
            color = request.request_value.get("color", {})

            success, response_value = await self.handle_color_request(color, self)
            request.response_value = response_value
            return success

        # Handle setColorTemperature action
        elif action == ACTION_SET_COLOR_TEMPERATURE:
            color_temperature = request.request_value.get("colorTemperature", 2700)

            success, response_value = await self.handle_color_temperature_request(
                color_temperature, self
            )
            request.response_value = response_value
            return success

        # Handle increaseColorTemperature action
        elif action == ACTION_INCREASE_COLOR_TEMPERATURE:
            success, response_value = await self.handle_increase_color_temperature_request(self)
            request.response_value = response_value
            return success

        # Handle decreaseColorTemperature action
        elif action == ACTION_DECREASE_COLOR_TEMPERATURE:
            success, response_value = await self.handle_decrease_color_temperature_request(self)
            request.response_value = response_value
            return success

        # Handle setSetting action
        elif action == ACTION_SET_SETTING:
            setting = request.request_value.get("setting", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting, value, self)
            request.response_value = response_value
            return success

        # Missing callback function
        request.error_message = f"Missing callback function: {action}"
        return False
