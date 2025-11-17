"""
ColorController Capability

Provides RGB color control functionality for color-capable devices.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_COLOR
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type alias for color callback
ColorCallback = Callable[[int, int, int], Awaitable[bool]]


class ColorController:
    """
    Mixin providing RGB color control capability.

    Provides methods to handle color changes and send color events.

    Example:
        >>> class MyLight(SinricProDevice, ColorController):
        ...     pass
        >>> light = MyLight("device_id", "LIGHT")
        >>> async def on_color(r: int, g: int, b: int) -> bool:
        ...     print(f"Color: RGB({r}, {g}, {b})")
        ...     return True
        >>> light.on_color(on_color)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize ColorController mixin."""
        super().__init__(*args, **kwargs)
        self._color_callback: ColorCallback | None = None
        self._color_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_color(self, callback: ColorCallback) -> None:
        """
        Register callback for color changes.

        Args:
            callback: Async function called when color changes.
                     Receives r, g, b (each 0-255), returns bool (success).

        Example:
            >>> async def handle_color(r: int, g: int, b: int) -> bool:
            ...     # Set device color to RGB(r, g, b)
            ...     print(f"Setting color to RGB({r}, {g}, {b})")
            ...     return True
            >>> light.on_color(handle_color)
        """
        self._color_callback = callback

    async def handle_color_request(
        self, color: dict[str, Any], device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle setColor request.

        Args:
            color: Color dict with 'r', 'g', 'b' keys (each 0-255)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._color_callback:
            SinricProLogger.error(f"No color callback registered for {device.get_device_id()}")
            return False, {}

        try:
            # Extract RGB values
            r = color.get("r", 0)
            g = color.get("g", 0)
            b = color.get("b", 0)

            # Validate RGB range
            if not all(0 <= val <= 255 for val in [r, g, b]):
                SinricProLogger.error(f"Invalid RGB values: ({r}, {g}, {b}) - must be 0-255")
                return False, {}

            success = await self._color_callback(r, g, b)
            if success:
                return True, {"color": {"r": r, "g": g, "b": b}}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in color callback: {e}")
            return False, {}

    async def send_color_event(
        self, r: int, g: int, b: int, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a color event to SinricPro.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await light.send_color_event(255, 0, 0)  # Red
            True
        """
        # Validate RGB range
        if not all(0 <= val <= 255 for val in [r, g, b]):
            SinricProLogger.error(f"Invalid RGB values: ({r}, {g}, {b}) - must be 0-255")
            return False

        # Check rate limiting
        if not self._color_limiter.can_send_event():
            SinricProLogger.warn("Color event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("ColorController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_COLOR,
            value={"color": {"r": r, "g": g, "b": b}},
            cause=cause,
        )

        if success:
            self._color_limiter.event_sent()

        return success
