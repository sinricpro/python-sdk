"""
BrightnessController Capability

Provides brightness control functionality for dimmable devices.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_BRIGHTNESS
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type alias for brightness callback
BrightnessCallback = Callable[[int], Awaitable[bool]]
AdjustBrightnessCallback = Callable[[int], Awaitable[tuple[bool, int]]]

class BrightnessController:
    """
    Mixin providing brightness control capability.

    Provides methods to handle brightness changes (0-100%) and send brightness events.

    Example:
        >>> class MyLight(SinricProDevice, BrightnessController):
        ...     pass
        >>> light = MyLight("device_id", "LIGHT")
        >>> async def on_brightness(brightness: int) -> bool:
        ...     print(f"Brightness: {brightness}%")
        ...     return True
        >>> light.on_brightness(on_brightness)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize BrightnessController mixin."""
        super().__init__(*args, **kwargs)
        self._brightness_callback: BrightnessCallback | None = None
        self._adjust_brightness_callback: AdjustBrightnessCallback | None = None
        self._brightness_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_brightness(self, callback: BrightnessCallback) -> None:
        """
        Register callback for brightness changes.

        Args:
            callback: Async function called when brightness changes.
                     Receives int (0-100), returns bool (success).

        Example:
            >>> async def handle_brightness(brightness: int) -> bool:
            ...     # Set device brightness to brightness%
            ...     print(f"Setting brightness to {brightness}%")
            ...     return True
            >>> light.on_brightness(handle_brightness)
        """
        self._brightness_callback = callback

    def on_adjust_brightness(self, callback: BrightnessCallback) -> None:
        """
        Register callback for adjust brightness changes.

        Args:
            callback: Async function called when brightness changes.
                     Receives int (0-100), returns bool (success).

        Example:
            >>> async def handle_adjust_brightness(brightnessDelta: int) -> bool:
            ...     # adjust device brightness to brightnessDelta%
            ...     print(f"Setting brightness to {brightnessDelta}%")
            ...     return True
            >>> light.on_adjust_brightness(handle_adjust_brightness)
        """
        self._adjust_brightness_callback = callback

    async def handle_brightness_request(
        self, brightness: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle setBrightness request.

        Args:
            brightness: Requested brightness level (0-100)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._brightness_callback:
            SinricProLogger.error(f"No brightness callback registered for {device.get_device_id()}")
            return False, {}

        # Validate brightness range
        if not 0 <= brightness <= 100:
            SinricProLogger.error(f"Invalid brightness value: {brightness} (must be 0-100)")
            return False, {}

        try:
            success = await self._brightness_callback(brightness)
            if success:
                return True, {"brightness": brightness}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in brightness callback: {e}")
            return False, {}

    async def handle_adjust_brightness_request(
        self, brightness_delta: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle adjustBrightness request (relative change).

        Args:
            brightness_delta: Brightness change amount (-100 to +100)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._adjust_brightness_callback:
            SinricProLogger.error(f"No adjust brightness callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success, brightness = await self._adjust_brightness_callback(brightness_delta)
            if success:
                return True, {"brightness": brightness}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in adjust brightness callback: {e}")
            return False, {}

    async def send_brightness_event(
        self, brightness: int, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a brightness event to SinricPro.

        Args:
            brightness: Current brightness level (0-100)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await light.send_brightness_event(75)  # Brightness at 75%
            True
        """
        # Validate brightness range
        if not 0 <= brightness <= 100:
            SinricProLogger.error(f"Invalid brightness value: {brightness} (must be 0-100)")
            return False

        # Check rate limiting
        if not self._brightness_limiter.can_send_event():
            SinricProLogger.warn("Brightness event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("BrightnessController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_BRIGHTNESS,
            value={"brightness": brightness},
            cause=cause,
        )

        if success:
            self._brightness_limiter.event_sent()

        return success
