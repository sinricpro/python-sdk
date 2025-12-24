"""
ModeController Capability

Provides mode control functionality for devices that support multiple modes.
Supports optional instanceId for multi-instance mode control.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_MODE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

# Callback receives mode and optional instance_id
ModeStateCallback = Callable[[str, str], Awaitable[bool]]


class ModeController:
    """Mixin providing mode control capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize ModeController mixin."""
        super().__init__(*args, **kwargs)
        self._mode_state_callback: ModeStateCallback | None = None
        self._mode_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_mode_state(self, callback: ModeStateCallback) -> None:
        """Register callback for mode changes.

        Args:
            callback: Async function that receives mode and instance_id, returns True on success.
                      Signature: async def callback(mode: str, instance_id: str) -> bool
                      instance_id will be empty string if not provided by server.
        """
        self._mode_state_callback = callback

    async def handle_mode_request(
        self, mode: str, instance_id: str, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle setMode request.

        Args:
            mode: The mode value to set
            instance_id: Optional instance ID for multi-instance mode control
            device: The device handling this request

        Returns:
            Tuple of (success, response_value)
        """
        if not self._mode_state_callback:
            SinricProLogger.error(f"No mode state callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._mode_state_callback(mode, instance_id)
            if success:
                return True, {"mode": mode}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in mode state callback: {e}")
            return False, {}

    async def send_mode_event(
        self, mode: str, instance_id: str = "", cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """Send mode event to SinricPro.

        Args:
            mode: The mode value
            instance_id: Optional instance ID for multi-instance mode control
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._mode_limiter.can_send_event():
            SinricProLogger.warn("Mode event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("ModeController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_MODE,
            value={"mode": mode},
            cause=cause,
            instance_id=instance_id
        )

        if success:
            self._mode_limiter.event_sent()

        return success
