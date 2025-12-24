"""
MuteController Capability

Provides mute/unmute functionality for speakers, TVs, and other audio devices.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_MUTE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

MuteCallback = Callable[[bool], Awaitable[bool]]


class MuteController:
    """Mixin providing mute control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize MuteController mixin."""
        super().__init__(*args, **kwargs)
        self._mute_callback: MuteCallback | None = None
        self._mute_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_mute(self, callback: MuteCallback) -> None:
        """Register callback for mute changes.

        Args:
            callback: Async function that receives mute state (True=muted) and returns True on success
        """
        self._mute_callback = callback

    async def handle_mute_request(
        self, mute: bool, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle setMute request."""
        if not self._mute_callback:
            SinricProLogger.error(f"No mute callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._mute_callback(mute)
            if success:
                return True, {"mute": mute}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in mute callback: {e}")
            return False, {}

    async def send_mute_event(self, mute: bool, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send mute event to SinricPro.

        Args:
            mute: True if muted, False if unmuted
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._mute_limiter.can_send_event():
            SinricProLogger.warn("Mute event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("MuteController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_MUTE, value={"mute": mute}, cause=cause)

        if success:
            self._mute_limiter.event_sent()

        return success
