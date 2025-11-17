"""RangeController Capability - Generic range value control."""
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_RANGE_VALUE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

RangeValueCallback = Callable[[int], Awaitable[bool]]
AdjustRangeValueCallback = Callable[[int], Awaitable[bool]]

class RangeController:
    """Mixin providing range value control capability."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._range_value_callback: RangeValueCallback | None = None
        self._adjust_range_value_callback: AdjustRangeValueCallback | None = None
        self._range_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_range_value(self, callback: RangeValueCallback) -> None:
        """Register callback for range value changes."""
        self._range_value_callback = callback

    def on_adjust_range_value(self, callback: AdjustRangeValueCallback) -> None:
        """Register callback for relative range value changes."""
        self._adjust_range_value_callback = callback

    async def handle_range_value_request(self, range_value: int, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setRangeValue request."""
        if not self._range_value_callback:
            return False, {}
        try:
            success = await self._range_value_callback(range_value)
            return (True, {"rangeValue": range_value}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in range value callback: {e}")
            return False, {}

    async def handle_adjust_range_value_request(self, range_value_delta: int, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle adjustRangeValue request."""
        if not self._adjust_range_value_callback:
            return False, {}
        try:
            success = await self._adjust_range_value_callback(range_value_delta)
            return (True, {"rangeValue": range_value_delta}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in adjust range value callback: {e}")
            return False, {}

    async def send_range_value_event(self, range_value: int, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send range value event."""
        if not self._range_limiter.can_send_event():
            return False
        if not hasattr(self, "send_event"):
            return False
        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_RANGE_VALUE, value={"rangeValue": range_value}, cause=cause)
        if success:
            self._range_limiter.event_sent()
        return success
