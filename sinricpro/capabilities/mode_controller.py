"""
ModeController Capability

Provides mode control functionality (open/close) for garage doors, etc.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_MODE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

ModeStateCallback = Callable[[str], Awaitable[bool]]


class ModeController:
    """Mixin providing door control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize ModeController mixin."""
        super().__init__(*args, **kwargs)
        self._mode_state_callback: ModeStateCallback | None = None
        self._mode_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_mode_state(self, callback: ModeStateCallback) -> None:
        """Register callback for mode changes."""
        self._mode_state_callback = callback

    async def handle_mode_request(
        self, mode: str, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle setMode request."""
        if not self._mode_state_callback:
            SinricProLogger.error(f"No door state callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._mode_state_callback(mode)
            if success:
                return True, {"mode": mode}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in door state callback: {e}")
            return False, {}

    async def send_mode_event(self, mode: str, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send door mode event (Open/Close)."""
        if not self._mode_limiter.can_send_event():
            SinricProLogger.warn("Door mode event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("ModeController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_MODE, value={"mode": mode}, cause=cause)

        if success:
            self._mode_limiter.event_sent()

        return success
