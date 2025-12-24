"""
ChannelController Capability

Provides TV channel control functionality.
"""

from typing import Any, Callable, Awaitable, TypedDict, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_CHANGE_CHANNEL, ACTION_SKIP_CHANNELS
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class ChannelInfo(TypedDict, total=False):
    """Channel information."""
    name: str
    number: str


ChangeChannelCallback = Callable[[ChannelInfo], Awaitable[bool]]
SkipChannelsCallback = Callable[[int], Awaitable[bool]]


class ChannelController:
    """Mixin providing TV channel control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize ChannelController mixin."""
        super().__init__(*args, **kwargs)
        self._change_channel_callback: ChangeChannelCallback | None = None
        self._skip_channels_callback: SkipChannelsCallback | None = None
        self._channel_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_change_channel(self, callback: ChangeChannelCallback) -> None:
        """Register callback for channel changes.

        Args:
            callback: Async function that receives channel info dict and returns True on success.
                      Channel dict may contain: name, number
        """
        self._change_channel_callback = callback

    def on_skip_channels(self, callback: SkipChannelsCallback) -> None:
        """Register callback for skipping channels.

        Args:
            callback: Async function that receives channel count (positive=forward, negative=backward)
                      and returns True on success
        """
        self._skip_channels_callback = callback

    async def handle_change_channel_request(
        self, channel: ChannelInfo, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle changeChannel request."""
        if not self._change_channel_callback:
            SinricProLogger.error(f"No change channel callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._change_channel_callback(channel)
            if success:
                return True, {"channel": channel}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in change channel callback: {e}")
            return False, {}

    async def handle_skip_channels_request(
        self, channel_count: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle skipChannels request."""
        if not self._skip_channels_callback:
            SinricProLogger.error(f"No skip channels callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._skip_channels_callback(channel_count)
            if success:
                return True, {"channelCount": channel_count}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in skip channels callback: {e}")
            return False, {}

    async def send_channel_event(
        self, channel: ChannelInfo, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """Send channel event to SinricPro.

        Args:
            channel: Channel information
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._channel_limiter.can_send_event():
            SinricProLogger.warn("Channel event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("ChannelController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_CHANGE_CHANNEL, value={"channel": channel}, cause=cause)

        if success:
            self._channel_limiter.event_sent()

        return success
