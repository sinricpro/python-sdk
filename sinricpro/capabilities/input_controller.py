"""
InputController Capability

Provides input selection functionality for TVs and AV receivers.
"""

from typing import Any, Callable, Awaitable, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SELECT_INPUT
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

SelectInputCallback = Callable[[str], Awaitable[bool]]


class InputController:
    """Mixin providing input selection capability."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize InputController mixin."""
        super().__init__(*args, **kwargs)
        self._select_input_callback: SelectInputCallback | None = None
        self._input_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_select_input(self, callback: SelectInputCallback) -> None:
        """Register callback for input selection.

        Args:
            callback: Async function that receives input name (e.g., HDMI1, HDMI2, TV, etc.)
                      and returns True on success
        """
        self._select_input_callback = callback

    async def handle_select_input_request(
        self, input_name: str, device: "SinricProDevice"
    ) -> tuple[bool, dict[str, Any]]:
        """Handle selectInput request."""
        if not self._select_input_callback:
            SinricProLogger.error(f"No select input callback registered for {device.get_device_id()}")
            return False, {}

        try:
            success = await self._select_input_callback(input_name)
            if success:
                return True, {"input": input_name}
            else:
                return False, {}
        except Exception as e:
            SinricProLogger.error(f"Error in select input callback: {e}")
            return False, {}

    async def send_input_event(
        self, input_name: str, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """Send input selection event to SinricPro.

        Args:
            input_name: Input name (e.g., HDMI1, HDMI2, TV)
            cause: Cause of the event

        Returns:
            True if event was sent successfully
        """
        if not self._input_limiter.can_send_event():
            SinricProLogger.warn("Input event rate limited")
            return False

        if not hasattr(self, "send_event"):
            SinricProLogger.error("InputController must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SELECT_INPUT, value={"input": input_name}, cause=cause)

        if success:
            self._input_limiter.event_sent()

        return success
