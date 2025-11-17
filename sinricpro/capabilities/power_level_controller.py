"""
PowerLevelController Capability

Provides power level control functionality (0-100 scale) for dimmable devices.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_POWER_LEVEL, ACTION_ADJUST_POWER_LEVEL
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type aliases for power level callbacks
PowerLevelCallback = Callable[[int], Awaitable[bool]]
AdjustPowerLevelCallback = Callable[[int], Awaitable[tuple[bool, int]]]


class PowerLevelController:
    """
    Mixin providing power level control capability.

    Provides methods to handle power level changes (0-100 scale) and send power level events.
    Used for dimmable switches and similar devices.

    Example:
        >>> class MyDimSwitch(SinricProDevice, PowerLevelController):
        ...     pass
        >>> device = MyDimSwitch("device_id", "DIMMABLE_SWITCH")
        >>> async def on_power_level(level: int) -> bool:
        ...     print(f"Power level: {level}%")
        ...     return True
        >>> device.on_power_level(on_power_level)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize PowerLevelController mixin."""
        super().__init__(*args, **kwargs)
        self._power_level_callback: PowerLevelCallback | None = None
        self._adjust_power_level_callback: AdjustPowerLevelCallback | None = None
        self._power_level_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_power_level(self, callback: PowerLevelCallback) -> None:
        """
        Register callback for power level changes.

        Args:
            callback: Async function called when power level changes.
                     Receives int (0-100), returns bool (success).

        Example:
            >>> async def handle_power_level(level: int) -> bool:
            ...     # Set device to power level (0-100)
            ...     print(f"Setting power level to {level}%")
            ...     return True
            >>> device.on_power_level(handle_power_level)
        """
        self._power_level_callback = callback

    def on_adjust_power_level(self, callback: AdjustPowerLevelCallback) -> None:
        """
        Register callback for relative power level adjustments.

        Args:
            callback: Async function called when power level should be adjusted.
                     Receives int delta (-100 to +100), returns bool (success).

        Example:
            >>> async def handle_adjust_power_level(delta: int) -> bool:
            ...     # Adjust power level by delta
            ...     new_level = max(0, min(100, current_level + delta))
            ...     print(f"Adjusting power level by {delta:+d}% to {new_level}%")
            ...     return True
            >>> device.on_adjust_power_level(handle_adjust_power_level)
        """
        self._adjust_power_level_callback = callback

    async def handle_power_level_request(
        self, power_level: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle setPowerLevel request.

        Args:
            power_level: Requested power level (0-100)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._power_level_callback:
            SinricProLogger.error(f"No power level callback registered for {device.get_device_id()}")
            return False, {}

        # Validate power level range
        if not 0 <= power_level <= 100:
            SinricProLogger.error(f"Invalid power level: {power_level} (must be 0-100)")
            return False, {}

        try:
            success = await self._power_level_callback(power_level)
            if success:
                return True, {"powerLevel": power_level}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in power level callback: {e}")
            return False, {}

    async def handle_adjust_power_level_request(
        self, power_level_delta: int, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle adjustPowerLevel request.

        Args:
            power_level_delta: Change in power level (-100 to +100)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._adjust_power_level_callback:
            SinricProLogger.error(f"No adjust power level callback registered for {device.get_device_id()}")
            return False, {}

        # Validate delta range
        if not -100 <= power_level_delta <= 100:
            SinricProLogger.error(f"Invalid power level delta: {power_level_delta} (must be -100 to +100)")
            return False, {}

        try:
            success, power_level = await self._adjust_power_level_callback(power_level_delta)
            if success:
                # Note: The callback should handle the actual level calculation
                # We return the delta in the response as per the C++ implementation
                return True, {"powerLevel": power_level}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in adjust power level callback: {e}")
            return False, {}

    async def send_power_level_event(
        self, power_level: int, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a power level event to SinricPro.

        Args:
            power_level: Current power level (0-100)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await device.send_power_level_event(75)  # Device set to 75%
            True
        """
        # Validate power level range
        if not 0 <= power_level <= 100:
            SinricProLogger.error(f"Invalid power level: {power_level} (must be 0-100)")
            return False

        # Check rate limiting
        if not self._power_level_limiter.can_send_event():
            SinricProLogger.warn("Power level event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("PowerLevelController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_POWER_LEVEL,
            value={"powerLevel": power_level},
            cause=cause,
        )

        if success:
            self._power_level_limiter.event_sent()

        return success
