"""
MediaController Capability

Provides media playback control functionality for speakers, TVs, and media devices.
"""

from typing import Any, Callable, Awaitable, Literal, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_MEDIA_CONTROL
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

MediaControl = Literal["Play", "Pause", "Stop", "StartOver", "Previous", "Next", "Rewind", "FastForward"]
MediaControlCallback = Callable[[MediaControl], Awaitable[bool]]


class MediaController:
    """Mixin providing media playback control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize MediaController mixin."""
        super().__init__(*args, **kwargs)
        self._media_control_callback: MediaControlCallback | None = None
        self._media_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_media_control(self, callback: MediaControlCallback) -> None:
        """Register callback for media control commands.

        Args:
            callback: Async function that receives media control command and returns True on success.
                      Commands: Play, Pause, Stop, StartOver, Previous, Next, Rewind, FastForward
        """
        self._media_control_callback = callback

    async def handle_media_control_request(
        self, control: MediaControl, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle mediaControl request."""
        if not self._media_control_callback:
            SinricProLogger.error(f"No media control callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._media_control_callback(control)
            if success:
                return True, {"control": control}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in media control callback: {e}")
            return False, {}

    async def send_media_control_event(
        self, control: MediaControl, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """Send media control event to SinricPro.

        Args:
            control: Media control command (Play, Pause, Stop, etc.)
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._media_limiter.can_send_event():
            SinricProLogger.warn("Media control event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("MediaController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_MEDIA_CONTROL, value={"control": control}, cause=cause)

        if success:
            self._media_limiter.event_sent()

        return success
