"""
VolumeController Capability

Provides volume control functionality for speakers, TVs, and other audio devices.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_VOLUME, ACTION_ADJUST_VOLUME
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

VolumeCallback = Callable[[int], Awaitable[bool]]
AdjustVolumeCallback = Callable[[int], Awaitable[bool]]


class VolumeController:
    """Mixin providing volume control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize VolumeController mixin."""
        super().__init__(*args, **kwargs)
        self._volume_callback: VolumeCallback | None = None
        self._adjust_volume_callback: AdjustVolumeCallback | None = None
        self._volume_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_volume(self, callback: VolumeCallback) -> None:
        """Register callback for volume changes.

        Args:
            callback: Async function that receives volume (0-100) and returns True on success
        """
        self._volume_callback = callback

    def on_adjust_volume(self, callback: AdjustVolumeCallback) -> None:
        """Register callback for volume adjustments.

        Args:
            callback: Async function that receives volume delta and returns True on success
        """
        self._adjust_volume_callback = callback

    async def handle_volume_request(
        self, volume: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle setVolume request."""
        if not self._volume_callback:
            SinricProLogger.error(f"No volume callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._volume_callback(volume)
            if success:
                return True, {"volume": volume}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in volume callback: {e}")
            return False, {}

    async def handle_adjust_volume_request(
        self, volume_delta: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle adjustVolume request."""
        if not self._adjust_volume_callback:
            SinricProLogger.error(f"No adjust volume callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._adjust_volume_callback(volume_delta)
            if success:
                return True, {"volume": volume_delta}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in adjust volume callback: {e}")
            return False, {}

    async def send_volume_event(self, volume: int, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send volume event to SinricPro.

        Args:
            volume: Volume level (0-100)
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._volume_limiter.can_send_event():
            SinricProLogger.warn("Volume event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("VolumeController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_VOLUME, value={"volume": volume}, cause=cause)

        if success:
            self._volume_limiter.event_sent()

        return success
