"""
EqualizerController Capability

Provides equalizer control functionality for speakers and audio devices.
Supports bass, midrange, and treble band adjustments.
"""

from typing import Any, Callable, Awaitable, TypedDict, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_BANDS, ACTION_ADJUST_BANDS
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class EqualizerBands(TypedDict, total=False):
    """Equalizer bands configuration."""
    bass: int
    midrange: int
    treble: int


SetBandsCallback = Callable[[EqualizerBands], Awaitable[bool]]
AdjustBandsCallback = Callable[[EqualizerBands], Awaitable[bool]]


class EqualizerController:
    """Mixin providing equalizer control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize EqualizerController mixin."""
        super().__init__(*args, **kwargs)
        self._set_bands_callback: SetBandsCallback | None = None
        self._adjust_bands_callback: AdjustBandsCallback | None = None
        self._equalizer_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_set_bands(self, callback: SetBandsCallback) -> None:
        """Register callback for setting equalizer bands.

        Args:
            callback: Async function that receives bands dict and returns True on success.
                      Bands dict may contain: bass, midrange, treble (values typically -10 to 10)
        """
        self._set_bands_callback = callback

    def on_adjust_bands(self, callback: AdjustBandsCallback) -> None:
        """Register callback for adjusting equalizer bands.

        Args:
            callback: Async function that receives bands delta dict and returns True on success.
                      Bands dict may contain: bass, midrange, treble (delta values)
        """
        self._adjust_bands_callback = callback

    async def handle_set_bands_request(
        self, bands: EqualizerBands, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle setBands request."""
        if not self._set_bands_callback:
            SinricProLogger.error(f"No set bands callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._set_bands_callback(bands)
            if success:
                return True, {"bands": bands}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in set bands callback: {e}")
            return False, {}

    async def handle_adjust_bands_request(
        self, bands: EqualizerBands, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle adjustBands request."""
        if not self._adjust_bands_callback:
            SinricProLogger.error(f"No adjust bands callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._adjust_bands_callback(bands)
            if success:
                return True, {"bands": bands}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in adjust bands callback: {e}")
            return False, {}

    async def send_bands_event(
        self, bands: EqualizerBands, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """Send equalizer bands event to SinricPro.

        Args:
            bands: Equalizer bands configuration
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._equalizer_limiter.can_send_event():
            SinricProLogger.warn("Equalizer bands event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("EqualizerController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_BANDS, value={"bands": bands}, cause=cause)

        if success:
            self._equalizer_limiter.event_sent()

        return success
