"""
PowerStateController Capability

Provides power state control (On/Off) functionality for devices.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_POWER_STATE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Type alias for power state callback
PowerStateCallback = Callable[[bool], Awaitable[bool]]


class PowerStateController:
    """
    Mixin providing power state control capability.

    Provides methods to handle power state changes and send power state events.

    Example:
        >>> class MyDevice(SinricProDevice, PowerStateController):
        ...     pass
        >>> device = MyDevice("device_id", "SWITCH")
        >>> async def on_power_state(state: bool) -> bool:
        ...     print(f"Power state: {'On' if state else 'Off'}")
        ...     return True
        >>> device.on_power_state(on_power_state)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize PowerStateController mixin."""
        super().__init__(*args, **kwargs)
        self._power_state_callback: PowerStateCallback | None = None
        self._power_state_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_power_state(self, callback: PowerStateCallback) -> None:
        """
        Register callback for power state changes.

        Args:
            callback: Async function called when power state changes.
                     Receives bool (True=On, False=Off), returns bool (success).

        Example:
            >>> async def handle_power_state(state: bool) -> bool:
            ...     if state:
            ...         # Turn on the device
            ...         return True
            ...     else:
            ...         # Turn off the device
            ...         return True
            >>> device.on_power_state(handle_power_state)
        """
        self._power_state_callback = callback

    async def handle_power_state_request(
        self, state: bool, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """
        Handle setPowerState request.

        Args:
            state: Requested power state (True=On, False=Off)
            device: The device instance

        Returns:
            Tuple of (success, response_value)
        """
        if not self._power_state_callback:
            SinricProLogger.error(f"No power state callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._power_state_callback(state)
            if success:
                return True, {"state": "On" if state else "Off"}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in power state callback: {e}")
            return False, {}

    async def send_power_state_event(
        self, state: bool, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a power state event to SinricPro.

        Args:
            state: Current power state (True=On, False=Off)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await device.send_power_state_event(True)  # Device turned on
            True
        """
        # Check rate limiting
        if not self._power_state_limiter.can_send_event():
            SinricProLogger.warn("Power state event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("PowerStateController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_POWER_STATE,
            value={"state": "On" if state else "Off"},
            cause=cause,
        )

        if success:
            self._power_state_limiter.event_sent()

        return success
