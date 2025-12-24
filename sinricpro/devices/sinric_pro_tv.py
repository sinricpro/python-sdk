"""
SinricProTV Device

Smart TV device with power, volume, mute, media, channel, and input control.
"""

from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.volume_controller import VolumeController
from sinricpro.capabilities.mute_controller import MuteController
from sinricpro.capabilities.media_controller import MediaController
from sinricpro.capabilities.channel_controller import ChannelController
from sinricpro.capabilities.input_controller import InputController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.actions import (
    ACTION_SET_POWER_STATE,
    ACTION_SET_VOLUME,
    ACTION_ADJUST_VOLUME,
    ACTION_SET_MUTE,
    ACTION_MEDIA_CONTROL,
    ACTION_CHANGE_CHANNEL,
    ACTION_SKIP_CHANNELS,
    ACTION_SELECT_INPUT,
    ACTION_SET_SETTING,
)
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest


class SinricProTV(
    SinricProDevice,
    PowerStateController,
    VolumeController,
    MuteController,
    MediaController,
    ChannelController,
    InputController,
    SettingController,
    PushNotification
):
    """
    SinricPro TV device.

    A smart TV with power, volume, mute, media playback, channel, and input control.

    Example:
        >>> from sinricpro import SinricPro, SinricProTV
        >>>
        >>> # Create TV
        >>> my_tv = SinricProTV("5dc1564130xxxxxxxxxxxxxx")
        >>>
        >>> # Register power state callback
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"TV {'on' if state else 'off'}")
        ...     return True
        >>>
        >>> # Register volume callback
        >>> async def on_volume(volume: int) -> bool:
        ...     print(f"Volume set to {volume}")
        ...     return True
        >>>
        >>> # Register channel callback
        >>> async def on_change_channel(channel: dict) -> bool:
        ...     print(f"Channel changed to {channel.get('name') or channel.get('number')}")
        ...     return True
        >>>
        >>> my_tv.on_power_state(on_power_state)
        >>> my_tv.on_volume(on_volume)
        >>> my_tv.on_change_channel(on_change_channel)
        >>>
        >>> # Add to SinricPro
        >>> sinric_pro = SinricPro.get_instance()
        >>> sinric_pro.add(my_tv)
    """

    def __init__(self, device_id: str) -> None:
        """
        Initialize a SinricProTV.

        Args:
            device_id: Unique device ID (24 hex characters)

        Example:
            >>> my_tv = SinricProTV("5dc1564130xxxxxxxxxxxxxx")
        """
        super().__init__(device_id=device_id, product_type="TV")

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle incoming requests for this TV.

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

        # Handle setVolume action
        elif action == ACTION_SET_VOLUME:
            volume = request.request_value.get("volume", 0)
            success, response_value = await self.handle_volume_request(volume, self)
            request.response_value = response_value
            return success

        # Handle adjustVolume action
        elif action == ACTION_ADJUST_VOLUME:
            volume_delta = request.request_value.get("volumeDelta", 0)
            success, response_value = await self.handle_adjust_volume_request(volume_delta, self)
            request.response_value = response_value
            return success

        # Handle setMute action
        elif action == ACTION_SET_MUTE:
            mute = request.request_value.get("mute", False)
            success, response_value = await self.handle_mute_request(mute, self)
            request.response_value = response_value
            return success

        # Handle mediaControl action
        elif action == ACTION_MEDIA_CONTROL:
            control = request.request_value.get("control", "")
            success, response_value = await self.handle_media_control_request(control, self)
            request.response_value = response_value
            return success

        # Handle changeChannel action
        elif action == ACTION_CHANGE_CHANNEL:
            channel = request.request_value.get("channel", {})
            success, response_value = await self.handle_change_channel_request(channel, self)
            request.response_value = response_value
            return success

        # Handle skipChannels action
        elif action == ACTION_SKIP_CHANNELS:
            channel_count = request.request_value.get("channelCount", 0)
            success, response_value = await self.handle_skip_channels_request(channel_count, self)
            request.response_value = response_value
            return success

        # Handle selectInput action
        elif action == ACTION_SELECT_INPUT:
            input_name = request.request_value.get("input", "")
            success, response_value = await self.handle_select_input_request(input_name, self)
            request.response_value = response_value
            return success

        # Handle setSetting action
        elif action == ACTION_SET_SETTING:
            setting_id = request.request_value.get("id", "")
            value = request.request_value.get("value")
            success, response_value = await self.handle_setting_request(setting_id, value, self)
            request.response_value = response_value
            return success

        # Missing callback function
        request.error_message = f"Missing callback function: {action}"
        return False
