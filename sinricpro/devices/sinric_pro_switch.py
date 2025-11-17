"""
SinricProSwitch Device

Smart switch device with power state control.
"""

from typing import Any

from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.actions import ACTION_SET_POWER_STATE, ACTION_SET_SETTING
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest


class SinricProSwitch(SinricProDevice, PowerStateController, SettingController, PushNotification):
    """
    SinricPro Switch device.

    A simple on/off switch with power state control capability.

    Example:
        >>> from sinricpro import SinricPro, SinricProSwitch
        >>>
        >>> # Create switch
        >>> my_switch = SinricProSwitch("5dc1564130xxxxxxxxxxxxxx")
        >>>
        >>> # Register power state callback
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"Switch {'on' if state else 'off'}")
        ...     # Turn physical switch on/off here
        ...     return True
        >>>
        >>> my_switch.on_power_state(on_power_state)
        >>>
        >>> # Add to SinricPro
        >>> sinric_pro = SinricPro.get_instance()
        >>> sinric_pro.add(my_switch)
    """

    def __init__(self, device_id: str) -> None:
        """
        Initialize a SinricProSwitch.

        Args:
            device_id: Unique device ID (24 hex characters)

        Example:
            >>> my_switch = SinricProSwitch("5dc1564130xxxxxxxxxxxxxx")
        """
        super().__init__(device_id=device_id, product_type="SWITCH")

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle incoming requests for this switch.

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
