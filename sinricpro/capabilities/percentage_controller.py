"""
PercentageController Capability

Provides percentage-based control (0-100%) for devices like blinds.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_PERCENTAGE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type alias for percentage callback
PercentageCallback = Callable[[int], Awaitable[bool]]


class PercentageController:
    """
    Mixin providing percentage control capability.

    Used for devices that have a position/level expressed as a percentage (0-100%).

    Example:
        >>> class MyBlinds(SinricProDevice, PercentageController):
        ...     pass
        >>> blinds = MyBlinds("device_id", "BLINDS")
        >>> async def on_percentage(percentage: int) -> bool:
        ...     print(f"Position: {percentage}%")
        ...     return True
        >>> blinds.on_percentage(on_percentage)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize PercentageController mixin."""
        super().__init__(*args, **kwargs)
        self._percentage_callback: PercentageCallback | None = None
        self._percentage_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_percentage(self, callback: PercentageCallback) -> None:
        """
        Register callback for percentage changes.

        Args:
            callback: Async function called when percentage changes.
                     Receives int (0-100), returns bool (success).

        Example:
            >>> async def handle_percentage(percentage: int) -> bool:
            ...     # Set device position to percentage%
            ...     print(f"Setting position to {percentage}%")
            ...     return True
            >>> device.on_percentage(handle_percentage)
        """
        self._percentage_callback = callback

    async def handle_percentage_request(
        self, percentage: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle setPercentage request.

        Args:
            percentage: Requested percentage (0-100)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._percentage_callback:
            SinricProLogger.error(f"No percentage callback registered for {device.get_device_id()}")
            return False, {}

        # Validate percentage range
        if not 0 <= percentage <= 100:
            SinricProLogger.error(f"Invalid percentage value: {percentage} (must be 0-100)")
            return False, {}

        try:
            success = await self._percentage_callback(percentage)
            if success:
                return True, {"percentage": percentage}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in percentage callback: {e}")
            return False, {}

    async def handle_adjust_percentage_request(
        self, percentage_delta: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle adjustPercentage request (relative change).

        Args:
            percentage_delta: Percentage change amount (-100 to +100)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._percentage_callback:
            SinricProLogger.error(f"No percentage callback registered for {device.get_device_id()}")
            return False, {}

        try:
            # Note: In real implementation, track current percentage and calculate new value
            success = await self._percentage_callback(percentage_delta)
            if success:
                return True, {"percentage": percentage_delta}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in adjust percentage callback: {e}")
            return False, {}

    async def send_percentage_event(
        self, percentage: int, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a percentage event to SinricPro.

        Args:
            percentage: Current percentage (0-100)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await blinds.send_percentage_event(75)  # 75% open
            True
        """
        # Validate percentage range
        if not 0 <= percentage <= 100:
            SinricProLogger.error(f"Invalid percentage value: {percentage} (must be 0-100)")
            return False

        # Check rate limiting
        if not self._percentage_limiter.can_send_event():
            SinricProLogger.warn("Percentage event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("PercentageController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_PERCENTAGE,
            value={"percentage": percentage},
            cause=cause,
        )

        if success:
            self._percentage_limiter.event_sent()

        return success
