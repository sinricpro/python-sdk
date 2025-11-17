"""LockController Capability - Provides lock/unlock functionality."""
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_LOCK_STATE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

LockStateCallback = Callable[[bool], Awaitable[bool]]

class LockController:
    """Mixin providing lock control capability."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._lock_state_callback: LockStateCallback | None = None
        self._lock_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_lock_state(self, callback: LockStateCallback) -> None:
        """Register callback for lock state changes (True=lock, False=unlock)."""
        self._lock_state_callback = callback

    async def handle_lock_state_request(self, lock: bool, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setLockState request."""
        if not self._lock_state_callback:
            SinricProLogger.error(f"No lock state callback registered for {device.get_device_id()}")
            return False, {}
        try:
            success = await self._lock_state_callback(lock)
            return (True, {"state": "LOCKED" if lock else "UNLOCKED"}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in lock state callback: {e}")
            return False, {}

    async def send_lock_state_event(self, locked: bool, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send lock state event."""
        if not self._lock_limiter.can_send_event():
            SinricProLogger.warn("Lock state event rate limited")
            return False
        if not hasattr(self, "send_event"):
            SinricProLogger.error("LockController must be mixed with SinricProDevice")
            return False
        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_LOCK_STATE, value={"state": "LOCKED" if locked else "UNLOCKED"}, cause=cause)
        if success:
            self._lock_limiter.event_sent()
        return success
