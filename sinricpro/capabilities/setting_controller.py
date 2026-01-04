"""SettingController Capability - Generic settings management."""
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from sinricpro.utils.logger import SinricProLogger
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.types import EVENT_LIMIT_STATE, PHYSICAL_INTERACTION

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

SettingCallback = Callable[[str, Any], Awaitable[bool]]

class SettingController:
    """Mixin providing settings management capability."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._setting_callback: SettingCallback | None = None
        self._setting_event_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_setting(self, callback: SettingCallback) -> None:
        """Register callback for setting changes (setting id, value)."""
        self._setting_callback = callback

    async def send_setting_event(
        self,
        setting_id: str,
        value: Any,
        cause: str = PHYSICAL_INTERACTION
    ) -> bool:
        """
        Send a setting event to SinricPro server.

        Args:
            setting_id: The setting identifier
            value: The setting value (can be any JSON-serializable type)
            cause: Reason for the event (default: 'PHYSICAL_INTERACTION')

        Returns:
            True if event was sent, False if rate limited or failed
        """
        if self._setting_event_limiter.is_limited():
            return False

        # Access self as a SinricProDevice
        device: "SinricProDevice" = self  # type: ignore[assignment]
        return await device.send_event("setSetting", {"id": setting_id, "value": value}, cause)

    async def handle_setting_request(self, setting_id: str, value: Any, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setSetting request."""
        if not self._setting_callback:
            SinricProLogger.error(f"No setting callback registered for {device.get_device_id()}")
            return False, {}
        try:
            success = await self._setting_callback(setting_id, value)
            return (True, {"id": setting_id, "value": value}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in setting callback: {e}")
            return False, {}
