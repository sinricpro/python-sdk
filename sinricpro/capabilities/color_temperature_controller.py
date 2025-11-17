"""
ColorTemperatureController Capability

Provides color temperature control functionality for lights.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_COLOR_TEMPERATURE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type alias for color temperature callback
ColorTemperatureCallback = Callable[[int], Awaitable[bool]]


class ColorTemperatureController:
    """
    Mixin providing color temperature control capability.

    Provides methods to handle color temperature changes (in Kelvin) and send events.

    Example:
        >>> class MyLight(SinricProDevice, ColorTemperatureController):
        ...     pass
        >>> light = MyLight("device_id", "LIGHT")
        >>> async def on_color_temperature(temp: int) -> bool:
        ...     print(f"Color temperature: {temp}K")
        ...     return True
        >>> light.on_color_temperature(on_color_temperature)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize ColorTemperatureController mixin."""
        super().__init__(*args, **kwargs)
        self._color_temperature_callback: ColorTemperatureCallback | None = None
        self._color_temperature_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_color_temperature(self, callback: ColorTemperatureCallback) -> None:
        """
        Register callback for color temperature changes.

        Args:
            callback: Async function called when color temperature changes.
                     Receives int (temperature in Kelvin, typically 2000-7000),
                     returns bool (success).

        Example:
            >>> async def handle_color_temperature(temp: int) -> bool:
            ...     # Set device color temperature
            ...     print(f"Setting color temperature to {temp}K")
            ...     return True
            >>> light.on_color_temperature(handle_color_temperature)
        """
        self._color_temperature_callback = callback

    async def handle_color_temperature_request(
        self, color_temperature: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle setColorTemperature request.

        Args:
            color_temperature: Requested color temperature in Kelvin (typically 2000-7000)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._color_temperature_callback:
            SinricProLogger.error(
                f"No color temperature callback registered for {device.get_device_id()}"
            )
            return False, {}

        # Validate color temperature range (typical range is 2000-7000K)
        if not 1000 <= color_temperature <= 10000:
            SinricProLogger.warn(
                f"Color temperature {color_temperature}K outside typical range (2000-7000K)"
            )

        try:
            success = await self._color_temperature_callback(color_temperature)
            if success:
                return True, {"colorTemperature": color_temperature}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in color temperature callback: {e}")
            return False, {}

    async def handle_increase_color_temperature_request(
        self, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle increaseColorTemperature request.

        Args:
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        # Note: In a real implementation, you'd need to track current temperature
        # and increase it by a defined step (e.g., 500K)
        SinricProLogger.warn("increaseColorTemperature not fully implemented - needs state tracking")
        return False, {}

    async def handle_decrease_color_temperature_request(
        self, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle decreaseColorTemperature request.

        Args:
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        # Note: In a real implementation, you'd need to track current temperature
        # and decrease it by a defined step (e.g., 500K)
        SinricProLogger.warn("decreaseColorTemperature not fully implemented - needs state tracking")
        return False, {}

    async def send_color_temperature_event(
        self, color_temperature: int, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a color temperature event to SinricPro.

        Args:
            color_temperature: Current color temperature in Kelvin
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await light.send_color_temperature_event(4000)  # 4000K (neutral white)
            True
        """
        # Validate color temperature range
        if not 1000 <= color_temperature <= 10000:
            SinricProLogger.warn(
                f"Color temperature {color_temperature}K outside typical range (2000-7000K)"
            )

        # Check rate limiting
        if not self._color_temperature_limiter.can_send_event():
            SinricProLogger.warn("Color temperature event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("ColorTemperatureController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_COLOR_TEMPERATURE,
            value={"colorTemperature": color_temperature},
            cause=cause,
        )

        if success:
            self._color_temperature_limiter.event_sent()

        return success
