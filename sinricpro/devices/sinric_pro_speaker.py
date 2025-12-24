"""
SinricProSpeaker Device

Smart speaker device with power, volume, mute, media, equalizer, and mode control.
"""

from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.volume_controller import VolumeController
from sinricpro.capabilities.mute_controller import MuteController
from sinricpro.capabilities.media_controller import MediaController
from sinricpro.capabilities.equalizer_controller import EqualizerController
from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.push_notification import PushNotification
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.core.actions import (
    ACTION_SET_POWER_STATE,
    ACTION_SET_VOLUME,
    ACTION_ADJUST_VOLUME,
    ACTION_SET_MUTE,
    ACTION_MEDIA_CONTROL,
    ACTION_SET_BANDS,
    ACTION_ADJUST_BANDS,
    ACTION_SET_MODE,
    ACTION_SET_SETTING,
)
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import SinricProRequest


class SinricProSpeaker(
    SinricProDevice,
    PowerStateController,
    VolumeController,
    MuteController,
    MediaController,
    EqualizerController,
    ModeController,
    SettingController,
    PushNotification
):
    """
    SinricPro Speaker device.

    A smart speaker with power, volume, mute, media playback, equalizer, and mode control.

    Example:
        >>> from sinricpro import SinricPro, SinricProSpeaker
        >>>
        >>> # Create Speaker
        >>> my_speaker = SinricProSpeaker("5dc1564130xxxxxxxxxxxxxx")
        >>>
        >>> # Register power state callback
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"Speaker {'on' if state else 'off'}")
        ...     return True
        >>>
        >>> # Register volume callback
        >>> async def on_volume(volume: int) -> bool:
        ...     print(f"Volume set to {volume}")
        ...     return True
        >>>
        >>> my_speaker.on_power_state(on_power_state)
        >>> my_speaker.on_volume(on_volume)
        >>>
        >>> # Add to SinricPro
        >>> sinric_pro = SinricPro.get_instance()
        >>> sinric_pro.add(my_speaker)
    """

    def __init__(self, device_id: str) -> None:
        """
        Initialize a SinricProSpeaker.

        Args:
            device_id: Unique device ID (24 hex characters)

        Example:
            >>> my_speaker = SinricProSpeaker("5dc1564130xxxxxxxxxxxxxx")
        """
        super().__init__(device_id=device_id, product_type="SPEAKER")

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle incoming requests for this speaker.

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

        # Handle setBands action
        elif action == ACTION_SET_BANDS:
            bands = request.request_value.get("bands", {})
            success, response_value = await self.handle_set_bands_request(bands, self)
            request.response_value = response_value
            return success

        # Handle adjustBands action
        elif action == ACTION_ADJUST_BANDS:
            bands = request.request_value.get("bands", {})
            success, response_value = await self.handle_adjust_bands_request(bands, self)
            request.response_value = response_value
            return success

        # Handle setMode action
        elif action == ACTION_SET_MODE:
            mode = request.request_value.get("mode", "")
            instance_id = request.instance
            success, response_value = await self.handle_mode_request(mode, instance_id, self)
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
