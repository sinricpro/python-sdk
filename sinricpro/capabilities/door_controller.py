"""
DoorController Capability

Provides door control functionality (open/close) for garage doors, etc.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_MODE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

DoorStateCallback = Callable[[str], Awaitable[bool]]


class DoorController:
    """Mixin providing door control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize DoorController mixin."""
        super().__init__(*args, **kwargs)
        self._door_state_callback: DoorStateCallback | None = None
        self._door_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_door_state(self, callback: DoorStateCallback) -> None:
        """Register callback for door state changes (Open/Close)."""
        self._door_state_callback = callback

    async def handle_door_state_request(
        self, mode: str, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle setDoorState request."""
        if not self._door_state_callback:
            SinricProLogger.error(f"No door state callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._door_state_callback(mode)
            if success:
                return True, {"mode": mode}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in door state callback: {e}")
            return False, {}

    async def send_door_state_event(self, mode: str, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send door mode event (Open/Close)."""
        if not self._door_limiter.can_send_event():
            SinricProLogger.warn("Door mode event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("DoorController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_MODE, value={"mode": mode}, cause=cause)

        if success:
            self._door_limiter.event_sent()

        return success
