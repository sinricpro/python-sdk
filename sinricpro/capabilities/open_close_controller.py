"""OpenCloseController Capability - Open/close control for blinds, curtains."""
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_RANGE_VALUE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

OpenCloseCallback = Callable[[int], Awaitable[bool]]  # 0-100 (0=closed, 100=open)

class OpenCloseController:
    """Mixin providing open/close control capability."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._open_close_callback: OpenCloseCallback | None = None
        self._open_close_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_open_close(self, callback: OpenCloseCallback) -> None:
        """Register callback for open/close position changes (0=closed, 100=open)."""
        self._open_close_callback = callback

    async def handle_open_close_request(self, position: int, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setRangeValue request (used for open/close)."""
        if not self._open_close_callback:
            SinricProLogger.error(f"No open/close callback registered for {device.get_device_id()}")
            return False, {}
        if not 0 <= position <= 100:
            SinricProLogger.error(f"Invalid position: {position} (must be 0-100)")
            return False, {}
        try:
            success = await self._open_close_callback(position)
            return (True, {"rangeValue": position}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in open/close callback: {e}")
            return False, {}

    async def send_open_close_event(self, position: int, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send open/close position event (0=closed, 100=open)."""
        if not 0 <= position <= 100:
            return False
        if not self._open_close_limiter.can_send_event():
            return False
        if not hasattr(self, "send_event"):
            return False
        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_RANGE_VALUE, value={"rangeValue": position}, cause=cause)
        if success:
            self._open_close_limiter.event_sent()
        return success
